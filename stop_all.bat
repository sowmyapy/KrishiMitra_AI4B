@echo off
REM KrishiMitra - Stop All Services (Windows)
REM This script stops backend, frontend, and ngrok

echo ==========================================
echo   KrishiMitra - Stopping All Services
echo ==========================================
echo.

REM Stop processes on port 8000 (Backend)
echo Stopping Backend (Port 8000)...
for /f "tokens=5" %%a in ('netstat -aon ^| find ":8000" ^| find "LISTENING"') do (
    taskkill /F /PID %%a >nul 2>&1
)
echo [OK] Backend stopped
echo.

REM Stop processes on port 3000 (Frontend)
echo Stopping Frontend (Port 3000)...
for /f "tokens=5" %%a in ('netstat -aon ^| find ":3000" ^| find "LISTENING"') do (
    taskkill /F /PID %%a >nul 2>&1
)
echo [OK] Frontend stopped
echo.

REM Stop ngrok
echo Stopping ngrok...
taskkill /F /IM ngrok.exe >nul 2>&1
if errorlevel 1 (
    echo [INFO] ngrok not running
) else (
    echo [OK] ngrok stopped
)
echo.

REM Stop any remaining Python processes (uvicorn)
echo Cleaning up Python processes...
taskkill /F /IM python.exe /FI "WINDOWTITLE eq uvicorn*" >nul 2>&1

REM Stop any remaining Node processes
echo Cleaning up Node processes...
taskkill /F /IM node.exe /FI "WINDOWTITLE eq npm*" >nul 2>&1

echo.
echo ==========================================
echo   All Services Stopped!
echo ==========================================
echo.
echo Log files preserved:
echo   backend.log
echo   frontend.log
echo   ngrok.log
echo.
pause
