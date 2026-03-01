# Quick Reference Card

## What You Need for AWS Deployment

### ✅ REQUIRED (Get These)

| Service | Why? | Cost/Month | Sign Up Link |
|---------|------|------------|--------------|
| **AWS** | Core infrastructure | $570 | Already have ✅ |
| **Twilio** | Phone calls to farmers | $425 | https://www.twilio.com/try-twilio |
| **Weather API** | Real-time weather data | $60 | https://openweathermap.org/api |
| **Sentinel Hub** | Satellite imagery | $75 | https://www.sentinel-hub.com/ |

**Total**: $1,130/month for 10,000 farmers = $0.113/farmer/month ✅

### ❌ NOT NEEDED (Skip These)

| Service | Why Skip? | Replaced By |
|---------|-----------|-------------|
| **OpenAI** | More expensive | AWS Bedrock (Claude) |
| **ElevenLabs** | More expensive | AWS Polly |

---

## Current Status

✅ AWS CLI configured  
✅ AWS Bedrock access (Claude 3.5 Sonnet v2)  
✅ AWS Transcribe access  
✅ AWS Polly access  
⏳ pip install running...  

---

## Next Commands (After pip install completes)

```powershell
# 1. Test AWS integration
python scripts/test_aws_integration.py

# 2. If tests pass, run the app
uvicorn src.main:app --reload

# 3. Visit API docs
# http://localhost:8000/docs
```

---

## Get API Keys (Do This After Testing)

### 1. Twilio (15 min)
```
1. Go to: https://www.twilio.com/try-twilio
2. Sign up → Get $15 free credit
3. Copy: Account SID, Auth Token, Phone Number
4. Add to .env
```

### 2. Weather API (5 min)
```
1. Go to: https://openweathermap.org/api
2. Sign up → Verify email
3. Copy: API Key
4. Add to .env
```

### 3. Sentinel Hub (20 min)
```
1. Go to: https://www.sentinel-hub.com/
2. Sign up → Create OAuth client
3. Copy: Client ID, Client Secret
4. Add to .env
```

---

## .env Configuration

### Minimal (For Testing AWS Only)
```env
AWS_REGION=ap-south-1
S3_BUCKET_AUDIO=krishimitra-audio-ap-south-1
LLM_PROVIDER=bedrock
USE_AWS_SERVICES=True
DATABASE_URL=sqlite:///./krishimitra.db
JWT_SECRET_KEY=any-random-string
```

### Full (For Production)
```env
# AWS
AWS_REGION=ap-south-1
S3_BUCKET_AUDIO=krishimitra-audio-ap-south-1
LLM_PROVIDER=bedrock
USE_AWS_SERVICES=True

# Twilio
TWILIO_ACCOUNT_SID=ACxxxx...
TWILIO_AUTH_TOKEN=your_token
TWILIO_PHONE_NUMBER=+1234567890

# Weather
WEATHER_API_KEY=your_key
WEATHER_API_URL=https://api.openweathermap.org/data/2.5

# Sentinel Hub
SENTINEL_HUB_CLIENT_ID=your_id
SENTINEL_HUB_CLIENT_SECRET=your_secret

# Database
DATABASE_URL=postgresql://user:pass@host:5432/krishimitra

# Redis
REDIS_URL=redis://localhost:6379/0

# JWT
JWT_SECRET_KEY=generate-random-string
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

---

## Cost Comparison

### AWS Services vs OpenAI

| Component | OpenAI | AWS | Savings |
|-----------|--------|-----|---------|
| LLM | $300 | $150 | 50% |
| STT | $200 | $120 | 40% |
| TTS | $100 | $100 | 0% |
| **Total** | **$600** | **$370** | **38%** |

**Winner**: AWS Bedrock + Transcribe + Polly 🏆

---

## Important Files

| File | Purpose |
|------|---------|
| **API_KEYS_GUIDE.md** | Detailed guide to get all API keys |
| **INSTALL_STEPS.md** | Step-by-step installation |
| **CHECKLIST.md** | Track your progress |
| **GIT_SETUP.md** | Commit to GitHub |
| **NEXT_STEPS.md** | What to do next |

---

## Troubleshooting

### pip install fails
→ Make sure using `requirements-aws.txt`

### AWS CLI not found
→ Use regular PowerShell, not Kiro terminal

### Tests fail
→ Check AWS credentials: `aws sts get-caller-identity`

### Can't make phone calls
→ Need Twilio keys (get from https://www.twilio.com)

---

## Support

**Documentation**: See API_KEYS_GUIDE.md for detailed instructions

**AWS Console**: https://console.aws.amazon.com/

**Twilio Console**: https://console.twilio.com/

**Weather API**: https://openweathermap.org/api

**Sentinel Hub**: https://www.sentinel-hub.com/
