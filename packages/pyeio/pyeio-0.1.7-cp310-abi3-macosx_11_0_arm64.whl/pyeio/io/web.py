import httpx
from io import BytesIO
from pathlib import Path
from typing import Optional
from tqdm import tqdm
from pyeio.file import utils

# todo: add user agent as parameter to remaining functions
# todo: add cookies to functions
# todo.ext: httpx params


def _add_custom_user_agent_to_headers(
    user_agent: Optional[str],
    headers: dict[str, str],
) -> dict[str, str]:
    if not (user_agent is None):
        headers["user-agent"] = user_agent
    return headers


def check_if_remote_accepts_byte_range(
    url: str,
    follow_redirects: bool = True,
    user_agent: Optional[str] = None,
) -> bool:
    """
    Check if a remote server accepts byte range requests.

    This function sends a HEAD request to the specified URL with a 'Range' header
    to determine if the server supports partial content requests.

    Args:
        url (str): The URL to check for byte range support.
        follow_redirects (bool, optional): Whether to follow redirects. Defaults to True.
        user_agent (str, optional): Optional custom user agent.

    Returns:
        bool: True if the server accepts byte range requests, False otherwise.
    """
    headers = {"Range": "bytes=0-8"}
    headers = _add_custom_user_agent_to_headers(user_agent, headers)
    response = httpx.head(url=url, headers=headers, follow_redirects=follow_redirects)
    response.raise_for_status()
    return response.status_code == 206


def load_binary_chunk(
    url: str,
    start: int,
    end: int,
    follow_redirects: bool = True,
    user_agent: Optional[str] = None,
) -> bytes:
    """
    Read a specific byte range from a remote resource.

    This function sends a GET request to the specified URL with a 'Range'
    header to retrieve a specific chunk of the resource.

    Args:
        url (str): The URL of the remote resource.
        start (int): The starting byte position of the chunk.
        end (int): The ending byte position of the chunk.
        follow_redirects (bool, optional): Whether to follow redirects. Defaults to True.
        user_agent (str, optional): Optional custom user agent.

    Returns:
        bytes: The requested chunk of the resource as bytes.

    Raises:
        Exception: If the remote server does not accept byte range requests.
    """
    headers = {"Range": f"bytes={start}-{end}"}
    headers = _add_custom_user_agent_to_headers(user_agent, headers)
    buffer = BytesIO()
    response = httpx.get(url, headers=headers, follow_redirects=follow_redirects)
    response.raise_for_status()
    if response.status_code != 206:
        raise Exception("The remote server does not accept byte range requests.")
    buffer.write(response.content)
    buffer.seek(0)
    return buffer.read()


def request_content_length(
    url: str,
    follow_redirects: bool = True,
    user_agent: Optional[str] = None,
) -> int:
    """
    Get the content length of a remote resource.

    This function sends a HEAD request to the specified URL and retrieves
    the 'Content-Length' header value.

    Args:
        url (str): The URL of the remote resource.
        follow_redirects (bool, optional): Whether to follow redirects. Defaults to True.
        user_agent (str, optional): Optional custom user agent.

    Returns:
        int: The content length of the resource in bytes.

    Raises:
        KeyError: If the 'Content-Length' header is not found in the response.
    """
    headers = dict()
    headers = _add_custom_user_agent_to_headers(user_agent, headers)
    response = httpx.head(url, headers=headers, follow_redirects=follow_redirects)
    response.raise_for_status()
    headers = {k.lower(): v for k, v in dict(response.headers).items()}
    if "content-length" not in headers.keys():
        raise KeyError("'content-length' header not found")
    else:
        return int(headers["content-length"])


def estimate_resource_size(
    url: str,
    initial_guess: int = 1 << 20,
    max_requests: int = 10,
    user_agent: Optional[str] = None,
) -> int:
    """
    Estimates the content length of a resource by making strategic byte range requests.

    Args:
        url (str): The URL of the resource.
        initial_guess (int): Initial guess for the file size in bytes. Default is 1MB.
        max_requests (int): Maximum number of requests to make before giving up.
        user_agent (str, optional): Optional custom user agent.

    Returns:
        int: Estimated content length in bytes
    """
    headers = dict()
    headers = _add_custom_user_agent_to_headers(user_agent, headers)
    with httpx.Client(headers=headers) as httpx_client:
        lower_bound = 0
        upper_bound = initial_guess
        requests_made = 0
        while requests_made < max_requests:
            requests_made += 1
            mid = (lower_bound + upper_bound) // 2
            headers = {"Range": f"bytes={mid}-{mid}"}
            response = httpx_client.get(url, headers=headers, follow_redirects=True)
            if response.status_code == 206:
                lower_bound = mid
                if upper_bound == lower_bound + 1:
                    return upper_bound
                if "Content-Range" in response.headers:
                    content_range = response.headers["Content-Range"]
                    total_size = int(content_range.split("/")[-1])
                    return total_size
            elif response.status_code == 416:
                upper_bound = mid
            else:
                raise Exception(
                    f"Unexpected status code: {response.status_code}",
                )
            if upper_bound - lower_bound <= 1:
                return upper_bound
            if upper_bound == initial_guess:
                upper_bound *= 2
        raise Exception("Cannot estimate remote resource size")


def get_resource_size(
    url: str,
    user_agent: Optional[str] = None,
) -> int:
    """
    Get the size of a remote resource.

    This function attempts to determine the size of a remote resource using different methods.
    It first tries to get the content length using a basic request. If that fails, it checks
    if the server accepts byte range requests. If so, it estimates the content length dynamically.

    Args:
        url (str): The URL of the remote resource.

    Returns:
        int: The size of the remote resource in bytes.

    Raises:
        Exception: If the size of the remote resource cannot be determined.
    """
    # headers = dict()
    # headers = _add_custom_user_agent_to_headers(user_agent, headers)
    try:
        size = request_content_length(url, user_agent=user_agent)
        return size
    except:
        range_accepted = check_if_remote_accepts_byte_range(url, user_agent=user_agent)
        if range_accepted:
            size = estimate_resource_size(url, user_agent=user_agent)
            return size
        else:
            raise Exception("cannot estimate remote resource size")


def save_file(
    url: str,
    path: str | Path,
    overwrite: bool = False,
    chunk_size: int = 1 << 10,
    follow_redirects: bool = True,
    evaluate_size: bool = True,
    show_progress: bool = False,
    show_file_name: bool = True,
) -> None:
    """
    Download a remote resource to a local file.

    This function downloads a resource from a given URL and saves it to a specified local path.
    It supports progress tracking, overwrite protection, and redirect following.

    Args:
        url (str): The URL of the remote resource to download.
        path (str | Path): The local path where the downloaded resource will be saved.
        allow_overwrite (bool, optional): If True, allows overwriting existing files. Defaults to False.
        chunk_size (int, optional): The size of chunks to use when downloading. Defaults to 1024 bytes.
        show_progress (bool, optional): If True, displays a progress bar during download. Defaults to False.
        follow_redirects (bool, optional): If True, follows HTTP redirects. Defaults to True.

    Raises:
        FileExistsError: If the target file already exists and allow_overwrite is False.
        Exception: If there's an error during the download process.

    Returns:
        None
    """
    path = Path(path)
    if path.exists() and not overwrite:
        raise FileExistsError(str(path))
    size = None
    if evaluate_size:
        size = get_resource_size(url)
    file_name = utils.extract_file_name_from_url(url)
    with open(path, "wb") as file:
        with tqdm(
            total=size,
            unit_scale=True,
            unit="B",
            unit_divisor=chunk_size,
            disable=not show_progress,
            desc=file_name if show_file_name else None,
            ncols=80,
        ) as bar:
            with httpx.stream(
                "GET", url, follow_redirects=follow_redirects
            ) as response:
                for chunk in response.iter_bytes(chunk_size):
                    file.write(chunk)
                    bar.update(len(chunk))
    file.close()


def load_binary(
    url: str,
    chunk_size: int = 1 << 10,
    follow_redirects: bool = True,
    evaluate_size: bool = True,
    show_progress: bool = False,
    show_file_name: bool = True,
) -> bytes:
    """
    Read a remote resource and return its content as bytes.

    This function downloads a resource from a given URL and returns its content as bytes.
    It supports progress tracking and redirect following.

    Args:
        url (str): The URL of the remote resource to read.
        chunk_size (int, optional): The size of chunks to use when downloading. Defaults to 1024 bytes.
        show_progress (bool, optional): If True, displays a progress bar during download. Defaults to False.
        follow_redirects (bool, optional): If True, follows HTTP redirects. Defaults to True.

    Returns:
        bytes: The content of the remote resource.

    Raises:
        Exception: If there's an error during the download process.
    """
    size = None
    if evaluate_size:
        size = get_resource_size(url)
    buffer = BytesIO()
    file_name = utils.extract_file_name_from_url(url)
    with tqdm(
        total=size,
        unit_scale=True,
        unit="B",
        unit_divisor=chunk_size,
        disable=not show_progress,
        desc=file_name if show_file_name else None,
        ncols=80,
    ) as bar:
        with httpx.stream("GET", url, follow_redirects=follow_redirects) as response:
            for chunk in response.iter_bytes(chunk_size):
                buffer.write(chunk)
                bar.update(len(chunk))
    buffer.seek(0)
    data = buffer.read()
    buffer.close()
    return data


# def get(
#     url: str,
#     show_progress: bool = False,
#     user_agent: Optional[str] = None,
# ) -> bytes:
#     """_summary_

#     Args:
#         url (str): _description_
#         progress (bool, optional): _description_. Defaults to False.

#     Returns:
#         bytes: _description_
#     """
#     headers = dict()
#     headers = _add_custom_user_agent_to_headers(user_agent, headers)
#     raise NotImplementedError()


# def download(
#     url: str,
#     path: str | Path,
#     show_progress: bool = False,
#     user_agent: Optional[str] = None,
# ) -> None:
#     """_summary_

#     Args:
#         url (str): _description_
#         path (str | Path): _description_
#         progress (bool, optional): _description_. Defaults to False.
#     """
#     headers = dict()
#     headers = _add_custom_user_agent_to_headers(user_agent, headers)
#     raise NotImplementedError()
