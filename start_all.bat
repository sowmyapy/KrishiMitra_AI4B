@echo off
REM KrishiMitra - Start All Services (Windows)
REM This script starts backend, frontend, and ngrok

echo ==========================================
echo   KrishiMitra - Starting All Services
echo ==========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found
    exit /b 1
)
echo [OK] Python found

REM Check if Node.js is installed
node --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Node.js not found
    exit /b 1
)
echo [OK] Node.js found

REM Check if ngrok is installed
ngrok version >nul 2>&1
if errorlevel 1 (
    echo [WARNING] ngrok not found - voice calls will not work
    set NGROK_AVAILABLE=false
) else (
    echo [OK] ngrok found
    set NGROK_AVAILABLE=true
)

echo.

REM Start Backend
echo ==========================================
echo   Starting Backend (Port 8000)
echo ==========================================

if not exist venv (
    echo [INFO] Creating virtual environment...
    python -m venv venv
)

echo Starting FastAPI backend...
start /B cmd /c "venv\Scripts\activate && python -m uvicorn src.main:app --reload --host 0.0.0.0 --port 8000 > backend.log 2>&1"
echo [OK] Backend started
echo   Log file: backend.log
echo.

REM Wait for backend to start
echo Waiting for backend to be ready...
timeout /t 5 /nobreak >nul

echo.

REM Start Frontend
echo ==========================================
echo   Starting Frontend (Port 3000)
echo ==========================================

cd frontend

if not exist node_modules (
    echo [WARNING] node_modules not found
    echo Installing dependencies...
    call npm install
)

echo Starting React frontend...
start /B cmd /c "npm run dev > ..\frontend.log 2>&1"
cd ..
echo [OK] Frontend started
echo   Log file: frontend.log
echo.

REM Wait for frontend to start
echo Waiting for frontend to be ready...
timeout /t 5 /nobreak >nul

echo.

REM Start ngrok
if "%NGROK_AVAILABLE%"=="true" (
    echo ==========================================
    echo   Starting ngrok (Port 8000)
    echo ==========================================
    
    echo Starting ngrok tunnel...
    start /B cmd /c "ngrok http 8000 > ngrok.log 2>&1"
    echo [OK] ngrok started
    echo   Log file: ngrok.log
    echo.
    
    REM Wait for ngrok to start
    echo Waiting for ngrok to be ready...
    timeout /t 3 /nobreak >nul
    
    REM Get ngrok URL
    echo.
    echo [INFO] To get ngrok URL, visit: http://localhost:4040
    echo [INFO] Or check ngrok.log file
    echo.
    echo [IMPORTANT] Update your .env file with the ngrok URL:
    echo   NGROK_URL=https://your-ngrok-url.ngrok-free.dev
    echo.
)

REM Summary
echo ==========================================
echo   All Services Started!
echo ==========================================
echo.
echo Service URLs:
echo   Backend:  http://localhost:8000
echo   Frontend: http://localhost:3000
if "%NGROK_AVAILABLE%"=="true" (
    echo   ngrok:    http://localhost:4040 (dashboard)
)
echo.
echo Log files:
echo   Backend:  backend.log
echo   Frontend: frontend.log
if "%NGROK_AVAILABLE%"=="true" (
    echo   ngrok:    ngrok.log
)
echo.
echo To stop all services, run: stop_all.bat
echo To view logs, run: type backend.log (or frontend.log, ngrok.log)
echo.
echo [SUCCESS] Ready to use! Open http://localhost:3000 in your browser
echo.
pause
