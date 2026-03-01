# Quick Start: End-to-End Test with Voice Call

## Pre-Flight Checklist

### ✅ Step 1: Verify Phone Number in Twilio (CRITICAL!)

**You MUST do this first for trial accounts!**

1. Go to: https://console.twilio.com/us1/develop/phone-numbers/manage/verified
2. Click "Add a new number"
3. Enter: `+918151910856`
4. Complete verification (SMS or voice)
5. ✅ Confirm verification successful

### ✅ Step 2: Update Farm Coordinates

Edit `scripts/test_real_farmer.py` lines 22-28:

```python
PLOT_LATITUDE = 13.2443   # Your farm latitude
PLOT_LONGITUDE = 77.7122  # Your farm longitude
```

**Get coordinates**: https://www.google.com/maps (right-click on location)

### ✅ Step 3: Verify Configuration

Check `.env` file has:
```
TWILIO_PHONE_NUMBER=+17752270557
TWILIO_ACCOUNT_SID=AC675ef23df325351b1b8f8a7b6e67635c
TWILIO_AUTH_TOKEN=fadff2426e040d4333c71eac1fa19ed8
```

## Run the Test (3 Terminals)

### Terminal 1: Server
```bash
cd C:\Users\Sowmya\OneDrive\projects\ai_crop_system
.\venv\Scripts\activate
uvicorn src.main:app --reload
```
✅ Wait for: "Application startup complete."

### Terminal 2: ngrok
```bash
cd "C:\Program Files\ngrok"
ngrok http 8000
```
✅ Copy the HTTPS URL (e.g., `https://emma-autecologic-gregg.ngrok-free.dev`)

### Terminal 3: Test Script
```bash
cd C:\Users\Sowmya\OneDrive\projects\ai_crop_system
.\venv\Scripts\activate
python scripts/test_real_farmer.py
```

## During the Test

1. **Press Enter** when prompted to start
2. **Watch the progress** through 6 steps
3. **When prompted for webhook URL**, paste your ngrok URL:
   ```
   https://your-ngrok-url.ngrok-free.dev/voice/advisory
   ```
4. **Type `yes`** to confirm the call
5. **Answer your phone** when it rings
6. **Listen to the Hindi advisory**

## What You'll See

```
======================================================================
STEP 1: Register Farmer
======================================================================
✓ Farmer registered

======================================================================
STEP 2: Fetch Satellite Data (Sentinel Hub)
======================================================================
✓ Satellite data fetched successfully
  NDVI Analysis: Mean NDVI: 0.550

======================================================================
STEP 3: Fetch Weather Data (OpenWeatherMap)
======================================================================
✓ Weather data fetched successfully
  Temperature: 38.5°C, Humidity: 25%

======================================================================
STEP 4: Generate Advisory
======================================================================
⚠ Advisory needed: water_stress
  Actions: 2, Total Cost: ₹1750

======================================================================
STEP 5: Generate Voice Message
======================================================================
✓ Voice message generated
  File: test_advisory_message.mp3

======================================================================
STEP 6: Make Voice Call
======================================================================
📞 Ready to call: +918151910856

Enter ngrok webhook URL: [PASTE YOUR URL HERE]
Proceed with call? (yes/no): yes

✓ Call initiated successfully!
🔔 Your phone should ring shortly!
```

## Success Criteria

✅ All 6 steps complete without errors
✅ Phone rings within 10 seconds
✅ Hindi message plays clearly
✅ Advisory mentions specific actions and costs
✅ Call completes successfully

## Quick Troubleshooting

### Phone doesn't ring?
- ✅ Verified phone number in Twilio?
- ✅ ngrok URL correct?
- ✅ Server running?

### Call fails with error 21212?
- ✅ Using Twilio number as "from" (+17752270557)?
- ✅ Not using personal number as "from"?

### Satellite data fails?
- ✅ Sentinel Hub credentials in .env?
- ✅ Processing units available?
- Test continues with simulated data

### Weather data fails?
- ✅ OpenWeatherMap API key in .env?
- ✅ Within rate limits?
- Test continues with simulated data

## Need Help?

See detailed guide: `RUN_END_TO_END_WITH_CALL.md`

Test individual components:
```bash
python scripts/test_sentinel.py
python scripts/test_api_keys.py
python scripts/make_real_call.py
```

---

**Ready?** Complete the checklist above and run the test! 🚀
