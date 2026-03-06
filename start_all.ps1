# KrishiMitra - Start All Services (PowerShell)
# This script starts backend, frontend, and ngrok

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "  KrishiMitra - Starting All Services" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""

# Check prerequisites
Write-Host "Checking prerequisites..." -ForegroundColor Yellow

# Check Python
try {
    $pythonVersion = python --version 2>&1
    Write-Host "[OK] Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "[ERROR] Python not found" -ForegroundColor Red
    exit 1
}

# Check Node.js
try {
    $nodeVersion = node --version 2>&1
    Write-Host "[OK] Node.js found: $nodeVersion" -ForegroundColor Green
} catch {
    Write-Host "[ERROR] Node.js not found" -ForegroundColor Red
    exit 1
}

# Check ngrok
try {
    $ngrokVersion = ngrok version 2>&1
    Write-Host "[OK] ngrok found: $ngrokVersion" -ForegroundColor Green
    $ngrokAvailable = $true
} catch {
    Write-Host "[WARNING] ngrok not found - voice calls will not work" -ForegroundColor Yellow
    $ngrokAvailable = $false
}

Write-Host ""

# Check if ports are already in use
$port8000 = Get-NetTCPConnection -LocalPort 8000 -State Listen -ErrorAction SilentlyContinue
if ($port8000) {
    Write-Host "[WARNING] Port 8000 already in use (Backend may already be running)" -ForegroundColor Yellow
}

$port3000 = Get-NetTCPConnection -LocalPort 3000 -State Listen -ErrorAction SilentlyContinue
if ($port3000) {
    Write-Host "[WARNING] Port 3000 already in use (Frontend may already be running)" -ForegroundColor Yellow
}

Write-Host ""

# Start Backend
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "  Starting Backend (Port 8000)" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan

if (-not (Test-Path "venv")) {
    Write-Host "[INFO] Creating virtual environment..." -ForegroundColor Yellow
    python -m venv venv
}

Write-Host "Starting FastAPI backend..." -ForegroundColor Yellow
$backendJob = Start-Job -ScriptBlock {
    Set-Location $using:PWD
    & .\venv\Scripts\python.exe -m uvicorn src.main:app --reload --host 0.0.0.0 --port 8000 2>&1 | Out-File -FilePath backend.log
}
$backendJob.Id | Out-File -FilePath backend.pid
Write-Host "[OK] Backend started (Job ID: $($backendJob.Id))" -ForegroundColor Green
Write-Host "  Log file: backend.log" -ForegroundColor Gray
Write-Host ""

# Wait for backend to start
Write-Host "Waiting for backend to be ready..." -ForegroundColor Yellow
Start-Sleep -Seconds 5

# Check if backend is responding
try {
    $response = Invoke-WebRequest -Uri "http://localhost:8000/health" -TimeoutSec 2 -ErrorAction SilentlyContinue
    Write-Host "[OK] Backend is responding" -ForegroundColor Green
} catch {
    Write-Host "[WARNING] Backend may still be starting..." -ForegroundColor Yellow
}

Write-Host ""

# Start Frontend
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "  Starting Frontend (Port 3000)" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan

Set-Location frontend

if (-not (Test-Path "node_modules")) {
    Write-Host "[WARNING] node_modules not found" -ForegroundColor Yellow
    Write-Host "Installing dependencies..." -ForegroundColor Yellow
    npm install
}

Write-Host "Starting React frontend..." -ForegroundColor Yellow
$frontendJob = Start-Job -ScriptBlock {
    Set-Location "$using:PWD\frontend"
    npm run dev 2>&1 | Out-File -FilePath ..\frontend.log
}
Set-Location ..
$frontendJob.Id | Out-File -FilePath frontend.pid
Write-Host "[OK] Frontend started (Job ID: $($frontendJob.Id))" -ForegroundColor Green
Write-Host "  Log file: frontend.log" -ForegroundColor Gray
Write-Host ""

# Wait for frontend to start
Write-Host "Waiting for frontend to be ready..." -ForegroundColor Yellow
Start-Sleep -Seconds 5

Write-Host ""

# Start ngrok
if ($ngrokAvailable) {
    Write-Host "==========================================" -ForegroundColor Cyan
    Write-Host "  Starting ngrok (Port 8000)" -ForegroundColor Cyan
    Write-Host "==========================================" -ForegroundColor Cyan
    
    Write-Host "Starting ngrok tunnel..." -ForegroundColor Yellow
    $ngrokJob = Start-Job -ScriptBlock {
        Set-Location $using:PWD
        ngrok http 8000 2>&1 | Out-File -FilePath ngrok.log
    }
    $ngrokJob.Id | Out-File -FilePath ngrok.pid
    Write-Host "[OK] ngrok started (Job ID: $($ngrokJob.Id))" -ForegroundColor Green
    Write-Host "  Log file: ngrok.log" -ForegroundColor Gray
    Write-Host ""
    
    # Wait for ngrok to start
    Write-Host "Waiting for ngrok to be ready..." -ForegroundColor Yellow
    Start-Sleep -Seconds 3
    
    # Get ngrok URL
    try {
        $ngrokApi = Invoke-RestMethod -Uri "http://localhost:4040/api/tunnels" -ErrorAction SilentlyContinue
        $ngrokUrl = $ngrokApi.tunnels | Where-Object { $_.proto -eq "https" } | Select-Object -First 1 -ExpandProperty public_url
        
        if ($ngrokUrl) {
            Write-Host "[OK] ngrok tunnel established" -ForegroundColor Green
            Write-Host "  Public URL: $ngrokUrl" -ForegroundColor Cyan
            Write-Host ""
            Write-Host "[IMPORTANT] Update your .env file with:" -ForegroundColor Yellow
            Write-Host "  NGROK_URL=$ngrokUrl" -ForegroundColor White
        } else {
            Write-Host "[WARNING] Could not retrieve ngrok URL" -ForegroundColor Yellow
            Write-Host "  Check ngrok.log for details" -ForegroundColor Gray
        }
    } catch {
        Write-Host "[WARNING] Could not retrieve ngrok URL" -ForegroundColor Yellow
        Write-Host "  Visit http://localhost:4040 for ngrok dashboard" -ForegroundColor Gray
    }
    Write-Host ""
}

# Summary
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "  All Services Started!" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Service URLs:" -ForegroundColor Yellow
Write-Host "  Backend:  http://localhost:8000" -ForegroundColor White
Write-Host "  Frontend: http://localhost:3000" -ForegroundColor White
if ($ngrokAvailable -and $ngrokUrl) {
    Write-Host "  ngrok:    $ngrokUrl" -ForegroundColor White
}
Write-Host ""
Write-Host "Job IDs:" -ForegroundColor Yellow
Write-Host "  Backend:  $($backendJob.Id) (saved to backend.pid)" -ForegroundColor White
Write-Host "  Frontend: $($frontendJob.Id) (saved to frontend.pid)" -ForegroundColor White
if ($ngrokAvailable) {
    Write-Host "  ngrok:    $($ngrokJob.Id) (saved to ngrok.pid)" -ForegroundColor White
}
Write-Host ""
Write-Host "Log files:" -ForegroundColor Yellow
Write-Host "  Backend:  backend.log" -ForegroundColor White
Write-Host "  Frontend: frontend.log" -ForegroundColor White
if ($ngrokAvailable) {
    Write-Host "  ngrok:    ngrok.log" -ForegroundColor White
}
Write-Host ""
Write-Host "To stop all services, run: .\stop_all.ps1" -ForegroundColor Yellow
Write-Host "To view logs, run: Get-Content backend.log -Wait" -ForegroundColor Yellow
Write-Host ""
Write-Host "[SUCCESS] Ready to use! Open http://localhost:3000 in your browser" -ForegroundColor Green
Write-Host ""
