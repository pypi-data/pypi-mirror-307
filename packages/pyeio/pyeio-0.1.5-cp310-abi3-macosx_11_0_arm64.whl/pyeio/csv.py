# uses result, returns a higher level object that operations can be applied to
# eg: CSV class, with append, prepend methods, type validation for data, automatically prepends after first column if column defined, etc


import pandas as pd
from pathlib import Path


def open(path: str | Path) -> pd.DataFrame:
    return pd.read_csv(path)


def save(data: pd.DataFrame, path: str | Path, overwrite: bool = False): ...


def get(url: str) -> pd.DataFrame: ...


# ! ---


class Streamer:
    def __init__(self, url: str) -> None:
        self.url = url


class Reader:
    def __init__(self, file: str | Path) -> None:
        self.file = Path(file)
        self.__column_names: list[str] | None = None

    @property
    def column_names(self) -> list[str]: ...

    def read_rows(self): ...

    def read_column_names(self): ...
