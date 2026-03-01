# Complete Real Farm Test with Voice Call

## What This Does

Tests KrishiMitra with a REAL farm plot using:
1. **Real satellite data** from Sentinel Hub
2. **Real weather data** from OpenWeatherMap  
3. **AI analysis** of crop health
4. **Advisory generation** based on actual conditions
5. **Voice message** in Hindi
6. **Actual phone call** to your number

## Prerequisites

### 1. API Keys Configured

Make sure `.env` has:
```env
# Satellite
SENTINEL_HUB_CLIENT_ID=your_id
SENTINEL_HUB_CLIENT_SECRET=your_secret

# Weather
OPENWEATHERMAP_API_KEY=your_key

# Twilio
TWILIO_ACCOUNT_SID=AC675ef23df325351b1b8f8a7b6e67635c
TWILIO_AUTH_TOKEN=fadff2426e040d4333c71eac1fa19ed8
TWILIO_PHONE_NUMBER=+17752270557

# AWS
AWS_ACCESS_KEY_ID=your_key
AWS_SECRET_ACCESS_KEY=your_secret
```

### 2. Phone Number Verified

For Twilio trial accounts:
1. Go to: https://console.twilio.com/
2. Navigate to: **Phone Numbers** → **Verified Caller IDs**
3. Add and verify: `+918151910856`

### 3. Update Farm Coordinates

Edit `scripts/test_real_farmer.py` (lines 22-28):

```python
FARMER_PHONE = "+918151910856"  # Your phone
FARMER_LANGUAGE = "hi"  # Hindi
PLOT_LATITUDE = 13.2443  # UPDATE with your farm's latitude
PLOT_LONGITUDE = 77.7122  # UPDATE with your farm's longitude
PLOT_AREA_HECTARES = 2.5  # UPDATE with actual plot size
CROP_TYPES = ["mango"]  # UPDATE with actual crops
```

## Running the Test

### Terminal 1: Start Server

```powershell
cd C:\Users\Sowmya\OneDrive\projects\ai_crop_system
.\venv\Scripts\Activate.ps1
uvicorn src.main:app --reload
```

### Terminal 2: Start ngrok

```powershell
ngrok http 8000
```

Copy the HTTPS URL (e.g., `https://emma-autecologic-gregg.ngrok-free.dev`)

### Terminal 3: Run Test

```powershell
cd C:\Users\Sowmya\OneDrive\projects\ai_crop_system
.\venv\Scripts\Activate.ps1
python scripts/test_real_farmer.py
```

## What Happens

### Step 1: Register Farmer
```
======================================================================
STEP 1: Register Farmer
======================================================================
✓ Using existing farmer
  ID: aa25b281-8515-4be1-a8de-25b244b403b5
  Phone: +918151910856
  Language: hi
```

### Step 2: Fetch Satellite Data
```
======================================================================
STEP 2: Fetch Satellite Data (Sentinel Hub)
======================================================================
  Location: 13.2443, 77.7122
  Bbox: (77.7072, 13.2393, 77.71719999999999, 13.249300000000002)
  Fetching last 7 days of data...
✓ Satellite data fetched successfully
  Data size: 145926 bytes
  Image size: 256x256
  Date range: 2026-02-22 to 2026-03-01

  NDVI Analysis:
    Mean NDVI: 0.550
    Status: Moderate vegetation (may need attention)
```

### Step 3: Fetch Weather Data
```
======================================================================
STEP 3: Fetch Weather Data (OpenWeatherMap)
======================================================================
  Location: 13.2443, 77.7122
  Fetching current weather and forecast...
✓ Weather data fetched successfully

  Current Conditions:
    Temperature: 30.73°C
    Feels like: 29.03°C
    Humidity: 24%
    Wind: 3.69 m/s
    Weather: clear sky

  5-Day Forecast:
    40 data points fetched

  ⚠ Weather Risks Detected:
    - Drought conditions
```

### Step 4: Generate Advisory
```
======================================================================
STEP 4: Generate Advisory
======================================================================
  Analyzing conditions...
    NDVI: 0.550
    Temperature: 30.73°C
    Humidity: 24%

⚠ Advisory needed: general_stress

  Advisory Details:
    Risk Score: 75/100
    Confidence: 85%
    Actions: 3
      1. Monitor soil moisture levels
         Priority: high, Cost: ₹200, Time: 24 hours
      2. Light irrigation if needed
         Priority: medium, Cost: ₹400, Time: 2 days
      3. Apply organic fertilizer
         Priority: low, Cost: ₹800, Time: 1 week
    Total Cost: ₹1400
```

### Step 5: Generate Voice Message
```
======================================================================
STEP 5: Generate Voice Message
======================================================================
  Message created in hi
  Length: 344 characters
  Generating audio with AWS Polly...
✓ Voice message generated
  File: test_advisory_message.mp3
  Size: 192200 bytes
```

### Step 6: Make Voice Call
```
======================================================================
STEP 6: Make Voice Call
======================================================================

📞 Ready to call: +918151910856
  From: +17752270557

⚠ This will make an ACTUAL phone call!
  Make sure:
    1. Server is running (Terminal 1)
    2. ngrok is running (Terminal 2)
    3. Phone number is verified in Twilio

Enter ngrok webhook URL (or press Enter to skip): https://emma-autecologic-gregg.ngrok-free.dev/voice/advisory

Proceed with call? (yes/no): yes

✓ Voice service initialized

📞 Initiating call...

✓ Call initiated successfully!

  Call Details:
    Call SID: CAxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
    To: +918151910856
    From: +17752270557
    Status: queued
    Initiated: 2026-03-01T12:45:30.123456

  🔔 Your phone should ring shortly!
  📱 Answer to hear the Hindi advisory

  Waiting 15 seconds to check call status...

  Call Status Update:
    Status: completed
    Duration: 58 seconds
```

### Summary
```
======================================================================
  TEST COMPLETE
======================================================================

  Data Sources:
    ✓ Real satellite data from Sentinel Hub
    ✓ Real weather data from OpenWeatherMap

  Advisory Summary:
    Type: general_stress
    Risk: 75/100
    Actions: 3
    Total Cost: ₹1400

  Voice Message:
    ✓ Generated: test_advisory_message.mp3

  Voice Call:
    ✓ Call made to: +918151910856
    Call SID: CAxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
    Status: completed

  🎉 Complete end-to-end test finished!
```

## What You'll Hear

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

## Troubleshooting

### Satellite data fails

**Error**: "Failed to fetch satellite data"

**Solutions**:
1. Check Sentinel Hub credentials in `.env`
2. Check processing units quota
3. Script will use simulated data as fallback

### Weather data fails

**Error**: "Failed to fetch weather data"

**Solutions**:
1. Check OpenWeatherMap API key in `.env`
2. Check API rate limits
3. Script will use simulated data as fallback

### Call fails

**Error**: "Failed to make call"

**Solutions**:
1. Verify phone number in Twilio Console
2. Check ngrok is running
3. Check webhook URL is correct
4. Check server is running

## Success Criteria

Test is successful if:
- ✓ Real satellite data fetched (or fallback used)
- ✓ Real weather data fetched (or fallback used)
- ✓ Advisory generated based on actual conditions
- ✓ Voice message created in Hindi
- ✓ Phone call made successfully
- ✓ You hear the advisory on your phone

## Cost

**Per test**:
- Sentinel Hub: ~10 processing units (free tier: 30,000/month)
- OpenWeatherMap: 1 API call (free tier: 1,000/day)
- AWS Polly: ~350 characters (free tier: 5M chars/month)
- Twilio: ~₹1.40 per call (trial: $15 credit)

## Next Steps

After successful test:
1. Test with different farm locations
2. Test with different crop types
3. Set up automated monitoring
4. Deploy to production
5. Add more farmers

---

**This is the complete KrishiMitra workflow!** From real satellite data to a voice call on your phone! 🛰️📞🌾
