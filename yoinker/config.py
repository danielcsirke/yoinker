"""Remembers the user's language, download folder and advanced settings between runs."""

import json
import os
import sys
from pathlib import Path

# Everything on the Advanced tab, with the values a fresh install uses.
# "codec": compat = H.264 + AAC, plays on every Windows/Mac/TV/phone;
#          best   = whatever is highest quality (often AV1/VP9), not always playable.
ADVANCED_DEFAULTS = {
    "codec": "compat",
    "container": "mp4",
    "audio_format": "mp3",
    "audio_bitrate": "192",
    "thumbnail": False,
    "subtitles": False,
    "subtitle_lang": "hu,en",
    "embed_subtitles": True,
    "cookies_browser": "none",
    "filename": "%(title).150B [%(id)s].%(ext)s",
    "rate_limit": "",
    "extra_ytdlp": "",
    "extra_ffmpeg": "",
}

CONTAINERS = ["mp4", "mkv", "webm"]
AUDIO_FORMATS = ["mp3", "m4a", "opus", "flac", "wav"]
AUDIO_BITRATES = ["128", "192", "256", "320"]
BROWSERS = ["none", "chrome", "firefox", "edge", "safari", "brave", "chromium", "opera", "vivaldi"]


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


def advanced(settings: dict) -> dict:
    """The advanced settings with defaults filled in for anything missing or odd."""
    stored = settings.get("advanced")
    stored = stored if isinstance(stored, dict) else {}
    result = dict(ADVANCED_DEFAULTS)
    for key, default in ADVANCED_DEFAULTS.items():
        value = stored.get(key, default)
        result[key] = value if isinstance(value, type(default)) else default
    return result
