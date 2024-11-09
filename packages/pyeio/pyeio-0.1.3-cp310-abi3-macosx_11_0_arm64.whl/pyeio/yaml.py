import yaml
from pathlib import Path
from pyeio.common.types import FilePath, PyYAML, SerializedYAML
from pyeio.common.exceptions import MissingExtraError
from pyeio.file import io, utils
from pyeio.io import web


try:
    import yaml
except ImportError:
    raise MissingExtraError(extra="yaml")


# todo: add and account for yaml base lib parameters


def parse(data: SerializedYAML) -> PyYAML:
    if isinstance(data, bytes):
        # todo: add chardet detection
        data = data.decode("utf-8")
    if not isinstance(data, str):
        raise TypeError(
            f"Expected data to be of type 'str' or 'bytes', got {type(data)}"
        )
    yaml_data = yaml.safe_load(data)
    return yaml_data


def serialize(data: PyYAML, default_flow_style: bool = False) -> str:
    serialized_data = yaml.dump(data, default_flow_style=default_flow_style)
    return serialized_data


def open(
    path: FilePath,
    validate_file_extension: bool = True,
) -> PyYAML:
    path = Path(path)
    if validate_file_extension:
        utils.run_file_extension_validation(
            module_name="yaml",
            path=path,
        )
    serialized_yaml = io.open_text(path=path)
    return parse(serialized_yaml)


def save(
    data: PyYAML,
    path: FilePath,
    overwrite: bool = False,
    default_flow_style: bool = False,
    validate_file_extension: bool = True,
) -> None:
    """
    Save data to a YAML file.

    Args:
        data (PyYAML): YAML-compatible Python data structure to serialize and save.
        path (FilePath): The path to the file as a `str` or `pathlib.Path`.
        overwrite (bool, optional): Allow existing file to be overwritten. Defaults to False.
        default_flow_style (bool, optional): Set to True to use the block style for nested collections. Defaults to False.
        validate_file_extension (bool, optional): Validate the file extension is supported and correct. Defaults to True.
    """
    path = Path(path)
    if validate_file_extension:
        utils.run_file_extension_validation(
            module_name="yaml",
            path=path,
        )
    serialized_yaml: str = serialize(data, default_flow_style=default_flow_style)
    io.save_text(data=serialized_yaml, path=path, overwrite=overwrite)


def load(
    url: str,
    chunk_size: int = 1 << 10,
    follow_redirects: bool = True,
    evaluate_size: bool | None = None,
    show_progress: bool = False,
    show_file_name: bool = True,
) -> PyYAML:
    """
    Load a YAML file from a URL directly into memory.

    Args:
        url (str): The URL of the YAML file.
        chunk_size (int, optional): The size of chunks to use when downloading. Defaults to 1024 bytes.
        follow_redirects (bool, optional): If True, follows HTTP redirects. Defaults to True.
        evaluate_size (bool, optional): Evaluate the size of the resource before downloading. Defaults to None.
        show_progress (bool, optional): Show progress bar. Defaults to False.
        show_file_name (bool, optional): Show name of file in progress bar if used. Defaults to True.

    Returns:
        PyYAML: YAML data as built-in Python data structures.
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
    yaml_data = parse(serialized_data)
    return yaml_data


def download(
    url: str,
    path: FilePath,
    overwrite: bool = False,
    default_flow_style: bool = False,
    validate_file_extension: bool = True,
    chunk_size: int = 1 << 10,
    follow_redirects: bool = True,
    evaluate_size: bool | None = None,
    show_progress: bool = False,
    show_file_name: bool = True,
) -> None:
    """
    Download a YAML file from a URL directly to a local YAML file on disk.

    Args:
        url (str): The URL of the YAML file.
        path (FilePath): The path to the file as a `str` or `pathlib.Path`.
        overwrite (bool, optional): Allow existing file to be overwritten. Defaults to False.
        default_flow_style (bool, optional): Set to True to use the block style for nested collections. Defaults to False.
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
            module_name="yaml",
            path=path,
        )
    if path.exists() and not overwrite:
        raise FileExistsError(str(path))
    yaml_data = load(
        url=url,
        chunk_size=chunk_size,
        follow_redirects=follow_redirects,
        evaluate_size=evaluate_size,
        show_progress=show_progress,
        show_file_name=show_file_name,
    )
    save(
        data=yaml_data,
        path=path,
        overwrite=overwrite,
        default_flow_style=default_flow_style,
        validate_file_extension=validate_file_extension,
    )
