Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$ProjectRoot = Split-Path -Parent $PSScriptRoot
Set-Location $ProjectRoot

$PythonCommands = @(
    @{ Exe = Join-Path $ProjectRoot ".python-nuget\tools\python.exe"; Args = @() },
    @{ Exe = Join-Path $ProjectRoot ".python\python.exe"; Args = @() },
    @{ Exe = "python"; Args = @() },
    @{ Exe = "py"; Args = @("-3") },
    @{ Exe = "python3"; Args = @() }
)

$PythonCommand = $null

foreach ($Candidate in $PythonCommands) {
    if (-not (Get-Command $Candidate.Exe -ErrorAction SilentlyContinue)) {
        continue
    }

    try {
        $VersionOutput = & $Candidate.Exe @($Candidate.Args) --version 2>&1
    }
    catch {
        continue
    }

    if ($LASTEXITCODE -eq 0 -and ($VersionOutput -join "`n") -notmatch "No installed Python") {
        $PythonCommand = $Candidate
        break
    }
}

if (-not $PythonCommand) {
    throw "No Python command found. Install Python or add python, py, or python3 to PATH."
}

& $PythonCommand.Exe @($PythonCommand.Args) -m unittest tests.test_manual_plan_cases -v
