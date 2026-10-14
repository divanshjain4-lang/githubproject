$ErrorActionPreference = 'Stop'
if (-not (Test-Path '.venv\Scripts\python.exe')) {
  Write-Host 'Run .\setup.ps1 first.'
  exit 1
}
if (-not (Test-Path 'models\customer_segment_model.joblib')) {
  & .\.venv\Scripts\python.exe -m app.cli train-sample
}
& .\.venv\Scripts\python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8000
