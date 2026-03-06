# KrishiMitra - Quick Start Guide

## TL;DR - Get Running in 3 Steps

### Windows (PowerShell)
```powershell
# 1. Start all services
.\start_all.ps1

# 2. Open browser
start http://localhost:3000

# 3. When done, stop services
.\stop_all.ps1
```

### Linux/Mac
```bash
# 1. Start all services
chmod +x start_all.sh
./start_all.sh

# 2. Open browser
open http://localhost:3000  # Mac
xdg-open http://localhost:3000  # Linux

# 3. When done, stop services
./stop_all.sh
```

## What You Get

- **Frontend**: http://localhost:3000 - Farmer management UI
- **Backend API**: http://localhost:8000 - REST API
- **API Docs**: http://localhost:8000/docs - Interactive API documentation
- **ngrok Dashboard**: http://localhost:4040 - Tunnel status (if ngrok installed)

## Current Features Working

✅ **Farmer Registration** - Register farmers with phone, language, timezone
✅ **Plot Management** - Add farm plots with location and crop types
✅ **Advisory Generation** - Generate advisories based on satellite + weather data
✅ **Advisory Display** - View advisories with color-coded urgency levels
✅ **Voice Calls** - Initiate calls to deliver advisories in Hindi
✅ **Real Data Integration** - Sentinel Hub (satellite) + OpenWeatherMap (weather)

## Test Data Available

### Farmer 1
- Phone: +918151910856
- Location: Bangalore (12.9716, 77.5946)
- Crops: wheat, rice
- Has plot and advisories

### Farmer 2
- Phone: +918095666788
- Location: Chennai (13.0827, 80.2707)
- Crops: rice, sugarcane
- Has plot and advisories

## Common Tasks

### View Farmers
1. Go to http://localhost:3000/farmers
2. Click eye icon to view details

### Generate Advisory
1. View farmer details
2. Click "Generate Advisory" button
3. Wait 10-15 seconds (fetching satellite/weather data)
4. Advisory appears in table below

### Make Voice Call
1. Generate advisory first (if not done)
2. Click "Make Voice Call" button
3. Farmer receives call with advisory in Hindi

### View Logs
```powershell
# Windows
Get-Content backend.log -Wait

# Linux/Mac
tail -f backend.log
```

## Troubleshooting

### Services Won't Start
```powershell
# Stop everything first
.\stop_all.ps1

# Then start again
.\start_all.ps1
```

### Port Already in Use
```powershell
# Windows - Kill processes on ports
Get-NetTCPConnection -LocalPort 8000 | ForEach-Object { Stop-Process -Id $_.OwningProcess -Force }
Get-NetTCPConnection -LocalPort 3000 | ForEach-Object { Stop-Process -Id $_.OwningProcess -Force }

# Linux/Mac
lsof -ti:8000 | xargs kill -9
lsof -ti:3000 | xargs kill -9
```

### Backend Crashed
Check `backend.log` for errors. Common issues:
- Missing dependencies: `pip install -r requirements.txt`
- Database issues: Delete `krishimitra.db` and restart

### Frontend Not Loading
Check `frontend.log` for errors. Common issues:
- Missing dependencies: `cd frontend && npm install`
- Port conflict: Stop other apps using port 3000

## Next Steps

1. **Explore the UI** - Register new farmers, add plots
2. **Test Advisory Generation** - Generate advisories for different farmers
3. **Review Dataset Recommendations** - See `DATASET_RECOMMENDATIONS.md`
4. **Check API Documentation** - Visit http://localhost:8000/docs

## Important Files

- `.env` - Configuration (API keys, ngrok URL)
- `backend.log` - Backend logs
- `frontend.log` - Frontend logs
- `ngrok.log` - ngrok tunnel logs
- `TESTING_GUIDE.md` - Detailed testing instructions
- `DATASET_RECOMMENDATIONS.md` - Data sources and integration guide

## Need Help?

1. Check log files for errors
2. Review `STARTUP_SCRIPTS_README.md` for detailed troubleshooting
3. Ensure all prerequisites are installed (Python, Node.js, ngrok)
