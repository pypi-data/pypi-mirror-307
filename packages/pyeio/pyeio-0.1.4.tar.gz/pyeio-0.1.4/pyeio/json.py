import json
from pathlib import Path
from pyeio.core.types import FilePath, PyJSON, SerializedJSON
from pyeio.file import utils
from pyeio.io import web, loc


def parse(data: SerializedJSON) -> PyJSON:
    """
    Just calls `json.loads`. Included to increase API standardization between different formats.

    Args:
        data (SerializedJSON): Serialized JSON data as type (`str`, `bytes`, or `bytearray`).

    Returns:
        PyJSON: JSON data as built-in python data structure(s).
    """
    json_data = json.loads(data)
    return json_data


def serialize(
    data: PyJSON,
    skipkeys: bool = False,
    ensure_ascii: bool = False,
    check_circular: bool = True,
    allow_nan: bool = True,
    sort_keys: bool = True,
    compact_serialization: bool = True,
) -> str:
    """
    Just calls `json.dumps`. Included to increase API standardization between different formats.

    Args:
        data (PyJSON): JSON data to serialize.
        skipkeys (bool, optional): Skip `dict` keys that are not in (`str`,`int`,`float`,`bool`,`None`) instead of raising `TypeError`. Defaults to False.
        ensure_ascii (bool, optional): Ensure the serialized string only contains ascii characters. Defaults to False.
        check_circular (bool, optional): Check circular reference for container types to avoid `RecursionError`. Defaults to True.
        allow_nan (bool, optional): Allow (`nan`, `inf`, `-inf`) values. Defaults to True.
        sort_keys (bool, optional): Sort the output dictionaries by key. Defaults to True.
        compact_serialization (bool, optional): Make the serialization compact. Set to `False` to pretty format. Defaults to True.

    Returns:
        str: Serialized JSON data.
    """
    indent = None if compact_serialization else 4
    separators = (",", ":") if compact_serialization else (", ", ": ")
    serialized_data = json.dumps(
        data,
        skipkeys=skipkeys,
        ensure_ascii=ensure_ascii,
        check_circular=check_circular,
        allow_nan=allow_nan,
        indent=indent,
        separators=separators,
        sort_keys=sort_keys,
    )
    return serialized_data


def open(
    path: FilePath,
    validate_file_extension: bool = True,
) -> PyJSON:
    """
    Open a JSON file.

    Args:
        path (FilePath): The path to the file as a `str` or `pathlib.Path`.
        validate_file_extension (bool, optional): Validate the file extension is supported and correct. Defaults to True.

    Returns:
        PyJSON: JSON data as built-in python data structure(s).
    """
    path = Path(path)
    if validate_file_extension:
        utils.run_file_extension_validation(
            module_name="json",
            path=path,
        )
    serialized_json: str = loc.open_text(path=path)
    json_data = parse(serialized_json)
    return json_data


def save(
    data: PyJSON,
    path: FilePath,
    overwrite: bool = False,
    skipkeys: bool = False,
    ensure_ascii: bool = False,
    check_circular: bool = True,
    allow_nan: bool = True,
    sort_keys: bool = True,
    compact_serialization: bool = True,
    validate_file_extension: bool = True,
) -> None:
    """
    Save data to a JSON file.

    Args:
        data (PyJSON): JSON compatible python data structure data to serialize and save.
        path (FilePath): The path to the file as a `str` or `pathlib.Path`.
        overwrite (bool, optional): Allow existing file to be overwritten. Defaults to False.
        data (PyJSON): JSON data to serialize.
        skipkeys (bool, optional): Skip `dict` keys that are not in (`str`,`int`,`float`,`bool`,`None`) instead of raising `TypeError`. Defaults to False.
        ensure_ascii (bool, optional): Ensure the serialized string only contains ascii characters. Defaults to False.
        check_circular (bool, optional): Check circular reference for container types to avoid `RecursionError`. Defaults to True.
        allow_nan (bool, optional): Allow (`nan`, `inf`, `-inf`) values. Defaults to True.
        sort_keys (bool, optional): Sort the output dictionaries by key. Defaults to True.
        compact_serialization (bool, optional): Make the serialization compact. Set to `False` to pretty format. Defaults to True.
        validate_file_extension (bool, optional): Validate the file extension is supported and correct. Defaults to True.
    """
    path = Path(path)
    if validate_file_extension:
        utils.run_file_extension_validation(
            module_name="json",
            path=path,
        )
    serialized_json: str = serialize(
        data=data,
        skipkeys=skipkeys,
        ensure_ascii=ensure_ascii,
        check_circular=check_circular,
        allow_nan=allow_nan,
        sort_keys=sort_keys,
        compact_serialization=compact_serialization,
    )
    loc.save_text(data=serialized_json, path=path, overwrite=overwrite)


def load(
    url: str,
    chunk_size: int = 1 << 10,
    follow_redirects: bool = True,
    evaluate_size: bool | None = None,
    show_progress: bool = False,
    show_file_name: bool = True,
) -> PyJSON:
    """
    Load a JSON file at a URL directly into memory.

    Args:
        url (str): The URL of the JSON file.
        chunk_size (int, optional): The size of chunks to use when downloading. Defaults to 1024 bytes.
        follow_redirects (bool, optional): If True, follows HTTP redirects. Defaults to True.
        evaluate_size (bool, optional): Evaluate the size of the resource before downloading. Defaults to None.
        show_progress (bool, optional): Show progress bar. Defaults to False.
        show_file_name (bool, optional): Show name of file in progress bar if used. Defaults to True.

    Returns:
        PyJSON: JSON data as built-in python data structure(s).
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
    # todo.fix: need to do character detection and account for when utf-8 fails
    serialized_data = binary_data.decode("utf-8")
    # todo.ext: additionally, do mime detection, data detection, add a bunch of params for exp features
    json_data = parse(serialized_data)
    return json_data


def download(
    url: str,
    path: FilePath,
    overwrite: bool = False,
    skipkeys: bool = False,
    ensure_ascii: bool = False,
    check_circular: bool = True,
    allow_nan: bool = True,
    sort_keys: bool = True,
    compact_serialization: bool = True,
    validate_file_extension: bool = True,
    chunk_size: int = 1 << 10,
    follow_redirects: bool = True,
    evaluate_size: bool | None = None,
    show_progress: bool = False,
    show_file_name: bool = True,
) -> None:
    """
    Download a JSON file at a URL directly to a local JSON file on disk.

    Args:
        url (str): The URL of the JSON file.
        path (FilePath): The path to the file as a `str` or `pathlib.Path`.
        overwrite (bool, optional): Allow existing file to be overwritten. Defaults to False.
        data (PyJSON): JSON data to serialize.
        skipkeys (bool, optional): Skip `dict` keys that are not in (`str`,`int`,`float`,`bool`,`None`) instead of raising `TypeError`. Defaults to False.
        ensure_ascii (bool, optional): Ensure the serialized string only contains ascii characters. Defaults to False.
        check_circular (bool, optional): Check circular reference for container types to avoid `RecursionError`. Defaults to True.
        allow_nan (bool, optional): Allow (`nan`, `inf`, `-inf`) values. Defaults to True.
        sort_keys (bool, optional): Sort the output dictionaries by key. Defaults to True.
        compact_serialization (bool, optional): Make the serialization compact. Set to `False` to pretty format. Defaults to True.
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
            module_name="json",
            path=path,
        )
    if path.exists() and (not overwrite):
        raise FileExistsError(str(path))
    json_data = load(
        url=url,
        chunk_size=chunk_size,
        follow_redirects=follow_redirects,
        evaluate_size=evaluate_size,
        show_progress=show_progress,
        show_file_name=show_file_name,
    )
    save(
        data=json_data,
        path=path,
        overwrite=overwrite,
        skipkeys=skipkeys,
        ensure_ascii=ensure_ascii,
        check_circular=check_circular,
        allow_nan=allow_nan,
        sort_keys=sort_keys,
        compact_serialization=compact_serialization,
        validate_file_extension=validate_file_extension,
    )
