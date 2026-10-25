# Maintainers' notes

How the project is put together and how to ship a new version.

## Why most releases happen

Video sites (YouTube especially) change their players and anti-bot measures every few weeks. yt-dlp fixes them fast, but the yt-dlp *inside a built Yoinker* is frozen at build time. So:

**When users report "The website refused the download", the fix is almost always: rebuild with the newest yt-dlp and publish a new tag.** No code change needed.

The `Weekly yt-dlp check` workflow runs the tests against the latest yt-dlp every Monday, so a breaking yt-dlp change (rare) is noticed before a user hits it.

## Releasing

```bash
# 1. make sure main is green on GitHub Actions
# 2. bump the version in TWO places:
#      yoinker/__init__.py   __version__ = "1.0.1"
#      pyproject.toml        version = "1.0.1"
#    (yoinker.spec's CFBundleShortVersionString is cosmetic; bump it too if you care)
# 3. write 2-3 lines in docs/RELEASE_NOTES.md (shown on the Release page; keep it human)
git commit -am "Release 1.0.1"
git tag v1.0.1
git push && git push --tags
```

GitHub Actions then: runs tests → builds Windows `.exe`, macOS `.dmg`, Linux binary → creates the Release with the three files attached. ~10 minutes. The link `https://github.com/danielcsirke/yoinker/releases/latest` always points at the newest one, which is why the docs and the app's "get the newest version" button use it.

Every push to `main` also builds all three, kept 14 days under the workflow run's **Artifacts** — handy for testing before tagging.

## Code map

| File | Role |
|---|---|
| `yoinker/app.py` | The Tk window. All user interaction. Never calls yt-dlp directly. |
| `yoinker/downloader.py` | `Job` runs yt-dlp in a thread and pushes event tuples into a `queue.Queue`; the window polls it every 100 ms. This keeps the GUI responsive and means the engine is testable without a display. |
| `yoinker/i18n.py` | Every visible string, EN + HU. `classify_error()` maps raw yt-dlp messages to `err_*` keys via an ordered substring list. **Add a new rule here when users send you a Details log with an unhelpful "generic" error.** |
| `yoinker/config.py` | `settings.json` in the OS-appropriate config dir. Only `language` and `folder`. |
| `yoinker.spec` | PyInstaller. Bundles the FFmpeg binary that `imageio-ffmpeg` downloads at `pip install` time into `imageio_ffmpeg/binaries/`, where the package expects it at runtime. |

Design rules worth keeping:
- **No other GUI dependency than Tkinter** — it's in every Python, builds everywhere, no Qt licensing or 80 MB downloads.
- **The GUI never shows a raw exception.** Everything goes through `classify_error` → a friendly sentence; the raw text goes only to the collapsed Details box.
- **Both languages always complete.** `tests/test_i18n.py` fails if a key is missing or a `{placeholder}` differs.

## Changing the logo

Edit `assets/yoinker.svg` (the only master), then `pip install cairosvg pillow`
and `python scripts/make_icons.py`. It regenerates the `.ico`, `.icns`, the
window icon in `yoinker/assets/`, and the site's favicon/logo. Commit all of
them; CI only consumes the generated files.

## Adding a language

Add a dict to `STRINGS` and an entry to `LANGUAGES` in `i18n.py`; run `pytest`. The language picker populates itself.

## Testing locally

```bash
pip install -e ".[dev]"
pytest                      # unit tests, no network except one deliberate DNS failure
python -m yoinker           # run the GUI
./scripts/build.sh          # or scripts\build.ps1 — full PyInstaller build into dist/
```

## Code signing (not done)

Builds are unsigned, hence the SmartScreen / Gatekeeper warnings documented in the guides. Signing needs a paid Apple Developer account (~100 USD/yr, plus notarization) and a Windows code-signing certificate (~200+ USD/yr). If that ever becomes worth it, the hooks go into `build.yml` after the PyInstaller step.
