# Testing KrishiMitra - Complete Application Guide

## Prerequisites

1. **Application Running**: Make sure the server is running
   ```powershell
   .\venv\Scripts\Activate.ps1
   uvicorn src.main:app --reload
   ```

2. **Server URL**: http://127.0.0.1:8000

## Testing Methods

### Method 1: Interactive API Documentation (Easiest)

1. **Open Swagger UI**: http://127.0.0.1:8000/api/v1/docs
   - This provides an interactive interface to test all endpoints
   - You can see all available APIs and try them directly

2. **Authenticate in Swagger UI**:
   - Click the "Authorize" button (lock icon) at the top right
   - You'll need a JWT token to access protected endpoints
   - For testing, you can generate a token using the test script

3. **Test Basic Endpoints**:
   - Click on any endpoint (e.g., `GET /`)
   - Click "Try it out"
   - Click "Execute"
   - See the response

### Method 2: Using PowerShell/cURL

Open a new PowerShell window (keep the server running in the first one):

```powershell
# Test root endpoint (no auth required)
Invoke-RestMethod -Uri "http://127.0.0.1:8000/" -Method Get

# Test health check (no auth required)
Invoke-RestMethod -Uri "http://127.0.0.1:8000/health" -Method Get

# For authenticated endpoints, you need a JWT token
# Use the test script to generate one (see Method 3)
```

### Method 3: Complete End-to-End Test Script (Recommended)

The automated test script handles authentication automatically:

```powershell
# In a new PowerShell window
.\venv\Scripts\Activate.ps1
python scripts/test_complete_app.py
```

This script will:
- Generate a test JWT token automatically
- Test all endpoints with proper authentication
- Show detailed results for each test

## What to Test

### 1. Basic API Endpoints (No Auth Required)

**Root Endpoint**:
- URL: http://127.0.0.1:8000/
- Expected: Welcome message with app info

**Health Check**:
- URL: http://127.0.0.1:8000/health
- Expected: Status "healthy"

**API Documentation**:
- URL: http://127.0.0.1:8000/api/v1/docs
- Expected: Interactive Swagger UI

### 2. Farmer Management (Auth Required)

**Note**: These endpoints require JWT authentication. Use the test script or generate a token.

**Create a Farmer**:
```powershell
# You need a JWT token first
# Use the test script: python scripts/test_complete_app.py
```

**List Farmers**:
```powershell
# You need a JWT token first
# Use the test script: python scripts/test_complete_app.py
```

### 3. AWS Services (Already Tested)

- ✓ AWS Transcribe (STT) - Working
- ✓ AWS Polly (TTS) - Working
- ✗ AWS Bedrock (LLM) - Rate limited (will work after quota resets)

### 4. Database Operations

All database tables are created and ready:
- farmers
- farm_plots
- crop_health_indicators
- stress_predictions
- advisories
- actions
- resources
- call_records
- farmer_feedback
- chatbot_sessions
- conversation_turns
- chatbot_metrics

## Current Limitations

### What's NOT Working Yet (Expected)

1. **External API Keys Not Configured**:
   - Weather API (OpenWeatherMap)
   - Satellite Data (Sentinel Hub)
   - Twilio (Voice calls)
   - ElevenLabs (TTS alternative)

2. **Services Not Running**:
   - Redis (caching)
   - Kafka (message queue)
   - ChromaDB (vector database)

3. **AWS Bedrock Rate Limit**:
   - LLM quota exhausted
   - Will reset in 24 hours

### What IS Working

1. ✓ FastAPI server
2. ✓ Database (SQLite)
3. ✓ All API endpoints defined
4. ✓ AWS Transcribe (STT)
5. ✓ AWS Polly (TTS)
6. ✓ Data models
7. ✓ Authentication structure

## Quick Test Checklist

- [ ] Server starts without errors
- [ ] Can access http://127.0.0.1:8000/docs
- [ ] Root endpoint returns welcome message
- [ ] Health check returns "healthy"
- [ ] Can create a farmer via API
- [ ] Can list farmers via API
- [ ] AWS Transcribe test passes
- [ ] AWS Polly test passes

## Next Steps for Full Testing

To test the complete application with all features:

1. **Get API Keys** (see `API_KEYS_GUIDE.md`):
   - OpenWeatherMap API key
   - Sentinel Hub credentials
   - Twilio account (for voice calls)

2. **Start Supporting Services**:
   ```powershell
   # Redis
   docker run -d -p 6379:6379 redis:latest
   
   # Kafka
   docker-compose up -d kafka
   
   # ChromaDB
   docker run -d -p 8001:8000 chromadb/chroma
   ```

3. **Update .env** with real API keys

4. **Wait for AWS Bedrock quota reset** (24 hours)

5. **Run full integration tests**:
   ```powershell
   python scripts/test_complete_app.py
   ```

## Troubleshooting

**Server won't start**:
- Check if port 8000 is already in use
- Make sure virtual environment is activated

**Can't access http://127.0.0.1:8000**:
- Check if server is running
- Try http://localhost:8000 instead

**Database errors**:
- Delete `krishimitra.db` and restart server
- Database will be recreated automatically

**Import errors**:
- Make sure you're in the virtual environment
- Run: `pip install -r requirements-aws.txt`

## Success Criteria

Your application is successfully running if:
1. Server starts without errors
2. You can access the Swagger UI at /docs
3. Basic endpoints return expected responses
4. You can create and retrieve farmers via API
5. AWS STT and TTS services work

## Current Status: ✓ READY FOR BASIC TESTING

The core application is running and ready for basic API testing. Full feature testing requires additional API keys and services.
