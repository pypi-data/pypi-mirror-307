from pathlib import Path
from pyeio.common.types import FilePath, PyTOML, SerializedTOML
from pyeio.common.exceptions import MissingExtraError
from pyeio.file import io, utils
from pyeio.io import web

try:
    import toml
except ImportError:
    raise MissingExtraError(extra="toml")


def parse(data: SerializedTOML) -> PyTOML:
    if isinstance(data, bytes):
        # todo.fix: will not always work
        data = str(data.decode())
    if not isinstance(data, str):
        # todo: add details on type error
        raise TypeError()
    toml_data = toml.loads(data)
    return toml_data


def serialize(data: PyTOML) -> str:
    serialized_data = toml.dumps(data)
    return serialized_data


def open(
    path: FilePath,
    validate_file_extension: bool = True,
) -> PyTOML:
    path = Path(path)
    if validate_file_extension:
        utils.run_file_extension_validation(
            module_name="toml",
            path=path,
        )
    serialized_toml = io.open_text(path=path)
    return parse(serialized_toml)


def save(
    data: PyTOML,
    path: FilePath,
    overwrite: bool = False,
    validate_file_extension: bool = True,
) -> None:
    """
    Save data to a TOML file.

    Args:
        data (PyTOML): TOML-compatible Python data structure to serialize and save.
        path (FilePath): The path to the file as a `str` or `pathlib.Path`.
        overwrite (bool, optional): Allow existing file to be overwritten. Defaults to False.
        validate_file_extension (bool, optional): Validate the file extension is supported and correct. Defaults to True.
    """
    path = Path(path)
    if validate_file_extension:
        utils.run_file_extension_validation(
            module_name="toml",
            path=path,
        )
    serialized_toml: str = serialize(data)
    io.save_text(data=serialized_toml, path=path, overwrite=overwrite)


def load(
    url: str,
    chunk_size: int = 1 << 10,
    follow_redirects: bool = True,
    evaluate_size: bool | None = None,
    show_progress: bool = False,
    show_file_name: bool = True,
) -> PyTOML:
    """
    Load a TOML file from a URL directly into memory.

    Args:
        url (str): The URL of the TOML file.
        chunk_size (int, optional): The size of chunks to use when downloading. Defaults to 1024 bytes.
        follow_redirects (bool, optional): If True, follows HTTP redirects. Defaults to True.
        evaluate_size (bool, optional): Evaluate the size of the resource before downloading. Defaults to None.
        show_progress (bool, optional): Show progress bar. Defaults to False.
        show_file_name (bool, optional): Show name of file in progress bar if used. Defaults to True.

    Returns:
        PyTOML: TOML data as built-in Python data structures.
    """
    if evaluate_size is None:
        evaluate_size = show_progress
    binary_data = web.load_binary(
        url=url,
        chunk_size=chunk_size,
        follow_redirects=follow_redirects,
        evaluate_size=evaluate_size,
        show_progress=show_progress,
        show_file_name=show_file_name,
    )
    serialized_data = binary_data.decode("utf-8")
    toml_data = parse(serialized_data)
    return toml_data


def download(
    url: str,
    path: FilePath,
    overwrite: bool = False,
    validate_file_extension: bool = True,
    chunk_size: int = 1 << 10,
    follow_redirects: bool = True,
    evaluate_size: bool | None = None,
    show_progress: bool = False,
    show_file_name: bool = True,
) -> None:
    """
    Download a TOML file from a URL directly to a local TOML file on disk.

    Args:
        url (str): The URL of the TOML file.
        path (FilePath): The path to the file as a `str` or `pathlib.Path`.
        overwrite (bool, optional): Allow existing file to be overwritten. Defaults to False.
        validate_file_extension (bool, optional): Validate the file extension is supported and correct. Defaults to True.
        chunk_size (int, optional): The size of chunks to use when downloading. Defaults to 1024 bytes.
        follow_redirects (bool, optional): If True, follows HTTP redirects. Defaults to True.
        evaluate_size (bool, optional): Evaluate the size of the resource before downloading. Defaults to None.
        show_progress (bool, optional): Show progress bar. Defaults to False.
        show_file_name (bool, optional): Show name of file in progress bar if used. Defaults to True.

    Raises:
        FileExistsError: File already exists. Set `overwrite` to `True` to bypass.
    """
    if evaluate_size is None:
        evaluate_size = show_progress
    path = Path(path)
    if validate_file_extension:
        utils.run_file_extension_validation(
            module_name="toml",
            path=path,
        )
    if path.exists() and (not overwrite):
        raise FileExistsError(str(path))
    toml_data = load(
        url=url,
        chunk_size=chunk_size,
        follow_redirects=follow_redirects,
        evaluate_size=evaluate_size,
        show_progress=show_progress,
        show_file_name=show_file_name,
    )
    save(
        data=toml_data,
        path=path,
        overwrite=overwrite,
        validate_file_extension=validate_file_extension,
    )
