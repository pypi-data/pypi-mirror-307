"""Root module for the typer application."""

import sys

import typer

import gfp.example

app = typer.Typer(no_args_is_help=True)
app.add_typer(gfp.example.app, name="ex", no_args_is_help=True, help="Example commands.")


@app.command(no_args_is_help=True)
def aws(cmd: str = "") -> None:
    """AWS-related commands."""
    sys.stdout.write(f"You called: aws {cmd}\n")
