# Fix "Not authenticated" Error When Updating Farmer

## The Problem
When trying to change a farmer's language, you get a "Not authenticated" error.

## Root Cause
The backend code was updated to disable authentication, but the running server still has the old code loaded in memory.

## Solution: Restart the Backend

### Step 1: Stop the Backend

If you started with the script:
```powershell
.\stop_all.ps1
```

Or if running manually, press `Ctrl+C` in the terminal where the backend is running.

### Step 2: Start the Backend Again

If you want to start everything:
```powershell
.\start_all.ps1
```

Or if you want to start just the backend:
```powershell
python -m uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

### Step 3: Verify the Fix

Run the test script:
```powershell
python test_update_farmer.py
```

You should see:
```
✅ SUCCESS! Farmer updated successfully
New language: te
```

If you still see authentication errors, the backend might not have restarted properly.

## Alternative: Test Directly with curl

Test the endpoint directly:

```powershell
# Get farmers list
curl http://localhost:8000/api/v1/farmers/

# Update a farmer (replace FARMER_ID with actual ID)
curl -X PUT http://localhost:8000/api/v1/farmers/FARMER_ID `
  -H "Content-Type: application/json" `
  -d '{\"phone_number\":\"+918151910856\",\"preferred_language\":\"te\",\"timezone\":\"Asia/Kolkata\"}'
```

## After Restart

1. Go to the web interface: http://localhost:3000
2. Navigate to Farmers → Click on a farmer
3. Click "Edit" button
4. Change language to Telugu
5. Click "Update"
6. Should work without authentication error!

## Why This Happens

Python's uvicorn server with `--reload` flag should automatically reload when files change, but:
- Sometimes it doesn't detect all changes
- Cached imports can cause issues
- Manual restart ensures clean state

## Troubleshooting

### Backend won't start?
Check if port 8000 is already in use:
```powershell
netstat -ano | findstr :8000
```

Kill the process if needed:
```powershell
taskkill /PID <PID> /F
```

### Still getting authentication error?
1. Check the backend logs for errors
2. Verify the code change is in `src/api/farmers.py`:
   ```python
   @router.put("/{farmer_id}", response_model=FarmerResponse)
   async def update_farmer(
       farmer_id: UUID,
       farmer_data: FarmerCreate,
       db: Session = Depends(get_db)
       # Authentication temporarily disabled for testing
       # current_user: dict = Depends(get_current_user)
   ):
   ```
3. Make sure you saved the file
4. Try a hard restart (stop all, wait 5 seconds, start all)

### Frontend still showing error?
1. Clear browser cache (Ctrl+Shift+Delete)
2. Refresh the page (Ctrl+F5)
3. Check browser console for errors (F12)

## Quick Test Commands

Test if backend is running:
```powershell
curl http://localhost:8000/health
```

Test if farmers endpoint works:
```powershell
curl http://localhost:8000/api/v1/farmers/
```

Test update endpoint (use actual farmer ID):
```powershell
python test_update_farmer.py
```

All should return successful responses without authentication errors.
