from pathlib import Path

import pytest
import yt_dlp

from yoinker.config import ADVANCED_DEFAULTS
from yoinker.downloader import (
    BadSettings, Job, build_options, extra_ytdlp_options, format_selector, looks_like_link,
)


def test_looks_like_link():
    assert looks_like_link("https://www.youtube.com/watch?v=abc")
    assert looks_like_link("  http://example.com/x ")
    assert not looks_like_link("")
    assert not looks_like_link("youtube")
    assert not looks_like_link("hello world")
    assert not looks_like_link("https://no spaces allowed.com")


def test_format_selector_prefers_h264_by_default():
    assert format_selector("audio", "best") == "bestaudio/best"
    sel = format_selector("video", "720")
    assert sel.startswith("bv*[height<=720][vcodec^=avc1]+ba[acodec^=mp4a]")
    assert "[height<=720]" in sel
    assert "height" not in format_selector("video", "best")


def test_format_selector_best_mode_has_no_codec_filter():
    sel = format_selector("video", "1080", compat=False)
    assert "avc1" not in sel and "[height<=1080]" in sel


def test_defaults_are_the_plays_everywhere_ones(tmp_path):
    opts = build_options("video", "best", tmp_path, playlist=False)
    assert "avc1" in opts["format"]
    assert opts["merge_output_format"] == "mp4"
    keys = [p["key"] for p in opts["postprocessors"]]
    assert "FFmpegVideoConvertor" in keys  # re-encode safety net
    assert "FFmpegMetadata" in keys
    assert "cookiesfrombrowser" not in opts and "ratelimit" not in opts


def test_build_options_audio_makes_mp3(tmp_path):
    opts = build_options("audio", "best", tmp_path, playlist=False)
    pp = next(p for p in opts["postprocessors"] if p["key"] == "FFmpegExtractAudio")
    assert pp["preferredcodec"] == "mp3" and pp["preferredquality"] == "192"
    assert opts["noplaylist"] is True
    assert "ffmpeg_location" not in opts


def test_build_options_respects_advanced(tmp_path):
    adv = {**ADVANCED_DEFAULTS, "codec": "best", "container": "mkv", "thumbnail": True,
           "subtitles": True, "subtitle_lang": "hu, en", "cookies_browser": "firefox",
           "rate_limit": "2M", "extra_ffmpeg": "-threads 2", "filename": "%(title)s.%(ext)s"}
    opts = build_options("video", "1080", tmp_path, playlist=True, ffmpeg="/x/ffmpeg", advanced=adv)
    keys = [p["key"] for p in opts["postprocessors"]]
    assert "avc1" not in opts["format"]
    assert "FFmpegVideoConvertor" not in keys
    assert opts["merge_output_format"] == "mkv"
    assert "EmbedThumbnail" in keys and opts["writethumbnail"] is True
    assert "FFmpegEmbedSubtitle" in keys and opts["subtitleslangs"] == ["hu", "en"]
    assert opts["cookiesfrombrowser"] == ("firefox",)
    assert opts["ratelimit"] == 2 * 1024 * 1024
    assert opts["postprocessor_args"] == {"ffmpeg": ["-threads", "2"]}
    assert opts["outtmpl"].endswith("%(title)s.%(ext)s")
    assert opts["noplaylist"] is False and opts["ffmpeg_location"] == "/x/ffmpeg"


def test_audio_format_and_bitrate(tmp_path):
    adv = {**ADVANCED_DEFAULTS, "audio_format": "flac", "audio_bitrate": "320"}
    opts = build_options("audio", "best", tmp_path, False, advanced=adv)
    pp = next(p for p in opts["postprocessors"] if p["key"] == "FFmpegExtractAudio")
    assert pp["preferredcodec"] == "flac"


def test_extra_ytdlp_options():
    assert extra_ytdlp_options("") == {}
    got = extra_ytdlp_options("--no-mtime --limit-rate 1M")
    assert got["updatetime"] is False and got["ratelimit"] == 1024 * 1024
    with pytest.raises(BadSettings):
        extra_ytdlp_options("--no-such-flag")


def test_extra_ytdlp_postprocessors_are_added_not_replaced(tmp_path):
    adv = {**ADVANCED_DEFAULTS, "extra_ytdlp": "--embed-chapters"}
    opts = build_options("video", "best", tmp_path, False, advanced=adv)
    keys = [p["key"] for p in opts["postprocessors"]]
    assert "FFmpegVideoConvertor" in keys and "FFmpegMetadata" in keys


def test_bad_rate_limit_is_a_settings_error(tmp_path):
    with pytest.raises(BadSettings):
        build_options("video", "best", tmp_path, False, advanced={**ADVANCED_DEFAULTS, "rate_limit": "fast"})


def test_options_are_accepted_by_yt_dlp(tmp_path):
    """yt-dlp validates option names lazily; make sure ours construct cleanly."""
    for kind in ("video", "audio"):
        for codec in ("compat", "best"):
            adv = {**ADVANCED_DEFAULTS, "codec": codec, "thumbnail": True, "subtitles": True}
            with yt_dlp.YoutubeDL(build_options(kind, "720", tmp_path, False, advanced=adv)):
                pass


def test_job_reports_bad_settings_as_event(tmp_path):
    events = []
    Job("https://example.com/v", "video", "best", tmp_path, False, events.append,
        advanced={**ADVANCED_DEFAULTS, "extra_ytdlp": "--bogus"}).run()
    assert events[-1][0] == "error" and events[-1][1] == "err_settings"


def test_job_reports_error_as_event_not_exception(tmp_path):
    events = []
    job = Job("https://definitely-not-a-real-site.invalid/v/1", "video", "best",
              tmp_path, False, events.append)
    job.run()  # must not raise
    err = next(e for e in events if e[0] == "error")
    assert err[1].startswith("err_")


def test_cancel_before_start_reports_cancelled(tmp_path, monkeypatch):
    events = []
    job = Job("https://example.com/v", "video", "best", tmp_path, False, events.append)
    job.cancel()

    def fake_download(self, urls):
        job._progress({"status": "downloading", "downloaded_bytes": 1, "total_bytes": 2})

    monkeypatch.setattr(yt_dlp.YoutubeDL, "download", fake_download)
    job.run()
    assert events[-1] == ("cancelled",)


def test_progress_event_math(tmp_path):
    events = []
    job = Job("https://example.com/v", "video", "best", tmp_path, False, events.append)
    job._progress({"status": "downloading", "downloaded_bytes": 50, "total_bytes": 200,
                   "speed": 1000, "eta": 3})
    assert events == [("progress", 25.0, 1000, 3)]
    job._progress({"status": "finished"})
    assert events[-1] == ("status", "converting")
    assert Path(tmp_path).exists()
