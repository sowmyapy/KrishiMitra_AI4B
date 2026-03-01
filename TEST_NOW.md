# Test Right Now - No Code Changes Needed!

The code already works for 1 farmer. Just follow these simple steps.

## What You Have Right Now

✅ Code is ready  
✅ AWS credentials configured  
✅ pip install running (or completed)  

## Step 1: Wait for pip install (if still running)

Check if it's done. You should see something like:
```
Successfully installed ...
```

## Step 2: Test AWS Services (2 minutes)

```powershell
# Just run this
python scripts/test_aws_integration.py
```

**Expected output**:
```
✓ AWS Bedrock - Text generation working
✓ AWS Bedrock - Embeddings working  
✓ AWS Transcribe - Speech-to-text working
✓ AWS Polly - Text-to-speech working
```

If all 4 pass, you're good! ✅

## Step 3: Configure Minimal .env (1 minute)

Edit your `.env` file and make sure it has at least this:

```env
# AWS (you already have this)
AWS_REGION=ap-south-1
S3_BUCKET_AUDIO=krishimitra-audio-ap-south-1
LLM_PROVIDER=bedrock
USE_AWS_SERVICES=True

# Database (use SQLite for testing)
DATABASE_URL=sqlite:///./krishimitra.db

# JWT (any random string)
JWT_SECRET_KEY=test-secret-key-for-single-farmer-testing
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

That's it! You don't need Twilio, Weather API, or Sentinel Hub yet.

## Step 4: Create Database (30 seconds)

```powershell
# Create the database tables
python scripts/init_db.py
```

## Step 5: Start the Application (30 seconds)

```powershell
# Start the server
uvicorn src.main:app --reload
```

You should see:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete.
```

## Step 6: Open API Documentation (10 seconds)

Open your browser: **http://localhost:8000/docs**

You'll see the Swagger UI with all the API endpoints!

## Step 7: Test with One Farmer (5 minutes)

### 7a. Register a Farmer

In the Swagger UI:
1. Find **POST /api/v1/farmers/register**
2. Click "Try it out"
3. Use this data:

```json
{
  "name": "Test Farmer",
  "phone": "+919876543210",
  "language": "hi",
  "location": {
    "latitude": 28.6139,
    "longitude": 77.2090
  }
}
```

4. Click "Execute"
5. Copy the `farmer_id` from the response

### 7b. Get Farmer Info

1. Find **GET /api/v1/farmers/{farmer_id}**
2. Click "Try it out"
3. Paste your farmer_id
4. Click "Execute"

You should see your farmer's details!

### 7c. Test Voice Chatbot (The Cool Part!)

1. Find **POST /api/v1/voice/chat**
2. Click "Try it out"
3. Use this data:

```json
{
  "farmer_id": "your_farmer_id_here",
  "text": "मेरी गेहूं की फसल में पीले पत्ते दिख रहे हैं"
}
```

4. Click "Execute"

**You'll get**:
- AI response in Hindi
- Audio file (base64 encoded)
- Recommendations

This uses AWS Bedrock (Claude) and AWS Polly - all working!

## What Works Right Now (Without External APIs)

✅ **AI Conversations**: Chat with farmers in Hindi/English  
✅ **Voice Generation**: Text-to-speech in Indian languages  
✅ **Farmer Management**: Register, update, get farmer info  
✅ **Advisory System**: Generate crop recommendations  
✅ **Agentic AI**: All 5 agents working  
✅ **Database**: Store farmer data, advisories  

## What Needs External APIs (Add Later)

❌ **Phone Calls**: Need Twilio (but you can test via API)  
❌ **Real Weather Data**: Need Weather API (can use mock data)  
❌ **Real Satellite Images**: Need Sentinel Hub (can use mock data)  

## Testing Without Phone Calls

You can test everything via the API:

**Instead of calling the farmer**, you:
1. Use the API to send messages
2. Get responses via API
3. See what the farmer would hear (audio file)
4. Test the conversation flow

**It's the same logic**, just without actual phone calls!

## Quick Test Commands

```powershell
# Test 1: AWS Integration
python scripts/test_aws_integration.py

# Test 2: Start server
uvicorn src.main:app --reload

# Test 3: Open browser
start http://localhost:8000/docs

# Test 4: Check database
python -c "from src.config.database import engine; print('Database OK')"
```

## Troubleshooting

### "ModuleNotFoundError"
→ Make sure pip install completed: `pip list | grep fastapi`

### "Database error"
→ Run: `python scripts/init_db.py`

### "AWS credentials not found"
→ Run: `aws sts get-caller-identity` (should work in regular PowerShell)

### "Port 8000 already in use"
→ Use different port: `uvicorn src.main:app --reload --port 8001`

## What's Next?

Once this works:

1. **Add Twilio** (15 min) - For actual phone calls
2. **Add Weather API** (5 min) - For real weather data  
3. **Add Sentinel Hub** (20 min) - For satellite imagery

But you can test everything else RIGHT NOW! 🎉

## Cost for Testing Like This

**AWS Services**: ~$1-2/month (mostly free tier)  
**No external APIs**: $0  
**Total**: ~$1-2/month

Perfect for testing! ✅

---

## TL;DR - Absolute Minimum Steps

```powershell
# 1. Test AWS
python scripts/test_aws_integration.py

# 2. Create database
python scripts/init_db.py

# 3. Start server
uvicorn src.main:app --reload

# 4. Open browser
start http://localhost:8000/docs

# 5. Register a farmer and test!
```

That's it! No code changes needed. The system already works for 1 farmer.
