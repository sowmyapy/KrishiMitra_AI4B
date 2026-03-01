# AWS Deployment - Services Needed

## Visual Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    KrishiMitra Application                   │
│                  (Running on AWS ECS/Fargate)                │
└─────────────────────────────────────────────────────────────┘
                              │
                              │ Uses these services:
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
        ▼                     ▼                     ▼
┌──────────────┐      ┌──────────────┐     ┌──────────────┐
│  AWS NATIVE  │      │   EXTERNAL   │     │   EXTERNAL   │
│   SERVICES   │      │   SERVICES   │     │   SERVICES   │
│              │      │              │     │              │
│ ✅ Bedrock   │      │ ✅ Twilio    │     │ ✅ Weather   │
│ ✅ Transcribe│      │   (Calls)    │     │    API       │
│ ✅ Polly     │      │              │     │              │
│ ✅ S3        │      │              │     │ ✅ Sentinel  │
│ ✅ RDS       │      │              │     │    Hub       │
│ ✅ ECS       │      │              │     │  (Satellite) │
└──────────────┘      └──────────────┘     └──────────────┘
     FREE*                 PAID                  PAID
  (AWS account)        ($425/month)          ($135/month)
```

*AWS services are pay-as-you-go, ~$570/month for 10k farmers

---

## Services Breakdown

### 🟢 AWS Native Services (Already Have Access)

| Service | Purpose | Status |
|---------|---------|--------|
| **AWS Bedrock** | LLM (Claude 3.5 Sonnet) | ✅ Verified |
| **AWS Transcribe** | Speech-to-Text (Hindi, etc.) | ✅ Verified |
| **AWS Polly** | Text-to-Speech (Neural voices) | ✅ Verified |
| **AWS S3** | Audio file storage | ✅ Ready |
| **AWS RDS** | PostgreSQL database | ✅ Ready |
| **AWS ECS** | Container hosting | ✅ Ready |
| **AWS Lambda** | Serverless functions | ✅ Ready |
| **AWS CloudWatch** | Monitoring & logs | ✅ Ready |

**Cost**: ~$570/month for 10,000 farmers

---

### 🔵 External Services (Need API Keys)

#### 1. Twilio - Phone Calls ✅ REQUIRED

**What it does**: Makes actual phone calls to farmers

**Why needed**: AWS doesn't have a phone calling service in India

**How to get**:
- Sign up: https://www.twilio.com/try-twilio
- Free trial: $15 credit
- Get: Account SID, Auth Token, Phone Number

**Cost**: ~$425/month for 10k farmers (5 min/call/month)

**Can we skip?**: ❌ No - Core feature is calling farmers

---

#### 2. Weather API - Real-time Weather ✅ REQUIRED

**What it does**: Provides real-time weather data for crop monitoring

**Why needed**: AWS doesn't have a weather data service

**Recommended**: OpenWeatherMap

**How to get**:
- Sign up: https://openweathermap.org/api
- Free tier: 1,000 calls/day
- Get: API Key

**Cost**: ~$60/month for 10k farmers

**Can we skip?**: ❌ No - Weather data is core to predictions

**AWS Alternative**: ❌ None available in India region

---

#### 3. Sentinel Hub - Satellite Imagery ✅ REQUIRED

**What it does**: Provides satellite imagery for crop health (NDVI)

**Why needed**: AWS doesn't provide processed satellite imagery

**How to get**:
- Sign up: https://www.sentinel-hub.com/
- Free trial: 30 days
- Get: Client ID, Client Secret

**Cost**: ~$75/month for 10k farmers

**Can we skip?**: ❌ No - Satellite monitoring is core feature

**AWS Alternative**: 
- ⚠️ AWS Ground Station (too complex, expensive)
- ⚠️ AWS Data Exchange (limited satellite data)

---

### 🔴 Services NOT Needed (Using AWS Instead)

#### OpenAI ❌ NOT NEEDED

**Why not**: Using AWS Bedrock (Claude) instead
- AWS Bedrock: $150/month
- OpenAI GPT-4: $300/month
- **Savings**: 50%

#### ElevenLabs ❌ NOT NEEDED

**Why not**: Using AWS Polly instead
- AWS Polly: $100/month
- ElevenLabs: $200/month
- **Savings**: 50%

---

## Cost Summary

### Total Monthly Cost (10,000 farmers)

| Category | Service | Cost |
|----------|---------|------|
| **AWS Services** | Bedrock + Transcribe + Polly + Infrastructure | $570 |
| **Phone Calls** | Twilio | $425 |
| **Weather Data** | OpenWeatherMap | $60 |
| **Satellite Data** | Sentinel Hub | $75 |
| **TOTAL** | | **$1,130** |

**Per Farmer**: $0.113/month ✅ (Under $1 target!)

---

## What Can Run Without External APIs?

### ✅ Works Without External APIs (For Testing)

- AWS Bedrock (LLM conversations)
- AWS Transcribe (Speech-to-text)
- AWS Polly (Text-to-speech)
- Database operations
- API endpoints
- Agentic AI system
- Mock data testing

### ❌ Needs External APIs (For Production)

- Actual phone calls → Needs Twilio
- Real weather data → Needs Weather API
- Real satellite imagery → Needs Sentinel Hub

---

## Decision Matrix

### Can I deploy to AWS without external APIs?

**For Testing/Demo**: ✅ YES
- Use mock data for weather and satellite
- Skip phone calls (test via API only)
- Everything else works with AWS services

**For Production**: ❌ NO
- Need Twilio for phone calls (core feature)
- Need Weather API for real weather data
- Need Sentinel Hub for real satellite imagery

---

## Recommended Approach

### Phase 1: AWS Testing (Now)
```
✅ AWS Bedrock, Transcribe, Polly
✅ Mock data for weather/satellite
✅ API testing only (no phone calls)
Cost: ~$50/month (minimal usage)
```

### Phase 2: Add External Services (Later)
```
✅ Add Twilio (phone calls)
✅ Add Weather API (real weather)
✅ Add Sentinel Hub (real satellite)
Cost: ~$1,130/month (full production)
```

---

## Getting Started Order

1. **Now**: Test AWS services (Bedrock, Transcribe, Polly)
   - Run: `python scripts/test_aws_integration.py`

2. **Next**: Get Twilio (most important external service)
   - Sign up: https://www.twilio.com/try-twilio
   - Test phone calls

3. **Then**: Get Weather API (second priority)
   - Sign up: https://openweathermap.org/api
   - Test weather data

4. **Finally**: Get Sentinel Hub (can use mock data initially)
   - Sign up: https://www.sentinel-hub.com/
   - Test satellite imagery

---

## FAQ

**Q: Can I use AWS services exclusively?**
A: Almost! You need Twilio for phone calls, Weather API for weather data, and Sentinel Hub for satellite imagery. AWS doesn't provide these services in India.

**Q: Why not use AWS Connect for phone calls?**
A: AWS Connect is available but more complex and expensive than Twilio for this use case.

**Q: Can I use free tiers?**
A: Yes for testing! Twilio ($15 credit), Weather API (1k calls/day), Sentinel Hub (30 day trial).

**Q: What's the minimum to get started?**
A: Just AWS credentials! You can test everything else with mock data.

**Q: When do I need to pay?**
A: Only when you exceed free tiers or go to production with real farmers.

---

## Next Steps

See **API_KEYS_GUIDE.md** for detailed instructions on getting each API key.
