"""This module contains example tests."""

from pathlib import Path

from gfp.example import hello


def test_my_function() -> None:
    expected = None
    assert hello([]) == expected


def test_use_test_resource(resource_dir: Path) -> None:
    assert resource_dir.joinpath("example_resource.txt").is_file()
