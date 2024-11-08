"""Entrypoints for the gfp package."""

import gfp.typer


# Function entrypoint
def main() -> None:
    """Function entrypoint for the gfp package."""
    gfp.typer.app()


# Module entrypoint
if __name__ == "__main__":
    gfp.typer.app()
