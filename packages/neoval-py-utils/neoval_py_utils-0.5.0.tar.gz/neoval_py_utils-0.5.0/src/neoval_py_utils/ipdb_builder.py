"""In process (embedded) Database Builder class."""

import concurrent.futures
import datetime

from typing import Optional, ClassVar

import json
from json import JSONDecodeError
from textwrap import dedent
import os
from pathlib import Path

import sqlite3
from sqlite3 import Connection as SQLiteConnection
import yaml

from google.cloud.bigquery import Client as BigQueryClient
from google.cloud.bigquery.table import Table as ArrowTable
from google.cloud.storage import Client as StorageClient
from google.cloud.storage import Blob

from pyarrow import RecordBatch

import duckdb
from duckdb import DuckDBPyConnection

from neoval_py_utils.exporter import Exporter
from neoval_py_utils.ipdb_build_event import IPDBBuildEvent, IPDBBuildEventType
from neoval_py_utils.template import Template
from neoval_py_utils.utils import gcs_blob_to_table

_EventTypes = IPDBBuildEventType
_Event = IPDBBuildEvent


class IPDBBuilder:
    """In process Database Builder class.

    A class for constructing local SQLite3 and DuckDB databases from the contents
    of a Google Bigquery dataset.
    """

    def __init__(self, dataset: str, project: str) -> None:  # noqa: D107
        self.dataset = dataset
        self.project = project
        self._client: BigQueryClient = None

        self._source_dataset_metadata: list[dict] = None

        self._exporter = Exporter()

    BQ_SQLITE_TYPE_MAP: ClassVar = {
        "INT64": "INTEGER",
        "FLOAT64": "REAL",
        "STRING": "TEXT",
        # These types don't exist in SQlite - but should logically be serialized
        # as strings. They don't need to be converted on the way back out - since
        # JSON itself cannot encode these types.
        "DATE": "TEXT",
        "DATETIME": "TEXT",
        "TIMESTAMP": "TEXT",
        "BOOL": "BOOLEAN",  # The SQLite type affinity is `NUMERIC`.
        # This doesn't exist in SQlite, but will be serialized as a WKT string.
        # It cannot / should not be compared / sorted / transformed in a query.
        #
        # NOTE: This _could_ be done with an adapter, but that would not be
        # a solution for DuckDB... the most consistent solution to the
        # serialization of geography types is to always store (in the BQ source
        # dataset) x / y pairs for `POINT()` types and GeoJSON encoding for
        # all shapes / lines.
        "GEOGRAPHY": "GEOGRAPHY",
        # NOTE: These types don't natively exist in SQLite, but we can add a
        # dynamic type that will allow us to serialize them as integers or
        # strings automagically.
        #
        # SEE: `https://docs.python.org/3/library/sqlite3.html#sqlite3.register_adapter`.
        #
        # Similarly, any API response code should register converters so that these
        # values are converted to the logical Python type prior to
        # JSON serialization of the response data.
        "STRUCT": "COMPOSITE",
        "ARRAY": "COMPOSITE",
    }

    @staticmethod
    def _composite_adapter(value: dict | list | tuple) -> str:
        """Composite adapter.

        Converts any value that is landing in a `COMPOSITE` type column in
        SQLite into a string (JSON) prior to insertion (see docs in the type
        mapping above).
        """
        return json.dumps(value, sort_keys=False)

    @property
    def client(self) -> BigQueryClient:
        if not self._client:
            self._client = BigQueryClient()

        return self._client

    @staticmethod
    def _parse_table_metadata(table_metadata: dict) -> dict:
        # Table descriptions are sometimes (for some reason) JSON encoded -
        # this works around that, while also handling the value `None`.
        try:
            description = table_metadata["description"]
            if description is not None:
                table_metadata["description"] = json.loads(
                    table_metadata["description"]
                )
        except JSONDecodeError:
            pass

        # Remove the `description` key where it has no value.
        columns = table_metadata.get("columns")
        for column in columns:
            if column.get("description") is None:
                column.pop("description")

        return table_metadata

    @property
    def source_dataset_metadata(self) -> list:
        if self._source_dataset_metadata:
            return self._source_dataset_metadata

        query = dedent(
            """\
                WITH table_name AS (
                    SELECT DISTINCT
                        table_name AS name
                    FROM {project}.{dataset}.INFORMATION_SCHEMA.TABLES
                    WHERE table_type = 'BASE TABLE'
                ),

                table_description AS (
                    SELECT
                        table_name AS name,
                        option_value AS description
                    FROM
                        {project}.{dataset}.INFORMATION_SCHEMA.TABLE_OPTIONS table_option
                    WHERE UPPER(option_name) = 'DESCRIPTION'
                ),

                table AS (
                    SELECT name, NULLIF(description, '""') AS description,
                    FROM table_name LEFT JOIN table_description USING (name)
                ),

                table_column AS (
                    SELECT
                        tc.table_name AS name,
                        ARRAY_AGG(
                            STRUCT(
                                tc.column_name AS name,
                                tc.data_type AS type,
                                tfp.description AS description
                            ) ORDER BY tc.ordinal_position
                        ) AS columns
                    FROM
                        {project}.{dataset}.INFORMATION_SCHEMA.COLUMNS tc LEFT JOIN
                        {project}.{dataset}.INFORMATION_SCHEMA.COLUMN_FIELD_PATHS tfp USING (
                            table_name,
                            column_name
                        )
                    GROUP BY tc.table_name
                )

                SELECT * FROM table LEFT JOIN table_column USING (name) ORDER BY name
            """
        ).format(project=self.project, dataset=self.dataset)

        self._source_dataset_metadata = [
            self._parse_table_metadata(dict(r))
            for r in self.client.query(query).result()
        ]

        return self._source_dataset_metadata

    @staticmethod
    def _normalize_config(val: list | str) -> list:
        if val is None:
            return []

        if isinstance(val, str):
            return [val]

        return val

    @staticmethod
    def _merge_config_and_dataset_metadata(
        dataset_metadata: list[dict], config: list[dict]
    ) -> list[list[dict]]:
        """Takes the provided config and adds metadata from BigQuery.

        Returns a list of table metadata for both duckdb and sqlite.
        """
        if "duckdb" in config:
            _config = {
                table_config["name"]: {
                    "primary_key": IPDBBuilder._normalize_config(
                        table_config.get("primary_key", [])
                    )
                }
                for table_config in (config["duckdb"] or [])
            }

            _dataset_metadata = json.loads(json.dumps(dataset_metadata))

            # NOTE: This mutates the above variable (hence the copy).
            for table_metadata in _dataset_metadata:
                name: str = table_metadata["name"]
                table_config: dict = _config.get(
                    name,
                    {
                        "primary_key": [],
                    },
                )

                table_metadata.update(table_config)

            # This should remove the tables that are not in the config
            duckdb_metadata = [
                table_metadata
                for table_metadata in _dataset_metadata
                if table_metadata["name"] in _config
            ]
        else:
            duckdb_metadata = None

        if "sqlite" in config:
            _config = {
                table_config["name"]: {
                    "primary_key": IPDBBuilder._normalize_config(
                        table_config.get("primary_key", [])
                    )
                }
                for table_config in (config["sqlite"] or [])
            }

            _dataset_metadata = json.loads(json.dumps(dataset_metadata))

            # NOTE: This mutates the above variable (hence the copy).
            for table_metadata in _dataset_metadata:
                name: str = table_metadata["name"]
                table_config: dict = _config.get(
                    name,
                    {
                        "primary_key": [],
                    },
                )

                table_metadata.update(table_config)

            # This should remove the tables that are not in the config
            sqlite_metadata = [
                table_metadata
                for table_metadata in _dataset_metadata
                if table_metadata["name"] in _config
            ]
        else:
            sqlite_metadata = None

        return [duckdb_metadata, sqlite_metadata]

    @staticmethod
    def _render_duckdb_create_table_statement(
        con: DuckDBPyConnection,
        target_name: str,
        source_name: str = "temp",
        primary_key: list[str] = [],
    ) -> str:
        declarations = (
            con.execute(
                dedent(
                    """\
                        SELECT
                            CONCAT(column_name, ' ', data_type) AS declaration,
                        FROM INFORMATION_SCHEMA.COLUMNS
                        WHERE table_name = '{}'
                        ORDER BY ordinal_position ASC
                    """
                ).format(source_name)
            )
            .arrow()
            .to_pylist()
        )

        pk = (
            ""
            if not primary_key
            else ",\n\n    PRIMARY KEY ({})".format(", ".join(primary_key))
        )

        return (
            f"CREATE OR REPLACE TABLE {target_name} (\n"
            + (",\n".join(["    " + v["declaration"] for v in declarations]))
            + pk
            + "\n)"
        )

    @staticmethod
    def _render_sqlite_column_declaration(column: dict) -> str:
        name = column["name"]
        dtype = IPDBBuilder.BQ_SQLITE_TYPE_MAP.get(column["type"], "UNKNOWN")

        return f"{name} {dtype}"

    @staticmethod
    def _render_sqlite_create_table_statement(table_metadata: list[dict]) -> str:
        name = table_metadata["name"]
        columns = table_metadata["columns"]

        primary_key = table_metadata.get("primary_key", [])
        pk = (
            ""
            if not primary_key
            else ",\n\n    PRIMARY KEY ({})".format(", ".join(primary_key))
        )

        return (
            f"CREATE TABLE {name} (\n"
            + (
                ",\n".join(
                    [
                        "    " + IPDBBuilder._render_sqlite_column_declaration(column)
                        for column in columns
                    ]
                )
            )
            + pk
            + "\n)"
        )

    @staticmethod
    def _prepare_directory_and_pathname(path_ref: str | Path, pathname: str) -> Path:
        """Prepare pathname for build method.

        Ensure that `path_ref` exists, and that the specified pathname within it
        does not. If those files / folders exist, they are deleted - so that the
        returned `Path`s always reference files that don't exist on disk.
        """
        p: Path = Path(path_ref)

        if not p.exists():
            p.mkdir()

        pathname = p / pathname
        if pathname.exists():
            pathname.unlink()

        return pathname

    @staticmethod
    def _verify_directory_and_pathname(path_ref: str | Path, pathname: str) -> Path:
        """Prepare pathnames for prepare method.

        Ensure that `path_ref` and the pathnames exist, otherwise raises an error.
        Opposite to the method above, this is used in the `prepare` method to ensure
        that the databases we want to operate on have already been created.
        """
        p: Path = Path(path_ref)

        if not p.exists():
            raise ValueError(f"{path_ref} directory does not exist.")

        pathname = p / pathname
        if not pathname.exists():
            raise FileNotFoundError(f"{pathname} does not exist.")

        return pathname

    def _insert_data(
        self, blob: Blob, cur: DuckDBPyConnection, name: str, i: int
    ) -> None:
        attempt = 1
        while attempt < 6:  # noqa: PLR2004
            try:
                t: ArrowTable = gcs_blob_to_table(blob)  # noqa: F841
                cur.execute(f"INSERT INTO {name} SELECT * FROM t")
                return "SUCCESS"
            except:  # noqa: E722
                attempt += 1
        return f"ERROR: blob {i}"

    def _create_duckdb_table(
        self, table_metadata: dict, duckdb_con: DuckDBPyConnection
    ) -> IPDBBuildEvent:
        cur = duckdb_con.cursor()

        name = table_metadata["name"]
        primary_key = table_metadata["primary_key"]

        blobs: list[Blob] = self._exporter.bq_to_gcs(
            f"{self.project}.{self.dataset}.{name}"
        )

        temp: ArrowTable = gcs_blob_to_table(blobs[0])  # noqa: F841
        cur.execute(
            f"CREATE OR REPLACE TABLE temp_{name} AS SELECT * FROM temp LIMIT 1000"
        )

        duck_db_create_table_statement = self._render_duckdb_create_table_statement(
            cur,
            target_name=name,
            source_name=f"temp_{name}",
            primary_key=primary_key,
        )

        cur.execute(duck_db_create_table_statement)
        # Download each parquet file from GCS at a time and insert into duckdb
        # 14/6/24 Parallel inserts would intermittently hang with duckdb versions >= 0.10.0.
        # At present setting max_worker to 1 increased build by 40s, please revisit in the future.
        with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
            futures = [
                executor.submit(self._insert_data, blob, cur, name, i)
                for i, blob in enumerate(blobs)
            ]

            for future in concurrent.futures.as_completed(futures):
                if future.result().startswith("ERROR"):
                    return _Event(
                        _EventTypes.FAILURE,
                        data={
                            "name": name,
                        },
                    )

        cur.execute(f"DROP TABLE temp_{name}")

        return _Event(
            _EventTypes.DUCKDB_TABLE_CREATED,
            data={
                "name": name,
                "create_table_statement": duck_db_create_table_statement,
            },
        )

    def _create_sqlite_table(
        self, table_metadata: dict, sqlite_con: SQLiteConnection
    ) -> IPDBBuildEvent:
        table_data: ArrowTable = self._exporter.export(
            f"{self.project}.{self.dataset}.{table_metadata['name']}"
        ).to_arrow()
        name = table_metadata["name"]
        sqlite_create_table_statement = self._render_sqlite_create_table_statement(
            table_metadata
        )

        sqlite_con.execute("BEGIN TRANSACTION")
        sqlite_con.execute(sqlite_create_table_statement)

        b: RecordBatch
        for b in table_data.to_batches(500):
            rows = [tuple(r.values()) for r in b.to_pylist()]

            q = ", ".join(["?" for _ in rows[0]])
            sqlite_con.executemany(f"INSERT INTO {name} VALUES({q})", rows)

        sqlite_con.commit()

        return _Event(
            _EventTypes.SQLITE_TABLE_CREATED,
            data={
                "name": name,
                "create_table_statement": sqlite_create_table_statement,
            },
        )

    def _build_sqlite(self, sqlite_path: Path, metadata: list) -> None:
        sqlite_con: SQLiteConnection = sqlite3.connect(str(sqlite_path))
        try:
            sqlite3.register_adapter(dict, IPDBBuilder._composite_adapter)
            sqlite3.register_adapter(list, IPDBBuilder._composite_adapter)

            sqlite_con.execute("PRAGMA journal_mode = WAL;")
            sqlite_con.execute("PRAGMA cache_size = -5000;")
            sqlite_con.execute("PRAGMA synchronous = NORMAL")

            for table in metadata:
                yield self._create_sqlite_table(table, sqlite_con)

            sqlite_con.execute("VACUUM;")
        finally:
            sqlite_con.close()

    def _build_duckdb(self, duckdb_path: Path, metadata: list) -> None:
        duckdb_con: DuckDBPyConnection = duckdb.connect(str(duckdb_path))
        try:
            for table in metadata:
                yield self._create_duckdb_table(table, duckdb_con)

        finally:
            duckdb_con.close()

    def build(
        self,
        directory: str | Path,
        config: list[dict],
        upload_bucket: Optional[str] = None,
    ) -> None:
        (
            duckdb_metadata,
            sqlite_metadata,
        ) = self._merge_config_and_dataset_metadata(
            self.source_dataset_metadata, config
        )
        """
        Build the In-process duckdb and sqlite databases from a BQ dataset.

        Args:
            directory: Path to the directory where the database files will be stored
            config: Configuration for the database.
            upload_bucket: The GCS bucket to upload the db files to.
        Yields:
            _Event: IPDBBuildEvent indicating the progress or completion of the build process.
        """

        yield _Event(
            _EventTypes.SOURCE_DATASET_METADATA_RETRIEVED,
            data={"metadata": None},
        )

        pathnames = []

        if duckdb_metadata:
            duckdb_path = self._prepare_directory_and_pathname(
                directory, "main.duck.db"
            )
            pathnames.append(duckdb_path)

            events = self._build_duckdb(duckdb_path, duckdb_metadata)
            for event in events:
                yield event
            yield _Event(_EventTypes.BUILD_COMPLETE, data={"name": "duckdb"})

        if sqlite_metadata:
            sqlite_path = self._prepare_directory_and_pathname(
                directory, "main.sqlite.db"
            )
            pathnames.append(sqlite_path)

            events = self._build_sqlite(sqlite_path, sqlite_metadata)
            for event in events:
                yield event
            yield _Event(_EventTypes.BUILD_COMPLETE, data={"name": "sqlite"})

        if upload_bucket:
            bucket = StorageClient().bucket(upload_bucket)
            for path in pathnames:
                blob = bucket.blob(f"databases/{'/'.join(str(path).split('/')[-2:])}")

                if blob.exists():
                    bucket.copy_blob(
                        blob,
                        bucket,
                        f"databases/market/archive/{int(datetime.datetime.now().timestamp())}_{'/'.join(str(path).split('/')[-1:])}",
                    )

                blob.upload_from_filename(str(path), timeout=300)
                yield _Event(
                    _EventTypes.UPLOAD_COMPLETE,
                    data={"name": str(path).rsplit("/", maxsplit=1)[-1]},
                )

    def prepare(self, db_directory: str | Path, template_path: str | Path) -> None:
        """Run prepare scripts.

        This method assumes there is a `duckdb` and/or `sqlite` folder inside the
        `template_path`, which is used to concat multiple queries and may contain
        macros. The individual queries that need to be run to create views should
        also exist within a `prepare` folder. For example:

        app/templates/duckdb/prepare.sql
        app/templates/duckdb/prepare/view1.sql
        app/templates/duckdb/prepare/view2.sql
        """
        env = Template(template_path)

        if os.path.exists(f"{template_path}/duckdb/prepare.sql"):
            duckdb_path = self._verify_directory_and_pathname(
                db_directory, "main.duck.db"
            )
            duckdb_con: DuckDBPyConnection = duckdb.connect(str(duckdb_path))
            files = os.listdir(f"{template_path}/duckdb/prepare")

            duckdb_query = env.get("prepare.sql", "duckdb").render(files=files)

            try:
                duckdb_con.execute(duckdb_query)

                r = duckdb_con.execute(
                    "SELECT table_name, table_type FROM information_schema.tables"
                )

                yield _Event(
                    _EventTypes.PREPARE_SCRIPTS_COMPLETE,
                    data={
                        "database": "duckdb",
                        "tables": yaml.safe_dump(r.arrow().to_pylist(), indent=4),
                    },
                )

            finally:
                duckdb_con.close()

        if os.path.exists(f"{template_path}/sqlite/prepare.sql"):
            sqlite_path = self._verify_directory_and_pathname(
                db_directory, "main.sqlite.db"
            )
            sqlite_con: SQLiteConnection = sqlite3.connect(str(sqlite_path))
            try:
                files = os.listdir(f"{template_path}/sqlite/prepare")
                sqlite_query = env.get("prepare.sql", "sqlite").render(files=files)

                sqlite_con.executescript(sqlite_query)
                sqlite_con.commit()
                r = sqlite_con.execute(
                    "SELECT type, tbl_name FROM sqlite_master WHERE type IN ('table', 'view')"
                )
                rows = r.fetchall()

                data = [{"table_name": row[1], "table_type": row[0]} for row in rows]

                yield _Event(
                    _EventTypes.PREPARE_SCRIPTS_COMPLETE,
                    data={
                        "database": "sqlite",
                        "tables": yaml.safe_dump(data, indent=4),
                    },
                )
            finally:
                sqlite_con.close()
