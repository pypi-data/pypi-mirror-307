"""A command line tool to build an in process DuckDB and/or SQLite database from BQ datasets."""

from sys import stderr
from pathlib import Path
import traceback

import yaml
import typer

from neoval_py_utils.ipdb_builder import (
    IPDBBuilder,
    IPDBBuildEventType,
    IPDBBuildEvent,
)
from neoval_py_utils.utils import fdump

app = typer.Typer()


@app.command()
def make_config(dataset: str, project: str) -> str:
    """Prints a default configuration to be used with the build command.

    The final config file should include the list of tables for each database.
    For example:

    sqlite:
        -   name: canonical_address
            primary_key: null
        -   name: sa2_locality_correspondence_2021
            primary_key: null
        -   name: gnaf_core
            primary_key: null
    duckdb:
        -   name: gnaf_core
            primary_key: null
    """
    b = IPDBBuilder(dataset=dataset, project=project)

    s = fdump(
        [
            {"name": table_metadata["name"], "primary_key": None}
            for table_metadata in b.source_dataset_metadata
        ]
    )

    print(s)
    return s


def _filter_table_metadata(table_metadata: dict) -> dict:
    name: str = table_metadata["name"]
    description: str = table_metadata.get("description", None)

    table_metadata = {"name": name}
    if description:
        table_metadata["description"] = description

    return table_metadata


@app.command()
def build(
    dataset: str,
    project: str,
    directory: Path,
    config: Path,
    upload_bucket: str = typer.Option(None),
) -> None:
    """Build the in process database(s)."""
    b = IPDBBuilder(dataset=dataset, project=project)
    directory = directory.resolve()
    directory.mkdir(parents=True, exist_ok=True)

    try:
        config = config.resolve()
        with config.open("r") as file:
            config = yaml.safe_load(file)

        # List all the tables built in either database
        all_tables = [item["name"] for sublist in config.values() for item in sublist]

        events = b.build(
            directory=directory.resolve(),
            config=config,
            upload_bucket=upload_bucket,
        )

        event: IPDBBuildEvent
        code = 0
        for event in events:
            if event.type == IPDBBuildEventType.FAILURE:
                code = 1
            print(event.type, event.data.get("name"), file=stderr)
            create_table_statement = event.data.get("create_table_statement", None)

            if create_table_statement:
                print(create_table_statement, "\n", file=stderr)
                continue

        with (directory / "main.metadata.yaml").open("w") as f:
            f.write(
                fdump(
                    [
                        _filter_table_metadata(table_metadata)
                        for table_metadata in b.source_dataset_metadata
                        if table_metadata["name"] in all_tables
                    ]
                )
            )

        if code == 1:
            raise typer.Exit(code=code)

    except Exception as e:
        traceback.print_exc()
        raise e


@app.command()
def prepare(
    dataset: str, project: str, db_directory: Path, template_path: Path
) -> None:
    """Run scripts to add views/virtual tables/etc. to the database(s)."""
    b = IPDBBuilder(dataset=dataset, project=project)

    try:
        events = b.prepare(
            db_directory=db_directory.resolve(), template_path=template_path.resolve()
        )

        event: IPDBBuildEvent
        for event in events:
            print(event.type, event.data.get("database"), file=stderr)
            print(event.data.get("tables"), "\n", file=stderr)

    except Exception as e:
        traceback.print_exc()
        typer.Exit(code=1)
        raise e


if __name__ == "__main__":
    app()
