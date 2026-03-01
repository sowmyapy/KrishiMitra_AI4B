# API Keys Guide - What You Need for AWS Deployment

## Quick Answer: What's Needed for AWS?

| Service | Needed for AWS? | Why? |
|---------|----------------|------|
| **AWS Credentials** | ✅ YES | Core infrastructure |
| **Twilio** | ✅ YES | Phone calls to farmers |
| **Weather API** | ✅ YES | Real-time weather data |
| **Sentinel Hub** | ✅ YES | Satellite imagery |
| **OpenAI** | ❌ NO | Using AWS Bedrock instead |
| **ElevenLabs** | ❌ NO | Using AWS Polly instead |

## Services You NEED for Full AWS Deployment

### 1. AWS Credentials ✅ (Already Have)

**Status**: ✅ You already have this configured

**What it's for**: 
- AWS Bedrock (LLM - Claude)
- AWS Transcribe (Speech-to-Text)
- AWS Polly (Text-to-Speech)
- S3 (Audio storage)
- RDS (Database)
- ECS (Container hosting)

**Already configured via**: `aws configure`

---

### 2. Twilio API Keys ✅ NEEDED

**What it's for**: Making actual phone calls to farmers

**How to get**:

1. **Sign up**: https://www.twilio.com/try-twilio
   - Free trial: $15 credit
   - Can make test calls immediately

2. **Get credentials**:
   - Go to: https://console.twilio.com/
   - Dashboard shows:
     - **Account SID**: `ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`
     - **Auth Token**: Click "Show" to reveal

3. **Get phone number**:
   - Go to: Phone Numbers → Manage → Buy a number
   - Choose a number with Voice capability
   - India numbers: ~$1/month
   - US numbers (for testing): ~$1/month

4. **Add to .env**:
   ```env
   TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
   TWILIO_AUTH_TOKEN=your_auth_token_here
   TWILIO_PHONE_NUMBER=+1234567890
   ```

**Cost**: 
- Phone number: $1/month
- Outbound calls: $0.0085/minute (India)
- For 10k farmers, 5 min/call/month: ~$425/month

**Free alternatives for testing**:
- Use Twilio trial (free $15 credit)
- Can only call verified numbers during trial

---

### 3. Weather API Keys ✅ NEEDED

**What it's for**: Real-time weather data for crop monitoring

**Recommended: OpenWeatherMap**

**How to get**:

1. **Sign up**: https://openweathermap.org/api
   - Free tier: 1,000 calls/day
   - Enough for testing

2. **Get API key**:
   - Sign up → Verify email
   - Go to: API keys section
   - Copy your API key

3. **Add to .env**:
   ```env
   WEATHER_API_KEY=your_openweathermap_api_key
   WEATHER_API_URL=https://api.openweathermap.org/data/2.5
   ```

**Cost**:
- Free tier: 1,000 calls/day (good for testing)
- Paid: $40/month for 100,000 calls/month
- For 10k farmers: ~$40-80/month

**Alternative providers**:
- **WeatherAPI.com**: Free tier 1M calls/month
- **Tomorrow.io**: Free tier 500 calls/day
- **AWS Weather Service**: Not available in all regions

---

### 4. Sentinel Hub (Satellite Imagery) ✅ NEEDED

**What it's for**: Satellite imagery for crop health monitoring (NDVI)

**How to get**:

1. **Sign up**: https://www.sentinel-hub.com/
   - Free trial: 30 days
   - Then: Pay-as-you-go

2. **Create account**:
   - Sign up → Verify email
   - Go to: Dashboard → User Settings

3. **Get credentials**:
   - Create OAuth client:
     - Dashboard → OAuth clients → Create new
     - Copy **Client ID** and **Client Secret**

4. **Add to .env**:
   ```env
   SENTINEL_HUB_CLIENT_ID=your_client_id
   SENTINEL_HUB_CLIENT_SECRET=your_client_secret
   SENTINEL_HUB_INSTANCE_ID=your_instance_id
   ```

**Cost**:
- Free trial: 30 days, 10,000 processing units
- Paid: ~$0.0001 per processing unit
- For 10k farmers (1 image/week): ~$50-100/month

**Alternative**:
- **Google Earth Engine**: Free for research/non-commercial
- **NASA EOSDIS**: Free but complex setup
- **Planet Labs**: Commercial, expensive

---

## Services You DON'T NEED for AWS Deployment

### 5. OpenAI API ❌ NOT NEEDED

**Why not needed**: Using AWS Bedrock (Claude) instead

**If you wanted it anyway**:
1. Sign up: https://platform.openai.com/signup
2. Add payment method: https://platform.openai.com/account/billing
3. Get API key: https://platform.openai.com/api-keys
4. Cost: ~$600/month for 10k farmers (more expensive than Bedrock)

**Don't get this** - AWS Bedrock is cheaper and better integrated.

---

### 6. ElevenLabs API ❌ NOT NEEDED

**Why not needed**: Using AWS Polly instead

**If you wanted it anyway**:
1. Sign up: https://elevenlabs.io/
2. Get API key from dashboard
3. Cost: ~$200/month for 10k farmers (more expensive than Polly)

**Don't get this** - AWS Polly is cheaper and supports Indian languages well.

---

## Summary: What to Get Now

### For Testing (Minimal)
✅ AWS credentials (already have)  
✅ Nothing else needed for basic testing!

### For Full Application (Production)
✅ AWS credentials (already have)  
✅ Twilio (phone calls) - **GET THIS**  
✅ Weather API (OpenWeatherMap) - **GET THIS**  
✅ Sentinel Hub (satellite) - **GET THIS**  
❌ OpenAI - **DON'T NEED**  
❌ ElevenLabs - **DON'T NEED**

---

## Cost Breakdown for 10,000 Farmers

| Service | Monthly Cost | Notes |
|---------|-------------|-------|
| AWS Bedrock | $150 | LLM (Claude) |
| AWS Transcribe | $120 | Speech-to-text |
| AWS Polly | $100 | Text-to-speech |
| AWS Infrastructure | $200 | ECS, RDS, S3, etc. |
| Twilio | $425 | Phone calls |
| Weather API | $60 | Real-time weather |
| Sentinel Hub | $75 | Satellite imagery |
| **TOTAL** | **$1,130/month** | **$0.113/farmer/month** |

Still under your target of <$1/farmer/month! ✅

---

## Step-by-Step: Get Keys in Order

### Step 1: Test AWS Integration First (Now)
```powershell
# Wait for pip install to complete
# Then run:
python scripts/test_aws_integration.py
```

### Step 2: Get Twilio (15 minutes)
1. Go to https://www.twilio.com/try-twilio
2. Sign up with email
3. Verify phone number
4. Get Account SID, Auth Token, Phone Number
5. Add to .env

### Step 3: Get Weather API (5 minutes)
1. Go to https://openweathermap.org/api
2. Sign up
3. Verify email
4. Copy API key
5. Add to .env

### Step 4: Get Sentinel Hub (20 minutes)
1. Go to https://www.sentinel-hub.com/
2. Sign up
3. Create OAuth client
4. Copy Client ID and Secret
5. Add to .env

**Total time**: ~40 minutes to get all keys

---

## Testing Without External APIs

You can test most functionality without external APIs:

**What works without keys**:
- ✅ AWS Bedrock (LLM)
- ✅ AWS Transcribe (STT)
- ✅ AWS Polly (TTS)
- ✅ Database operations
- ✅ API endpoints
- ✅ Agentic AI system

**What needs keys**:
- ❌ Actual phone calls (needs Twilio)
- ❌ Real weather data (needs Weather API)
- ❌ Real satellite imagery (needs Sentinel Hub)

**For testing**: You can use mock data for weather and satellite imagery.

---

## .env File Template

Here's what your complete .env should look like:

```env
# ============================================
# AWS Configuration (REQUIRED)
# ============================================
AWS_REGION=ap-south-1
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
S3_BUCKET_AUDIO=krishimitra-audio-ap-south-1

# ============================================
# Provider Selection (REQUIRED)
# ============================================
LLM_PROVIDER=bedrock
USE_AWS_SERVICES=True

# ============================================
# Twilio (REQUIRED for phone calls)
# ============================================
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=your_auth_token
TWILIO_PHONE_NUMBER=+1234567890

# ============================================
# Weather API (REQUIRED for weather data)
# ============================================
WEATHER_API_KEY=your_openweathermap_key
WEATHER_API_URL=https://api.openweathermap.org/data/2.5

# ============================================
# Sentinel Hub (REQUIRED for satellite data)
# ============================================
SENTINEL_HUB_CLIENT_ID=your_client_id
SENTINEL_HUB_CLIENT_SECRET=your_client_secret
SENTINEL_HUB_INSTANCE_ID=your_instance_id

# ============================================
# Database (REQUIRED)
# ============================================
DATABASE_URL=postgresql://user:password@localhost:5432/krishimitra
# For testing, use SQLite:
# DATABASE_URL=sqlite:///./krishimitra.db

# ============================================
# Redis (REQUIRED)
# ============================================
REDIS_URL=redis://localhost:6379/0

# ============================================
# JWT Security (REQUIRED)
# ============================================
JWT_SECRET_KEY=your-random-secret-key-generate-this
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# ============================================
# NOT NEEDED (Using AWS services instead)
# ============================================
# OPENAI_API_KEY=not_needed
# ELEVENLABS_API_KEY=not_needed
```

---

## Next Steps

1. **Now**: Wait for pip install to complete
2. **Then**: Test AWS integration
3. **After that**: Get Twilio, Weather API, Sentinel Hub keys
4. **Finally**: Test full application with all services

See **NEXT_STEPS.md** for detailed instructions.
