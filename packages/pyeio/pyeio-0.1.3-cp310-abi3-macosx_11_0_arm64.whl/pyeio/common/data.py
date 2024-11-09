from typing import get_args
from pyeio.common.types import (
    StandardFileExtension,
    VariantFileExtension,
    FileExtension,
)

standard_file_extensions: tuple[StandardFileExtension, ...] = get_args(
    StandardFileExtension
)
variant_file_extensions: tuple[VariantFileExtension, ...] = get_args(
    VariantFileExtension
)
file_extensions: tuple[FileExtension, ...] = (
    standard_file_extensions + variant_file_extensions
)


variant_to_standard: dict[VariantFileExtension, StandardFileExtension] = {
    "ndjson": "jsonl",
    "jsonlines": "jsonl",
    # "jpg": "jpeg",
    # "yml": "yaml",
    # "markdown": "md",
}


# used file extension : set { valid file extensions }
allowed_variants_lookup: dict[StandardFileExtension, set[FileExtension]] = {
    "json": {"json"},
    "jsonl": {
        "jsonl",
        "json",
        "jsonlines",
        "ndjson",
    },
}
