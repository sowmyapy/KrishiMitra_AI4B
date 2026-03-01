# 🌾 KrishiMitra - Complete End-to-End Test

## 🎯 What This Does

Complete workflow from satellite data to voice call:

```
🛰️ Satellite Data → 🌤️ Weather Data → 🤖 AI Analysis → 📋 Advisory → 🔊 Voice → 📞 Call
```

## ⚡ Quick Start (3 Steps)

### 1. Verify Phone Number
```
https://console.twilio.com/us1/develop/phone-numbers/manage/verified
→ Add: +918151910856
```

### 2. Start Services (3 Terminals)
```bash
# Terminal 1
uvicorn src.main:app --reload

# Terminal 2
ngrok http 8000

# Terminal 3
python scripts/test_real_farmer.py
```

### 3. Follow Prompts
- Paste ngrok URL
- Type `yes` to confirm
- Answer phone
- Listen to Hindi advisory

## 📚 Documentation

| Guide | Purpose | Time |
|-------|---------|------|
| **`START_HERE_END_TO_END.md`** | Main entry point | Start here |
| **`QUICK_TEST_GUIDE.md`** | 5-minute setup | 5 min |
| **`START_END_TO_END_TEST.md`** | Step-by-step checklist | 10 min |
| **`RUN_END_TO_END_WITH_CALL.md`** | Complete documentation | 15 min |
| **`END_TO_END_FLOW.md`** | Visual diagrams | 5 min |
| **`COMPLETE_TEST_SUMMARY.md`** | Full summary | 10 min |
| **`DOCUMENTATION_INDEX.md`** | All docs index | Reference |

## 🔍 Verify Setup

```bash
python scripts/verify_ready_for_test.py
```

## ✅ What You Get

- ✅ Real satellite data (NDVI analysis)
- ✅ Real weather data (temperature, humidity)
- ✅ AI-powered advisory (actions + costs)
- ✅ Hindi voice message
- ✅ Actual phone call

## 📊 Test Flow

```
Step 1: Register Farmer (1s)
Step 2: Fetch Satellite Data (3s) → NDVI: 0.55
Step 3: Fetch Weather Data (2s) → 38.5°C, 25% humidity
Step 4: AI Analysis (5s) → Water stress detected
Step 5: Generate Voice (2s) → Hindi MP3
Step 6: Make Call (1s) → Phone rings!

Total: ~70 seconds
```

## 🎧 What You'll Hear

Hindi advisory:
- Problem: Water stress
- Action 1: Irrigate (₹500, 24h)
- Action 2: Mulching (₹1250, 3d)
- Total: ₹1750

## 💰 Cost

~₹3.30 per test (~$0.04)

**Free tiers**:
- Twilio: $15 credit (750 tests)
- Sentinel Hub: 30,000 units/month
- OpenWeatherMap: 1,000 calls/day
- AWS Polly: 5M chars/month

## ⚠️ Troubleshooting

| Issue | Solution |
|-------|----------|
| Phone doesn't ring | Verify number in Twilio |
| Error 21212 | Check Twilio number in `.env` |
| Satellite fails | Test continues with simulated data |
| Weather fails | Test continues with simulated data |

## 🆘 Need Help?

### Test Components
```bash
python scripts/test_sentinel.py      # Satellite
python scripts/test_api_keys.py      # APIs
python scripts/make_real_call.py     # Voice
```

### Check Logs
- Server: Terminal 1
- ngrok: Terminal 2
- Test: Terminal 3
- Twilio: https://console.twilio.com/us1/monitor/logs/calls

## 📁 Files Created

- `test_advisory_message.mp3` - Voice message
- `krishimitra.db` - Database with farmer
- Twilio call logs

## 🎉 Success Criteria

- [ ] All 6 steps complete
- [ ] Phone rings within 10s
- [ ] Hindi message plays
- [ ] Call completes successfully

## 🚀 Ready?

**First time?** → `START_HERE_END_TO_END.md`

**Quick start?** → `QUICK_TEST_GUIDE.md`

**Need details?** → `RUN_END_TO_END_WITH_CALL.md`

---

**Let's test the complete KrishiMitra workflow!** 🌾📞
