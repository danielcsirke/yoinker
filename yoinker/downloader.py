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

import shlex
from pathlib import Path
from typing import Callable

import yt_dlp
from yt_dlp.utils import DownloadCancelled, DownloadError, parse_bytes

from yoinker.config import ADVANCED_DEFAULTS
from yoinker.i18n import classify_error

QUALITIES = {"best": None, "1080": 1080, "720": 720, "480": 480}


class BadSettings(ValueError):
    """Something on the Advanced tab cannot be used (e.g. a wrong yt-dlp flag)."""


def find_ffmpeg() -> str | None:
    """Path of the FFmpeg that ships inside Yoinker (None = use the system's)."""
    try:
        import imageio_ffmpeg

        return imageio_ffmpeg.get_ffmpeg_exe()
    except Exception:
        return None


def format_selector(kind: str, quality: str, compat: bool = True) -> str:
    """The yt-dlp 'format' string for a video/audio choice.

    compat=True asks for H.264 video + AAC audio first. That is what Windows
    Media Player, TVs and old phones can actually play; YouTube's "best"
    streams are usually AV1/VP9, which many of them cannot.
    """
    if kind == "audio":
        return "bestaudio/best"
    height = QUALITIES.get(quality)
    cap = f"[height<={height}]" if height else ""
    if compat:
        return (
            f"bv*{cap}[vcodec^=avc1]+ba[acodec^=mp4a]/"
            f"bv*{cap}[vcodec^=avc1]+ba/"
            f"b{cap}[vcodec^=avc1]/"
            f"bv*{cap}[ext=mp4]+ba[ext=m4a]/"
            f"bv*{cap}+ba/b{cap}/b"
        )
    return f"bv*{cap}+ba/b{cap}/b"


def extra_ytdlp_options(text: str) -> dict:
    """Turn free-text yt-dlp command line flags into YoutubeDL options.

    Only the options the flags actually change are returned, so they can be
    laid over Yoinker's own. Raises BadSettings for an unknown flag.
    """
    args = shlex.split(text or "")
    if not args:
        return {}
    try:
        base = yt_dlp.parse_options([]).ydl_opts
        user = yt_dlp.parse_options(args).ydl_opts
    except Exception as exc:  # optparse errors, bad values...
        raise BadSettings(str(exc).strip().splitlines()[-1]) from exc
    return {k: v for k, v in user.items() if base.get(k) != v}


def build_options(
    kind: str,
    quality: str,
    folder: Path,
    playlist: bool,
    ffmpeg: str | None = None,
    advanced: dict | None = None,
) -> dict:
    """All yt-dlp settings for one download (hooks are added by Job)."""
    adv = {**ADVANCED_DEFAULTS, **(advanced or {})}
    compat = adv["codec"] == "compat"
    opts: dict = {
        "format": format_selector(kind, quality, compat),
        "outtmpl": str(Path(folder) / (adv["filename"].strip() or ADVANCED_DEFAULTS["filename"])),
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

    pps: list[dict] = []
    if kind == "audio":
        pps.append({
            "key": "FFmpegExtractAudio",
            "preferredcodec": adv["audio_format"],
            "preferredquality": adv["audio_bitrate"],
        })
    else:
        opts["merge_output_format"] = adv["container"]
        if compat:
            # Safety net: if the site only had VP9/AV1, re-encode so it plays.
            pps.append({"key": "FFmpegVideoConvertor", "preferedformat": adv["container"]})
        if adv["subtitles"]:
            opts["writesubtitles"] = True
            opts["subtitleslangs"] = [s.strip() for s in adv["subtitle_lang"].split(",") if s.strip()] or ["en"]
            if adv["embed_subtitles"]:
                pps.append({"key": "FFmpegEmbedSubtitle"})
    pps.append({"key": "FFmpegMetadata"})
    if adv["thumbnail"]:
        opts["writethumbnail"] = True
        pps.append({"key": "EmbedThumbnail"})

    if adv["cookies_browser"] != "none":
        opts["cookiesfrombrowser"] = (adv["cookies_browser"],)
    if adv["rate_limit"].strip():
        limit = parse_bytes(adv["rate_limit"].strip())
        if not limit:
            raise BadSettings(f"rate limit: {adv['rate_limit']!r}")
        opts["ratelimit"] = limit
    if adv["extra_ffmpeg"].strip():
        opts["postprocessor_args"] = {"ffmpeg": shlex.split(adv["extra_ffmpeg"])}

    extra = extra_ytdlp_options(adv["extra_ytdlp"])
    for pp in extra.pop("postprocessors", []):
        if pp not in pps:
            pps.append(pp)
    opts.update(extra)
    opts["postprocessors"] = pps
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
        advanced: dict | None = None,
    ):
        self.url = url.strip()
        self.kind = kind
        self.quality = quality
        self.folder = Path(folder)
        self.playlist = playlist
        self.advanced = advanced
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
                self.kind, self.quality, self.folder, self.playlist, find_ffmpeg(), self.advanced
            )
            opts["logger"] = _Logger(self._emit)
            opts["progress_hooks"] = [self._progress]
            opts["postprocessor_hooks"] = [self._postprocess]
            with yt_dlp.YoutubeDL(opts) as ydl:
                ydl.download([self.url])
            self._emit(("done", str(self.folder)))
        except BadSettings as exc:
            self._emit(("error", "err_settings", str(exc)))
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
