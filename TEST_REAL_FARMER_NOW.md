# Test Real Farmer - Quick Start

All API keys configured! Let's test with a real farmer plot.

## Quick Test (5 minutes)

### Step 1: Update Farmer Details

Edit `scripts/test_real_farmer.py` (lines 20-27):

```python
FARMER_PHONE = "+918095666788"  # Your number
FARMER_LANGUAGE = "hi"  # Hindi
PLOT_LATITUDE = 18.5204  # UPDATE: Real plot latitude
PLOT_LONGITUDE = 73.8567  # UPDATE: Real plot longitude
PLOT_AREA_HECTARES = 2.5  # UPDATE: Real area
CROP_TYPES = ["wheat"]  # UPDATE: Real crops
PLANTING_DATE = "2024-11-01"  # UPDATE: Real date
```

### Step 2: Start Server

```powershell
# Terminal 1
.\venv\Scripts\Activate.ps1
uvicorn src.main:app --reload
```

### Step 3: Run Test

```powershell
# Terminal 2
.\venv\Scripts\Activate.ps1
python scripts/test_real_farmer.py
```

## What It Does

1. **Registers farmer** in database
2. **Fetches satellite data** from Sentinel Hub (real NDVI)
3. **Fetches weather data** from OpenWeatherMap (real conditions)
4. **Analyzes crop health** using AI
5. **Generates advisory** if needed
6. **Creates voice message** in Hindi using AWS Polly

## Expected Output

```
======================================================================
  KrishiMitra - Real Farmer Plot Testing
======================================================================

  Configuration:
    Farmer: +918095666788
    Location: 18.5204, 73.8567
    Area: 2.5 hectares
    Crops: wheat
    Language: hi

======================================================================
STEP 1: Register Farmer
======================================================================
✓ Farmer registered
  ID: abc-123-def
  Phone: +918095666788
  Language: hi

======================================================================
STEP 2: Fetch Satellite Data (Sentinel Hub)
======================================================================
  Location: 18.5204, 73.8567
  Bbox: (73.8617, 18.5154, 73.8717, 18.5254)
  Fetching last 7 days of data...
✓ Satellite data fetched successfully
  Data size: 3145728 bytes
  Image size: 256x256
  Date range: 2026-02-22 to 2026-03-01

  NDVI Analysis:
    Mean NDVI: 0.550
    Status: Moderate vegetation (may need attention)

======================================================================
STEP 3: Fetch Weather Data (OpenWeatherMap)
======================================================================
  Location: 18.5204, 73.8567
  Fetching current weather and forecast...
✓ Weather data fetched successfully

  Current Conditions:
    Temperature: 32.5°C
    Feels like: 34.2°C
    Humidity: 45%
    Wind: 3.5 m/s
    Weather: clear sky

  5-Day Forecast:
    40 data points fetched

  ✓ No immediate weather risks

======================================================================
STEP 4: Generate Advisory
======================================================================
  Analyzing conditions...
    NDVI: 0.550
    Temperature: 32.5°C
    Humidity: 45%

✓ Crops are healthy - no advisory needed

======================================================================
  TEST COMPLETE
======================================================================

  Data Sources:
    ✓ Real satellite data from Sentinel Hub
    ✓ Real weather data from OpenWeatherMap

  ✓ Crops are healthy - no advisory needed
```

## If Advisory Is Needed

When crops need attention, you'll see:

```
======================================================================
STEP 4: Generate Advisory
======================================================================
  Analyzing conditions...
    NDVI: 0.450
    Temperature: 38.5°C
    Humidity: 25%

⚠ Advisory needed: water_stress

  Advisory Details:
    Risk Score: 75/100
    Confidence: 85%
    Actions: 2
      1. Immediate irrigation
         Priority: high, Cost: ₹500, Time: 24 hours
      2. Apply mulch to retain moisture
         Priority: medium, Cost: ₹1250, Time: 3 days
    Total Cost: ₹1750

======================================================================
STEP 5: Generate Voice Message
======================================================================
  Message created in hi
  Length: 245 characters
  Generating audio with AWS Polly...
✓ Voice message generated
  File: test_advisory_message.mp3
  Size: 45678 bytes

======================================================================
  TEST COMPLETE
======================================================================

  Data Sources:
    ✓ Real satellite data from Sentinel Hub
    ✓ Real weather data from OpenWeatherMap

  Advisory Summary:
    Type: water_stress
    Risk: 75/100
    Actions: 2
    Total Cost: ₹1750

  Voice Message:
    ✓ Generated: test_advisory_message.mp3

  Next Steps:
    1. Listen to: test_advisory_message.mp3
    2. Make real call: python scripts/make_real_call.py
```

## Troubleshooting

### Sentinel Hub Fails

If you see:
```
✗ Failed to fetch satellite data: HTTPStatusError
  Using simulated data for testing...
```

**Check:**
1. Credentials in `.env` are correct (not placeholders)
2. Processing units quota: https://apps.sentinel-hub.com/dashboard/
3. Account is activated (wait 5-10 minutes after signup)

**Test separately:**
```powershell
python scripts/test_sentinel.py
```

### OpenWeatherMap Fails

If you see:
```
✗ Failed to fetch weather data: HTTPStatusError
  Using simulated data for testing...
```

**Check:**
1. API key in `.env` is correct
2. Rate limits (60 calls/minute for free tier)
3. API key is activated

### Server Not Running

If you see:
```
Connection refused
```

**Solution:**
Start the server in another terminal:
```powershell
uvicorn src.main:app --reload
```

## Get Real Plot Coordinates

### Method 1: Google Maps

1. Open https://maps.google.com/
2. Find the farm location
3. Right-click on the plot center
4. Click the coordinates to copy
5. Format: `18.5204, 73.8567`

### Method 2: GPS App

1. Use any GPS app on your phone
2. Stand at the plot center
3. Note the coordinates
4. Use decimal degrees format

### Method 3: Survey Number

1. Get survey number from farmer
2. Look up in land records
3. Use government portals (varies by state)

## Next Steps

After successful test:

1. **Listen to voice message**: `test_advisory_message.mp3`
2. **Make real call**: See `MAKE_REAL_CALL_GUIDE.md`
3. **Test with multiple plots**: Update coordinates and run again
4. **Deploy to production**: See `AWS_DEPLOYMENT.md`

## Production Use

For daily monitoring:

1. Set up automated satellite data fetching
2. Configure weather data polling
3. Enable automatic advisory generation
4. Schedule voice calls
5. Collect farmer feedback

See `REAL_FARMER_TESTING.md` for detailed production setup.

## Support

Need help?
- Check `REAL_FARMER_TESTING.md` for detailed guide
- Review `TROUBLESHOOTING.md`
- Test individual components separately
- Check logs in terminal

Good luck! 🌾
