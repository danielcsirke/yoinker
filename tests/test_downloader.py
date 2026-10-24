from pathlib import Path

import yt_dlp

from yoinker.downloader import Job, build_options, format_selector, looks_like_link


def test_looks_like_link():
    assert looks_like_link("https://www.youtube.com/watch?v=abc")
    assert looks_like_link("  http://example.com/x ")
    assert not looks_like_link("")
    assert not looks_like_link("youtube")
    assert not looks_like_link("hello world")
    assert not looks_like_link("https://no spaces allowed.com")


def test_format_selector():
    assert format_selector("audio", "best") == "bestaudio/best"
    assert "[height<=720]" in format_selector("video", "720")
    assert "height" not in format_selector("video", "best")


def test_build_options_audio_makes_mp3(tmp_path):
    opts = build_options("audio", "best", tmp_path, playlist=False)
    codecs = [p.get("preferredcodec") for p in opts["postprocessors"]]
    assert "mp3" in codecs
    assert opts["noplaylist"] is True
    assert "ffmpeg_location" not in opts


def test_build_options_video_is_mp4_and_respects_playlist(tmp_path):
    opts = build_options("video", "1080", tmp_path, playlist=True, ffmpeg="/x/ffmpeg")
    assert opts["merge_output_format"] == "mp4"
    assert opts["noplaylist"] is False
    assert opts["ffmpeg_location"] == "/x/ffmpeg"
    assert str(tmp_path) in opts["outtmpl"]


def test_options_are_accepted_by_yt_dlp(tmp_path):
    """yt-dlp validates option names lazily; make sure ours construct cleanly."""
    for kind in ("video", "audio"):
        with yt_dlp.YoutubeDL(build_options(kind, "720", tmp_path, False)):
            pass


def test_job_reports_error_as_event_not_exception(tmp_path):
    events = []
    job = Job("https://definitely-not-a-real-site.invalid/v/1", "video", "best",
              tmp_path, False, events.append)
    job.run()  # must not raise
    kinds = [e[0] for e in events]
    assert "error" in kinds
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
