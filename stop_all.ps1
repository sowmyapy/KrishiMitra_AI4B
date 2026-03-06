# KrishiMitra - Stop All Services (PowerShell)
# This script stops backend, frontend, and ngrok

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "  KrishiMitra - Stopping All Services" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""

# Function to stop a job
function Stop-ServiceJob {
    param(
        [string]$Name,
        [string]$PidFile
    )
    
    if (Test-Path $PidFile) {
        $jobId = Get-Content $PidFile
        $job = Get-Job -Id $jobId -ErrorAction SilentlyContinue
        
        if ($job) {
            Write-Host "Stopping $Name (Job ID: $jobId)..." -ForegroundColor Yellow
            Stop-Job -Id $jobId -ErrorAction SilentlyContinue
            Remove-Job -Id $jobId -Force -ErrorAction SilentlyContinue
            Write-Host "[OK] $Name stopped" -ForegroundColor Green
        } else {
            Write-Host "[WARNING] $Name job not found" -ForegroundColor Yellow
        }
        
        Remove-Item $PidFile -ErrorAction SilentlyContinue
    } else {
        Write-Host "[WARNING] $Name PID file not found" -ForegroundColor Yellow
    }
}

# Stop Backend
Write-Host "Stopping Backend..." -ForegroundColor Yellow
Stop-ServiceJob -Name "Backend" -PidFile "backend.pid"
Write-Host ""

# Stop Frontend
Write-Host "Stopping Frontend..." -ForegroundColor Yellow
Stop-ServiceJob -Name "Frontend" -PidFile "frontend.pid"
Write-Host ""

# Stop ngrok
Write-Host "Stopping ngrok..." -ForegroundColor Yellow
Stop-ServiceJob -Name "ngrok" -PidFile "ngrok.pid"
Write-Host ""

# Clean up any remaining processes
Write-Host "Cleaning up any remaining processes..." -ForegroundColor Yellow

# Kill processes on port 8000 (Backend)
$port8000 = Get-NetTCPConnection -LocalPort 8000 -State Listen -ErrorAction SilentlyContinue
if ($port8000) {
    Write-Host "Killing processes on port 8000..." -ForegroundColor Yellow
    $port8000 | ForEach-Object {
        Stop-Process -Id $_.OwningProcess -Force -ErrorAction SilentlyContinue
    }
}

# Kill processes on port 3000 (Frontend)
$port3000 = Get-NetTCPConnection -LocalPort 3000 -State Listen -ErrorAction SilentlyContinue
if ($port3000) {
    Write-Host "Killing processes on port 3000..." -ForegroundColor Yellow
    $port3000 | ForEach-Object {
        Stop-Process -Id $_.OwningProcess -Force -ErrorAction SilentlyContinue
    }
}

# Kill any remaining ngrok processes
Get-Process -Name ngrok -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue

# Kill any remaining uvicorn processes
Get-Process -Name python -ErrorAction SilentlyContinue | Where-Object { $_.CommandLine -like "*uvicorn*" } | Stop-Process -Force -ErrorAction SilentlyContinue

Write-Host ""
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "  All Services Stopped!" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Log files preserved:" -ForegroundColor Yellow
Write-Host "  backend.log" -ForegroundColor White
Write-Host "  frontend.log" -ForegroundColor White
Write-Host "  ngrok.log" -ForegroundColor White
Write-Host ""
