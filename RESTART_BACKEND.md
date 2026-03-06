# How to Restart Backend After Code Changes

## The Issue
When you make changes to Python backend code, the server needs to be restarted for the changes to take effect.

## Quick Fix

### Option 1: Using the Stop/Start Scripts

1. **Stop all services**:
   ```powershell
   .\stop_all.ps1
   ```

2. **Start all services again**:
   ```powershell
   .\start_all.ps1
   ```

### Option 2: Restart Backend Only

If you're running the backend manually:

1. **Stop the backend**:
   - Press `Ctrl+C` in the terminal where backend is running

2. **Start the backend again**:
   ```powershell
   python -m uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
   ```

### Option 3: Using Process Manager

If backend is running in background:

1. **Find the process**:
   ```powershell
   Get-Process | Where-Object {$_.ProcessName -like "*python*"}
   ```

2. **Kill the process**:
   ```powershell
   Stop-Process -Name python -Force
   ```

3. **Start backend again**:
   ```powershell
   python -m uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
   ```

## Verify Backend is Running

Check if backend is responding:
```powershell
curl http://localhost:8000/api/v1/farmers/
```

You should see a JSON response with the list of farmers.

## After Restart

1. The authentication should now be disabled for the update endpoint
2. Try changing the farmer's language again from the UI
3. It should work without the "Not authenticated" error

## Note

The `--reload` flag in uvicorn should automatically reload when you change Python files, but sometimes it doesn't catch all changes. A manual restart ensures all changes are loaded.
