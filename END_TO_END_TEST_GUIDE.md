# End-to-End Integration Test Guide

## Overview

This test simulates the complete KrishiMitra workflow from farmer registration to advisory delivery via voice call.

## Workflow Steps

```
Farmer Registration
        ↓
Farm Plot Creation
        ↓
Satellite Data Collection (NDVI)
        ↓
Weather Data Analysis
        ↓
Monitoring Agent (Anomaly Detection)
        ↓
Diagnostic Agent (Root Cause)
        ↓
Advisory Agent (Personalized Recommendations)
        ↓
Voice Call Service (TTS + Twilio)
        ↓
Farmer Receives Advisory
```

## Running the Test

### Prerequisites

1. **Server Running**:
   ```powershell
   .\venv\Scripts\Activate.ps1
   uvicorn src.main:app --reload
   ```

2. **AWS Services Configured** (for voice):
   - AWS Polly (TTS)
   - AWS Transcribe (STT)

### Run the Test

In a new PowerShell window:
```powershell
.\venv\Scripts\Activate.ps1
python scripts/test_end_to_end.py
```

## What the Test Does

### Step 1: Create Test Farmer
- Creates farmer with phone number +919876543210
- Sets language preference to Hindi
- Timezone: Asia/Kolkata

### Step 2: Create Farm Plot
- Location: Near Pune, Maharashtra (18.5204°N, 73.8567°E)
- Area: 2.5 hectares
- Crops: Wheat and Rice
- Planting date: 60 days ago
- Expected harvest: 30 days from now

### Step 3: Simulate Satellite Data
- Generates synthetic NDVI data (100x100 pixels)
- Simulates stressed crops: NDVI = 0.45 (normal is 0.6-0.8)
- Calculates vegetation indices
- Interprets crop health status

**Sample Output**:
```
NDVI Mean: 0.450 (stressed)
Health Status: moderate_vegetation
Description: Moderate vegetation health
```

### Step 4: Simulate Weather Data
- Current conditions: 38.5°C, 25% humidity (hot and dry)
- 7-day forecast: No rain expected
- 30-day history: No recent rainfall
- Risk analysis: Drought + Heat stress

**Sample Output**:
```
Overall Risk: high
Heat Stress: medium
Drought Risk: high
7-day Rainfall: 0 mm
```

### Step 5: Monitoring Agent Analysis
- Detects NDVI anomaly (current: 0.45 vs historical: 0.65)
- Investigates weather factors
- Assesses threat level
- Makes decision to escalate

**Sample Output**:
```
Anomaly Detected: True
Threat Level: high
Confidence: 85%
Action: escalate_to_diagnostic
Priority: high
```

### Step 6: Generate Advisory
- Diagnoses water stress (drought + low NDVI)
- Generates personalized actions
- Considers farmer's budget (₹2000)
- Provides cost estimates

**Sample Output**:
```
Summary: Your crop is showing signs of Water Stress with risk score 75/100
Actions:
  1. immediate_irrigation (high priority)
     Irrigate the field immediately to restore soil moisture
     Timeframe: within 24 hours, Cost: ₹500
  
  2. mulching (medium priority)
     Apply organic mulch to conserve soil moisture
     Timeframe: within 3 days, Cost: ₹1250

Total Cost: ₹1750
```

### Step 7: Test Voice Services
- Generates Hindi voice message using AWS Polly
- Message includes:
  - Greeting
  - Alert about water stress
  - Risk score
  - Immediate action needed

**Sample Output**:
```
TTS Provider: PollyTTSProvider
Generated speech audio: 12,000 bytes
Message: नमस्ते किसान भाई। आपकी फसल में पानी की कमी के संकेत दिख रहे हैं...
```

### Step 8: Simulate Voice Call
- Simulates Twilio call (doesn't actually call)
- Shows call script
- Logs call record

**Sample Output**:
```
To: +919876543210
Language: hi
Advisory Type: water_stress
Priority: High
Audio Ready: Yes (12,000 bytes)

Call Script:
  1. Greeting in Hindi
  2. Alert about water stress (risk: 75/100)
  3. Recommend immediate irrigation
  4. Provide cost estimate: ₹1750
  5. Ask for confirmation
```

## Test Scenarios

The test simulates a realistic scenario:

**Scenario: Drought-Stressed Wheat Field**
- **Problem**: No rain for 30 days, high temperatures
- **Symptoms**: Low NDVI (0.45), low soil moisture
- **Diagnosis**: Water stress with 75/100 risk score
- **Solution**: Immediate irrigation + mulching
- **Cost**: ₹1750 for 2.5 hectares
- **Delivery**: Voice call in Hindi

## Expected Results

All 8 steps should complete successfully:
- ✓ Farmer created
- ✓ Plot registered
- ✓ Satellite data analyzed
- ✓ Weather analyzed
- ✓ Monitoring agent detected anomaly
- ✓ Advisory generated
- ✓ Voice services ready
- ✓ Call simulated

## What's Simulated vs Real

### Simulated (for testing):
- Satellite data (uses synthetic NDVI values)
- Weather data (uses mock values)
- Voice call (doesn't actually call Twilio)
- Diagnostic agent (simplified logic)

### Real (actually working):
- Database operations (farmer, plot creation)
- NDVI calculations (real algorithms)
- Weather risk analysis (real algorithms)
- Monitoring agent logic (real AI agent)
- Advisory agent logic (real AI agent)
- TTS generation (real AWS Polly)
- JWT authentication

## Production Deployment

To make this work in production:

1. **Real Data Sources**:
   - Sentinel Hub API for satellite data
   - OpenWeatherMap API for weather
   - Historical data for baselines

2. **Real Voice Calls**:
   - Twilio account with credits
   - Phone number verification
   - Call recording and logging

3. **Real LLM**:
   - AWS Bedrock (currently rate-limited)
   - Or OpenAI GPT-4

4. **Supporting Services**:
   - Redis for caching
   - Kafka for message queue
   - ChromaDB for knowledge base

## Troubleshooting

**Server not running**:
```powershell
uvicorn src.main:app --reload
```

**Import errors**:
```powershell
pip install -r requirements-aws.txt
```

**AWS Polly errors**:
- Check AWS credentials in .env
- Verify AWS region is correct
- Check AWS Polly quota

**Database errors**:
- Delete krishimitra.db and restart server

## Next Steps

After successful test:
1. Configure real API keys
2. Set up Twilio account
3. Deploy to AWS
4. Test with real farmers
5. Monitor and optimize

## Cost Estimate

For 1000 farmers with daily monitoring:
- Satellite data: $50/month
- Weather API: $20/month
- AWS Polly: $16/month (4 calls/farmer/month)
- AWS Transcribe: $24/month
- AWS Bedrock: $30/month
- Twilio calls: $40/month (4 calls/farmer/month)

**Total: ~$180/month = $0.18/farmer/month**

Well within the target of <$1/farmer/month!
