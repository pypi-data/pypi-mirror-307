from pathlib import Path
from typing import Callable, Generator, Any
from zstandard import ZstdDecompressor


MAX_WINDOW_SIZE: int = 1 << 31


class Streamer: ...


class Reader:
    def __init__(
        self,
        file_path: str | Path,
        chunk_delimiter: bytes,
        chunk_parser: Callable[[bytes], Any] = lambda x: x,
        block_size_bytes: int = 1 << 20,
    ) -> None:
        self.file_path = file_path
        self.chunk_delimiter = chunk_delimiter
        self.chunk_parser = chunk_parser
        self.block_size_bytes = block_size_bytes
        self.reset()

    def reset(self) -> None:
        self.stream = ZstdDecompressor(
            max_window_size=MAX_WINDOW_SIZE,
        ).stream_reader(open(self.file_path, "rb"))
        self.buffer = b""
        self.chunks = []

    def __iter__(self) -> Generator[bytes, None, None]:
        while True:
            try:
                yield next(self)
            except StopIteration:
                break

    def __next__(self) -> bytes | Any:
        if len(self.chunks):
            current = self.chunks.pop(0)
            return self.chunk_parser(current)
        else:
            chunk = self.stream.read(self.block_size_bytes)
            if chunk:
                self.chunks = (self.buffer + chunk).split(self.chunk_delimiter)
                self.buffer = self.chunks[-1]
                self.chunks = self.chunks[:-1]
                current = self.chunks.pop(0)
                return self.chunk_parser(current)
            else:
                raise StopIteration()

    def read_chunk(self) -> bytes | Any:
        return self.__next__()

    def read_chunks(self, n: int) -> list[bytes] | list[Any]:
        return [self.read_chunk() for _ in range(n)]


def read(
    file_path: str | Path,
    chunk_delimiter: bytes = b"\n",
    block_size: int = 1 << 20,
    parser: Callable[[bytes], Any] = lambda x: x,
) -> Generator[bytes, None, None] | Generator[Any, None, None]:
    reader = Reader(
        file_path=file_path,
        chunk_delimiter=chunk_delimiter,
        block_size_bytes=block_size,
        chunk_parser=parser,
    )
    for chunk in reader:
        yield chunk


def compress():
    """Compress an existing file to ZST."""
    raise NotImplementedError()


def decompress():
    """Decompress an existing file."""
    raise NotImplementedError()


# def load():
#     """Decompress and load entire file into memory as bytes."""
#     raise NotImplementedError()


def save(data: bytes, path: str | Path) -> None:
    """Compress and save serializable data to .zst file."""
    raise NotImplementedError()


# from pyeio.core.types import FilePath


# def read(): ...


# def read_lines(): ...


# def compress(source: FilePath, target: FilePath): ...


# def decompress(source: FilePath, target: FilePath): ...
