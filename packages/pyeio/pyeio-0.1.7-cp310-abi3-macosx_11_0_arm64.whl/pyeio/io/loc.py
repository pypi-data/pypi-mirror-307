import re
from pathlib import Path
from typing import Pattern
from pyeio.core.types import FilePath


def open_text(path: FilePath) -> str:
    """
    Open a text file as a string.

    Args:
        path (FilePath): Path to the file.

    Returns:
        str: The data in the file.

    Raises:
        FileNotFoundError: Raised when file is not found.
    """
    with open(path, "r") as file:
        data = file.read()
    file.close()
    return data


def open_text_chars(path: FilePath) -> list[str]:
    """
    Open a text file and read its characters into a list of single characters.

    Args:
        path (FilePath): Path to the file.

    Returns:
        list[str]:  A list containing each character from the file as a string.

    Raises:
        FileNotFoundError: Raised when the file is not found at the specified path.
    """
    data = open_text(path=path)
    chars = list(data)
    return chars


# todo: adjust to stream in data and only keep relevant data in memory to reduce memory usage for large files
# todo: also add progress to all of the `open` functions


# todo.features
# drop_empty: drop empty strings
# logical (if multiple patterns, need to account for combinations of patterns, all, any, not, or, and, etc)
# keep_only: keep only groups containing matching patterns
# drop_match: drop groups containing matching patterns
def open_text_split(
    path: FilePath,
    delimiter: str,
    keep_delimiter: bool = True,
) -> list[str]:
    """
    Open a text file and split it into groups on a regex delimiter.

    Args:
        path (FilePath): Path to the file.
        delimiter (str): The regex string split the file into groups.
        keep (bool, optional): Whether to keep the delimiter. Defaults to True.

    Returns:
        list[str]: _description_
    """
    ...


# def open_text_tokens(
#     path: FilePath,
#     match: str | None,
#     groups
# )


def open_text_lines(path: FilePath) -> list[str]:
    """
    Open a text file and read its lines into a list of strings.

    Args:
        path (FilePath): Path to the file.

    Returns:
        list[str]: A list containing each line from the file as a string.

    Raises:
        FileNotFoundError: Raised when the file is not found at the specified path.
    """
    data = open_text(path=path)
    lines = data.split("\n")
    return lines


def save_text(
    data: str,
    path: str | Path,
    overwrite: bool = False,
) -> None:
    path = Path(path)
    if path.exists() and (not overwrite):
        raise FileExistsError(str(path))
    with open(path, "w") as file:
        file.write(data)
    file.close()


# def find_text(): ...


# def save_text_lines(): ...


# def read_text(): ...


# def read_text_lines(): ...


# def read_text_chars(): ...


# def read_text_chunk(path: FilePath, start: int, end: int) -> str: ...


# def read_text_segments():
#     """set start and end delimiters and stream the text between these"""
#     ...


# def append_text(): ...


# def prepend_text(): ...


# def insert_text(): ...


# def delete_text(): ...


# def append_text_line(): ...


# def append_text_lines(): ...


# def prepend_text_line(): ...


# def prepend_text_lines(): ...


# def insert_text_line(): ...


# def insert_text_lines(): ...


# def delete_text_line(): ...


# def delete_text_lines(): ...


# # def load_binary(): ...


# def open_binary_chunk(path: FilePath, start: int = 0, end: int | None = None) -> bytes:
#     """
#     start byte index
#     end byte index
#     """
#     ...


# def save_binary(): ...

# def open_text_chunk(path: FilePath, start: int = 0, end: int | None = None):
#     """
#     start char index
#     end char index
#     """
#     ...

# todo: add append and prepend data functions
# todo: add binary functions
# todo: add analogous web functions (load, stream)
