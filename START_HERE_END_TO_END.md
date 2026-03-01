# 🚀 START HERE - Complete End-to-End Test

## What You're About to Do

Test the COMPLETE KrishiMitra workflow:
- 🛰️ Fetch real satellite data
- 🌤️ Fetch real weather data  
- 🤖 AI analysis of crop health
- 📋 Generate actionable advisory
- 🔊 Create Hindi voice message
- 📞 Make actual phone call to farmer

**Total time**: ~5 minutes setup + ~1 minute test run

## ⚡ Quick Start (Choose Your Path)

### 🏃 Fast Track (Experienced Users)
→ Go to: `QUICK_TEST_GUIDE.md`

### 📋 Step-by-Step (First Time)
→ Go to: `START_END_TO_END_TEST.md`

### 📖 Detailed Documentation
→ Go to: `RUN_END_TO_END_WITH_CALL.md`

### 📊 Visual Flow Diagrams
→ Go to: `END_TO_END_FLOW.md`

### 📝 Complete Summary
→ Go to: `COMPLETE_TEST_SUMMARY.md`

## ✅ Pre-Flight Checklist

Before you start, make sure:

1. **Phone number verified in Twilio** (CRITICAL!)
   - Go to: https://console.twilio.com/us1/develop/phone-numbers/manage/verified
   - Add: +918151910856
   - Complete verification

2. **API keys configured in `.env`**
   - ✅ Twilio credentials
   - ✅ AWS credentials
   - ✅ Sentinel Hub credentials (optional)
   - ✅ OpenWeatherMap key (optional)

3. **Farm coordinates updated**
   - Edit `scripts/test_real_farmer.py` lines 22-28
   - Use your actual farm location

4. **System ready**
   - Python virtual environment activated
   - Dependencies installed
   - ngrok installed

### 🔍 Verify Everything
```bash
python scripts/verify_ready_for_test.py
```

## 🎯 What You Need

### 3 Terminal Windows

**Terminal 1**: FastAPI server
```bash
uvicorn src.main:app --reload
```

**Terminal 2**: ngrok tunnel
```bash
ngrok http 8000
```

**Terminal 3**: Test script
```bash
python scripts/test_real_farmer.py
```

## 📞 What Happens

1. **Register farmer** → Database entry created
2. **Fetch satellite data** → NDVI analysis
3. **Fetch weather data** → Temperature, humidity, risks
4. **AI analysis** → Detect crop stress
5. **Generate advisory** → Actions with costs
6. **Create voice message** → Hindi MP3 file
7. **Make phone call** → Your phone rings!
8. **Hear advisory** → Hindi message plays

**Total**: ~70 seconds from start to call completion

## 🎧 What You'll Hear

Hindi advisory message:
- Greeting from KrishiMitra
- Problem: Water stress detected
- Action 1: Irrigate (₹500, 24 hours)
- Action 2: Mulching (₹1250, 3 days)
- Total cost: ₹1750

## 💰 Cost

~₹3.30 per test (~$0.04)

**Free tiers available**:
- Twilio: $15 trial credit (750 tests)
- Sentinel Hub: 30,000 units/month
- OpenWeatherMap: 1,000 calls/day
- AWS Polly: 5M characters/month

## ⚠️ Common Issues

**Phone doesn't ring?**
→ Verify number in Twilio Console

**Error 21212?**
→ Check Twilio phone number in `.env`

**Satellite/Weather fails?**
→ Test continues with simulated data

## 🆘 Need Help?

### Test Individual Components
```bash
python scripts/test_sentinel.py      # Test satellite data
python scripts/test_api_keys.py      # Test all APIs
python scripts/make_real_call.py     # Test voice calls
```

### Check Configuration
```bash
python scripts/verify_ready_for_test.py
```

### Review Documentation
- API setup: `API_KEYS_GUIDE.md`
- Webhook setup: `WEBHOOK_SETUP_COMPLETE.md`
- Voice flow: `VOICE_CALL_FLOW.md`

## 🎉 Ready?

Pick your guide above and let's test the complete KrishiMitra workflow!

**Recommended for first-time users**: `START_END_TO_END_TEST.md`

---

**Questions?** All documentation files are in the project root directory.
