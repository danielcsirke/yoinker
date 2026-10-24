#!/usr/bin/env bash
# Build Yoinker on this machine (macOS or Linux). Output lands in dist/.
set -euo pipefail
cd "$(dirname "$0")/.."

if [ ! -d .venv ]; then
  python3 -m venv .venv
fi
# shellcheck disable=SC1091
source .venv/bin/activate
pip install -q -e ".[dev]"
pytest -q
pyinstaller --clean --noconfirm yoinker.spec

if [ "$(uname)" = "Darwin" ]; then
  rm -rf dmg && mkdir dmg && cp -R dist/Yoinker.app dmg/ && ln -s /Applications dmg/Applications
  hdiutil create -volname Yoinker -srcfolder dmg -ov -format UDZO dist/Yoinker-macOS.dmg
  echo "Done: dist/Yoinker-macOS.dmg"
else
  echo "Done: dist/Yoinker"
fi
