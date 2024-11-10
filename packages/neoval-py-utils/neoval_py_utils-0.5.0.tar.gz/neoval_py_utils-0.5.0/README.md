# neoval-py-utils

neoval-py-utils is a python utilities package developed by [Neoval](https://neoval.io) to assist with the Extract, Load and Transform
(ELT/ETL) of data from Google Cloud Platform (GCP) services.

The main difference between this utilities package and [BigQuery provided APIs](https://cloud.google.com/bigquery/docs/samples/bigquery-list-rows-dataframe)
is a faster export. Running a [BigQuery extract_job](https://cloud.google.com/python/docs/reference/bigquery/latest/google.cloud.bigquery.job.ExtractJob) 
to a bucket and downloading it is faster and can be improved by increasing the machine's download speed. We also use of local caching so that the same query will not needless be repeatedly be executed / downloaded. 
With this package the user can also create, databases that can be embedded to a machine for a website or application.

Functionalities include:
- exporter
  - Exporting data from BigQuery(bq) to a pandas DataFrame, pyArrow Table or Google Cloud Storage (GCS).
  - Can be a bq query or a bq table.
- ipdb
  - Building and preparing embedded in-process databases (IPDB) from BigQuery datasets.
  - Supports SQLite and DuckDB and configured with a YAML file please see examples below.
  - Supports templating for transformations post initial build.

# Development

All development must take place on a feature branch and a pull request is required; a user is not allowed to commit directly to `main`. The automated workflow in this repo (using `python-semantic-release`) requires the use of [angular style](https://github.com/angular/angular.js/blob/master/DEVELOPERS.md#commits) commit messages to update the package version and `CHANGELOG`. All commits must be formatted in this way before a user is able to merge a PR; a user who may want to develop without using this format for all commits can simply squash non-angular commit messages prior to merge. A PR may only be merged by the `rebase and merge` method. This is to ensure that only angular style commits end up on `main`.

Upon merge to `main`, the `deploy` workflow will facilitate the following:

- bump the version in `pyproject.toml`
- update the `CHANGELOG` using all commits added
- tag and release, if required
- publish to PyPi


## Getting Started

### Prerequisites
TODO

### Tests

For the integration tests to pass you will need to be authenticated with a Google project. With storage admin
and bigquery job permissions.

You can auth with `GOOGLE_APPLICATION_CREDENTIALS` as an environment variable or by 
running `gcloud auth application-default login`.

Specify gcp project with `gcloud config set project <project-id>`.

Run unit and integration tests with `poetry run task test`.

To run with coverage tests with `poetry run task test-with-coverage`.

# Usage

## TODO installation with pipy

Assuming that installed `neoval-py-utils`is successfully as a dependency and have permissions to gcp storage and bigquery.

## Examples of usage

### Export BQ datasets or Queries >> Dataframe or GCS #######

```python
from neoval_py_utils.exporter import Exporter
# To query a bigquery table and return a polar dataframe. Caches results, keeps for default 12 hours.
exporter = Exporter() # To use cache, pass path to the constructor. Eg Exporter(cache_dir=./cache)
pl_df = exporter.export("SELECT word FROM `bigquery-public-data.samples.shakespeare` GROUP BY word ORDER BY word DESC LIMIT 3")

# `export` is aliased by `<` operator. Will give same results as above.
pl_df = exporter < "SELECT word FROM `bigquery-public-data.samples.shakespeare` GROUP BY word ORDER BY word DESC LIMIT 3"


# To export a whole table
al_pl_df = exporter.export("bigquery-public-data.samples.shakespeare")


# To export bigquery table to a parquet file in a gcp storage bucket. Returns a list of blobs.
blobs = exporter.bq_to_gcs("my-dataset.my-table")
```
### Create In-process(Embedded) Databases #######

```shell
# Python cli example to build in-process db
poetry run ipdb build <DBT_DATASET> <GCLOUD_PROJECT_ID> <DB_PATH> <CONFIG_PATH> --upload-bucket <UPLOAD_BUCKET> 
# If you would like to run it in locally in this repo, you can run
# Upload bucket is optional, this will upload the in-process db to the specified bucket.
# Ensure your PYTHONPATH=./src
poetry run ipdb build samples bigquery-public-data tests/artifacts/in_process_db tests/resources/good.config.yaml

```
Example of config.yaml
```yaml
sqlite:
    -   name: shakespeare
        primary_key: null
duckdb:
    -   name: shakespeare
        primary_key: null
        description: "Word counts from Shakespeare work - gcp public dataset"
```

```shell
# To apply sql templates after the in-process db is built
poetry run ipdb prepare <DBT_DATASET> <GCLOUD_PROJECT_ID> <DB_PATH> <TEMPLATES_PATH>
# If you would like to run it in locally in this repo, you can run
poetry run ipdb prepare samples bigquery-public-data tests/artifacts/in_process_db tests/resources/templates
# For more info you can run
poetry run ipdb --help # which will return 
                                                                                                                                     
 Usage: ipdb [OPTIONS] COMMAND [ARGS]...                                                                                                                                                               
╭─ Commands ────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ build                           Build the in process database(s).                                                 │
│ make-config                     Prints a default configuration to be used with the build command.                 │
│ prepare                         Run scripts to add views/virtual tables/etc. to the database(s).                  │
╰───────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

