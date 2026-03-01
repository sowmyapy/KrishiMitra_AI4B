# Quick Test Guide - Voice Call End-to-End

## 🚀 5-Minute Setup

### 1️⃣ Verify Phone Number (MUST DO FIRST!)
```
https://console.twilio.com/us1/develop/phone-numbers/manage/verified
→ Add: +918151910856
→ Complete verification
```

### 2️⃣ Start 3 Terminals

**Terminal 1 - Server:**
```bash
cd C:\Users\Sowmya\OneDrive\projects\ai_crop_system
.\venv\Scripts\activate
uvicorn src.main:app --reload
```

**Terminal 2 - ngrok:**
```bash
cd "C:\Program Files\ngrok"
ngrok http 8000
```
Copy the HTTPS URL (e.g., `https://emma-autecologic-gregg.ngrok-free.dev`)

**Terminal 3 - Test:**
```bash
cd C:\Users\Sowmya\OneDrive\projects\ai_crop_system
.\venv\Scripts\activate
python scripts/test_real_farmer.py
```

### 3️⃣ During Test

1. Press Enter to start
2. Watch progress through 6 steps
3. When prompted, paste ngrok URL: `https://your-url.ngrok-free.dev/voice/advisory`
4. Type `yes` to confirm call
5. Answer your phone
6. Listen to Hindi advisory

## ✅ What You'll Get

- 🛰️ Real satellite data (NDVI analysis)
- 🌤️ Real weather data (temperature, humidity)
- 🤖 AI-powered advisory (actions + costs)
- 🔊 Hindi voice message
- 📞 Actual phone call to +918151910856

## 📊 Expected Output

```
✓ Farmer registered
✓ Satellite data fetched (NDVI: 0.55)
✓ Weather data fetched (38.5°C, 25% humidity)
⚠ Advisory needed: water_stress
  Actions: 2, Total Cost: ₹1750
✓ Voice message generated
✓ Call initiated
🔔 Phone rings → Answer → Hear Hindi message
```

## 🎧 What You'll Hear (Hindi)

Advisory about water stress with:
- Immediate irrigation (₹500, 24 hours)
- Apply mulching (₹1250, 3 days)
- Total cost: ₹1750

## ⚠️ Common Issues

**Phone doesn't ring?**
→ Verify number in Twilio Console

**Error 21212?**
→ Check `.env` has `TWILIO_PHONE_NUMBER=+17752270557`

**Satellite data fails?**
→ Test continues with simulated data

**Weather data fails?**
→ Test continues with simulated data

## 📁 Files Created

- `test_advisory_message.mp3` - Voice message audio
- Database entry for farmer
- Call logs in Twilio Console

## 💰 Cost Per Test

~₹3.30 (~$0.04) - Covered by free tiers

## 🔍 Verify Before Running

```bash
python scripts/verify_ready_for_test.py
```

## 📚 Detailed Guides

- `START_END_TO_END_TEST.md` - Step-by-step instructions
- `RUN_END_TO_END_WITH_CALL.md` - Complete documentation
- `END_TO_END_FLOW.md` - Visual flow diagrams

## 🆘 Need Help?

Test individual components:
```bash
python scripts/test_sentinel.py
python scripts/test_api_keys.py
python scripts/make_real_call.py
```

---

**Ready?** Follow steps 1-3 above and experience the complete KrishiMitra workflow! 🌾📞
