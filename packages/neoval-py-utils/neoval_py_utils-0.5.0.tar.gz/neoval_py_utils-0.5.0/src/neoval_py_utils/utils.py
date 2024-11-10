"""Utility functions for the neoval-py-utils package."""

from os import environ
from textwrap import dedent
from typing import Any, Optional

from google.cloud.storage import Blob
from pyarrow import Table as PyArrowTable
import polars as pl
from io import BytesIO
from hashlib import sha1
from functools import cache
from concurrent.futures import ThreadPoolExecutor
import yaml


@cache
def bq_hash(query: str) -> str:
    """Generate a hash from the query that is requested from bq and used for the local cache."""
    h = sha1()
    h.update(query.encode())
    return h.hexdigest()[:12]


def prepare_query_hash(query: str) -> tuple[str, str | None]:
    """Prepare the query and return the hash and the table reference.

    Args:
        query: Query or table name

    Returns:
        Tuple of the query hash and the table reference, if a query is given, None is returned.

    """
    query = dedent(query).strip()

    is_select_all_table = not any(char.isspace() for char in query)
    table_ref = None

    if is_select_all_table:
        table_ref = query
        query = f"SELECT * FROM `{query}`"

    return bq_hash(query), table_ref


def get_env_or_default(
    attribute: Any, default: Any, env_var: Optional[str] = None
) -> Any:
    """Return the attribute if not None, environment variable or default.

    Args:
        attribute: Method variable input.
        default: The default value if there is no environment variable.
        env_var: The name of the environment variable to check. Optional.

    Returns:
        The value of the attribute(function input) > environment variables > default value.
    """
    if attribute is not None:
        return attribute
    if env_var is not None:
        return environ.get(env_var.upper(), default)
    return default


def gcs_blobs_to_df(blobs: list[Blob]) -> pl.DataFrame:
    """Download all blobs in the cache bucket with the given prefix/table name.

    Args:
        blobs: List of blobs to download.

    Returns: List of bytes for each blob.

    """
    with ThreadPoolExecutor(24) as executor:
        blob_bytes = executor.map(
            lambda blob: BytesIO(blob.download_as_bytes()),
            blobs,
        )

    return pl.concat([pl.read_parquet(s) for s in blob_bytes])


def gcs_blob_to_table(blob: Blob) -> PyArrowTable:
    """Download a blob from GCS and convert to a PyArrowTable."""
    b = BytesIO(blob.download_as_bytes())
    df = pl.read_parquet(b)
    return df.to_arrow()


def fdump(data: list[dict]) -> str:
    """Format and dump the data to a yaml string."""
    yaml.SafeDumper.og_represent_str = yaml.SafeDumper.represent_str

    def str_representer(dumper, data):  # noqa: ANN001, ANN202
        if "\n" in data or len(data) > 20:  # noqa: PLR2004
            return dumper.represent_scalar("tag:yaml.org,2002:str", data, style=">")
        return dumper.og_represent_str(data)

    yaml.add_representer(str, str_representer, Dumper=yaml.SafeDumper)

    return yaml.safe_dump(data=data, sort_keys=False, indent=4, width=80)
