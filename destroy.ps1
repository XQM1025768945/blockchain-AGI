# Global Neural Brain - Stop distributed cluster
# Terminates all processes started by deploy.ps1, plus any
# python/cmd children still holding ports.

$ErrorActionPreference = "Continue"
$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
$StateFile = Join-Path $Root ".deployment_state"

Write-Host "=== Stopping distributed cluster ===" -ForegroundColor Cyan

# 1) Kill listed PIDs from state file
if (Test-Path $StateFile) {
    $states = Import-Csv -Path $StateFile -Encoding UTF8
    $count = 0
    foreach ($s in $states) {
        try {
            $proc = Get-Process -Id $s.PID -ErrorAction SilentlyContinue
            if ($proc -and -not $proc.HasExited) {
                Write-Host "  Stop [$($s.Role)] PID=$($s.PID)" -ForegroundColor Red
                Stop-Process -Id $s.PID -Force -ErrorAction SilentlyContinue
                $count++
            }
        } catch {}
    }
    Remove-Item $StateFile -Force -ErrorAction SilentlyContinue
    Write-Host "Stopped $count listed process(es)" -ForegroundColor Green
} else {
    Write-Host "No state file - broad cleanup of background python/cmd..." -ForegroundColor Yellow
}

# 2) Always kill any lingering python/cmd running in this session
#    (the agent processes are cmd -> python children, no window title)
$killed = 0
Get-Process -Name "python","cmd" -ErrorAction SilentlyContinue |
    Where-Object { $_.MainWindowTitle -eq "" } |
    ForEach-Object {
        try {
            Stop-Process -Id $_.Id -Force -ErrorAction SilentlyContinue
            $killed++
        } catch {}
    }
if ($killed -gt 0) { Write-Host "Killed $killed orphan python/cmd process(es)" }

# 3) Wait a moment then confirm port 8000 free
Start-Sleep -Seconds 1
try {
    $listener = [System.Net.Sockets.TcpListener]::new([System.Net.IPAddress]::Loopback, 8000)
    $listener.Start()
    $listener.Stop()
    Write-Host "[OK] Port 8000 is free" -ForegroundColor Green
} catch {
    Write-Host "[WARN] Port 8000 still in use - a process may still hold it" -ForegroundColor Yellow
}

Write-Host "Done" -ForegroundColor Gray
