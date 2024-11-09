from pytest import raises
from pyeio import json
from pyeio.common.exceptions import (
    MissingFileExtensionError,
    UnsupportedFileExtensionError,
    IncorrectFileExtensionError,
)


def test_parse_types():
    with raises(TypeError):
        _ = json.parse(data={"asdf", "1234"})  # type: ignore
