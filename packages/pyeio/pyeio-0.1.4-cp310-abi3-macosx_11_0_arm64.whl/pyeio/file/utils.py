from pathlib import Path
from typing import cast
from urllib.parse import urlparse
from pyeio.core import data
from pyeio.core.types import (
    FilePath,
    FileFormat,
    FileExtension,
    StandardFileExtension,
)
from pyeio.core.exceptions import (
    UnsupportedFileExtensionError,
    IncorrectFileExtensionError,
    MissingFileExtensionError,
)


def extract_raw_file_extension_from_path(path: FilePath) -> str | None:
    if isinstance(path, str):
        path = Path(path)
    file_name_components: list[str] = path.name.split(".")
    if len(file_name_components) == 1:
        return None
    else:
        file_extension = file_name_components[-1]
        return file_extension


def extract_raw_file_extension_from_url(url: str) -> str | None:
    parsed_url = urlparse(url)
    url_path = parsed_url.path
    file_extension = extract_raw_file_extension_from_path(path=url_path)
    return file_extension


def extract_file_name_from_path(path: FilePath) -> str:
    return Path(path).name


def extract_file_name_from_url(url: str) -> str:
    return urlparse(url).path.split("/")[-1]


def run_file_extension_validation(
    module_name: FileFormat,
    url: str | None = None,
    path: FilePath | None = None,
) -> None:
    if url:
        file_extension = extract_raw_file_extension_from_url(url)
        file_name = extract_file_name_from_url(url)
    elif path:
        file_extension = extract_raw_file_extension_from_path(path)
        file_name = extract_file_name_from_path(path=path)
    else:
        raise ValueError("Either `url` or `path` parameter must be passed.")
    if file_extension is None:
        raise MissingFileExtensionError(file=file_name)
    file_extension = file_extension.lower()
    if file_extension not in data.file_extensions:
        raise UnsupportedFileExtensionError(extension=file_extension)
    file_extension = cast(FileExtension, file_extension)
    allowed_variant_extensions = data.allowed_variants_lookup[module_name]
    if not (file_extension) in allowed_variant_extensions:
        raise IncorrectFileExtensionError(
            file_extension=file_extension,
            compatible_extensions=set(map(str, allowed_variant_extensions)),
        )


# def correct_file_extension(
#     real_extension: str | FileExtension,
#     expected_extension: FileExtension,
# ) -> None:
#     real_extension = real_extension.lower()
#     allowed_extensions: set[FileExtension] = index.allowed_variants_lookup[
#         real_extension
#     ]


# # todo: this should be refactored into a extension checking engine that includes warnings
# # for technically allowed file extensions, the ability to bypass checks with parameters, etc
# def is_valid_file_extension(extension: str, allowed: set[str]) -> bool:
#     return extension.lower() in allowed

# def raise_invalid_file_extension(extension: str, allowed: set[str]) -> None:


# todo
def rename_file():
    # todo: rename file on disk
    ...


def get_file_metadata():
    # todo: get builtin file metadata
    ...
