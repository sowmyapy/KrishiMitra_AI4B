# 🎯 START HERE: Voice Calls Setup

## What This Is

Complete guide to make your first voice call with KrishiMitra. You'll call your own phone (+918095666788) and hear a Hindi farming advisory.

## Time Required

- **First time**: 10 minutes
- **After setup**: 2 minutes per call

## Quick Decision Tree

```
Do you have ngrok installed?
├─ YES → Go to "Quick Start" below
└─ NO  → Go to "First Time Setup" below
```

---

## First Time Setup (10 minutes)

### Step 1: Verify Prerequisites (2 min)

Run the verification script:
```powershell
cd C:\Users\Sowmya\OneDrive\projects\ai_crop_system
.\venv\Scripts\Activate.ps1
python scripts/verify_call_setup.py
```

This checks:
- ✓ Twilio credentials
- ✓ Server configuration
- ✓ Voice endpoints
- ✓ ngrok installation
- ✓ Phone number format

### Step 2: Install ngrok (3 min)

**If verification shows ngrok is missing:**

1. Go to: https://ngrok.com/download
2. Download "Windows (64-bit)"
3. Extract ZIP to `C:\ngrok\`
4. Test: `C:\ngrok\ngrok.exe version`

**Or use Chocolatey:**
```powershell
choco install ngrok
```

### Step 3: Verify Twilio Phone Number (2 min)

**For trial accounts only:**

1. Go to: https://console.twilio.com/
2. Click "Phone Numbers" > "Verified Caller IDs"
3. Click "Add a new number"
4. Enter: +918095666788
5. Verify via SMS code

**Skip this if you have a paid account**

### Step 4: Test Setup (3 min)

Run verification again:
```powershell
python scripts/verify_call_setup.py
```

All checks should pass ✓

---

## Quick Start (2 minutes)

### Open 3 Terminals

**Terminal 1: Server**
```powershell
cd C:\Users\Sowmya\OneDrive\projects\ai_crop_system
.\venv\Scripts\Activate.ps1
uvicorn src.main:app --reload
```
Wait for: `Uvicorn running on http://127.0.0.1:8000`

**Terminal 2: ngrok**
```powershell
C:\ngrok\ngrok.exe http 8000
```
Copy the HTTPS URL (e.g., `https://abc123.ngrok.io`)

**Terminal 3: Call Script**
```powershell
cd C:\Users\Sowmya\OneDrive\projects\ai_crop_system
.\venv\Scripts\Activate.ps1
python scripts/make_real_call.py
```

### Follow Prompts

1. **Enter webhook URL**: `https://abc123.ngrok.io/voice/advisory`
2. **Confirm call**: `yes`
3. **Answer your phone**: +918095666788 will ring
4. **Listen**: You'll hear Hindi advisory
5. **Optional**: Press 1 to replay

---

## What You'll Hear

**Hindi Audio** (2 minutes):
```
नमस्ते। यह कृषि मित्र है।

आपकी फसल में पानी की कमी के संकेत दिख रहे हैं।
जोखिम स्कोर 75 प्रतिशत है।

तुरंत करने योग्य कार्य:

पहला: अगले 24 घंटे में सिंचाई करें। लागत लगभग 500 रुपये।

दूसरा: 3 दिन में मल्चिंग करें। लागत लगभग 1250 रुपये।

कुल अनुमानित लागत 1750 रुपये है।

कृपया जल्द से जल्द कार्रवाई करें।
धन्यवाद।
```

**English Translation**:
- Hello, this is KrishiMitra
- Your crop shows water shortage signs
- Risk score is 75%
- Action 1: Irrigate within 24 hours (₹500)
- Action 2: Apply mulching within 3 days (₹1250)
- Total cost: ₹1750
- Please take action soon
- Thank you

---

## Troubleshooting

### Problem: ngrok not found

**Error**: `ngrok: command not found`

**Solution**:
```powershell
# Use full path
C:\ngrok\ngrok.exe http 8000
```

### Problem: Server not running

**Error**: `Connection refused`

**Solution**: Start server in Terminal 1
```powershell
uvicorn src.main:app --reload
```

### Problem: Phone not verified

**Error**: Twilio says "Phone number not verified"

**Solution**: 
1. Go to https://console.twilio.com/
2. Phone Numbers > Verified Caller IDs
3. Add +918095666788
4. Verify via SMS

### Problem: No audio on call

**Check**:
- ✓ ngrok is running (Terminal 2)
- ✓ Webhook URL is correct
- ✓ Server shows POST request in logs

**Debug**:
1. Check Terminal 1 for errors
2. Check Terminal 2 for 200 OK
3. Check Twilio Console logs

### Problem: Call fails immediately

**Check Twilio Console**:
1. Go to https://console.twilio.com/
2. Monitor > Logs > Calls
3. Click your call
4. See error details

**Common causes**:
- Insufficient credits
- Phone not verified (trial)
- Webhook URL wrong
- Server not responding

---

## Cost

**Twilio Trial**: $15 free credit
**Per call**: ~₹1.40
**Total calls possible**: ~880

---

## Files Reference

| File | Purpose |
|------|---------|
| `CALL_NOW_QUICKSTART.md` | Detailed step-by-step guide |
| `VOICE_CALL_FLOW.md` | System architecture diagram |
| `MAKE_REAL_CALL_GUIDE.md` | Complete reference guide |
| `SETUP_WEBHOOK_NOW.md` | Webhook setup instructions |
| `scripts/verify_call_setup.py` | Verification script |
| `scripts/make_real_call.py` | Call script |

---

## Next Steps After Success

### 1. Test with Real Farmer Data
```powershell
python scripts/test_real_farmer.py
```
Uses real satellite and weather data

### 2. Test End-to-End Flow
```powershell
python scripts/test_end_to_end.py
```
Complete workflow from data to call

### 3. Customize Advisory Messages

Edit `src/api/voice.py` to change:
- Advisory text
- Language
- Voice settings
- Call flow

### 4. Add More Features

- Multiple advisory types
- Interactive voice response (IVR)
- Voice chatbot integration
- Call scheduling
- Retry logic

### 5. Deploy to Production

See `VOICE_CALL_ALTERNATIVES.md` for:
- AWS Connect (blocked on AISPL)
- Exotel (50% cheaper for India)
- Twilio production setup

---

## Success Checklist

After your first call, verify:

- [ ] Call connected to +918095666788
- [ ] Heard Hindi greeting
- [ ] Heard water stress advisory
- [ ] Heard cost estimates (₹1750)
- [ ] Audio was clear
- [ ] Could press 1 to replay (optional)
- [ ] Call ended cleanly
- [ ] No errors in server logs

All checked? **Congratulations!** 🎉

Your voice calling system is operational!

---

## Quick Commands Reference

```powershell
# Verify setup
python scripts/verify_call_setup.py

# Terminal 1: Start server
uvicorn src.main:app --reload

# Terminal 2: Start ngrok
C:\ngrok\ngrok.exe http 8000

# Terminal 3: Make call
python scripts/make_real_call.py

# Test with real data
python scripts/test_real_farmer.py

# End-to-end test
python scripts/test_end_to_end.py
```

---

## Support

**Need help?**

1. Run verification: `python scripts/verify_call_setup.py`
2. Check server logs (Terminal 1)
3. Check ngrok logs (Terminal 2)
4. Check Twilio Console: https://console.twilio.com/
5. Review detailed guides in repository

**Everything working?**

Time to celebrate! You've built a complete AI-powered voice advisory system for farmers! 🌾📞🎉

---

## Architecture Overview

```
┌─────────────┐
│ Your Script │ Initiates call
└──────┬──────┘
       │
       ▼
┌─────────────┐
│   Twilio    │ Makes phone call
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ Your Phone  │ Rings +918095666788
└──────┬──────┘
       │ Answer
       ▼
┌─────────────┐
│   Twilio    │ Requests instructions
└──────┬──────┘
       │ HTTP POST
       ▼
┌─────────────┐
│    ngrok    │ Public tunnel
└──────┬──────┘
       │ Forward
       ▼
┌─────────────┐
│  FastAPI    │ Generate TwiML
└──────┬──────┘
       │ Return XML
       ▼
┌─────────────┐
│   Twilio    │ Execute TwiML
└──────┬──────┘
       │ Audio stream
       ▼
┌─────────────┐
│ Your Phone  │ Hear advisory
└─────────────┘
```

Simple, elegant, and it works! 🚀
