# Third-party components / Harmadik féltől származó összetevők

Yoinker itself is "All rights reserved" (see `LICENSE`). It is built on top of
these open-source projects, which keep their own licenses:

| Component | What it does | License |
|-----------|--------------|---------|
| [yt-dlp](https://github.com/yt-dlp/yt-dlp) | Does the actual downloading | The Unlicense (public domain) |
| [FFmpeg](https://ffmpeg.org/) via [imageio-ffmpeg](https://github.com/imageio/imageio-ffmpeg) | Joins video+audio, makes MP3 | LGPL v2.1+ / GPL (binary as shipped by imageio-ffmpeg, BSD-2 wrapper) |
| [Python](https://www.python.org/) + Tkinter | The language and the window | PSF License |
| [PyInstaller](https://pyinstaller.org/) | Packs everything into one file | GPL with bootloader exception (build tool only, not shipped inside) |

FFmpeg source code is available from https://ffmpeg.org/download.html.
