# Build Yoinker on Windows. Output: dist\Yoinker.exe
$ErrorActionPreference = "Stop"
Set-Location (Join-Path $PSScriptRoot "..")

if (-not (Test-Path .venv)) { python -m venv .venv }
.\.venv\Scripts\Activate.ps1
pip install -q -e ".[dev]"
pytest -q
pyinstaller --clean --noconfirm yoinker.spec
Write-Host "Done: dist\Yoinker.exe"
