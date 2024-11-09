import annotated_types
from pathlib import Path
from datetime import datetime, date, time
from typing import Literal, TypeVar, Annotated


FileType = Literal[
    "text",
    "image",
    "video",
    "audio",
    "document",
]

FileFormat = Literal[
    "json",
    "jsonl",
    "toml",
    "yaml",
]

StandardFileExtension = FileFormat


VariantFileExtension = Literal[
    "ndjson",
    "jsonlines",
    "yml",
]

FileExtension = StandardFileExtension | VariantFileExtension

MimeType = Literal[
    "application/json",
    "application/jsonl",
]

FilePath = str | Path

# DataLocation = Literal[
#     "disk",
#     "web",
#     "memory",
# ]


# ! Python Data Types

JSON_TYPE = TypeVar("JSON_TYPE", bound="PyJSON")
PyJSON = bool | int | float | str | list[JSON_TYPE] | dict[str, JSON_TYPE]
SerializedJSON = str | bytes | bytearray

TOML_TYPE = TypeVar("TOML_TYPE", bound="TOML_VALUE_TYPE")
TOML_VALUE_TYPE = (
    bool
    | int
    | float
    | str
    | datetime
    | date
    | time
    | list[TOML_TYPE]
    | dict[str, TOML_TYPE]
)
PyTOML = dict[str, TOML_VALUE_TYPE]
SerializedTOML = str | bytes

YAML_TYPE = TypeVar("YAML_TYPE", bound="PyYAML")
PyYAML = bool | int | float | str | list[YAML_TYPE] | dict[str, YAML_TYPE]
SerializedYAML = str | bytes
