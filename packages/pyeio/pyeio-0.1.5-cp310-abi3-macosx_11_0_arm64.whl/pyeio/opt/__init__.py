import psutil
from pydantic import PositiveInt
from pathlib import Path
from pyeio.core.types import FilePath
from . import py

# todo: add automatic fallback to py functions if rust is unavailable
try:
    from . import rs
except ImportError:
    # todo: replace with custom exception
    raise Exception(
        "Missing rust binaries. Please submit a GitHub issue and I'll try and get to the bottom of this."
    )


def count_lines_in_file(
    path: FilePath,
    chunk_size: PositiveInt = 1 << 20,
    num_threads: PositiveInt | None = None,
) -> int:
    """
    Count the number of lines in a file.

    Args:
        path (FilePath): Path to the file.
        chunk_size (PositiveInt, optional): Size of chunks to read in bytes. Defaults to 1<<20.
        num_threads (PositiveInt | None, optional): Number of threads to use. If `None`, automatically determined.

    Returns:
        int: _description_
    """
    path = str(path)
    if not Path(path).exists():
        raise FileNotFoundError(path)
    if chunk_size < 1:
        raise TypeError(f"'chunk_size' must be a positive integer, is: {chunk_size}")
    num_available_threads = psutil.cpu_count(logical=True)
    if num_threads is None:
        num_threads = int(num_available_threads / 1.5)
    else:
        if num_threads < 1:
            raise TypeError(
                f"'num_threads' must be a positive integer, is: {num_threads}"
            )
        elif num_threads > num_available_threads:
            raise ValueError(
                f"Requested more threads than available ({num_threads} > {num_available_threads})"
            )
    return rs.count_lines_in_file(path, chunk_size, num_threads)
