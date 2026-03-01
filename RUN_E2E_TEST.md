# Run End-to-End Test - Quick Start

## What This Test Does

Simulates a complete farmer workflow:
1. Register farmer with phone number
2. Create 2.5 hectare wheat/rice plot near Pune
3. Analyze satellite data (simulated drought stress)
4. Analyze weather (hot, dry, no rain)
5. AI agent detects anomaly and assesses threat
6. Generate personalized advisory with cost estimates
7. Convert advisory to Hindi voice message
8. Simulate voice call delivery

## Run the Test

### Terminal 1: Start Server
```powershell
.\venv\Scripts\Activate.ps1
uvicorn src.main:app --reload
```

### Terminal 2: Run Test
```powershell
.\venv\Scripts\Activate.ps1
python scripts/test_end_to_end.py
```

## Expected Output

You should see 8 steps complete:

```
======================================================================
  STEP 1: Create Test Farmer
======================================================================
✓ Created farmer: <uuid>
  Phone: +919876543210
  Language: hi

======================================================================
  STEP 2: Create Farm Plot
======================================================================
✓ Created plot: <uuid>
  Location: 18.5204, 73.8567
  Area: 2.5 hectares
  Crops: wheat, rice

======================================================================
  STEP 3: Simulate Satellite Data
======================================================================
✓ Simulated satellite data
  NDVI Mean: 0.450 (stressed)
  Health Status: moderate_vegetation

======================================================================
  STEP 4: Simulate Weather Data
======================================================================
✓ Simulated weather data
  Current Temp: 38.5°C
  Humidity: 25%
  Overall Risk: high
  Drought Risk: high

======================================================================
  STEP 5: Monitoring Agent Analysis
======================================================================
✓ Monitoring agent analysis complete
  Anomaly Detected: True
  Threat Level: high
  Confidence: 85%
  Action: escalate_to_diagnostic

======================================================================
  STEP 6: Generate Advisory
======================================================================
✓ Advisory generated
  Summary: Your crop is showing signs of Water Stress...
  Risk Score: 75/100
  Total Cost: ₹1750
  
  Recommended Actions:
    1. immediate_irrigation (high priority)
       Irrigate the field immediately
       Timeframe: within 24 hours, Cost: ₹500
    
    2. mulching (medium priority)
       Apply organic mulch
       Timeframe: within 3 days, Cost: ₹1250

======================================================================
  STEP 7: Test Voice Services
======================================================================
✓ TTS Provider: PollyTTSProvider
✓ Generated speech audio: 12000 bytes
  Message: नमस्ते किसान भाई। आपकी फसल में पानी की कमी...

======================================================================
  STEP 8: Simulate Voice Call
======================================================================
✓ Voice call simulation
  To: +919876543210
  Language: hi
  Advisory Type: water_stress
  Audio Ready: Yes

======================================================================
  TEST SUMMARY
======================================================================
✓ All steps completed successfully!

Workflow Summary:
  1. Farmer created: +919876543210
  2. Plot registered: <uuid> (2.5 hectares)
  3. Satellite data analyzed: NDVI = 0.45 (stressed)
  4. Weather analyzed: Drought + Heat stress
  5. Monitoring agent: Anomaly detected (high threat)
  6. Advisory generated: 2 actions
  7. Voice services: Ready
  8. Call simulated: Advisory delivered

✓ End-to-end workflow validated!
```

## What Gets Tested

### Real Components (Actually Working):
- ✓ FastAPI REST API
- ✓ Database operations (SQLite)
- ✓ JWT authentication
- ✓ NDVI calculation algorithms
- ✓ Weather risk analysis algorithms
- ✓ AI Monitoring Agent logic
- ✓ AI Advisory Agent logic
- ✓ AWS Polly TTS (Hindi voice)

### Simulated Components (Mock Data):
- Satellite imagery (uses synthetic NDVI)
- Weather API (uses mock values)
- Twilio voice calls (simulated, not actual)

## Troubleshooting

**Error: Server not running**
- Start server in Terminal 1 first

**Error: ModuleNotFoundError**
```powershell
pip install -r requirements-aws.txt
```

**Error: AWS credentials**
- Check .env file has AWS keys
- Verify AWS_REGION is set

**Error: Database locked**
- Close other terminal windows
- Delete krishimitra.db and restart

## Success Criteria

Test passes if:
- All 8 steps complete without errors
- Farmer and plot created in database
- NDVI analysis shows stressed crops
- Weather analysis shows drought risk
- Monitoring agent detects anomaly
- Advisory generated with 2+ actions
- TTS generates Hindi audio
- Call simulation completes

## Time to Complete

Approximately 10-15 seconds

## Next Steps After Test

1. View farmer in database:
   - Open http://127.0.0.1:8000/api/v1/docs
   - Try GET /api/v1/farmers/ endpoint

2. Configure real APIs:
   - Sentinel Hub for satellite data
   - OpenWeatherMap for weather
   - Twilio for voice calls

3. Deploy to production:
   - See AWS_DEPLOYMENT.md

## Questions?

See END_TO_END_TEST_GUIDE.md for detailed explanation of each step.
