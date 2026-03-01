# Complete End-to-End Test with Voice Call

## What This Does

Tests the entire KrishiMitra workflow from data collection to actual voice call:
1. Data collection (simulated satellite + weather)
2. AI analysis (monitoring + advisory agents)
3. Advisory generation
4. Voice message creation
5. **Real Twilio voice call to your phone**

## Prerequisites

### 1. Verify Your Phone Number in Twilio

**Important**: For trial accounts, you must verify your destination number first!

1. Go to: https://console.twilio.com/
2. Navigate to: **Phone Numbers** → **Verified Caller IDs**
3. Click **"+"** to add a new number
4. Enter: `+918151910856`
5. Click **"Verify"**
6. Enter the SMS code you receive

### 2. Check Your Configuration

Make sure `.env` has:
```env
TWILIO_ACCOUNT_SID=AC675ef23df325351b1b8f8a7b6e67635c
TWILIO_AUTH_TOKEN=fadff2426e040d4333c71eac1fa19ed8
TWILIO_PHONE_NUMBER=+17752270557
```

## Running the Test

### Terminal 1: Start Server

```powershell
cd C:\Users\Sowmya\OneDrive\projects\ai_crop_system
.\venv\Scripts\Activate.ps1
uvicorn src.main:app --reload
```

Wait for: `Uvicorn running on http://127.0.0.1:8000`

### Terminal 2: Start ngrok

```powershell
ngrok http 8000
```

Copy the HTTPS URL (e.g., `https://emma-autecologic-gregg.ngrok-free.dev`)

### Terminal 3: Run Test

```powershell
cd C:\Users\Sowmya\OneDrive\projects\ai_crop_system
.\venv\Scripts\Activate.ps1
python scripts/test_complete_with_call.py
```

## What You'll See

```
======================================================================
  KrishiMitra - Complete End-to-End Test with Voice Call
======================================================================

📱 Farmer Phone: +918151910856
🌍 Language: Hindi (hi)

======================================================================
  STEP 1: Checking Prerequisites
======================================================================

✓ Twilio Account SID: AC675ef23d...
✓ Twilio Phone Number: +17752270557

⚠ Important: Make sure ngrok is running!
  Terminal 2 should show: ngrok http 8000

Enter your ngrok webhook URL: https://emma-autecologic-gregg.ngrok-free.dev/voice/advisory

✓ Webhook URL: https://emma-autecologic-gregg.ngrok-free.dev/voice/advisory

======================================================================
  STEP 2: Simulating Data Collection
======================================================================

📡 Satellite Data (Simulated):
  NDVI: 0.45 (Stressed vegetation)
  Status: ⚠ Crop stress detected

🌤️  Weather Data (Simulated):
  Temperature: 35.5°C
  Humidity: 25%
  Conditions: ⚠ Hot and dry - drought risk

======================================================================
  STEP 3: AI Analysis
======================================================================

🤖 Monitoring Agent:
  Anomaly detected: YES
  Confidence: 85%
  Issue: Water stress + heat stress

🤖 Advisory Agent:
  Advisory Type: water_stress
  Risk Score: 75/100

======================================================================
  STEP 4: Generating Advisory
======================================================================

✓ Advisory Generated:
  Actions: 2
  Total Cost: ₹1750

  Action 1: immediate_irrigation
    Description: अगले 24 घंटे में सिंचाई करें
    Priority: high
    Cost: ₹500
    Timeframe: 24 hours

  Action 2: mulching
    Description: 3 दिन में मल्चिंग करें
    Priority: medium
    Cost: ₹1250
    Timeframe: 3 days

======================================================================
  STEP 5: Generating Voice Message
======================================================================

✓ Message created in Hindi
  Length: 344 characters

======================================================================
  STEP 6: Making Voice Call
======================================================================

📞 Preparing to call: +918151910856
  From: +17752270557
  Webhook: https://emma-autecologic-gregg.ngrok-free.dev/voice/advisory

⚠ This will make an ACTUAL phone call!

Proceed with call? (yes/no): yes

✓ Voice service initialized

📞 Initiating call...

✓ Call initiated successfully!

  Call Details:
    Call SID: CAxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
    To: +918151910856
    From: +17752270557
    Status: queued
    Initiated: 2026-03-01T12:30:45.123456

  🔔 Your phone should ring shortly!
  📱 Answer to hear the Hindi advisory

  Waiting 15 seconds to check call status...

  Call Status Update:
    Status: completed
    Duration: 58 seconds

======================================================================
  TEST COMPLETE
======================================================================

✓ All steps completed successfully!

  Workflow Summary:
    1. ✓ Prerequisites checked
    2. ✓ Data collected (simulated)
    3. ✓ AI analysis performed
    4. ✓ Advisory generated
    5. ✓ Voice message created
    6. ✓ Voice call initiated

  Call Details:
    Farmer: +918151910856
    Language: Hindi
    Advisory: Water stress
    Actions: 2
    Cost: ₹1750

  🎉 KrishiMitra end-to-end test successful!
```

## What You'll Hear on the Call

When you answer your phone, you'll hear (in Hindi):

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

## Troubleshooting

### Phone doesn't ring

**Check**:
1. Phone number verified in Twilio Console?
2. ngrok running and URL correct?
3. Server running on port 8000?

### Call connects but no audio

**Check**:
1. Webhook URL includes `/voice/advisory`?
2. Server logs show POST request?
3. ngrok shows 200 OK response?

### Error: Phone not verified

**Solution**: Verify `+918151910856` in Twilio Console (see Prerequisites above)

## Success Criteria

Test is successful if:
- ✓ All 6 steps complete without errors
- ✓ Your phone rings within 10 seconds
- ✓ You hear clear Hindi audio
- ✓ Advisory message is complete
- ✓ Call status shows "completed"

## Cost

**Per test**: ~₹1.40 (using Twilio trial credit)

## Next Steps

After successful test:
1. Test with real satellite data: `python scripts/test_real_farmer.py`
2. Deploy to production
3. Set up call scheduling
4. Add more advisory types

---

**Ready to test?** Make sure all 3 terminals are running, then run the script!
