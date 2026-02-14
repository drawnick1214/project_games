from pathlib import Path

import yaml
from dotenv import load_dotenv

load_dotenv()

_PROJECT_ROOT = Path(__file__).resolve().parents[2]
_DEFAULT_CONFIG = _PROJECT_ROOT / "config" / "default.yaml"


def load_config(path: Path | str | None = None) -> dict:
    """Load YAML configuration, defaulting to config/default.yaml."""
    config_path = Path(path) if path else _DEFAULT_CONFIG
    with open(config_path) as f:
        return yaml.safe_load(f)


def get_project_root() -> Path:
    return _PROJECT_ROOT
