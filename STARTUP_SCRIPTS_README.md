# KrishiMitra Startup Scripts

This directory contains scripts to easily start and stop all KrishiMitra services.

## Available Scripts

### Windows (Recommended: PowerShell)

#### Start All Services
```powershell
# PowerShell (Recommended)
.\start_all.ps1

# Or using Batch
start_all.bat
```

#### Stop All Services
```powershell
# PowerShell (Recommended)
.\stop_all.ps1

# Or using Batch
stop_all.bat
```

### Linux/Mac

#### Start All Services
```bash
chmod +x start_all.sh
./start_all.sh
```

#### Stop All Services
```bash
chmod +x stop_all.sh
./stop_all.sh
```

## What Gets Started

1. **Backend (Port 8000)**
   - FastAPI server with auto-reload
   - Logs to: `backend.log`
   - API docs: http://localhost:8000/docs

2. **Frontend (Port 3000)**
   - React development server
   - Logs to: `frontend.log`
   - App URL: http://localhost:3000

3. **ngrok (Port 8000 tunnel)**
   - Public HTTPS tunnel for Twilio webhooks
   - Logs to: `ngrok.log`
   - Dashboard: http://localhost:4040

## Prerequisites

### Required
- Python 3.8+ (with venv)
- Node.js 16+ (with npm)

### Optional (for voice calls)
- ngrok (https://ngrok.com/download)

## First Time Setup

1. **Install Python dependencies**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   .\venv\Scripts\activate   # Windows
   pip install -r requirements.txt
   ```

2. **Install Node.js dependencies**
   ```bash
   cd frontend
   npm install
   cd ..
   ```

3. **Configure environment**
   - Copy `.env.example` to `.env`
   - Update with your API keys (Twilio, Sentinel Hub, OpenWeatherMap)

4. **Install ngrok (optional)**
   - Download from https://ngrok.com/download
   - Add to PATH or place in project directory

## Usage

### Starting Services

**Windows (PowerShell):**
```powershell
.\start_all.ps1
```

The script will:
1. Check prerequisites
2. Start backend on port 8000
3. Start frontend on port 3000
4. Start ngrok tunnel (if available)
5. Display all service URLs and log file locations

### Stopping Services

**Windows (PowerShell):**
```powershell
.\stop_all.ps1
```

The script will:
1. Stop all running services
2. Clean up any remaining processes on ports 8000 and 3000
3. Preserve log files for debugging

### Viewing Logs

**Windows (PowerShell):**
```powershell
# View backend logs (live)
Get-Content backend.log -Wait

# View frontend logs (live)
Get-Content frontend.log -Wait

# View ngrok logs (live)
Get-Content ngrok.log -Wait
```

**Linux/Mac:**
```bash
# View backend logs (live)
tail -f backend.log

# View frontend logs (live)
tail -f frontend.log

# View ngrok logs (live)
tail -f ngrok.log
```

## Troubleshooting

### Port Already in Use

If you see "Port already in use" warnings:

**Windows:**
```powershell
# Find process using port 8000
Get-NetTCPConnection -LocalPort 8000 | Select-Object OwningProcess
# Kill the process
Stop-Process -Id <PID> -Force

# Or use stop_all.ps1 to clean up
.\stop_all.ps1
```

**Linux/Mac:**
```bash
# Find and kill process on port 8000
lsof -ti:8000 | xargs kill -9

# Or use stop_all.sh to clean up
./stop_all.sh
```

### Backend Not Starting

1. Check if virtual environment exists:
   ```bash
   ls venv/  # Should show Scripts/ (Windows) or bin/ (Linux/Mac)
   ```

2. Check backend.log for errors:
   ```bash
   cat backend.log  # Linux/Mac
   type backend.log  # Windows
   ```

3. Common issues:
   - Missing dependencies: `pip install -r requirements.txt`
   - Database not initialized: Check `krishimitra.db` exists
   - Port 8000 in use: Run stop_all script first

### Frontend Not Starting

1. Check if node_modules exists:
   ```bash
   ls frontend/node_modules/
   ```

2. Check frontend.log for errors:
   ```bash
   cat frontend.log  # Linux/Mac
   type frontend.log  # Windows
   ```

3. Common issues:
   - Missing dependencies: `cd frontend && npm install`
   - Port 3000 in use: Run stop_all script first
   - Node version too old: Update to Node 16+

### ngrok Not Starting

1. Check if ngrok is installed:
   ```bash
   ngrok version
   ```

2. Check ngrok.log for errors:
   ```bash
   cat ngrok.log  # Linux/Mac
   type ngrok.log  # Windows
   ```

3. Common issues:
   - ngrok not in PATH: Add to PATH or place in project directory
   - ngrok not authenticated: Run `ngrok authtoken <your-token>`
   - Port 4040 in use: Stop other ngrok instances

### Getting ngrok URL

After starting services, get the ngrok public URL:

**Option 1: From script output**
- The start script will display the ngrok URL

**Option 2: From ngrok dashboard**
- Visit http://localhost:4040
- Copy the HTTPS URL

**Option 3: From API**
```bash
curl http://localhost:4040/api/tunnels | jq -r '.tunnels[0].public_url'
```

**Update .env file:**
```bash
NGROK_URL=https://your-unique-id.ngrok-free.dev
```

## Manual Start (Alternative)

If the scripts don't work, you can start services manually:

### Backend
```bash
# Activate virtual environment
source venv/bin/activate  # Linux/Mac
.\venv\Scripts\activate   # Windows

# Start backend
python -m uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend
```bash
cd frontend
npm run dev
```

### ngrok
```bash
ngrok http 8000
```

## Process Management

### View Running Services

**Windows (PowerShell):**
```powershell
# Check port 8000 (Backend)
Get-NetTCPConnection -LocalPort 8000 -State Listen

# Check port 3000 (Frontend)
Get-NetTCPConnection -LocalPort 3000 -State Listen

# Check ngrok process
Get-Process -Name ngrok
```

**Linux/Mac:**
```bash
# Check port 8000 (Backend)
lsof -i:8000

# Check port 3000 (Frontend)
lsof -i:3000

# Check ngrok process
ps aux | grep ngrok
```

## Log Files

All services log to separate files:

- `backend.log` - Backend API logs (FastAPI/uvicorn)
- `frontend.log` - Frontend dev server logs (Vite)
- `ngrok.log` - ngrok tunnel logs

These files are preserved when stopping services for debugging purposes.

## Tips

1. **Always use stop_all before start_all** to ensure clean startup
2. **Check logs if services don't respond** - errors are logged there
3. **Update ngrok URL in .env** after each restart (URL changes)
4. **Keep terminal open** to see real-time status updates
5. **Use PowerShell on Windows** for better error handling

## Support

If you encounter issues:

1. Check the log files for error messages
2. Ensure all prerequisites are installed
3. Try manual start to isolate the problem
4. Check port availability with netstat/lsof
5. Verify .env file has correct configuration
