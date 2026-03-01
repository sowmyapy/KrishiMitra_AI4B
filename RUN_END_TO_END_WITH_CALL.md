# Complete End-to-End Test with Voice Call

## What This Test Does

This is the COMPLETE KrishiMitra workflow test:
1. ✅ Register farmer in database
2. 🛰️ Fetch REAL satellite data from Sentinel Hub
3. 🌤️ Fetch REAL weather data from OpenWeatherMap
4. 🤖 AI analysis to detect crop stress
5. 📋 Generate actionable advisory with cost estimates
6. 🔊 Generate Hindi voice message using AWS Polly
7. 📞 Make ACTUAL phone call using Twilio

## Prerequisites

### 1. Verify Phone Number in Twilio

**CRITICAL**: For Twilio trial accounts, you MUST verify the destination number first!

1. Go to: https://console.twilio.com/us1/develop/phone-numbers/manage/verified
2. Click "Add a new number"
3. Enter: `+918151910856`
4. Verify via SMS or voice call
5. Wait for verification to complete

### 2. Update Farm Coordinates

Edit `scripts/test_real_farmer.py` (lines 22-28):

```python
PLOT_LATITUDE = 13.2443   # UPDATE with your actual farm latitude
PLOT_LONGITUDE = 77.7122  # UPDATE with your actual farm longitude
PLOT_AREA_HECTARES = 2.5  # UPDATE with actual plot size
CROP_TYPES = ["ragi", "mango"]  # UPDATE with actual crops
```

### 3. Check API Keys

Verify these are set in `.env`:
- ✅ `SENTINEL_HUB_CLIENT_ID` and `SENTINEL_HUB_CLIENT_SECRET`
- ✅ `OPENWEATHERMAP_API_KEY`
- ✅ `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY`
- ✅ `TWILIO_ACCOUNT_SID` and `TWILIO_AUTH_TOKEN`
- ✅ `TWILIO_PHONE_NUMBER=+17752270557`

## Running the Test

### Terminal 1: Start Server

```bash
cd C:\Users\Sowmya\OneDrive\projects\ai_crop_system
.\venv\Scripts\activate
uvicorn src.main:app --reload
```

Wait for: `Application startup complete.`

### Terminal 2: Start ngrok

```bash
cd "C:\Program Files\ngrok"
ngrok http 8000
```

Copy the HTTPS URL (e.g., `https://emma-autecologic-gregg.ngrok-free.dev`)

### Terminal 3: Run Test

```bash
cd C:\Users\Sowmya\OneDrive\projects\ai_crop_system
.\venv\Scripts\activate
python scripts/test_real_farmer.py
```

## What Happens During the Test

### Step 1: Register Farmer
```
✓ Farmer registered
  ID: 1
  Phone: +918151910856
  Language: hi
```

### Step 2: Fetch Satellite Data
```
✓ Satellite data fetched successfully
  Data size: 196608 bytes
  Image size: 256x256
  NDVI Analysis:
    Mean NDVI: 0.550
    Status: Moderate vegetation (may need attention)
```

### Step 3: Fetch Weather Data
```
✓ Weather data fetched successfully
  Current Conditions:
    Temperature: 38.5°C
    Humidity: 25%
    Wind: 15 m/s
  ⚠ Weather Risks Detected:
    - Heat stress
    - Drought conditions
```

### Step 4: Generate Advisory
```
⚠ Advisory needed: water_stress
  Risk Score: 75/100
  Confidence: 85%
  Actions:
    1. Immediate irrigation
       Priority: high, Cost: ₹500, Time: 24 hours
    2. Apply mulch to retain moisture
       Priority: medium, Cost: ₹1250, Time: 3 days
  Total Cost: ₹1750
```

### Step 5: Generate Voice Message
```
✓ Voice message generated
  File: test_advisory_message.mp3
  Size: 45678 bytes
```

### Step 6: Make Voice Call

The script will prompt you:

```
📞 Ready to call: +918151910856
  From: +17752270557

⚠ This will make an ACTUAL phone call!
  Make sure:
    1. Server is running (Terminal 1)
    2. ngrok is running (Terminal 2)
    3. Phone number is verified in Twilio

Enter ngrok webhook URL (or press Enter to skip):
```

**Enter your ngrok URL**: `https://emma-autecologic-gregg.ngrok-free.dev/voice/advisory`

```
Proceed with call? (yes/no):
```

**Type**: `yes`

```
✓ Call initiated successfully!

  Call Details:
    Call SID: CA1234567890abcdef
    To: +918151910856
    From: +17752270557
    Status: queued
    Initiated: 2025-03-01 12:30:45

  🔔 Your phone should ring shortly!
  📱 Answer to hear the Hindi advisory

  Waiting 15 seconds to check call status...

  Call Status Update:
    Status: completed
    Duration: 45 seconds
```

## Expected Results

### Success Indicators

✅ **Farmer registered** - Database entry created
✅ **Real satellite data** - Fetched from Sentinel Hub
✅ **Real weather data** - Fetched from OpenWeatherMap
✅ **Advisory generated** - AI analysis complete
✅ **Voice message created** - MP3 file generated
✅ **Call initiated** - Twilio call started
✅ **Phone rings** - You receive the call
✅ **Hindi message plays** - Advisory delivered in Hindi

### What You'll Hear

When you answer the call, you'll hear (in Hindi):

```
नमस्ते किसान भाई,

यह कृषि मित्र से एक महत्वपूर्ण सलाह है।

हमारे उपग्रह विश्लेषण से पता चला है कि आपकी फसल में पानी की कमी है।

तुरंत करें:
1. अगले 24 घंटों में सिंचाई करें - खर्च लगभग 500 रुपये
2. 3 दिनों में मल्चिंग करें - खर्च लगभग 1250 रुपये

कुल अनुमानित खर्च: 1750 रुपये

अधिक जानकारी के लिए हमें कॉल करें।
धन्यवाद।
```

Translation:
```
Hello farmer brother,

This is an important advisory from KrishiMitra.

Our satellite analysis has detected water stress in your crops.

Take immediate action:
1. Irrigate within 24 hours - cost approximately ₹500
2. Apply mulching within 3 days - cost approximately ₹1250

Total estimated cost: ₹1750

Call us for more information.
Thank you.
```

## Troubleshooting

### Phone Doesn't Ring

**Check**:
1. Phone number verified in Twilio Console
2. Twilio account has credits (trial accounts get $15)
3. ngrok URL is correct and accessible
4. Server is running and responding

**Test webhook manually**:
```bash
curl https://your-ngrok-url.ngrok-free.dev/voice/advisory
```

Should return TwiML XML.

### Call Fails with Error 21212

**Error**: "From number must be valid and not on DNO list"

**Solution**: You're using a personal number as "from". Must use Twilio number:
- Check `.env`: `TWILIO_PHONE_NUMBER=+17752270557`
- This is your Twilio trial number

### Satellite Data Fails

**Error**: "Failed to fetch satellite data"

**Solutions**:
1. Check Sentinel Hub credentials in `.env`
2. Verify processing units quota: https://apps.sentinel-hub.com/dashboard/#/account/settings
3. Try different coordinates (some areas may have no recent data)
4. Test will continue with simulated data

### Weather Data Fails

**Error**: "Failed to fetch weather data"

**Solutions**:
1. Check OpenWeatherMap API key in `.env`
2. Verify API key is active: https://home.openweathermap.org/api_keys
3. Check rate limits (60 calls/minute for free tier)
4. Test will continue with simulated data

### Voice Generation Fails

**Error**: "Failed to generate voice"

**Solutions**:
1. Check AWS credentials in `.env`
2. Verify AWS Polly is enabled in your region
3. Check IAM permissions for Polly
4. Test will continue but call won't be made

## Cost Breakdown

### Per Test Run

- **Sentinel Hub**: ~1 processing unit (~$0.01)
- **OpenWeatherMap**: Free (within 60 calls/min limit)
- **AWS Polly**: ~$0.004 per request
- **Twilio Call**: ~$0.02 per minute (trial credits available)

**Total per test**: ~$0.03 (₹2.50)

### Trial Credits

- **Twilio**: $15 free credit = ~750 test calls
- **Sentinel Hub**: 30,000 free processing units/month
- **OpenWeatherMap**: 1,000 free calls/day
- **AWS Polly**: 5 million characters free/month (first year)

## Next Steps

After successful test:

1. **Review call logs**: https://console.twilio.com/us1/monitor/logs/calls
2. **Check audio file**: `test_advisory_message.mp3`
3. **Verify database**: Farmer and advisory records created
4. **Test with different coordinates**: Try various farm locations
5. **Test different stress conditions**: Modify coordinates to get different NDVI values

## Production Deployment

For production use:

1. **Upgrade Twilio account** - Remove trial restrictions
2. **Add more phone numbers** - No verification needed
3. **Set up proper webhook domain** - Replace ngrok with permanent domain
4. **Configure auto-scaling** - Handle multiple concurrent calls
5. **Add monitoring** - Track call success rates and costs

## Support

If you encounter issues:

1. Check all three terminals for error messages
2. Review Twilio call logs
3. Test each component individually:
   - `python scripts/test_sentinel.py`
   - `python scripts/test_api_keys.py`
   - `python scripts/make_real_call.py`
4. Verify all API keys are active and have quota

---

**Ready to test?** Follow the steps above and experience the complete KrishiMitra workflow! 🚀
