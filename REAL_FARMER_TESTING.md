# Real Farmer Plot Testing - Complete Guide

## Overview

This guide will help you test KrishiMitra with a real farmer's plot using actual satellite imagery and weather data.

## Prerequisites

### 1. API Keys Required

You need these API keys for real data:

- **Sentinel Hub** (Satellite imagery): https://www.sentinel-hub.com/
- **OpenWeatherMap** (Weather data): https://openweathermap.org/api
- **Twilio** (Voice calls): https://www.twilio.com/
- **AWS** (Already configured): Bedrock, Transcribe, Polly

### 2. Farmer Information Needed

Collect this information from the farmer:
- Phone number (e.g., +918095666788)
- Farm location (latitude, longitude)
- Farm area (in hectares)
- Crop types (e.g., wheat, rice, cotton)
- Planting date
- Expected harvest date
- Preferred language (Hindi, Telugu, etc.)

## Step-by-Step Testing Process

### STEP 1: Get API Keys

#### A. Sentinel Hub (Satellite Data)

1. Go to https://www.sentinel-hub.com/
2. Sign up for free trial (1 month free)
3. Create an OAuth client:
   - Dashboard > User Settings > OAuth clients
   - Click "Create new"
   - Copy Client ID and Client Secret
4. Add to `.env`:
   ```env
   SENTINEL_HUB_CLIENT_ID=your_client_id
   SENTINEL_HUB_CLIENT_SECRET=your_client_secret
   ```

#### B. OpenWeatherMap (Weather Data)

1. Go to https://openweathermap.org/api
2. Sign up for free account
3. Get API key from dashboard
4. Add to `.env`:
   ```env
   OPENWEATHERMAP_API_KEY=your_api_key
   ```

#### C. Twilio (Voice Calls)

1. Go to https://www.twilio.com/try-twilio
2. Sign up (free $15 credit)
3. Verify farmer's phone number
4. Get a Twilio phone number
5. Add to `.env`:
   ```env
   TWILIO_ACCOUNT_SID=ACxxxxx
   TWILIO_AUTH_TOKEN=your_token
   TWILIO_PHONE_NUMBER=+1234567890
   ```

### STEP 2: Locate the Farm

#### Option A: Use Google Maps

1. Open Google Maps
2. Find the farmer's location
3. Right-click on the plot
4. Click coordinates to copy
5. Example: `18.5204, 73.8567`

#### Option B: Use GPS Device

1. Visit the farm with GPS device
2. Record coordinates at plot center
3. Note: Use decimal degrees format

#### Option C: Ask Farmer

Many farmers know their survey numbers. You can:
1. Get survey number
2. Look up coordinates in land records
3. Use government portals (varies by state)

### STEP 3: Create Test Script for Real Plot

Create `scripts/test_real_farmer.py`:

```python
#!/usr/bin/env python3
"""
Test with real farmer plot
"""
import asyncio
import sys
from pathlib import Path
from datetime import datetime, timedelta
from jose import jwt

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.config.settings import settings
from src.services.data_ingestion.satellite_client import SatelliteDataClient
from src.services.data_ingestion.weather_client import WeatherDataClient
from src.services.monitoring.ndvi_calculator import NDVICalculator
from src.services.monitoring.weather_analyzer import WeatherAnalyzer
from src.services.agents.monitoring_agent import MonitoringAgent
from src.services.agents.advisory_agent import AdvisoryAgent
from src.services.agents.knowledge_base import KnowledgeBase
from src.services.agents.tool_registry import ToolRegistry
import httpx

BASE_URL = "http://127.0.0.1:8000"

# REAL FARMER DATA - UPDATE THESE
FARMER_PHONE = "+918095666788"
FARMER_LANGUAGE = "hi"
PLOT_LATITUDE = 18.5204  # UPDATE: Your farmer's plot latitude
PLOT_LONGITUDE = 73.8567  # UPDATE: Your farmer's plot longitude
PLOT_AREA_HECTARES = 2.5  # UPDATE: Actual plot size
CROP_TYPES = ["wheat", "rice"]  # UPDATE: Actual crops
PLANTING_DATE = "2024-11-01"  # UPDATE: Actual planting date


def create_test_token():
    """Create JWT token"""
    payload = {
        "sub": "test_user",
        "role": "staff",
        "exp": datetime.utcnow() + timedelta(hours=1),
        "iat": datetime.utcnow(),
        "type": "access"
    }
    return jwt.encode(payload, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)


async def step1_create_farmer():
    """Create farmer in database"""
    print("\n" + "="*70)
    print("STEP 1: Register Farmer")
    print("="*70)
    
    farmer_data = {
        "phone_number": FARMER_PHONE,
        "preferred_language": FARMER_LANGUAGE,
        "timezone": "Asia/Kolkata"
    }
    
    token = create_test_token()
    headers = {"Authorization": f"Bearer {token}"}
    
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{BASE_URL}/api/v1/farmers/",
            json=farmer_data,
            headers=headers
        )
        
        if response.status_code == 201:
            farmer = response.json()
        elif response.status_code == 400:
            # Already exists
            response = await client.get(
                f"{BASE_URL}/api/v1/farmers/",
                headers=headers
            )
            farmers = response.json()
            farmer = [f for f in farmers if f['phone_number'] == FARMER_PHONE][0]
        else:
            raise Exception(f"Failed: {response.text}")
    
    print(f"✓ Farmer registered: {farmer['farmer_id']}")
    print(f"  Phone: {farmer['phone_number']}")
    return farmer


async def step2_create_plot(farmer_id):
    """Register farm plot"""
    print("\n" + "="*70)
    print("STEP 2: Register Farm Plot")
    print("="*70)
    
    plot_data = {
        "latitude": PLOT_LATITUDE,
        "longitude": PLOT_LONGITUDE,
        "area_hectares": PLOT_AREA_HECTARES,
        "crop_types": CROP_TYPES,
        "planting_date": PLANTING_DATE,
        "expected_harvest_date": (
            datetime.fromisoformat(PLANTING_DATE) + timedelta(days=120)
        ).isoformat()
    }
    
    token = create_test_token()
    headers = {"Authorization": f"Bearer {token}"}
    
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{BASE_URL}/api/v1/farmers/{farmer_id}/plots",
            json=plot_data,
            headers=headers
        )
        
        if response.status_code != 201:
            raise Exception(f"Failed: {response.text}")
        
        plot = response.json()
    
    print(f"✓ Plot registered: {plot['plot_id']}")
    print(f"  Location: {PLOT_LATITUDE}, {PLOT_LONGITUDE}")
    print(f"  Area: {PLOT_AREA_HECTARES} hectares")
    print(f"  Crops: {', '.join(CROP_TYPES)}")
    return plot


async def step3_fetch_satellite_data():
    """Fetch REAL satellite data from Sentinel Hub"""
    print("\n" + "="*70)
    print("STEP 3: Fetch Satellite Data (Sentinel Hub)")
    print("="*70)
    
    try:
        satellite_client = SatelliteDataClient()
        
        # Calculate bounding box (500m x 500m around plot center)
        bbox_size = 0.0045  # ~500m in degrees
        bbox = (
            PLOT_LONGITUDE - bbox_size,
            PLOT_LATITUDE - bbox_size,
            PLOT_LONGITUDE + bbox_size,
            PLOT_LATITUDE + bbox_size
        )
        
        print(f"  Fetching data for bbox: {bbox}")
        print(f"  Date: {datetime.utcnow().date()}")
        
        # Fetch tile
        tile_data = await satellite_client.fetch_tile(
            bbox=bbox,
            start_date=datetime.utcnow() - timedelta(days=7),
            end_date=datetime.utcnow(),
            resolution=10  # 10m resolution
        )
        
        # Calculate NDVI
        calculator = NDVICalculator()
        result = calculator.process_tile(
            tile_data=tile_data,
            bbox=bbox,
            timestamp=datetime.utcnow()
        )
        
        print(f"✓ Satellite data fetched")
        print(f"  NDVI Mean: {result['ndvi']['mean']:.3f}")
        print(f"  NDVI Status: {result['ndvi']['interpretation']['status']}")
        print(f"  Description: {result['ndvi']['interpretation']['description']}")
        
        return result
        
    except Exception as e:
        print(f"✗ Failed to fetch satellite data: {e}")
        print(f"  Using simulated data instead...")
        
        # Fallback to simulated data
        import numpy as np
        ndvi_values = np.random.normal(0.45, 0.05, (100, 100))
        calculator = NDVICalculator()
        ndvi_stats = calculator.calculate_statistics(ndvi_values)
        
        return {
            "ndvi": ndvi_stats,
            "interpretation": calculator.interpret_ndvi(ndvi_stats['mean']),
            "simulated": True
        }


async def step4_fetch_weather_data():
    """Fetch REAL weather data from OpenWeatherMap"""
    print("\n" + "="*70)
    print("STEP 4: Fetch Weather Data (OpenWeatherMap)")
    print("="*70)
    
    try:
        weather_client = WeatherDataClient()
        
        # Fetch current weather
        current_weather = await weather_client.get_current_weather(
            lat=PLOT_LATITUDE,
            lon=PLOT_LONGITUDE
        )
        
        # Fetch forecast
        forecast = await weather_client.get_forecast(
            lat=PLOT_LATITUDE,
            lon=PLOT_LONGITUDE,
            days=7
        )
        
        # Fetch historical (last 30 days)
        weather_history = []
        for i in range(30):
            date = datetime.utcnow() - timedelta(days=i)
            hist = await weather_client.get_historical_weather(
                lat=PLOT_LATITUDE,
                lon=PLOT_LONGITUDE,
                date=date
            )
            weather_history.append(hist)
        
        # Analyze risks
        analyzer = WeatherAnalyzer()
        risk_analysis = analyzer.analyze_weather_risks(
            current_weather,
            forecast,
            weather_history
        )
        
        print(f"✓ Weather data fetched")
        print(f"  Temperature: {current_weather['temperature']}°C")
        print(f"  Humidity: {current_weather['humidity']}%")
        print(f"  Overall Risk: {risk_analysis['overall_risk']}")
        print(f"  Heat Stress: {risk_analysis['heat_stress']['risk_level']}")
        print(f"  Drought: {risk_analysis['drought']['risk_level']}")
        
        return {
            "current_weather": current_weather,
            "forecast": forecast,
            "weather_history": weather_history,
            "risk_analysis": risk_analysis,
            "simulated": False
        }
        
    except Exception as e:
        print(f"✗ Failed to fetch weather data: {e}")
        print(f"  Using simulated data instead...")
        
        # Fallback to simulated data
        current_weather = {
            "temperature": 38.5,
            "humidity": 25,
            "wind_speed": 15,
            "rain_1h": 0,
            "timestamp": datetime.utcnow()
        }
        
        forecast = [
            {"temp_max": 39, "temp_min": 28, "pop": 0.1, "wind_speed": 12}
            for _ in range(7)
        ]
        
        weather_history = [
            {"temperature": 36, "humidity": 30, "rain_1h": 0, "timestamp": datetime.utcnow() - timedelta(days=i)}
            for i in range(30)
        ]
        
        analyzer = WeatherAnalyzer()
        risk_analysis = analyzer.analyze_weather_risks(
            current_weather,
            forecast,
            weather_history
        )
        
        return {
            "current_weather": current_weather,
            "forecast": forecast,
            "weather_history": weather_history,
            "risk_analysis": risk_analysis,
            "simulated": True
        }


async def step5_analyze_and_generate_advisory(satellite_data, weather_data):
    """Analyze data and generate advisory"""
    print("\n" + "="*70)
    print("STEP 5: AI Analysis & Advisory Generation")
    print("="*70)
    
    # Initialize agents
    tools = ToolRegistry()
    knowledge_base = KnowledgeBase()
    
    monitoring_agent = MonitoringAgent(tools, knowledge_base)
    advisory_agent = AdvisoryAgent(tools, knowledge_base)
    
    # Monitoring agent analysis
    monitoring_context = {
        "ndvi_data": satellite_data.get("ndvi", {}),
        "weather_data": weather_data["risk_analysis"],
        "historical_data": {
            "ndvi_mean": 0.65,
            "ndvi_std": 0.05
        },
        "plot_info": {
            "crop_types": CROP_TYPES,
            "area_hectares": PLOT_AREA_HECTARES
        }
    }
    
    monitoring_decision = monitoring_agent.think(monitoring_context)
    
    print(f"✓ Monitoring Analysis:")
    print(f"  Anomaly: {monitoring_decision['anomaly_detected']}")
    print(f"  Threat: {monitoring_decision['threat_level']}")
    print(f"  Action: {monitoring_decision['action']}")
    
    # Generate advisory
    if monitoring_decision['anomaly_detected']:
        diagnosis = {
            "stress_type": "water_stress",
            "risk_score": 75,
            "confidence": 0.85
        }
        
        advisory_context = {
            "diagnosis": diagnosis,
            "farmer_profile": {
                "language": FARMER_LANGUAGE,
                "experience_level": "intermediate"
            },
            "plot_info": {
                "crop_types": CROP_TYPES,
                "area_hectares": PLOT_AREA_HECTARES
            },
            "constraints": {
                "max_budget": 5000,  # ₹5000 budget
                "area_hectares": PLOT_AREA_HECTARES
            }
        }
        
        advisory = advisory_agent.think(advisory_context)
        
        print(f"\n✓ Advisory Generated:")
        print(f"  Risk Score: {advisory['risk_score']}/100")
        print(f"  Actions: {len(advisory['actions'])}")
        print(f"  Total Cost: ₹{advisory['total_estimated_cost']}")
        
        return advisory
    else:
        print(f"\n✓ No advisory needed - crops are healthy")
        return None


async def step6_make_voice_call(farmer, advisory):
    """Make voice call to farmer"""
    print("\n" + "="*70)
    print("STEP 6: Voice Call to Farmer")
    print("="*70)
    
    if not advisory:
        print("  No advisory to deliver")
        return
    
    print(f"  To: {farmer['phone_number']}")
    print(f"  Language: {farmer['preferred_language']}")
    print(f"  Message: Advisory about {advisory['stress_type']}")
    
    print(f"\n  See MAKE_REAL_CALL_GUIDE.md for voice call setup")
    print(f"  Run: python scripts/make_real_call.py")


async def main():
    """Run complete real farmer test"""
    print("\n" + "="*70)
    print("  KrishiMitra - Real Farmer Plot Testing")
    print("="*70)
    print(f"\n  Farmer: {FARMER_PHONE}")
    print(f"  Location: {PLOT_LATITUDE}, {PLOT_LONGITUDE}")
    print(f"  Area: {PLOT_AREA_HECTARES} hectares")
    print(f"  Crops: {', '.join(CROP_TYPES)}")
    
    try:
        # Step 1: Register farmer
        farmer = await step1_create_farmer()
        
        # Step 2: Register plot
        plot = await step2_create_plot(farmer['farmer_id'])
        
        # Step 3: Fetch satellite data
        satellite_data = await step3_fetch_satellite_data()
        
        # Step 4: Fetch weather data
        weather_data = await step4_fetch_weather_data()
        
        # Step 5: Analyze and generate advisory
        advisory = await step5_analyze_and_generate_advisory(
            satellite_data,
            weather_data
        )
        
        # Step 6: Voice call
        if advisory:
            await step6_make_voice_call(farmer, advisory)
        
        # Summary
        print("\n" + "="*70)
        print("  TEST COMPLETE")
        print("="*70)
        
        if satellite_data.get("simulated"):
            print("  ⚠ Used simulated satellite data (Sentinel Hub not configured)")
        else:
            print("  ✓ Used real satellite data from Sentinel Hub")
        
        if weather_data.get("simulated"):
            print("  ⚠ Used simulated weather data (OpenWeatherMap not configured)")
        else:
            print("  ✓ Used real weather data from OpenWeatherMap")
        
        if advisory:
            print(f"\n  Advisory Summary:")
            print(f"    Risk: {advisory['risk_score']}/100")
            print(f"    Actions: {len(advisory['actions'])}")
            print(f"    Cost: ₹{advisory['total_estimated_cost']}")
        else:
            print(f"\n  ✓ Crops are healthy - no advisory needed")
        
        return 0
        
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
```

### STEP 4: Update Configuration

Edit the script `scripts/test_real_farmer.py` and update:

```python
# Line 20-27: Update with real farmer data
FARMER_PHONE = "+918095666788"  # Real phone number
FARMER_LANGUAGE = "hi"  # or "te", "ta", etc.
PLOT_LATITUDE = 18.5204  # Real latitude
PLOT_LONGITUDE = 73.8567  # Real longitude
PLOT_AREA_HECTARES = 2.5  # Real area
CROP_TYPES = ["wheat", "rice"]  # Real crops
PLANTING_DATE = "2024-11-01"  # Real planting date
```

### STEP 5: Run the Test

```powershell
# Terminal 1: Start server
.\venv\Scripts\Activate.ps1
uvicorn src.main:app --reload

# Terminal 2: Run real farmer test
.\venv\Scripts\Activate.ps1
python scripts/test_real_farmer.py
```

### STEP 6: Interpret Results

The test will show:

1. **Satellite Data**:
   - NDVI value (0-1 scale)
   - Crop health status
   - Whether data is real or simulated

2. **Weather Data**:
   - Current conditions
   - Risk levels (drought, heat, frost, wind)
   - Whether data is real or simulated

3. **AI Analysis**:
   - Anomaly detection results
   - Threat level assessment
   - Recommended actions

4. **Advisory**:
   - Risk score (0-100)
   - Specific actions to take
   - Cost estimates
   - Timeframes

## Expected Outcomes

### Scenario 1: Healthy Crops
```
NDVI: 0.65-0.80 (healthy)
Weather: Normal conditions
Result: No advisory needed
Action: Continue monitoring
```

### Scenario 2: Water Stress
```
NDVI: 0.40-0.55 (stressed)
Weather: Drought conditions
Result: Advisory generated
Actions:
  1. Immediate irrigation (₹500)
  2. Apply mulch (₹1250)
Total: ₹1750
```

### Scenario 3: Heat Stress
```
NDVI: 0.50-0.60 (moderate stress)
Weather: High temperature (>38°C)
Result: Advisory generated
Actions:
  1. Increase irrigation frequency (₹300)
  2. Shade netting if possible (₹2000)
```

## Troubleshooting

### Issue: Sentinel Hub API Error

**Cause**: API key not configured or quota exceeded

**Solution**:
1. Check `.env` has correct credentials
2. Verify account has credits
3. Check API usage in dashboard
4. Test will fall back to simulated data

### Issue: OpenWeatherMap API Error

**Cause**: API key invalid or rate limit exceeded

**Solution**:
1. Verify API key in `.env`
2. Check rate limits (60 calls/minute for free tier)
3. Wait and retry
4. Test will fall back to simulated data

### Issue: No Anomaly Detected

**Cause**: Crops are actually healthy!

**Solution**: This is good news! The system is working correctly.

### Issue: Wrong Location Data

**Cause**: Incorrect coordinates

**Solution**:
1. Verify coordinates on Google Maps
2. Ensure format is decimal degrees
3. Check latitude/longitude are not swapped

## Data Interpretation Guide

### NDVI Values
- **0.8-1.0**: Very healthy, dense vegetation
- **0.6-0.8**: Healthy vegetation
- **0.4-0.6**: Moderate vegetation (may need attention)
- **0.2-0.4**: Sparse/stressed vegetation (action needed)
- **<0.2**: Bare soil or severe stress

### Weather Risk Levels
- **None**: No action needed
- **Low**: Monitor situation
- **Medium**: Prepare preventive measures
- **High**: Immediate action required

### Advisory Priority
- **High**: Act within 24-48 hours
- **Medium**: Act within 3-7 days
- **Low**: Act within 1-2 weeks

## Cost Estimates

Typical advisory costs per hectare:
- Irrigation: ₹200-500
- Fertilizer: ₹400-800
- Pesticide: ₹300-600
- Mulching: ₹500-1000
- Labor: ₹200-400

## Next Steps

After successful testing:

1. **Collect Feedback**: Ask farmer if advisory was helpful
2. **Track Results**: Monitor crop improvement after actions
3. **Refine System**: Update thresholds based on outcomes
4. **Scale Up**: Add more farmers
5. **Automate**: Set up daily monitoring
6. **Deploy**: Move to production AWS infrastructure

## Production Deployment

For production use:
1. Set up automated daily satellite data fetching
2. Configure weather data polling
3. Enable automatic advisory generation
4. Set up voice call scheduling
5. Implement feedback collection
6. Add monitoring and alerts

See `AWS_DEPLOYMENT.md` for production setup.

## Support

Need help?
- Check logs in terminal
- Review API documentation
- Test individual components
- Contact support

Good luck with your real farmer testing! 🌾
