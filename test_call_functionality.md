# Testing Voice Call Functionality

## Current Implementation Status

The voice call functionality is **FULLY IMPLEMENTED** in the automated monitoring system. Here's how it works:

### Code Flow

1. **Monitoring Loop** (`auto_monitor_service.py`):
   ```python
   async def _check_farmer(self, farmer: Farmer, db: Session):
       # Calculate risk score
       risk_score = await self._calculate_risk_score(farmer, plots[0], db)
       
       # If risk >= 70%, generate advisory
       if risk_score >= self.risk_threshold:
           advisory_created = await self._generate_advisory(farmer, db)
           
           # If risk >= 80% AND advisory created, make call
           if advisory_created and risk_score >= self.call_threshold:
               await self._make_call(farmer)
   ```

2. **Make Call** (`_make_call` method):
   ```python
   async def _make_call(self, farmer: Farmer):
       # Check calling hours (9 AM - 7 PM)
       can_call = await self.voice_service.check_calling_hours(farmer.timezone)
       
       if not can_call:
           return  # Skip if outside hours
       
       # Initiate Twilio call
       call_result = await self.voice_service.initiate_call(
           to_number=farmer.phone_number,
           callback_url=f"{base_url}/api/v1/voice/advisory",
           farmer_id=str(farmer.farmer_id),
           call_type="advisory"
       )
       
       self.monitoring_stats["calls_made"] += 1
   ```

### Why Calls Might Not Be Made

1. **Risk Score < 80%**: 
   - Current thresholds: Advisory at 70%, Call at 80%
   - If NDVI and weather conditions don't indicate severe stress, risk stays below 80%

2. **Outside Calling Hours**:
   - Only calls between 9 AM - 7 PM in farmer's timezone
   - If you test outside these hours, calls are skipped

3. **Recent Advisory Exists**:
   - If farmer received advisory in last 6 hours, entire check is skipped
   - This prevents duplicate calls

4. **Advisory Generation Failed**:
   - If advisory creation fails, call is not attempted
   - Check backend logs for errors

### How to Test

#### Option 1: Lower the Call Threshold (Temporary)

Modify `src/services/monitoring/auto_monitor_service.py`:

```python
def __init__(self):
    self.call_threshold = 60  # Lower from 80 to 60 for testing
```

Then restart backend and click "Check Now"

#### Option 2: Force High Risk Scenario

Modify `_calculate_risk_score` to return a high value for testing:

```python
async def _calculate_risk_score(self, farmer: Farmer, plot: FarmPlot, db: Session) -> float:
    # FOR TESTING ONLY - Force high risk
    return 85.0  # This will trigger both advisory and call
```

#### Option 3: Manual API Call

Use the existing voice call endpoint directly:

```bash
curl -X POST http://localhost:8000/api/v1/voice/call/{farmer_id}
```

### Verification Steps

1. **Check Backend Logs**:
   ```powershell
   Get-Content backend.log -Tail 50 | Select-String "call|risk"
   ```

2. **Check Monitoring Stats**:
   ```bash
   curl http://localhost:8000/api/v1/monitoring/status
   ```
   Look for `calls_made` counter

3. **Check Twilio Dashboard**:
   - Go to https://console.twilio.com/
   - Check "Calls" section for outbound calls

4. **Check Database**:
   ```sql
   SELECT * FROM call_records ORDER BY created_at DESC LIMIT 5;
   ```

### Expected Behavior

When "Check Now" is clicked:

1. System checks all 3 farmers
2. For each farmer:
   - Fetches NDVI from Sentinel Hub
   - Fetches weather from OpenWeatherMap
   - Calculates risk score (0-100)
   - If risk >= 70%: Creates advisory
   - If risk >= 80% AND within calling hours: Makes call

### Current Risk Calculation

```
Base Risk: 50

NDVI Impact:
- < 0.2: +40 (Severe)
- < 0.3: +30 (High)
- < 0.4: +20 (Moderate)
- < 0.5: +10 (Mild)

Temperature Impact:
- > 35°C: +15
- > 30°C: +10

Humidity Impact:
- < 30%: +10 (Dry)
- > 80%: +5 (Humid)

Maximum: 100
```

### Example Scenarios

**Scenario 1: Healthy Crop**
- NDVI: 0.65 (healthy)
- Temp: 28°C
- Humidity: 50%
- **Risk: 50** → No action

**Scenario 2: Moderate Stress**
- NDVI: 0.35 (moderate stress)
- Temp: 32°C
- Humidity: 28%
- **Risk: 80** → Advisory + Call

**Scenario 3: Severe Stress**
- NDVI: 0.18 (severe stress)
- Temp: 36°C
- Humidity: 25%
- **Risk: 100** → Advisory + Call

### Troubleshooting

**No calls being made?**

1. Check current time - must be 9 AM - 7 PM
2. Check risk scores in logs - must be >= 80
3. Check Twilio credentials in .env
4. Check phone numbers are verified in Twilio
5. Check ngrok URL is correct and accessible

**Calls failing?**

1. Verify Twilio credentials
2. Check phone number format (+91XXXXXXXXXX)
3. Verify phone number in Twilio console
4. Check ngrok tunnel is running
5. Check backend logs for detailed errors

### Quick Test Command

To force a call for testing (bypasses monitoring logic):

```bash
# Get farmer ID
curl http://localhost:8000/api/v1/farmers/ | jq '.[0].farmer_id'

# Make call directly
curl -X POST "http://localhost:8000/api/v1/voice/call/{farmer_id}"
```

This will immediately initiate a call regardless of risk score or recent advisories.
