# Automated Monitoring System - Complete Guide

## Overview

The automated monitoring system continuously monitors all registered farmers, calculates risk scores based on satellite and weather data, generates advisories when needed, and makes voice calls for critical situations.

## Features

### 1. Continuous Monitoring
- Checks all farmers at regular intervals (default: 1 hour)
- Calculates risk scores from satellite and weather data
- Tracks monitoring statistics

### 2. Risk-Based Actions
- **Risk ≥ 70%**: Automatically generates advisory
- **Risk ≥ 80%**: Automatically makes voice call
- Respects calling hours (9 AM - 7 PM in farmer's timezone)

### 3. Smart Scheduling
- Skips farmers with recent advisories (within 6 hours)
- Only calls during appropriate hours
- Configurable check intervals

### 4. Multi-Language Support
- Advisories generated in farmer's preferred language
- Voice calls in farmer's language (Hindi, English, Telugu, Tamil, Marathi)

## Architecture

### Backend Components

#### 1. Auto Monitor Service (`src/services/monitoring/auto_monitor_service.py`)
- Main monitoring loop
- Risk calculation
- Advisory generation trigger
- Voice call initiation

#### 2. Monitoring API (`src/api/monitoring.py`)
- `/monitoring/start` - Start monitoring service
- `/monitoring/stop` - Stop monitoring service
- `/monitoring/status` - Get current status
- `/monitoring/settings` - Update settings
- `/monitoring/check-now` - Trigger immediate check

### Frontend Components

#### Enhanced Monitoring Page (`frontend/src/pages/MonitoringEnhanced.tsx`)
- Start/Stop controls
- Real-time status display
- Statistics dashboard
- Settings configuration
- How it works explanation

## Setup Instructions

### 1. Backend Setup

The monitoring service is already integrated into the main application. No additional setup needed!

### 2. Start the Application

```powershell
.\start_all.ps1
```

Or manually:
```powershell
# Backend
python -m uvicorn src.main:app --reload --host 0.0.0.0 --port 8000

# Frontend
cd frontend
npm run dev
```

### 3. Access the Monitoring Page

Navigate to: http://localhost:3000/monitoring

## Usage Guide

### Starting Monitoring

1. Go to the Monitoring page
2. Click "Start Monitoring" button
3. The service will begin checking all farmers every hour

### Stopping Monitoring

1. Click "Stop Monitoring" button
2. The service will stop after completing the current check

### Triggering Immediate Check

1. While monitoring is running, click "Check Now"
2. All farmers will be checked immediately

### Configuring Settings

1. Click "Settings" button
2. Adjust the following:
   - **Check Interval**: How often to check farmers (in seconds)
   - **Risk Threshold**: Minimum risk to generate advisory (%)
   - **Call Threshold**: Minimum risk to make voice call (%)
3. Click "Save Settings"

## How It Works

### Monitoring Flow

```
1. Service starts
   ↓
2. Wait for check interval
   ↓
3. Get all farmers from database
   ↓
4. For each farmer:
   ├─ Check if has recent advisory (< 6 hours)
   ├─ If yes: Skip
   └─ If no:
      ├─ Get farmer's plots
      ├─ Calculate risk score
      ├─ If risk ≥ 70%: Generate advisory
      └─ If risk ≥ 80%: Make voice call
   ↓
5. Update statistics
   ↓
6. Repeat from step 2
```

### Risk Calculation

The system calculates risk based on:
- **NDVI (Vegetation Health)**: From satellite data
- **Temperature**: From weather API
- **Humidity**: From weather API
- **Crop Type**: Different thresholds for different crops
- **Historical Data**: Trends over time

### Advisory Generation

When risk exceeds threshold:
1. Fetch latest satellite data
2. Fetch current weather data
3. Calculate NDVI and stress type
4. Generate advisory text in farmer's language
5. Save to database
6. If risk is critical, proceed to call

### Voice Call

When risk is critical:
1. Check if within calling hours (9 AM - 7 PM)
2. If yes, initiate Twilio call
3. Twilio calls webhook with farmer's phone
4. Webhook fetches farmer and advisory
5. Generates TwiML in farmer's language
6. Farmer receives call with advisory

## Configuration

### Default Settings

```python
check_interval = 3600  # 1 hour
risk_threshold = 70    # Generate advisory at 70%
call_threshold = 80    # Make call at 80%
```

### Recommended Settings

**For Testing**:
- Check Interval: 300 seconds (5 minutes)
- Risk Threshold: 60%
- Call Threshold: 70%

**For Production**:
- Check Interval: 3600 seconds (1 hour)
- Risk Threshold: 70%
- Call Threshold: 80%

**For High-Risk Areas**:
- Check Interval: 1800 seconds (30 minutes)
- Risk Threshold: 60%
- Call Threshold: 75%

## Monitoring Statistics

The system tracks:
- **Farmers Monitored**: Total number of farmers checked
- **Advisories Generated**: Number of advisories created
- **Calls Made**: Number of voice calls initiated
- **Errors**: Number of errors encountered
- **Started At**: When monitoring started
- **Last Check**: When last check completed

## API Endpoints

### Start Monitoring
```http
POST /api/v1/monitoring/start
```

Response:
```json
{
  "status": "success",
  "message": "Monitoring service started",
  "monitoring_status": { ... }
}
```

### Stop Monitoring
```http
POST /api/v1/monitoring/stop
```

### Get Status
```http
GET /api/v1/monitoring/status
```

Response:
```json
{
  "is_running": true,
  "check_interval_seconds": 3600,
  "risk_threshold": 70,
  "call_threshold": 80,
  "stats": {
    "started_at": "2024-01-15T10:30:00",
    "last_check": "2024-01-15T11:30:00",
    "farmers_monitored": 25,
    "advisories_generated": 5,
    "calls_made": 2,
    "errors": 0
  }
}
```

### Update Settings
```http
PUT /api/v1/monitoring/settings
Content-Type: application/json

{
  "check_interval": 1800,
  "risk_threshold": 65,
  "call_threshold": 75
}
```

### Trigger Immediate Check
```http
POST /api/v1/monitoring/check-now
```

## Troubleshooting

### Monitoring Won't Start
- Check backend logs for errors
- Verify database connection
- Ensure no other monitoring instance is running

### No Advisories Generated
- Check if farmers have plots
- Verify satellite/weather API keys are configured
- Check risk threshold settings
- Look at backend logs for calculation errors

### No Calls Made
- Verify Twilio credentials in .env
- Check if risk exceeds call threshold
- Verify it's within calling hours
- Check ngrok URL is correct

### High Error Count
- Check backend logs for specific errors
- Verify API keys are valid
- Check database connectivity
- Ensure sufficient API quota

## Best Practices

### 1. Start with Testing
- Use short check intervals (5 minutes)
- Lower thresholds to see system in action
- Monitor logs closely

### 2. Gradual Rollout
- Start with a few farmers
- Increase check frequency gradually
- Monitor system performance

### 3. Regular Monitoring
- Check statistics daily
- Review error logs
- Adjust thresholds based on results

### 4. Cost Management
- Monitor Twilio usage
- Set appropriate call thresholds
- Use calling hours to limit calls

### 5. Farmer Feedback
- Collect feedback on advisory quality
- Adjust language translations
- Refine risk thresholds

## Integration with Existing Features

### Dashboard
- Shows monitoring status
- Displays recent advisories
- Links to monitoring page

### Farmer Detail Page
- Manual advisory generation still available
- Manual call initiation still works
- View auto-generated advisories

### Analytics Page
- Track advisory trends
- Monitor call success rates
- Analyze risk patterns

## Future Enhancements

Potential improvements:
1. Machine learning for risk prediction
2. Historical trend analysis
3. Weather forecast integration
4. Pest/disease detection
5. Market price alerts
6. SMS notifications
7. Email reports
8. Mobile app integration

## Support

For issues or questions:
1. Check backend logs: `backend.log`
2. Check frontend console (F12)
3. Review this documentation
4. Check API endpoint responses

## Summary

The automated monitoring system provides:
- ✅ Continuous farmer monitoring
- ✅ Risk-based advisory generation
- ✅ Automatic voice calls for critical situations
- ✅ Multi-language support
- ✅ Configurable thresholds
- ✅ Real-time statistics
- ✅ Smart scheduling

Start monitoring now and let the system take care of your farmers! 🌾
