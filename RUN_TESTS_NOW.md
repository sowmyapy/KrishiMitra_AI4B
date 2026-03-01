# Run Tests Now - Quick Guide

## What Was Fixed

1. **Correct API Documentation URL**: Changed from `/docs` to `/api/v1/docs`
2. **Authentication**: Added JWT token generation for protected endpoints
3. **Test Phone Number**: Using `+919876543210` (fake number for testing)

## Run the Tests

### Step 1: Make sure the server is running

In one PowerShell window:
```powershell
.\venv\Scripts\Activate.ps1
uvicorn src.main:app --reload
```

### Step 2: Run the test script

In another PowerShell window:
```powershell
.\venv\Scripts\Activate.ps1
python scripts/test_complete_app.py
```

## Expected Results

All 5 tests should now PASS:
- ✓ Root Endpoint
- ✓ Health Check
- ✓ API Documentation
- ✓ Create Farmer
- ✓ List Farmers

## Access the Application

After tests pass, you can access:
- **API**: http://127.0.0.1:8000
- **Interactive Docs**: http://127.0.0.1:8000/api/v1/docs

## About the Test Data

- **Phone Number**: `+919876543210` is a fake number used for testing
- **JWT Token**: Auto-generated with 1-hour expiration
- **Role**: Test token has "staff" role to access all endpoints

See `TEST_DATA_EXPLAINED.md` for more details.

## Troubleshooting

**Port 8000 already in use**:
- Stop the existing server process
- Or use a different port: `uvicorn src.main:app --reload --port 8001`

**Authentication errors**:
- The test script automatically generates JWT tokens
- No manual token creation needed

**Database errors**:
- Delete `krishimitra.db` and restart the server
- Database will be recreated automatically
