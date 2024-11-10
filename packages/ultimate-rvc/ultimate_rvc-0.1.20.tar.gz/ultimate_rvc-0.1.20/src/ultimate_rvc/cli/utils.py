"""
Module which defines the utilities command for the Ultimate RVC
CLI.
"""

import typer
from rich import print as rprint

from ultimate_rvc.core.common import download_base_models
from ultimate_rvc.core.generate.song_cover import initialize_audio_separator
from ultimate_rvc.core.manage.models import download_sample_models

app = typer.Typer(
    name="utils",
    no_args_is_help=True,
    help="Common utilities for the Ultimate RVC project",
    rich_markup_mode="markdown",
)


@app.command()
def initialize() -> None:
    """Initialize the Ultimate RVC project."""
    download_base_models()
    download_sample_models()
    initialize_audio_separator()
    rprint("Initialization complete.")


if __name__ == "__main__":
    app()
