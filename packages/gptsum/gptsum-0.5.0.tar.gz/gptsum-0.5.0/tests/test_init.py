"""Tests for :mod:`gptsum`."""

import os
import uuid
from pathlib import Path
from typing import Any, Callable, List

import pytest

import gptsum
from tests import conftest, utils


@pytest.mark.parametrize(("attr"), ["author", "contact", "license", "version"])
def test_attribute(attr: str) -> None:
    """Test expected metadata attributes on the package."""
    real_attr = f"__{attr}__"
    assert hasattr(gptsum, real_attr)
    # pylint: disable-next=unidiomatic-typecheck
    assert type(getattr(gptsum, real_attr)) is str


@pytest.mark.parametrize(
    ("func", "args"),
    [
        (gptsum.get_guid, []),
        (gptsum.set_guid, [uuid.UUID("656156c4-2456-4038-b7f3-dfa0ae263e95")]),
        (gptsum.calculate_expected_guid, []),
        (gptsum.embed, []),
        (gptsum.verify, []),
    ],
)
def test_argument_conflicts(func: Callable[..., Any], args: List[Any]) -> None:
    """Ensure ``fd``/``path`` can't be passed at the same time."""
    with pytest.raises(ValueError, match="Either fd or path must be given"):
        func(*args, fd=None, path=None)

    with pytest.raises(ValueError, match="Both fd and path can't be given"):
        func(*args, fd=0, path=Path("/"))


@pytest.mark.parametrize(
    ("disk_file", "expected_guid"),
    [
        (conftest.TESTDATA_DISK, conftest.TESTDATA_DISK_GUID),
        (conftest.TESTDATA_EMBEDDED_DISK, conftest.TESTDATA_EMBEDDED_DISK_GUID),
    ],
)
def test_get_guid(disk_file: Path, expected_guid: uuid.UUID) -> None:
    """Test :func:`gptsum.get_guid`."""
    assert gptsum.get_guid(path=disk_file) == expected_guid

    with open(disk_file, "rb") as fd:
        assert gptsum.get_guid(fd=fd.fileno()) == expected_guid


@pytest.mark.parametrize(("method"), ["by_fd", "by_path"])
def test_set_guid(method: str, disk_image: Path) -> None:
    """Test :func:`gptsum.set_guid`."""
    new_guid = uuid.UUID("e81f41f2-1807-49aa-876b-57a7e727b3f8")

    assert gptsum.get_guid(path=disk_image) != new_guid

    if method == "by_fd":
        with open(disk_image, "rb+") as fd:
            gptsum.set_guid(new_guid, fd=fd.fileno())
    else:
        assert method == "by_path"
        gptsum.set_guid(new_guid, path=disk_image)

    assert gptsum.get_guid(path=disk_image) == new_guid


@pytest.mark.parametrize(
    ("disk_file", "expected_guid"),
    [
        (conftest.TESTDATA_DISK, conftest.TESTDATA_EMBEDDED_DISK_GUID),
        (conftest.TESTDATA_EMBEDDED_DISK, conftest.TESTDATA_EMBEDDED_DISK_GUID),
    ],
)
def test_calculate_expected_guid(disk_file: Path, expected_guid: uuid.UUID) -> None:
    """Test :func:`gptsum.calculate_expected_guid`."""
    assert gptsum.calculate_expected_guid(path=disk_file) == expected_guid

    with open(disk_file, "rb") as fd:
        assert gptsum.calculate_expected_guid(fd=fd.fileno()) == expected_guid


@pytest.mark.parametrize(("method"), ["by_fd", "by_path"])
def test_embed(method: str, disk_image: Path) -> None:
    """Test :func:`gptsum.embed`."""
    if method == "by_fd":
        with open(disk_image, "rb+") as fd:
            gptsum.embed(fd=fd.fileno())
    else:
        assert method == "by_path"
        gptsum.embed(path=disk_image)

    guid = gptsum.get_guid(path=disk_image)
    assert guid == conftest.TESTDATA_EMBEDDED_DISK_GUID

    utils.assert_files_equal(
        conftest.TESTDATA_EMBEDDED_DISK,
        disk_image,
    )


def test_embed_noop(disk_image: Path) -> None:
    """Test to ensure issuing :option:`embed` on an already-prepared file is a no-op."""
    gptsum.embed(path=disk_image)
    stat1 = os.stat(disk_image)
    gptsum.embed(path=disk_image)
    stat2 = os.stat(disk_image)

    assert stat2.st_mtime == stat1.st_mtime
    assert stat2.st_ctime == stat1.st_ctime


@pytest.mark.parametrize(("method"), ["by_fd", "by_path"])
def test_verify(method: str, disk_image: Path) -> None:
    """Test :func:`gptsum.verify`."""
    if method == "by_fd":
        with open(disk_image, "rb") as fd:
            with pytest.raises(gptsum.VerificationFailure):
                gptsum.verify(fd=fd.fileno())
    else:
        assert method == "by_path"
        with pytest.raises(gptsum.VerificationFailure):
            gptsum.verify(path=disk_image)

    gptsum.embed(path=disk_image)

    if method == "by_fd":
        with open(disk_image, "rb") as fd:
            gptsum.verify(fd=fd.fileno())
    else:
        assert method == "by_path"
        gptsum.verify(path=disk_image)
