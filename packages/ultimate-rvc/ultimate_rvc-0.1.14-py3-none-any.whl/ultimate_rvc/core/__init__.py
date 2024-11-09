"""
core package for the Ultimate RVC project.

This package contains modules for managing audio files, voice models,
and song cover generation.

"""

from pathlib import Path

import static_ffmpeg
import static_sox
from rich import print as rprint

import requests

from common import RVC_MODELS_DIR
from typing_extra import StrPath

from core.manage_models import download_model

RVC_DOWNLOAD_URL = "https://huggingface.co/lj1995/VoiceConversionWebUI/resolve/main/"


def _download_base_model(url: str, name: str, directory: StrPath) -> None:
    """
    Download a base model and save it to a directory.

    Parameters
    ----------
    url : str
        An URL pointing to a location where a base model is hosted.
    name : str
        The name of the base model to download.
    directory : str
        The path to the directory where the base model should be saved.

    """
    dir_path = Path(directory)
    dir_path.mkdir(parents=True, exist_ok=True)
    with requests.get(f"{url}{name}", timeout=10) as r:
        r.raise_for_status()
        with (dir_path / name).open("wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)


def initialize_models() -> None:
    """Download base models and sample RVC models."""
    base_model_names = ["hubert_base.pt", "rmvpe.pt"]
    for base_model_name in base_model_names:
        if not Path(RVC_MODELS_DIR / base_model_name).is_file():
            rprint(f"Downloading {base_model_name}...")
            _download_base_model(RVC_DOWNLOAD_URL, base_model_name, RVC_MODELS_DIR)

    named_model_links = [
        (
            "https://huggingface.co/damnedraxx/TaylorSwift/resolve/main/TaylorSwift.zip",
            "Taylor Swift",
        ),
        (
            "https://huggingface.co/Vermiculos/balladjames/resolve/main/Ballad%20James.zip?download=true",
            "James Hetfield",
        ),
        ("https://huggingface.co/ryolez/MMLP/resolve/main/MMLP.zip", "Eminem"),
    ]
    for model_url, model_name in named_model_links:
        if not Path(RVC_MODELS_DIR / model_name).is_dir():
            rprint(f"Downloading {model_name}...")
            try:
                download_model(model_url, model_name)
            except Exception as e:
                rprint(f"Failed to download {model_name}: {e}")


initialize_models()
static_ffmpeg.add_paths()
static_sox.add_paths()
