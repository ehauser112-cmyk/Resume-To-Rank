Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$ProjectRoot = Split-Path -Parent $PSScriptRoot
$Python = Join-Path $ProjectRoot ".python-nuget\tools\python.exe"
$HostAddress = if ($env:RESUME_TO_RANK_HOST) { $env:RESUME_TO_RANK_HOST } else { "0.0.0.0" }
$Port = if ($env:RESUME_TO_RANK_PORT) { $env:RESUME_TO_RANK_PORT } else { "5055" }

if (-not (Test-Path $Python)) {
    throw "Local Python was not found at $Python. Run the test setup before starting the app."
}

Set-Location $ProjectRoot
$env:RESUME_TO_RANK_HOST = $HostAddress
$env:RESUME_TO_RANK_PORT = $Port
& $Python serve_frontend.py
