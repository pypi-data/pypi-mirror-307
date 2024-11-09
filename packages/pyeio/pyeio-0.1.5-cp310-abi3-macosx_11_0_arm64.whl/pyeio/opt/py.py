# This file is unrelated to PyPy - it's just for profiling differences in speed of same underlying functionality.

from pydantic import PositiveInt
from pyeio.core.types import FilePath


def count_lines_in_file(path: FilePath, chunk_size: PositiveInt = 1 << 20) -> int:
    """
    Count the number of lines in a file.

    Args:
        path (FilePath): Path to the file.
        chunk_size (PositiveInt, optional): Size of chunks to read in bytes. Defaults to 1<<20.

    Returns:
        int: Number of lines in the file.
    """

    lines = 0
    with open(path, "rb") as f:
        read_chunk = f.read
        chunk = read_chunk(chunk_size)
        while chunk:
            lines += chunk.count(b"\n")
            chunk = read_chunk(chunk_size)
    return lines
