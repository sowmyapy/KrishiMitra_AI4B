# Quick Start - Run This!

## Step 1: Open PowerShell as Administrator (if needed)

Right-click PowerShell and select "Run as Administrator"

## Step 2: Allow Script Execution (One-time setup)

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Press `Y` when prompted.

## Step 3: Navigate to Project Directory

```powershell
cd C:\Users\Sowmya\OneDrive\projects\ai_crop_system
```

## Step 4: Run the Start Script

```powershell
.\start_all.ps1
```

## What Will Happen

The script will:
1. ✅ Check if Python, Node.js, and ngrok are installed
2. ✅ Start Backend on port 8000
3. ✅ Start Frontend on port 3000
4. ✅ Start ngrok tunnel (for voice calls)
5. ✅ Display all URLs and log files

## Expected Output

```
==========================================
  KrishiMitra - Starting All Services
==========================================

Checking prerequisites...
[OK] Python found: Python 3.10.5
[OK] Node.js found: v16.x.x
[OK] ngrok found: ngrok version x.x.x

==========================================
  Starting Backend (Port 8000)
==========================================
Starting FastAPI backend...
[OK] Backend started (Job ID: 1)
  Log file: backend.log

Waiting for backend to be ready...
[OK] Backend is responding

==========================================
  Starting Frontend (Port 3000)
==========================================
Starting React frontend...
[OK] Frontend started (Job ID: 2)
  Log file: frontend.log

==========================================
  Starting ngrok (Port 8000)
==========================================
Starting ngrok tunnel...
[OK] ngrok started (Job ID: 3)
  Log file: ngrok.log

[OK] ngrok tunnel established
  Public URL: https://xxxx-xxxx-xxxx.ngrok-free.dev

[IMPORTANT] Update your .env file with:
  NGROK_URL=https://xxxx-xxxx-xxxx.ngrok-free.dev

==========================================
  All Services Started!
==========================================

Service URLs:
  Backend:  http://localhost:8000
  Frontend: http://localhost:3000
  ngrok:    https://xxxx-xxxx-xxxx.ngrok-free.dev

[SUCCESS] Ready to use! Open http://localhost:3000 in your browser
```

## Step 5: Open Browser

```powershell
start http://localhost:3000
```

## Step 6: Test the Application

1. Go to Farmers page
2. Click eye icon on any farmer
3. Click "Generate Advisory" - should see different advisories for different farmers!
4. Click "Make Voice Call" - farmer receives call

## To Stop Everything

```powershell
.\stop_all.ps1
```

## Troubleshooting

### If script won't run:
```powershell
# Check execution policy
Get-ExecutionPolicy

# Should show "RemoteSigned" or "Unrestricted"
# If not, run:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### If ports are in use:
```powershell
# Stop everything first
.\stop_all.ps1

# Then start again
.\start_all.ps1
```

### View logs while running:
```powershell
# Backend logs
Get-Content backend.log -Wait

# Frontend logs
Get-Content frontend.log -Wait

# ngrok logs
Get-Content ngrok.log -Wait
```

## What's New

After starting, you'll see:
- ✅ Different advisories for Bangalore vs Chennai farmers
- ✅ Location-based NDVI values
- ✅ Crop-specific recommendations
- ✅ Weather-adjusted risk scores
- ✅ Personalized action items

Enjoy! 🎉
