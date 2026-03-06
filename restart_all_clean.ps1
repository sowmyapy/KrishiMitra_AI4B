#!/usr/bin/env pwsh
# Complete restart script with cache clearing

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Complete Restart with Cache Clear" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Step 1: Stop all services
Write-Host "Step 1: Stopping all services..." -ForegroundColor Yellow
& .\stop_all.ps1
Start-Sleep -Seconds 2

# Step 2: Clear frontend cache
Write-Host ""
Write-Host "Step 2: Clearing frontend cache..." -ForegroundColor Yellow
if (Test-Path "frontend/node_modules/.vite") {
    Remove-Item -Recurse -Force "frontend/node_modules/.vite"
    Write-Host "  ✓ Vite cache cleared" -ForegroundColor Green
} else {
    Write-Host "  ℹ No Vite cache found" -ForegroundColor Gray
}

if (Test-Path "frontend/.vite") {
    Remove-Item -Recurse -Force "frontend/.vite"
    Write-Host "  ✓ Frontend .vite folder cleared" -ForegroundColor Green
}

# Step 3: Clear Python cache
Write-Host ""
Write-Host "Step 3: Clearing Python cache..." -ForegroundColor Yellow
Get-ChildItem -Path . -Include __pycache__ -Recurse -Force | Remove-Item -Recurse -Force -ErrorAction SilentlyContinue
Get-ChildItem -Path . -Include *.pyc -Recurse -Force | Remove-Item -Force -ErrorAction SilentlyContinue
Write-Host "  ✓ Python cache cleared" -ForegroundColor Green

# Step 4: Wait a moment
Write-Host ""
Write-Host "Step 4: Waiting for cleanup..." -ForegroundColor Yellow
Start-Sleep -Seconds 2

# Step 5: Start backend
Write-Host ""
Write-Host "Step 5: Starting backend..." -ForegroundColor Yellow
$backendProcess = Start-Process pwsh -ArgumentList "-NoExit", "-Command", ".\venv\Scripts\python.exe -m uvicorn src.main:app --reload --host 0.0.0.0 --port 8000" -PassThru -WindowStyle Normal
$backendProcess.Id | Out-File -FilePath "backend.pid" -Force
Write-Host "  ✓ Backend started (PID: $($backendProcess.Id))" -ForegroundColor Green
Write-Host "  ℹ Backend URL: http://localhost:8000" -ForegroundColor Cyan

# Step 6: Wait for backend to start
Write-Host ""
Write-Host "Step 6: Waiting for backend to initialize..." -ForegroundColor Yellow
Start-Sleep -Seconds 5

# Step 7: Start ngrok
Write-Host ""
Write-Host "Step 7: Starting ngrok..." -ForegroundColor Yellow
$ngrokProcess = Start-Process pwsh -ArgumentList "-NoExit", "-Command", "ngrok http 8000" -PassThru -WindowStyle Normal
$ngrokProcess.Id | Out-File -FilePath "ngrok.pid" -Force
Write-Host "  ✓ Ngrok started (PID: $($ngrokProcess.Id))" -ForegroundColor Green
Write-Host "  ℹ Ngrok dashboard: http://localhost:4040" -ForegroundColor Cyan

# Step 8: Wait for ngrok
Write-Host ""
Write-Host "Step 8: Waiting for ngrok to initialize..." -ForegroundColor Yellow
Start-Sleep -Seconds 3

# Step 9: Start frontend
Write-Host ""
Write-Host "Step 9: Starting frontend..." -ForegroundColor Yellow
Set-Location frontend
$frontendProcess = Start-Process pwsh -ArgumentList "-NoExit", "-Command", "npm run dev" -PassThru -WindowStyle Normal
$frontendProcess.Id | Out-File -FilePath "../frontend.pid" -Force
Set-Location ..
Write-Host "  ✓ Frontend started (PID: $($frontendProcess.Id))" -ForegroundColor Green
Write-Host "  ℹ Frontend URL: http://localhost:3000" -ForegroundColor Cyan

# Step 10: Summary
Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "  All Services Started Successfully!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Service URLs:" -ForegroundColor White
Write-Host "  • Frontend:  http://localhost:3000" -ForegroundColor Cyan
Write-Host "  • Backend:   http://localhost:8000" -ForegroundColor Cyan
Write-Host "  • API Docs:  http://localhost:8000/api/v1/docs" -ForegroundColor Cyan
Write-Host "  • Ngrok:     http://localhost:4040" -ForegroundColor Cyan
Write-Host ""
Write-Host "Process IDs saved in:" -ForegroundColor White
Write-Host "  • backend.pid" -ForegroundColor Gray
Write-Host "  • frontend.pid" -ForegroundColor Gray
Write-Host "  • ngrok.pid" -ForegroundColor Gray
Write-Host ""
Write-Host "To stop all services, run: .\stop_all.ps1" -ForegroundColor Yellow
Write-Host ""
Write-Host "Monitoring Page: http://localhost:3000/monitoring" -ForegroundColor Magenta
Write-Host ""
