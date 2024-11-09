from typing import Optional
from pathlib import Path
from urllib.parse import urlparse
from pyeio.common.types import FilePath
from pyeio import __meta__


class UnexpectedError(Exception):
    """Raised when something unexpected happens."""

    def __init__(
        self,
        details: Optional[str] = None,
        issues: bool = True,
    ) -> None:
        self.message = "This was unexpected!"
        if details:
            self.message += f"\nDetails: {details}"
        if issues:
            self.message += f"\nPlease submit a GitHub issue with the code that generated this error at:\n{__meta__.__issues__}"
        super().__init__(self.message)


class IncorrectFileExtensionError(Exception):
    """Raised when the provided extension does not match the expected extension(s)."""

    def __init__(
        self,
        file_extension: str,
        compatible_extensions: set[str],
    ) -> None:
        self.file_extension = file_extension
        self.compatible_extensions = compatible_extensions
        self.message = f"Extension '{self.file_extension}' should be in '{self.compatible_extensions}'"
        super().__init__(self.message)


class MissingExtraError(Exception):
    def __init__(self, extra: str, *args: object) -> None:
        self.message = f"To use this module install: '{__meta__.__package__}[{extra}]'"
        super().__init__(*args)


class MissingFileExtensionError(Exception):
    """Raised when the file in question doesn't have an extension."""

    def __init__(
        self,
        file: str,
    ) -> None:
        self.message = f"'{file}' does not have a file extension. You may be able to bypass this by passing 'False' to the parameter that validates file extensions."
        super().__init__(self.message)


class UnsupportedFileExtensionError(Exception):
    """Raised when the provided extension is not known/supported yet."""

    def __init__(
        self,
        extension: str,
    ) -> None:
        self.extension = extension
        self.message = f"'{self.extension}' is not yet supported."
        super().__init__(self.message)
