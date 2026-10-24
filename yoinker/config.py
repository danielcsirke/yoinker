"""Remembers the user's language and download folder between runs."""

import json
import os
import sys
from pathlib import Path


def default_download_dir() -> Path:
    return Path.home() / "Downloads" / "Yoinker"


def config_path() -> Path:
    if sys.platform == "win32":
        base = Path(os.environ.get("APPDATA", Path.home() / "AppData" / "Roaming"))
    elif sys.platform == "darwin":
        base = Path.home() / "Library" / "Application Support"
    else:
        base = Path(os.environ.get("XDG_CONFIG_HOME", Path.home() / ".config"))
    return base / "Yoinker" / "settings.json"


def load(path: Path | None = None) -> dict:
    """Read the settings; a missing or broken file just means 'no settings'."""
    try:
        data = json.loads((path or config_path()).read_text(encoding="utf-8"))
        return data if isinstance(data, dict) else {}
    except (OSError, ValueError):
        return {}


def save(settings: dict, path: Path | None = None) -> None:
    """Write the settings; failing to save is never worth bothering the user."""
    target = path or config_path()
    try:
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(json.dumps(settings, indent=2), encoding="utf-8")
    except OSError:
        pass
