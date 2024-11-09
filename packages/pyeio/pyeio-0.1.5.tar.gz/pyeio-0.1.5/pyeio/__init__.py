import importlib
from pathlib import Path
from typing import Any, Literal
from pyeio.core.types import FileFormat

# todo.fix: figure out how to do proper type hints
# todo: need to add format identification and dynamic module loading based on format to avoid taking a massive amount of time to import
# todo: should


def parse(
    data: str | bytes, format: FileFormat | Literal["detect"] = "detect"
) -> Any: ...


def serialize(data, format: FileFormat = "json") -> str: ...


def open(path: str | Path) -> Any: ...


def save(): ...


def load(): ...


def download(): ...


def decompress(): ...


def compress(): ...


# todo.feature:
# * add a function named (connect/interface/?)? which allowes user to open dynamic format type from base schema File, with expanded functionality
#   * need to account for on disk file, or URL
