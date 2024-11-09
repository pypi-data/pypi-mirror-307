from typing import Generator
from pyeio.core.types import FilePath


class ChunkReader:
    """For reading chunks of data with defined number of bytes in each chunk."""

    def __init__(self, path: FilePath, size: int = 1024) -> None:
        self.path = path
        self.size = size
        self.file = open(self.path, "rb")

    def __next__(self) -> bytes:
        chunk = self.file.read(self.size)
        if chunk:
            return chunk
        else:
            raise StopIteration()

    def __iter__(self) -> Generator[bytes, None, None]:
        while True:
            try:
                yield next(self)
            except StopIteration:
                break

    def reset(self) -> None:
        self.file.seek(0)


class BlockReader:
    """Reads blocks based on whether they match the delimiter pattern"""

    ...


class ParseReader: ...


class TokenReader: ...
