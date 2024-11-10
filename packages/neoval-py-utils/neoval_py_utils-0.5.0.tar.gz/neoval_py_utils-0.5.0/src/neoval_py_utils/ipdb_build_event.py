"""Events for the build process."""

from dataclasses import dataclass
from enum import Enum


class IPDBBuildEventType(Enum):
    """Enum of the event types that can occur during the build process."""

    SOURCE_DATASET_METADATA_RETRIEVED = 1
    PULLING_SOURCE_TABLE = 2
    DUCKDB_TABLE_CREATED = 3
    SQLITE_TABLE_CREATED = 4
    BUILD_COMPLETE = 5
    UPLOAD_COMPLETE = 6
    PREPARE_SCRIPTS_COMPLETE = 7
    FAILURE = 8


@dataclass
class IPDBBuildEvent:
    """Event class for the build process."""

    type: IPDBBuildEventType
    data: dict
