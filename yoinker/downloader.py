"""The yt-dlp part of Yoinker. No GUI code lives here, so it can be tested alone.

A Job runs in a background thread and reports back through the on_event
callback with tuples:
    ("status", key)                  e.g. "starting", "converting"
    ("progress", percent, speed, eta_seconds)
    ("log", text)
    ("done", folder)
    ("cancelled",)
    ("error", err_key, technical_detail)
"""

from pathlib import Path
from typing import Callable

import yt_dlp
from yt_dlp.utils import DownloadCancelled, DownloadError

from yoinker.i18n import classify_error

QUALITIES = {"best": None, "1080": 1080, "720": 720, "480": 480}


def find_ffmpeg() -> str | None:
    """Path of the FFmpeg that ships inside Yoinker (None = use the system's)."""
    try:
        import imageio_ffmpeg

        return imageio_ffmpeg.get_ffmpeg_exe()
    except Exception:
        return None


def format_selector(kind: str, quality: str) -> str:
    """The yt-dlp 'format' string for a video/audio choice."""
    if kind == "audio":
        return "bestaudio/best"
    height = QUALITIES.get(quality)
    cap = f"[height<={height}]" if height else ""
    # Prefer mp4/m4a so the result plays everywhere; fall back to anything.
    return (
        f"bv*{cap}[ext=mp4]+ba[ext=m4a]/"
        f"bv*{cap}+ba/"
        f"b{cap}/b"
    )


def build_options(
    kind: str,
    quality: str,
    folder: Path,
    playlist: bool,
    ffmpeg: str | None = None,
) -> dict:
    """All yt-dlp settings for one download (hooks are added by Job)."""
    opts: dict = {
        "format": format_selector(kind, quality),
        "outtmpl": str(folder / "%(title).150B [%(id)s].%(ext)s"),
        "noplaylist": not playlist,
        "windowsfilenames": True,
        "quiet": True,
        "no_warnings": True,
        "noprogress": True,
        "retries": 5,
        "fragment_retries": 5,
        "socket_timeout": 30,
        "continuedl": True,
    }
    if ffmpeg:
        opts["ffmpeg_location"] = ffmpeg
    if kind == "audio":
        opts["postprocessors"] = [
            {"key": "FFmpegExtractAudio", "preferredcodec": "mp3", "preferredquality": "192"},
            {"key": "FFmpegMetadata"},
        ]
    else:
        opts["merge_output_format"] = "mp4"
    return opts


def looks_like_link(text: str) -> bool:
    text = text.strip().lower()
    return text.startswith(("http://", "https://")) and " " not in text and "." in text


class _Logger:
    """Sends yt-dlp's own messages to the 'Details' box."""

    def __init__(self, emit):
        self._emit = emit

    def debug(self, msg):
        if not msg.startswith("[debug]"):
            self._emit(("log", msg))

    def info(self, msg):
        self._emit(("log", msg))

    def warning(self, msg):
        self._emit(("log", "WARNING: " + msg))

    def error(self, msg):
        self._emit(("log", "ERROR: " + msg))


class Job:
    def __init__(
        self,
        url: str,
        kind: str,
        quality: str,
        folder: Path,
        playlist: bool,
        on_event: Callable[[tuple], None],
    ):
        self.url = url.strip()
        self.kind = kind
        self.quality = quality
        self.folder = Path(folder)
        self.playlist = playlist
        self._emit = on_event
        self._cancel = False

    def cancel(self) -> None:
        self._cancel = True

    def _progress(self, d: dict) -> None:
        if self._cancel:
            raise DownloadCancelled()
        if d.get("status") == "downloading":
            total = d.get("total_bytes") or d.get("total_bytes_estimate") or 0
            done = d.get("downloaded_bytes") or 0
            percent = min(100.0, done * 100.0 / total) if total else 0.0
            self._emit(("progress", percent, d.get("speed"), d.get("eta")))
        elif d.get("status") == "finished":
            self._emit(("status", "converting"))

    def _postprocess(self, d: dict) -> None:
        if self._cancel:
            raise DownloadCancelled()
        if d.get("status") == "started":
            self._emit(("status", "converting"))

    def run(self) -> None:
        """Do the download. Never raises: everything is reported as an event."""
        try:
            self.folder.mkdir(parents=True, exist_ok=True)
            self._emit(("status", "starting"))
            opts = build_options(
                self.kind, self.quality, self.folder, self.playlist, find_ffmpeg()
            )
            opts["logger"] = _Logger(self._emit)
            opts["progress_hooks"] = [self._progress]
            opts["postprocessor_hooks"] = [self._postprocess]
            with yt_dlp.YoutubeDL(opts) as ydl:
                ydl.download([self.url])
            self._emit(("done", str(self.folder)))
        except DownloadCancelled:
            self._emit(("cancelled",))
        except DownloadError as exc:
            if self._cancel:
                self._emit(("cancelled",))
            else:
                self._emit(("error", classify_error(str(exc)), str(exc)))
        except OSError as exc:
            self._emit(("error", "err_disk", str(exc)))
        except Exception as exc:  # last resort: the GUI must never freeze
            self._emit(("error", classify_error(str(exc)), repr(exc)))
