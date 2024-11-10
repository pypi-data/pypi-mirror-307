"""Utility class for exporting BigQuery data."""

from time import time
from datetime import timedelta
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from functools import cache

import polars as pl

from google.cloud.storage import Client as StorageClient, Bucket, Blob
from google.cloud.bigquery import Client as BQClient, Table, ExtractJobConfig

from neoval_py_utils.utils import (
    get_env_or_default,
    gcs_blobs_to_df,
    prepare_query_hash,
)
from typing import Optional


class Exporter:
    """A wrapper around a BQ query facilitating fast export and local caching.

    For efficient BigQuery data export and caching to prevent redundant query
    executions.

    The class can be used as a singleton: it should be instantiated
    once, and the same instance can repeatedly have queries passed to it.

    For simplicity, export method is aliased by the `<` operator.

    ```py
    exporter = Exporter()

    # `df` would contain a cached copy of query results - subsequent calls
    # with the same query string would not actually execute the query.
    df = exporter < "SELECT * FROM `my-dataset.my-table`"

    # The same instance should be used for all queries.
    df = exporter < "SELECT x, y FROM `my-dataset.my-other-table`"
    ```

    Limitations (Will be addressed in future versions):
    - The class is not thread-safe.
    - Does not check if the table it is exporting has been updated since cached.
    """

    def __init__(
        self,
        cache_max_age: Optional[float] = None,
        cache_bucket: Optional[str] = None,
        cache_dir: Optional[str] = None,
        bq_client: BQClient = None,
        gcs_client: StorageClient = None,
    ) -> None:
        """Initialise the Exporter class.

        Args:
            cache_max_age: Hours to cache local files.
            cache_bucket: Google Cloud Storage bucket name.
            cache_dir: Path to the local cache directory. Default is None.
            bq_client: Bigquery client.
            gcs_client: Google storage client.
        """
        # Default values
        self.cache_max_age = get_env_or_default(
            cache_max_age, 12, env_var="CACHE_MAX_AGE"
        )
        self.cache_dir = get_env_or_default(cache_dir, None, env_var="CACHE_DIR")
        self.cache_bucket = get_env_or_default(
            cache_bucket, "py_utils_cache", env_var="CACHE_BUCKET"
        )
        self.gcs_client: StorageClient = get_env_or_default(gcs_client, StorageClient())
        self.bq_client: BQClient = get_env_or_default(bq_client, BQClient())
        self.cache_bucket: Bucket = self.gcs_client.bucket(self.cache_bucket)

        # Setting up gcs buckets
        if not self.cache_bucket.exists():
            self.cache_bucket: Bucket = self.gcs_client.create_bucket(
                self.cache_bucket,
                location="US",
            )

            self.cache_bucket.add_lifecycle_delete_rule(age=1)
            self.cache_bucket.patch()

        # Setting up local cache directory
        self.cache_dir = None if self.cache_dir is None else Path(self.cache_dir)
        if self.cache_dir is not None:
            self.cache_dir.mkdir(parents=True, exist_ok=True)

    def export(self, query: str) -> pl.DataFrame:
        """Export a query to a parquet file, and return a polars DataFrame."""
        query_hash, table_ref = prepare_query_hash(query)

        cache_path = self._cache_path(query_hash)

        if cache_path is not None:
            self._cleanup_cache()
            if cache_path.exists():
                delta = time() - cache_path.stat().st_mtime
                if timedelta(hours=int(self.cache_max_age)) > timedelta(seconds=delta):
                    df = pl.read_parquet(cache_path)
                    return df

        if table_ref is None:
            job = self.bq_client.query(query)
            table_ref = job.result()._table

        blobs = self.bq_to_gcs(table_ref, query_hash, deterministic=False)

        df = gcs_blobs_to_df(blobs)

        if cache_path is not None:
            df.write_parquet(cache_path)

        return df

    def __lt__(self, query: str) -> pl.DataFrame:
        """Set the `less than` operator to the export method."""
        return self.export(query)

    @cache
    def _cache_path(self, name: str) -> Path | None:
        """Get the path to the cached parquet file."""
        if self.cache_dir is None:
            return None

        return self.cache_dir / f"{name}.parquet"

    def _cleanup_cache(self) -> None:
        fs = self.cache_dir.glob("*.parquet")
        for f in fs:
            delta = time() - f.stat().st_mtime
            if timedelta(seconds=delta) > timedelta(hours=int(self.cache_max_age)):
                f.unlink()

    def _list_blobs(self, name: str) -> list[Blob]:
        """List all blobs in the cache bucket with the given prefix."""
        i = self.gcs_client.list_blobs(self.cache_bucket, prefix=f"{name}")
        return list(i)

    def _delete_blobs_in_bucket(self, name: str) -> None:
        """Delete all blobs in the cache bucket with the given prefix."""
        with ThreadPoolExecutor(24) as executor:
            executor.map(
                lambda blob: blob.delete(),
                self._list_blobs(name),
            )

    def bq_to_gcs(
        self, table_ref: str, folder_name: str | None = None, deterministic: bool = True
    ) -> list[Blob]:
        """Export a BigQuery table to a GCS bucket.

        Args:
            table_ref: Bigquery table reference
            folder_name: Name of folder in GCS bucket
            deterministic: If true, data is ordered by a hash of all columns

        Returns: List of blobs in the GCS bucket that were result of the export

        """
        if folder_name is None:
            folder_name = table_ref.split(".")[-1]

        self._delete_blobs_in_bucket(folder_name)

        table: Table = self.bq_client.get_table(table_ref)
        location: str = (
            f"gs://{self.cache_bucket.name}/{folder_name}/{folder_name.split('/')[-1]}_*"
        )

        if deterministic:
            query = f"""
                EXPORT DATA OPTIONS (
                    uri='{location}',
                    format='PARQUET',
                    overwrite=true) AS
                SELECT *
                FROM {table} AS t
                ORDER BY FARM_FINGERPRINT(TO_JSON_STRING(t))
            """
            self.bq_client.query(query).result()

        else:
            self.bq_client.extract_table(
                table,
                [location],
                job_config=ExtractJobConfig(
                    destination_format="PARQUET",
                ),
            ).result()

        return self._list_blobs(folder_name)
