"""Render assets/yoinker.svg into every icon format Yoinker needs.

    pip install cairosvg pillow
    python scripts/make_icons.py

Outputs (all committed, so CI needs neither cairo nor this script):
    assets/yoinker.ico       Windows exe icon
    assets/yoinker.icns      macOS app icon
    assets/yoinker-512.png   README / misc
    yoinker/assets/icon.png  window icon, bundled into the app
    docs/favicon.png         Pages site
"""

import io
from pathlib import Path

import cairosvg
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
SVG = ROOT / "assets" / "yoinker.svg"


def render(size: int) -> Image.Image:
    png = cairosvg.svg2png(url=str(SVG), output_width=size, output_height=size)
    return Image.open(io.BytesIO(png)).convert("RGBA")


def main() -> None:
    sizes = {s: render(s) for s in (16, 24, 32, 48, 64, 128, 256, 512, 1024)}

    sizes[512].save(ROOT / "assets" / "yoinker-512.png")
    sizes[256].save(ROOT / "yoinker" / "assets" / "icon.png")
    sizes[64].save(ROOT / "docs" / "favicon.png")
    sizes[256].save(ROOT / "docs" / "img" / "logo.png")
    (ROOT / "docs" / "img" / "logo.svg").write_bytes(SVG.read_bytes())

    ico_sizes = [16, 24, 32, 48, 64, 128, 256]
    sizes[256].save(
        ROOT / "assets" / "yoinker.ico",
        format="ICO",
        sizes=[(s, s) for s in ico_sizes],
        append_images=[sizes[s] for s in ico_sizes if s != 256],
    )

    icns_sizes = [16, 32, 64, 128, 256, 512, 1024]
    sizes[1024].save(
        ROOT / "assets" / "yoinker.icns",
        format="ICNS",
        append_images=[sizes[s] for s in icns_sizes if s != 1024],
    )
    for p in ("assets/yoinker.ico", "assets/yoinker.icns", "assets/yoinker-512.png",
              "yoinker/assets/icon.png", "docs/favicon.png"):
        print(f"{p:28s} {(ROOT / p).stat().st_size:>8} bytes")


if __name__ == "__main__":
    main()
