"""Contains an example function."""

from __future__ import annotations

import logging
import sys
from typing import Optional

import typer

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = typer.Typer()


@app.command()
def echo(args: list[str]) -> None:
    """My function Docstring.

    And here is an example doctest.

        >>> main(["Alice"])
        Hello Alice

    Returns:
        Hello + the first argument, if provided.
    """
    for k, v in enumerate(args):
        sys.stdout.write(f"args[{k}] = {v}\n")


@app.command()
def constant(args: list[str]) -> None:
    """Say hello n times."""
    for i in range(len(args)):
        sys.stdout.write(f"Hello {i}\n")


@app.command()
def hello(_: Optional[list[str]] = None) -> None:
    """Say hello."""
    sys.stdout.write("Hello")
