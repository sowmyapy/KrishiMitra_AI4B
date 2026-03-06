# Auto Monitoring System - How It Works

## Overview
The automated monitoring system continuously monitors all registered farmers and takes action based on their crop health risk scores.

## How It Works

### 1. Monitoring Loop
- **Frequency**: Checks all farmers every 1 hour (3600 seconds) when running
- **Background Process**: Runs continuously in the background
- **Manual Trigger**: "Check Now" button triggers an immediate check

### 2. Risk Assessment Process

For each farmer, the system:

1. **Fetches Real Data**:
   - Satellite data (NDVI) from Sentinel Hub for the last 7 days
   - Current weather data (temperature, humidity) from OpenWeatherMap

2. **Calculates Risk Score** (0-100):
   - **Base Risk**: 50
   - **NDVI Impact**:
     - NDVI < 0.2: +40 (Severe stress)
     - NDVI < 0.3: +30 (High stress)
     - NDVI < 0.4: +20 (Moderate stress)
     - NDVI < 0.5: +10 (Mild stress)
   - **Temperature Impact**:
     - Temp > 35°C: +15 (Heat stress)
     - Temp > 30°C: +10
   - **Humidity Impact**:
     - Humidity < 30%: +10 (Dry conditions)
     - Humidity > 80%: +5 (High humidity)
   - **Maximum**: Capped at 100

### 3. Action Thresholds

Based on the calculated risk score:

- **Risk ≥ 70%**: 
  - ✅ Generate advisory
  - Advisory includes: stress type, recommendations, weather info
  - Advisory saved to database
  - Advisory text in farmer's preferred language (Hindi/English/Telugu)

- **Risk ≥ 80%**: 
  - ✅ Generate advisory
  - ✅ Make voice call to farmer
  - Call only made during calling hours (9 AM - 7 PM in farmer's timezone)
  - Voice message in farmer's preferred language

### 4. Smart Skipping

The system avoids redundant actions:

- **Recent Advisory Check**: If farmer already has an advisory from the last 6 hours, skip
- **Calling Hours**: Voice calls only between 9 AM - 7 PM
- **Error Handling**: If a check fails, waits 1 minute before retry

### 5. Statistics Tracking

The system tracks:
- **Farmers Monitored**: Total count of farmers checked
- **Advisories Generated**: Number of advisories created
- **Calls Made**: Number of voice calls initiated
- **Errors**: Count of any errors encountered
- **Last Check**: Timestamp of most recent check

## Using the System

### Start Monitoring
1. Click "Start" button on Monitoring page
2. System begins checking all farmers every hour
3. Green "System is actively monitoring" message appears

### Stop Monitoring
1. Click "Stop" button
2. System stops the monitoring loop
3. "System is currently stopped" message appears

### Check Now
1. Click "Check Now" button
2. System immediately checks all farmers (bypasses 1-hour wait)
3. Notification shows results: "Check complete! Monitored: X, Advisories: Y"
4. **Does NOT call farmers every time** - only calls if:
   - Risk score ≥ 80%
   - No recent advisory (last 6 hours)
   - Within calling hours (9 AM - 7 PM)

## Example Scenario

**Farmer**: Ramesh (+918151910856)
**Location**: Bangalore (12.9716, 77.5946)
**Crop**: Wheat

**Check Now clicked at 2:00 PM:**

1. System fetches NDVI: 0.35 (moderate stress)
2. System fetches weather: 32°C, 28% humidity
3. Risk calculation:
   - Base: 50
   - NDVI < 0.4: +20
   - Temp > 30°C: +10
   - Humidity < 30%: +10
   - **Total Risk: 90**

4. Actions taken:
   - ✅ Advisory generated (risk ≥ 70%)
   - ✅ Voice call made (risk ≥ 80%, within calling hours)

5. Next check:
   - If "Check Now" clicked again within 6 hours: **SKIPPED** (recent advisory exists)
   - If automatic check runs: **SKIPPED** (recent advisory exists)
   - After 6 hours: Will check again and generate new advisory if needed

## Configuration

Current settings (can be modified in code):
- **Check Interval**: 3600 seconds (1 hour)
- **Risk Threshold**: 70% (generate advisory)
- **Call Threshold**: 80% (make voice call)
- **Advisory Validity**: 6 hours (skip if recent)
- **Calling Hours**: 9 AM - 7 PM

## Benefits

1. **Proactive**: Catches crop stress before it becomes severe
2. **Automated**: No manual intervention needed
3. **Smart**: Avoids redundant advisories and calls
4. **Real Data**: Uses actual satellite and weather data
5. **Multilingual**: Advisories and calls in farmer's language
6. **Respectful**: Only calls during appropriate hours

## Troubleshooting

**No advisories generated?**
- Check if farmers have plots registered
- Verify risk scores are ≥ 70%
- Check if recent advisories exist (last 6 hours)
- View backend logs for errors

**No calls made?**
- Check if risk scores are ≥ 80%
- Verify it's within calling hours (9 AM - 7 PM)
- Check Twilio credentials in .env
- Verify phone numbers are verified in Twilio

**System not running?**
- Click "Start" button on Monitoring page
- Check backend logs for errors
- Restart backend if needed
