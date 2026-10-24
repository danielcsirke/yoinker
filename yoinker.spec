# PyInstaller recipe. Run:  pyinstaller yoinker.spec
# Produces a single-folder app with FFmpeg bundled, so users need nothing else.

import os
import sys

import imageio_ffmpeg
from PyInstaller.utils.hooks import collect_submodules

block_cipher = None
ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
# imageio_ffmpeg looks for the binary relative to its own package folder.
ffmpeg_dest = os.path.join("imageio_ffmpeg", "binaries")

icon = None
if sys.platform == "win32" and os.path.exists("assets/yoinker.ico"):
    icon = "assets/yoinker.ico"
elif sys.platform == "darwin" and os.path.exists("assets/yoinker.icns"):
    icon = "assets/yoinker.icns"

a = Analysis(
    ["yoinker/__main__.py"],
    pathex=["."],
    binaries=[(ffmpeg_exe, ffmpeg_dest)],
    datas=[],
    hiddenimports=collect_submodules("yt_dlp"),
    hookspath=[],
    runtime_hooks=[],
    excludes=["pytest"],
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

if sys.platform == "darwin":
    exe = EXE(pyz, a.scripts, [], exclude_binaries=True, name="Yoinker",
              console=False, icon=icon)
    coll = COLLECT(exe, a.binaries, a.zipfiles, a.datas, name="Yoinker")
    app = BUNDLE(coll, name="Yoinker.app", icon=icon,
                 bundle_identifier="com.danielcsirke.yoinker",
                 info_plist={"NSHighResolutionCapable": True,
                             "CFBundleShortVersionString": "1.0.0"})
else:
    # One single file on Windows and Linux: easiest thing to hand to someone.
    exe = EXE(pyz, a.scripts, a.binaries, a.zipfiles, a.datas, [],
              name="Yoinker", console=False, icon=icon,
              upx=False, strip=False)
