# Global Neural Brain - Distributed cluster deploy script
# Provisions 1 orchestrator + multiple neuron agents across regions
# Usage:
#   powershell -ExecutionPolicy Bypass -File .\deploy.ps1
#   powershell -ExecutionPolicy Bypass -File .\deploy.ps1 -Regions "cn-north,us-east,eu-west"

param(
    [string]$RegionsCsv = "cn-north,cn-east,cn-south,cn-west,us-east,us-west,eu-west,ap-southeast,ap-northeast",
    [int]$Port = 8000,
    [string]$OrchestratorUrl = "http://localhost:8000",
    [int]$HeartbeatInterval = 3
)

$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
$LogsDir = Join-Path $Root "logs"
$StateFile = Join-Path $Root ".deployment_state"

$Regions = $RegionsCsv -split "," | ForEach-Object { $_.Trim() } | Where-Object { $_ }

# -------- Setup --------
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host " Global Neural Brain - Deploy            " -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "Project root : $Root"
Write-Host "Logs dir     : $LogsDir"
Write-Host "Orchestrator : $OrchestratorUrl (TCP $Port)"
Write-Host "Regions      : $($Regions -join ', ')"
Write-Host ""

if (-not (Test-Path $LogsDir)) { New-Item -ItemType Directory -Path $LogsDir -Force | Out-Null }

# Python check
try {
    $py = & python --version 2>&1
    Write-Host "[OK] Python available: $py"
} catch {
    Write-Host "[FAIL] Python not found in PATH - please install Python 3.x first" -ForegroundColor Red
    exit 1
}

# Dependencies (idempotent)
$required = @("fastapi", "uvicorn", "pydantic", "requests")
foreach ($pkg in $required) {
    $check = & python -c "import $($pkg -replace '\[.*?\]',''); print('ok')" 2>&1
    if ($check -ne 'ok') {
        Write-Host "[INSTALL] $pkg ..."
        & python -m pip install $pkg --quiet
    }
}
Write-Host "[OK] Dependencies ready"

# Cleanup previous deployment if any
if (Test-Path $StateFile) {
    Write-Host "[INFO] Previous deployment detected - cleaning" -ForegroundColor Yellow
    & powershell -ExecutionPolicy Bypass -File (Join-Path $Root "destroy.ps1")
    Start-Sleep -Seconds 2
}

$processes = New-Object System.Collections.ArrayList

# -------- Orchestrator --------
$orchLog = Join-Path $LogsDir "orchestrator.log"
$orchScript = Join-Path (Join-Path $Root "orchestrator") "main.py"

Write-Host ""
Write-Host "[1/2] Starting orchestrator -> $orchLog" -ForegroundColor Green
# Use cmd /c to safely handle spaces in script path
$orchProc = Start-Process -FilePath "cmd" `
    -ArgumentList @("/c", "python", "`"$orchScript`"") `
    -RedirectStandardOutput $orchLog -RedirectStandardError "$orchLog.err" `
    -NoNewWindow -PassThru
[void]$processes.Add([pscustomobject]@{Role="orchestrator"; PID=$orchProc.Id; Log=$orchLog})
Write-Host "    PID=$($orchProc.Id)"

# Healthcheck (max 15s)
$ready = $false
for ($i = 0; $i -lt 30; $i++) {
    try {
        $resp = Invoke-WebRequest -Uri "$OrchestratorUrl/" -UseBasicParsing -TimeoutSec 2
        if ($resp.StatusCode -eq 200) { $ready = $true; break }
    } catch {}
    Start-Sleep -Milliseconds 500
}
if (-not $ready) {
    Write-Host "[FAIL] Orchestrator not ready - aborting" -ForegroundColor Red
    Stop-Process -Id $orchProc.Id -Force -ErrorAction SilentlyContinue
    exit 2
}
Write-Host "    Healthcheck passed"

# -------- Neuron agents --------
Write-Host ""
Write-Host "[2/2] Starting $($Regions.Count) neuron nodes..." -ForegroundColor Green
$agentScript = Join-Path (Join-Path $Root "neuron-agent") "agent.py"

foreach ($region in $Regions) {
    $nodeLog = Join-Path $LogsDir "neuron-$region.log"
    # Build a .cmd wrapper setting env vars then running python,
    # keeps environment isolated and avoids quoting issues with spaces.
    $wrapper = "@echo off`r`n" + `
        "set ORCHESTRATOR_URL=$OrchestratorUrl`r`n" + `
        "set REGION=$region`r`n" + `
        "set HEARTBEAT_INTERVAL=$HeartbeatInterval`r`n" + `
        "set LOG_FILE=$nodeLog`r`n" + `
        "python `"$agentScript`"`r`n"
    $wrapperFile = Join-Path $LogsDir "run-$region.cmd"
    Set-Content -Path $wrapperFile -Value $wrapper -Encoding ASCII

    $nodeProc = Start-Process -FilePath "cmd" `
        -ArgumentList @("/c", "`"$wrapperFile`"") `
        -RedirectStandardOutput "$nodeLog.stdout" -RedirectStandardError "$nodeLog.stderr" `
        -NoNewWindow -PassThru
    [void]$processes.Add([pscustomobject]@{Role="neuron-$region"; PID=$nodeProc.Id; Log=$nodeLog})
    Write-Host "    [$region] PID=$($nodeProc.Id) log=$nodeLog"
}

# Persist state
$processes | Export-Csv -Path $StateFile -NoTypeInformation -Encoding UTF8

# Wait for nodes to register
Write-Host ""
Write-Host "[WAIT] Waiting for nodes to register (5s)..."
Start-Sleep -Seconds 5

# Final verification
try {
    $metrics = Invoke-RestMethod -Uri "$OrchestratorUrl/aip/v1/metrics" -UseBasicParsing
    $regionCount = ($metrics.regions | Measure-Object).Count
    Write-Host ""
    Write-Host "==========================================" -ForegroundColor Cyan
    Write-Host " Deployment complete!                    " -ForegroundColor Green
    Write-Host "   Online nodes : $($metrics.online_nodes) / $($metrics.total_nodes)"
    Write-Host "   Regions      : $regionCount"
    Write-Host "   Uptime       : $($metrics.uptime_seconds)s"
    Write-Host "==========================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Dashboard      : $OrchestratorUrl/dashboard/" -ForegroundColor Yellow
    Write-Host "Swagger API    : $OrchestratorUrl/docs" -ForegroundColor Yellow
    Write-Host "Metrics JSON   : $OrchestratorUrl/aip/v1/metrics" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "PID file       : $StateFile" -ForegroundColor Gray
    Write-Host "Stop cluster   : powershell -ExecutionPolicy Bypass -File .\destroy.ps1" -ForegroundColor Gray
} catch {
    Write-Host "[WARN] Could not fetch metrics: $_" -ForegroundColor Yellow
}
