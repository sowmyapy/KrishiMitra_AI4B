# Single Farmer Testing Guide

Testing KrishiMitra with just one farmer - minimal cost, full functionality!

## Cost for 1 Farmer Testing

| Service | Monthly Cost | Notes |
|---------|-------------|-------|
| AWS Bedrock | ~$0.50 | Few test conversations |
| AWS Transcribe | ~$0.30 | Few voice interactions |
| AWS Polly | ~$0.20 | Few voice responses |
| AWS Infrastructure | FREE | Free tier |
| Twilio | FREE | $15 trial credit |
| Weather API | FREE | Free tier (1k calls/day) |
| Sentinel Hub | FREE | 30-day trial |
| **TOTAL** | **~$1-2/month** | Mostly free! |

## What You Need

### ✅ Already Have
- AWS credentials (Bedrock, Transcribe, Polly)
- Python environment
- Code repository

### ✅ Get These (All Have Free Tiers!)

1. **Twilio** - FREE trial ($15 credit)
2. **Weather API** - FREE tier (1,000 calls/day)
3. **Sentinel Hub** - FREE trial (30 days)

## Step-by-Step Setup

### Step 1: Test AWS Services (5 minutes)

```powershell
# Make sure pip install completed
# Then test AWS integration
python scripts/test_aws_integration.py
```

Expected output:
```
✓ AWS Bedrock - Text generation working
✓ AWS Bedrock - Embeddings working
✓ AWS Transcribe - Speech-to-text working
✓ AWS Polly - Text-to-speech working
```

---

### Step 2: Get Twilio (FREE - 15 minutes)

**Why**: To make actual phone calls to test farmer

1. **Sign up**: https://www.twilio.com/try-twilio
   - Use your email
   - Verify your phone number
   - Get **$15 FREE credit** (enough for ~30 hours of calls!)

2. **Get credentials**:
   - Dashboard: https://console.twilio.com/
   - Copy **Account SID**: `ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`
   - Copy **Auth Token**: Click "Show" to reveal

3. **Get phone number**:
   - Go to: Phone Numbers → Buy a number
   - Choose any country (US is cheapest for testing: $1/month)
   - Select a number with Voice capability
   - Buy it (uses your $15 credit)

4. **Add to .env**:
   ```env
   TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
   TWILIO_AUTH_TOKEN=your_auth_token_here
   TWILIO_PHONE_NUMBER=+1234567890
   ```

5. **Verify your test number**:
   - During trial, you can only call verified numbers
   - Go to: Phone Numbers → Verified Caller IDs
   - Add your personal phone number (the one you want to test with)
   - Twilio will call you to verify

**Cost**: FREE (uses $15 trial credit)

---

### Step 3: Get Weather API (FREE - 5 minutes)

**Why**: To get real weather data for your test farmer's location

1. **Sign up**: https://openweathermap.org/api
   - Create account
   - Verify email

2. **Get API key**:
   - Go to: API keys section
   - Copy your default API key

3. **Add to .env**:
   ```env
   WEATHER_API_KEY=your_openweathermap_api_key
   WEATHER_API_URL=https://api.openweathermap.org/data/2.5
   ```

**Cost**: FREE (1,000 calls/day - way more than you need!)

---

### Step 4: Get Sentinel Hub (FREE - 20 minutes)

**Why**: To get satellite imagery for your test farmer's field

1. **Sign up**: https://www.sentinel-hub.com/
   - Create account
   - Verify email

2. **Create configuration**:
   - Dashboard → Configuration Utility
   - Create new configuration
   - Copy **Instance ID**

3. **Create OAuth client**:
   - Dashboard → User Settings → OAuth clients
   - Create new client
   - Copy **Client ID** and **Client Secret**

4. **Add to .env**:
   ```env
   SENTINEL_HUB_CLIENT_ID=your_client_id
   SENTINEL_HUB_CLIENT_SECRET=your_client_secret
   SENTINEL_HUB_INSTANCE_ID=your_instance_id
   ```

**Cost**: FREE (30-day trial, 10,000 processing units - enough for testing!)

---

### Step 5: Configure .env File

Your complete `.env` file should look like this:

```env
# ============================================
# AWS Configuration (REQUIRED)
# ============================================
AWS_REGION=ap-south-1
S3_BUCKET_AUDIO=krishimitra-audio-ap-south-1

# Provider Selection
LLM_PROVIDER=bedrock
USE_AWS_SERVICES=True

# ============================================
# Twilio (FREE trial)
# ============================================
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=your_auth_token
TWILIO_PHONE_NUMBER=+1234567890

# ============================================
# Weather API (FREE tier)
# ============================================
WEATHER_API_KEY=your_openweathermap_key
WEATHER_API_URL=https://api.openweathermap.org/data/2.5

# ============================================
# Sentinel Hub (FREE trial)
# ============================================
SENTINEL_HUB_CLIENT_ID=your_client_id
SENTINEL_HUB_CLIENT_SECRET=your_client_secret
SENTINEL_HUB_INSTANCE_ID=your_instance_id

# ============================================
# Database (SQLite for testing)
# ============================================
DATABASE_URL=sqlite:///./krishimitra.db

# ============================================
# Redis (Optional for testing)
# ============================================
REDIS_URL=redis://localhost:6379/0

# ============================================
# JWT Security
# ============================================
JWT_SECRET_KEY=test-secret-key-change-in-production
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

---

### Step 6: Initialize Database

```powershell
# Create database tables
python scripts/init_db.py
```

---

### Step 7: Create Test Farmer

```powershell
# Run the seed data script to create a test farmer
python scripts/seed_data.py
```

This will create:
- 1 test farmer with your phone number
- Sample field location
- Sample crop data

---

### Step 8: Start the Application

```powershell
# Start FastAPI server
uvicorn src.main:app --reload
```

You should see:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete.
```

---

### Step 9: Test the API

Open your browser: http://localhost:8000/docs

You'll see the Swagger UI with all API endpoints.

**Try these endpoints**:

1. **Register a farmer** (POST `/api/v1/farmers/register`):
   ```json
   {
     "name": "Test Farmer",
     "phone": "+1234567890",
     "language": "hi",
     "location": {
       "latitude": 28.6139,
       "longitude": 77.2090
     }
   }
   ```

2. **Get farmer info** (GET `/api/v1/farmers/{farmer_id}`)

3. **Create advisory** (POST `/api/v1/advisories/`)

4. **Test voice chatbot** (POST `/api/v1/voice/chat`)

---

### Step 10: Test Voice Call (The Cool Part!)

**Option A: Via API**

```powershell
# Use curl or Postman to call the voice endpoint
curl -X POST "http://localhost:8000/api/v1/voice/call" \
  -H "Content-Type: application/json" \
  -d '{
    "farmer_id": "your_farmer_id",
    "message": "Your crops need water. Please irrigate within 24 hours."
  }'
```

**Option B: Via Python Script**

Create a test script `test_call.py`:

```python
import requests

response = requests.post(
    "http://localhost:8000/api/v1/voice/call",
    json={
        "farmer_id": "your_farmer_id",
        "message": "Your crops need water. Please irrigate within 24 hours."
    }
)

print(response.json())
```

Run it:
```powershell
python test_call.py
```

**You should receive a phone call!** 📞

The system will:
1. Call your verified phone number
2. Speak the message in Hindi (or your chosen language)
3. Allow you to respond with voice
4. Use AI to understand and respond

---

## Testing Checklist

- [ ] AWS integration tests pass
- [ ] Twilio account created (FREE trial)
- [ ] Weather API key obtained (FREE tier)
- [ ] Sentinel Hub account created (FREE trial)
- [ ] .env file configured
- [ ] Database initialized
- [ ] Test farmer created
- [ ] Application running
- [ ] API endpoints working
- [ ] Voice call received successfully! 🎉

---

## What You Can Test

### ✅ Full Functionality Available

1. **Voice Conversations**:
   - Call farmer with advisory
   - Farmer responds with voice
   - AI understands and responds
   - Natural conversation in Hindi/English

2. **Crop Monitoring**:
   - Get satellite imagery for test field
   - Calculate NDVI (crop health)
   - Get weather data for location
   - Predict crop stress

3. **AI Agents**:
   - Monitoring agent analyzes data
   - Advisory agent generates recommendations
   - Communication agent handles conversations

4. **API Endpoints**:
   - Register farmers
   - Create advisories
   - Get crop health reports
   - Voice chatbot interactions

---

## Troubleshooting

### Twilio: "Cannot call unverified number"
**Solution**: Verify your phone number in Twilio console (Phone Numbers → Verified Caller IDs)

### Weather API: "Invalid API key"
**Solution**: Wait 10 minutes after signup - API key activation takes time

### Sentinel Hub: "Authentication failed"
**Solution**: Make sure you created OAuth client and copied correct credentials

### Database error
**Solution**: Run `python scripts/init_db.py` to create tables

### AWS Bedrock: "Model not found"
**Solution**: Enable Claude models at https://console.aws.amazon.com/bedrock

---

## Cost Tracking

After testing for a week:

```powershell
# Check AWS costs
aws ce get-cost-and-usage \
  --time-period Start=2024-01-01,End=2024-01-31 \
  --granularity MONTHLY \
  --metrics BlendedCost
```

Expected costs:
- AWS: $1-2 (mostly free tier)
- Twilio: $0 (using trial credit)
- Weather API: $0 (free tier)
- Sentinel Hub: $0 (trial)

**Total**: ~$1-2 for the entire month! 🎉

---

## Next Steps

Once testing works:

1. **Add more farmers**: Scale to 10, 100, 1000 farmers
2. **Deploy to AWS**: Use ECS/Fargate for production
3. **Set up monitoring**: CloudWatch, Grafana
4. **Add more features**: SMS notifications, mobile app
5. **Optimize costs**: Use reserved instances, spot instances

---

## Support

**Issues?** Check these files:
- API_KEYS_GUIDE.md - Detailed API key instructions
- INSTALL_STEPS.md - Installation troubleshooting
- TESTING_GUIDE.md - Testing instructions

**Questions?** The application logs will show detailed error messages.
