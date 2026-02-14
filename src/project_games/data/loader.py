import os
from pathlib import Path

import pandas as pd

from project_games.config import get_project_root, load_config


def load_raw_data(path: str | Path | None = None) -> pd.DataFrame:
    """Load the raw games dataset.

    Resolution order:
    1. Explicit *path* argument
    2. ``DATA_PATH`` environment variable
    3. ``data.raw_path`` from config/default.yaml
    """
    if path is None:
        path = os.getenv("DATA_PATH")
    if path is None:
        cfg = load_config()
        path = get_project_root() / cfg["data"]["raw_path"]

    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Dataset not found: {path}")

    return pd.read_csv(path)


def load_processed_data(path: str | Path | None = None) -> pd.DataFrame:
    """Load the processed (cleaned + imputed) dataset."""
    if path is None:
        cfg = load_config()
        path = get_project_root() / cfg["data"]["processed_path"]

    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Processed dataset not found: {path}")

    return pd.read_csv(path)
