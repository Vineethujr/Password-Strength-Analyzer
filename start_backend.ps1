Set-Location $PSScriptRoot
if (-not (Test-Path .venv)) {
  py -3.10 -m venv .venv
}
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
uvicorn backend.app:app --reload --host 127.0.0.1 --port 8000
