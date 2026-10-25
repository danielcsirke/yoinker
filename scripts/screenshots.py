"""Take the Hungarian screenshots used on the GitHub Pages site.

Needs an X display (real or Xvfb) and Pillow. Writes PNGs into docs/img/hu/.

    Xvfb :99 -screen 0 1000x800x24 &
    DISPLAY=:99 python scripts/screenshots.py
"""

import os
import sys
import tkinter as tk
from pathlib import Path

from PIL import ImageGrab

from yoinker import config
from yoinker.app import YoinkerApp
from yoinker.i18n import tr

OUT = Path(__file__).resolve().parent.parent / "docs" / "img" / "hu"
DISPLAY = os.environ.get("DISPLAY", ":0")
LINK = "https://www.youtube.com/watch?v=aqz-KE-bpKQ"


def shot(app: tk.Tk, name: str) -> None:
    app.update_idletasks()
    app.update()
    x, y = app.winfo_rootx(), app.winfo_rooty()
    w, h = app.winfo_width(), app.winfo_height()
    # Include the window manager frame if there is one; Xvfb has none.
    img = ImageGrab.grab(bbox=(x, y, x + w, y + h), xdisplay=DISPLAY)
    OUT.mkdir(parents=True, exist_ok=True)
    img.save(OUT / f"{name}.png")
    print("saved", name, img.size)


def main() -> None:
    # Force Hungarian and a friendly-looking folder regardless of this machine.
    config.save = lambda *_a, **_k: None  # don't touch the real settings file
    config.load = lambda *_a, **_k: {"language": "hu", "folder": "C:\\Users\\Anna\\Downloads\\Yoinker"}

    app = YoinkerApp()
    app.geometry("+0+0")
    app.update()
    shot(app, "01_ures")

    app.url_entry.insert(0, LINK)
    shot(app, "02_link_beillesztve")

    app.kind.set("audio")
    app._kind_changed()
    shot(app, "03_csak_zene")
    app.kind.set("video")
    app._kind_changed()

    app._busy(True)
    app._handle(("progress", 43.0, 2.2 * 1024 * 1024, 12))
    shot(app, "04_letoltes_kozben")

    app._handle(("done", "x"))
    shot(app, "05_kesz")

    app._handle(("error", "err_login", "ERROR: [youtube] abc: Private video"))
    shot(app, "06_hiba")

    app._set_status("status_ready")
    app.log.configure(state="normal")
    app.log.delete("1.0", "end")
    app.log.configure(state="disabled")
    app._toggle_details()
    app._log("[youtube] aqz-KE-bpKQ: Downloading webpage")
    app._log("[info] aqz-KE-bpKQ: Downloading 1 format(s): 251")
    shot(app, "07_reszletek")
    app._toggle_details()

    app.notebook.select(1)
    shot(app, "08_halado")

    app.destroy()


if __name__ == "__main__":
    main()
