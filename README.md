<p align="center"><img src="assets/yoinker-512.png" width="128" height="128" alt="Yoinker logo"></p>

# Yoinker

**Download videos and music from the internet with one button. No setup, no typing, no "terminal".**

🇭🇺 [Magyar leírás itt](README.hu.md) · 🌐 **Hungarian step-by-step page with pictures: https://danielcsirke.github.io/yoinker/**

![Three steps: paste the link, choose video or music, press DOWNLOAD](docs/img/window.svg)

---

## Get it (3 minutes)

1. Open the **[Downloads page](https://github.com/danielcsirke/yoinker/releases/latest)**.
2. Under **Assets**, click the file for your computer:

   | Your computer | Click this | Then |
   |---|---|---|
   | **Windows** | `Yoinker-Windows.exe` | Double-click it. If Windows says *"Windows protected your PC"*, click **More info → Run anyway**. (It says that for every small program not sold in the Microsoft Store.) |
   | **Mac** | `Yoinker-macOS.dmg` | Open it, drag **Yoinker** onto **Applications**. First time only: **right-click → Open → Open** (otherwise the Mac says it "can't be opened"). |
   | **Linux** | `Yoinker-Linux` | Right-click → Properties → tick *"Allow executing as program"*, then double-click. |

3. Done. You do **not** need to install Python, yt-dlp, FFmpeg or anything else — it's all inside.

👉 The full step-by-step walkthrough, with every click, is in **[docs/GUIDE.md](docs/GUIDE.md)**.

## Use it (30 seconds)

1. On YouTube (or almost any video site), copy the address of the video from the top of the browser.
2. In Yoinker, press **Paste**.
3. Choose **Video** or **Music only (MP3)**.
4. Press the big **DOWNLOAD** button.
5. When it says *Done!*, press **Open the folder**. Your file is there.

Files go to `Downloads/Yoinker` unless you choose another folder. Yoinker remembers your folder and language.

## Something not working?

Read the message under the progress bar — it tells you what's wrong in plain words.
The common ones (and what to do) are in **[docs/TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md)**.

The most common fix: **get the newest version from the [Downloads page](https://github.com/danielcsirke/yoinker/releases/latest)**. Video sites change often and Yoinker is updated to keep up.

## What it can do

- Video as MP4 that **actually plays** on Windows, Macs, TVs and phones (H.264 + AAC by default; YouTube's raw "best" is often AV1/VP9, which Windows Media Player can't open) in Best / 1080p / 720p / 480p quality
- Music only (MP3, 192 kbps) with title and artist tags
- Whole playlists, if you tick the box
- Works on YouTube and [more than a thousand other sites](https://github.com/yt-dlp/yt-dlp/blob/master/supportedsites.md)
- English and Hungarian — picks your computer's language, switchable at the bottom
- Nothing is uploaded anywhere, no account, no ads, no tracking
- An **Advanced** tab for the few who want it: best-quality codecs, MKV/WebM, MP3/M4A/Opus/FLAC/WAV, cover art, subtitles, login taken from your browser (fixes "needs a login"), file-name pattern, speed limit, and raw yt-dlp / FFmpeg arguments. Everything there is saved automatically.

## For technical people

Yoinker is a small Python/Tkinter front-end over [yt-dlp](https://github.com/yt-dlp/yt-dlp), with FFmpeg bundled through [imageio-ffmpeg](https://github.com/imageio/imageio-ffmpeg), packed into a single executable by PyInstaller on GitHub Actions.

```bash
git clone git@github.com:danielcsirke/yoinker.git && cd yoinker
python3 -m venv .venv && source .venv/bin/activate     # Windows: .venv\Scripts\activate
pip install -e ".[dev]"
python -m yoinker          # run it
pytest                    # test it
./scripts/build.sh        # build it (Windows: scripts\build.ps1)
```

Layout:

```
yoinker/app.py          the window (Tkinter, no other GUI dependency)
yoinker/downloader.py   the yt-dlp part; runs in a thread, reports events to the window
yoinker/i18n.py         all texts in EN + HU, and the rules that turn yt-dlp errors into human sentences
yoinker/config.py       remembers language + folder + the Advanced tab (defaults live here)
yoinker.spec            PyInstaller recipe (bundles FFmpeg)
.github/workflows/      tests + builds for Windows/macOS/Linux; a tag v* makes a Release
docs/                   user guide, troubleshooting, maintainers' notes
```

How to release a new version: [docs/MAINTAINERS.md](docs/MAINTAINERS.md).

## License

Copyright © 2026 Daniel Csirke. **All rights reserved.** You may use Yoinker for free for personal use; you may not copy, modify or redistribute it. Full terms in English and Hungarian: [LICENSE](LICENSE). Open-source components it uses: [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).

Only download what you have the right to download.
