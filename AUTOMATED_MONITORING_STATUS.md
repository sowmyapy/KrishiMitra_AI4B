# Automated Monitoring System - Current Status

## ✅ What's Working

1. **Monitoring Service**: Running and checking farmers
2. **Risk Calculation**: Using real NDVI + weather data
3. **Advisory Generation**: Creating advisories when risk ≥ 70%
4. **Voice Call API**: Can initiate calls via `/voice/call/{farmer_id}`
5. **Calling Hours Restriction**: REMOVED (calls anytime now)

## ⚠️ Current Issues

### Issue 1: "Check Now" Not Making Calls

**Reason**: Farmers already have recent advisories (within 6 hours)

**Solution**: The system has a 6-hour cooldown to prevent annoying farmers. To test:

**Option A - Delete Recent Advisories**:
```sql
DELETE FROM advisories WHERE created_at > datetime('now', '-6 hours');
```

**Option B - Lower Call Threshold** (ALREADY DONE):
Changed from 80% to 60% in `auto_monitor_service.py` line 27

**Option C - Restart Backend** (REQUIRED):
The code changes need a backend restart to take effect.

### Issue 2: Voice Call Has No Message

**Reason**: Twilio webhook not receiving/finding the advisory

**Possible Causes**:
1. Ngrok URL mismatch
2. Phone number format mismatch
3. Advisory not found in database

**Solution**: Enhanced webhook logging (ALREADY DONE in `voice.py`)

## 🔧 Required Actions

### 1. Restart Backend (CRITICAL)

```powershell
.\restart_all_clean.ps1
```

This will apply:
- Lowered call threshold (60% instead of 80%)
- Removed calling hours restriction
- Enhanced webhook logging

### 2. Clear Old Advisories (Optional)

To force new advisory generation:

```bash
# Via API (if endpoint exists)
curl -X DELETE http://localhost:8000/api/v1/advisories/clear-old

# Or via database
sqlite3 krishimitra.db "DELETE FROM advisories WHERE created_at < datetime('now', '-1 hour');"
```

### 3. Test Call Flow

**Step 1: Generate Fresh Advisory**
```bash
curl -X POST http://localhost:8000/api/v1/advisories/generate/fc008579-7fcb-4f31-8ab8-837ef8d44f83
```

**Step 2: Make Call**
```bash
curl -X POST http://localhost:8000/api/v1/voice/call/fc008579-7fcb-4f31-8ab8-837ef8d44f83
```

**Step 3: Check Backend Logs**
```powershell
Get-Content backend.log -Tail 50 | Select-String "webhook|advisory"
```

### 4. Test Automated Monitoring

**Step 1: Click "Check Now"** on monitoring page

**Step 2: Check Stats**
- Should show calls_made > 0 if risk ≥ 60%

**Step 3: Check Logs**
```powershell
Get-Content backend.log -Tail 100 | Select-String "risk score|call initiated"
```

## 📊 Current Configuration

```python
# auto_monitor_service.py
check_interval = 3600  # 1 hour
risk_threshold = 70    # Generate advisory
call_threshold = 60    # Make call (LOWERED FOR TESTING)
cooldown_period = 6    # Hours between advisories
```

## 🐛 Debugging Steps

### Check 1: Is Monitoring Running?
```bash
curl http://localhost:8000/api/v1/monitoring/status
```

Expected: `"is_running": true`

### Check 2: Do Farmers Have Plots?
```bash
curl http://localhost:8000/api/v1/farmers/ | jq '.[].farmer_id' | xargs -I {} curl http://localhost:8000/api/v1/farmers/{}/plots
```

### Check 3: What Are Risk Scores?
```powershell
Get-Content backend.log | Select-String "risk score"
```

### Check 4: Are Calls Being Initiated?
```powershell
Get-Content backend.log | Select-String "call initiated|Call initiated"
```

### Check 5: Is Webhook Being Hit?
```powershell
Get-Content backend.log | Select-String "Advisory call webhook"
```

### Check 6: Check Twilio Dashboard
- Go to https://console.twilio.com/
- Navigate to "Monitor" → "Logs" → "Calls"
- Look for recent outbound calls
- Check call status and any errors

## 🎯 Expected Behavior After Fixes

1. **Click "Check Now"**:
   - System checks all 3 farmers
   - Calculates risk scores
   - If risk ≥ 70%: Generates advisory
   - If risk ≥ 60%: Makes voice call
   - Updates stats (calls_made counter)

2. **Voice Call**:
   - Farmer receives call
   - Hears greeting in their language
   - Hears full advisory message
   - Option to press 1 to replay
   - Hears goodbye message

3. **Monitoring Dashboard**:
   - Shows updated statistics
   - Calls counter increments
   - Last check timestamp updates

## 📝 Next Steps

1. **Restart backend** to apply code changes
2. **Test manual call** to verify webhook works
3. **Clear old advisories** to allow new generation
4. **Click "Check Now"** to test automated flow
5. **Monitor logs** to see what's happening
6. **Check Twilio dashboard** for call status

## 🔍 Troubleshooting Guide

### Problem: No calls made after "Check Now"

**Check**:
```bash
curl http://localhost:8000/api/v1/advisories/farmer/fc008579-7fcb-4f31-8ab8-837ef8d44f83
```

**If advisories exist from last 6 hours**: System skips farmer
**Solution**: Wait 6 hours OR delete old advisories

### Problem: Call received but no message

**Check backend logs**:
```powershell
Get-Content backend.log -Tail 100 | Select-String "webhook"
```

**If no webhook logs**: Ngrok URL issue or Twilio not reaching webhook
**If webhook logs show "Farmer not found"**: Phone number mismatch
**If webhook logs show "No advisory found"**: Advisory not in database

### Problem: Risk scores too low

**Current calculation**:
- Base: 50
- NDVI < 0.5: +10 to +40
- Temp > 30°C: +10 to +15
- Humidity < 30% or > 80%: +5 to +10

**To increase risk scores**:
- Lower thresholds in `_calculate_risk_score`
- Or wait for actual crop stress conditions

## ✅ Success Criteria

- [ ] Backend restarted with new code
- [ ] Call threshold lowered to 60%
- [ ] Calling hours restriction removed
- [ ] Manual call works with advisory message
- [ ] "Check Now" initiates calls
- [ ] Webhook logs show advisory being found
- [ ] Farmer hears complete message
- [ ] Stats show calls_made > 0

## 📞 Test Farmer Details

**Farmer ID**: fc008579-7fcb-4f31-8ab8-837ef8d44f83
**Phone**: +918151910856
**Language**: Hindi
**Location**: Bangalore (12.9716, 77.5946)
**Crops**: wheat, rice
**Plot Size**: 2.5 hectares

Use this farmer for all testing as they have a plot registered.
