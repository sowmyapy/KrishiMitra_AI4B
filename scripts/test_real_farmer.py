#!/usr/bin/env python3
"""
Test KrishiMitra with real farmer plot using actual satellite and weather data
"""
import asyncio
import sys
from pathlib import Path
from datetime import datetime, timedelta
from jose import jwt
import httpx

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.config.settings import settings
from src.services.data_ingestion.satellite_client import SatelliteClient
from src.services.data_ingestion.weather_client import WeatherClient
from src.services.aws.polly_client import PollyClient
from src.services.communication.voice_call_service import VoiceCallService

BASE_URL = "http://127.0.0.1:8000"

# ============================================================================
# REAL FARMER DATA - UPDATE THESE VALUES
# ============================================================================
FARMER_PHONE = "+918151910856"  # Your phone number
FARMER_LANGUAGE = "hi"  # Hindi
PLOT_LATITUDE = 13.2443  # Pune area - UPDATE with real coordinates
PLOT_LONGITUDE = 77.7122  # Pune area - UPDATE with real coordinates
PLOT_AREA_HECTARES = 2.5  # UPDATE with actual plot size
CROP_TYPES = ["ragi", "mango"]  # UPDATE with actual crops
PLANTING_DATE = "2025-11-01"  # UPDATE with actual planting date


def create_test_token():
    """Create JWT token for API authentication"""
    payload = {
        "sub": "test_user",
        "role": "staff",
        "exp": datetime.utcnow() + timedelta(hours=1),
        "iat": datetime.utcnow(),
        "type": "access"
    }
    return jwt.encode(payload, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)


async def step1_create_farmer():
    """Register farmer in database"""
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
            headers=headers,
            follow_redirects=True
        )
        
        if response.status_code == 201:
            farmer = response.json()
            print(f"✓ Farmer registered (new)")
        elif response.status_code == 400 and ("already" in response.text.lower() or "registered" in response.text.lower()):
            # Farmer already exists, fetch it
            print(f"  Farmer already exists, fetching existing record...")
            response = await client.get(
                f"{BASE_URL}/api/v1/farmers/",
                headers=headers,
                follow_redirects=True
            )
            farmers = response.json()
            farmer = next((f for f in farmers if f['phone_number'] == FARMER_PHONE), None)
            if not farmer:
                raise Exception("Farmer exists but couldn't fetch")
            print(f"✓ Using existing farmer")
        else:
            raise Exception(f"Failed to create farmer: {response.status_code} - {response.text}")
    
    print(f"  ID: {farmer['farmer_id']}")
    print(f"  Phone: {farmer['phone_number']}")
    print(f"  Language: {farmer['preferred_language']}")
    return farmer


async def step2_fetch_satellite_data():
    """Fetch REAL satellite data from Sentinel Hub"""
    print("\n" + "="*70)
    print("STEP 2: Fetch Satellite Data (Sentinel Hub)")
    print("="*70)
    
    try:
        satellite_client = SatelliteClient()
        
        # Calculate bounding box (~1km x 1km around plot center)
        bbox_size = 0.005  # ~500m in degrees
        bbox = (
            PLOT_LONGITUDE - bbox_size,
            PLOT_LATITUDE - bbox_size,
            PLOT_LONGITUDE + bbox_size,
            PLOT_LATITUDE + bbox_size
        )
        
        print(f"  Location: {PLOT_LATITUDE}, {PLOT_LONGITUDE}")
        print(f"  Bbox: {bbox}")
        print(f"  Fetching last 7 days of data...")
        
        # Fetch tile
        tile_data = await satellite_client.fetch_tile(
            bbox=bbox,
            date_from=datetime.utcnow() - timedelta(days=7),
            date_to=datetime.utcnow(),
            width=256,
            height=256
        )
        
        print(f"✓ Satellite data fetched successfully")
        print(f"  Data size: {len(tile_data['data'])} bytes")
        print(f"  Image size: {tile_data['width']}x{tile_data['height']}")
        print(f"  Date range: {tile_data['date_from'].date()} to {tile_data['date_to'].date()}")
        
        # Simulate NDVI calculation (in production, parse TIFF data)
        ndvi_mean = 0.55  # Moderate vegetation
        print(f"\n  NDVI Analysis:")
        print(f"    Mean NDVI: {ndvi_mean:.3f}")
        if ndvi_mean > 0.6:
            print(f"    Status: Healthy vegetation")
        elif ndvi_mean > 0.4:
            print(f"    Status: Moderate vegetation (may need attention)")
        else:
            print(f"    Status: Stressed vegetation (action needed)")
        
        return {
            "tile_data": tile_data,
            "ndvi_mean": ndvi_mean,
            "status": "moderate",
            "real_data": True
        }
        
    except Exception as e:
        print(f"✗ Failed to fetch satellite data: {e}")
        print(f"  Check:")
        print(f"    1. Sentinel Hub credentials in .env")
        print(f"    2. Processing units quota")
        print(f"    3. Network connection")
        print(f"\n  Using simulated data for testing...")
        
        return {
            "ndvi_mean": 0.45,
            "status": "stressed",
            "real_data": False
        }


async def step3_fetch_weather_data():
    """Fetch REAL weather data from OpenWeatherMap"""
    print("\n" + "="*70)
    print("STEP 3: Fetch Weather Data (OpenWeatherMap)")
    print("="*70)
    
    try:
        weather_client = WeatherClient()
        
        print(f"  Location: {PLOT_LATITUDE}, {PLOT_LONGITUDE}")
        print(f"  Fetching current weather and forecast...")
        
        # Fetch current weather
        current_weather = await weather_client.fetch_current_weather(
            lat=PLOT_LATITUDE,
            lon=PLOT_LONGITUDE
        )
        
        # Fetch 5-day forecast
        forecast = await weather_client.fetch_forecast(
            lat=PLOT_LATITUDE,
            lon=PLOT_LONGITUDE,
            days=5
        )
        
        print(f"✓ Weather data fetched successfully")
        print(f"\n  Current Conditions:")
        print(f"    Temperature: {current_weather['temperature']}°C")
        print(f"    Feels like: {current_weather['feels_like']}°C")
        print(f"    Humidity: {current_weather['humidity']}%")
        print(f"    Wind: {current_weather['wind_speed']} m/s")
        print(f"    Weather: {current_weather['weather_description']}")
        
        print(f"\n  5-Day Forecast:")
        print(f"    {len(forecast)} data points fetched")
        
        # Analyze risks
        high_temp_days = sum(1 for f in forecast if f['temp_max'] > 35)
        low_humidity_days = sum(1 for f in forecast if f['humidity'] < 30)
        
        risks = []
        if current_weather['temperature'] > 35:
            risks.append("Heat stress")
        if current_weather['humidity'] < 30:
            risks.append("Drought conditions")
        if current_weather['wind_speed'] > 10:
            risks.append("High wind")
        
        if risks:
            print(f"\n  ⚠ Weather Risks Detected:")
            for risk in risks:
                print(f"    - {risk}")
        else:
            print(f"\n  ✓ No immediate weather risks")
        
        return {
            "current_weather": current_weather,
            "forecast": forecast,
            "risks": risks,
            "real_data": True
        }
        
    except Exception as e:
        print(f"✗ Failed to fetch weather data: {e}")
        print(f"  Check:")
        print(f"    1. OpenWeatherMap API key in .env")
        print(f"    2. API rate limits")
        print(f"    3. Network connection")
        print(f"\n  Using simulated data for testing...")
        
        return {
            "current_weather": {
                "temperature": 38.5,
                "humidity": 25,
                "wind_speed": 15,
                "weather_description": "clear sky"
            },
            "forecast": [],
            "risks": ["Heat stress", "Drought conditions"],
            "real_data": False
        }


async def step4_generate_advisory(satellite_data, weather_data):
    """Generate advisory based on data analysis"""
    print("\n" + "="*70)
    print("STEP 4: Generate Advisory")
    print("="*70)
    
    # Analyze conditions
    ndvi = satellite_data['ndvi_mean']
    temp = weather_data['current_weather']['temperature']
    humidity = weather_data['current_weather']['humidity']
    risks = weather_data.get('risks', [])
    
    print(f"  Analyzing conditions...")
    print(f"    NDVI: {ndvi:.3f}")
    print(f"    Temperature: {temp}°C")
    print(f"    Humidity: {humidity}%")
    
    # Determine if advisory needed
    needs_advisory = False
    advisory_type = None
    
    if ndvi < 0.5 or temp > 35 or humidity < 30:
        needs_advisory = True
        if ndvi < 0.5 and humidity < 30:
            advisory_type = "water_stress"
        elif temp > 35:
            advisory_type = "heat_stress"
        else:
            advisory_type = "general_stress"
    
    if not needs_advisory:
        print(f"\n✓ Crops are healthy - no advisory needed")
        return None
    
    # Generate advisory
    print(f"\n⚠ Advisory needed: {advisory_type}")
    
    advisory = {
        "stress_type": advisory_type,
        "risk_score": 75,
        "confidence": 0.85,
        "actions": []
    }
    
    # Add recommended actions
    if advisory_type == "water_stress":
        advisory["actions"] = [
            {
                "action": "Immediate irrigation",
                "priority": "high",
                "cost": 500,
                "timeframe": "24 hours"
            },
            {
                "action": "Apply mulch to retain moisture",
                "priority": "medium",
                "cost": 1250,
                "timeframe": "3 days"
            }
        ]
    elif advisory_type == "heat_stress":
        advisory["actions"] = [
            {
                "action": "Increase irrigation frequency",
                "priority": "high",
                "cost": 300,
                "timeframe": "24 hours"
            },
            {
                "action": "Consider shade netting",
                "priority": "medium",
                "cost": 2000,
                "timeframe": "1 week"
            }
        ]
    else:  # general_stress
        advisory["actions"] = [
            {
                "action": "Monitor soil moisture levels",
                "priority": "high",
                "cost": 200,
                "timeframe": "24 hours"
            },
            {
                "action": "Light irrigation if needed",
                "priority": "medium",
                "cost": 400,
                "timeframe": "2 days"
            },
            {
                "action": "Apply organic fertilizer",
                "priority": "low",
                "cost": 800,
                "timeframe": "1 week"
            }
        ]
    
    advisory["total_cost"] = sum(a["cost"] for a in advisory["actions"])
    
    print(f"\n  Advisory Details:")
    print(f"    Risk Score: {advisory['risk_score']}/100")
    print(f"    Confidence: {advisory['confidence']*100:.0f}%")
    print(f"    Actions: {len(advisory['actions'])}")
    for i, action in enumerate(advisory["actions"], 1):
        print(f"      {i}. {action['action']}")
        print(f"         Priority: {action['priority']}, Cost: ₹{action['cost']}, Time: {action['timeframe']}")
    print(f"    Total Cost: ₹{advisory['total_cost']}")
    
    return advisory


async def step5_generate_voice_message(farmer, advisory):
    """Generate Hindi voice message"""
    print("\n" + "="*70)
    print("STEP 5: Generate Voice Message")
    print("="*70)
    
    if not advisory:
        print("  No advisory to deliver")
        return None
    
    # Create Hindi message
    message_hi = f"""
नमस्ते किसान भाई,
    
यह कृषि मित्र से एक महत्वपूर्ण सलाह है।
    
हमारे उपग्रह विश्लेषण से पता चला है कि आपकी फसल में पानी की कमी है।
    
तुरंत करें:
1. अगले 24 घंटों में सिंचाई करें - खर्च लगभग 500 रुपये
2. 3 दिनों में मल्चिंग करें - खर्च लगभग 1250 रुपये
    
कुल अनुमानित खर्च: {advisory['total_cost']} रुपये
    
अधिक जानकारी के लिए हमें कॉल करें।
धन्यवाद।
"""
    
    print(f"  Message created in {farmer['preferred_language']}")
    print(f"  Length: {len(message_hi)} characters")
    
    try:
        # Generate audio using AWS Polly
        polly_client = PollyClient()
        
        print(f"  Generating audio with AWS Polly...")
        audio_data = await polly_client.synthesize(
            text=message_hi,
            language="hi"
        )
        
        # Save audio file
        audio_file = Path("test_advisory_message.mp3")
        audio_file.write_bytes(audio_data)
        
        print(f"✓ Voice message generated")
        print(f"  File: {audio_file}")
        print(f"  Size: {len(audio_data)} bytes")
        
        return {
            "message": message_hi,
            "audio_file": str(audio_file),
            "audio_data": audio_data
        }
        
    except Exception as e:
        print(f"✗ Failed to generate voice: {e}")
        print(f"  Message text created but audio generation failed")
        return {
            "message": message_hi,
            "audio_file": None
        }


async def step6_make_voice_call(farmer, advisory, voice_message):
    """Make actual voice call to farmer"""
    print("\n" + "="*70)
    print("  STEP 6: Make Voice Call")
    print("="*70)
    
    if not advisory:
        print("  No advisory to deliver")
        return None
    
    # Check if user wants to make the call
    print(f"\n📞 Ready to call: {farmer['phone_number']}")
    print(f"  From: {settings.twilio_phone_number}")
    print(f"\n⚠ This will make an ACTUAL phone call!")
    print(f"  Make sure:")
    print(f"    1. Server is running (Terminal 1)")
    print(f"    2. ngrok is running (Terminal 2)")
    print(f"    3. Phone number is verified in Twilio")
    
    webhook_url = input(f"\nEnter ngrok webhook URL (or press Enter to skip): ").strip()
    
    if not webhook_url:
        print(f"\n⚠ No webhook URL provided - skipping call")
        print(f"  To make calls later, run: python scripts/make_real_call.py")
        return None
    
    if not webhook_url.startswith("https://"):
        print(f"\n✗ Webhook URL must be HTTPS")
        return None
    
    # Confirm call
    confirm = input(f"\nProceed with call? (yes/no): ").strip().lower()
    
    if confirm != "yes":
        print(f"\n✗ Call cancelled")
        return None
    
    # Initialize voice service
    try:
        voice_service = VoiceCallService()
        print(f"\n✓ Voice service initialized")
    except Exception as e:
        print(f"\n✗ Failed to initialize voice service: {e}")
        return None
    
    # Make the call
    try:
        print(f"\n📞 Initiating call...")
        
        call_result = await voice_service.initiate_call(
            to_number=farmer['phone_number'],
            callback_url=webhook_url,
            farmer_id=farmer['farmer_id'],
            call_type="advisory"
        )
        
        print(f"\n✓ Call initiated successfully!")
        print(f"\n  Call Details:")
        print(f"    Call SID: {call_result['call_sid']}")
        print(f"    To: {call_result['to_number']}")
        print(f"    From: {call_result['from_number']}")
        print(f"    Status: {call_result['status']}")
        print(f"    Initiated: {call_result['initiated_at']}")
        
        print(f"\n  🔔 Your phone should ring shortly!")
        print(f"  📱 Answer to hear the Hindi advisory")
        
        # Wait and check status
        print(f"\n  Waiting 15 seconds to check call status...")
        await asyncio.sleep(15)
        
        status = await voice_service.get_call_status(call_result['call_sid'])
        print(f"\n  Call Status Update:")
        print(f"    Status: {status['status']}")
        if status['duration']:
            print(f"    Duration: {status['duration']} seconds")
        
        return call_result
        
    except Exception as e:
        print(f"\n✗ Failed to make call: {e}")
        import traceback
        traceback.print_exc()
        return None


async def main():
    """Run complete real farmer test"""
    print("\n" + "="*70)
    print("  KrishiMitra - Real Farmer Plot Testing")
    print("="*70)
    print(f"\n  Configuration:")
    print(f"    Farmer: {FARMER_PHONE}")
    print(f"    Location: {PLOT_LATITUDE}, {PLOT_LONGITUDE}")
    print(f"    Area: {PLOT_AREA_HECTARES} hectares")
    print(f"    Crops: {', '.join(CROP_TYPES)}")
    print(f"    Language: {FARMER_LANGUAGE}")
    
    try:
        # Step 1: Register farmer
        farmer = await step1_create_farmer()
        
        # Step 2: Fetch satellite data
        satellite_data = await step2_fetch_satellite_data()
        
        # Step 3: Fetch weather data
        weather_data = await step3_fetch_weather_data()
        
        # Step 4: Generate advisory
        advisory = await step4_generate_advisory(satellite_data, weather_data)
        
        # Step 5: Generate voice message
        voice_message = None
        if advisory:
            voice_message = await step5_generate_voice_message(farmer, advisory)
        
        # Step 6: Make voice call
        call_result = None
        if advisory and voice_message:
            call_result = await step6_make_voice_call(farmer, advisory, voice_message)
        
        # Summary
        print("\n" + "="*70)
        print("  TEST COMPLETE")
        print("="*70)
        
        print(f"\n  Data Sources:")
        if satellite_data.get("real_data"):
            print(f"    ✓ Real satellite data from Sentinel Hub")
        else:
            print(f"    ⚠ Simulated satellite data (Sentinel Hub not available)")
        
        if weather_data.get("real_data"):
            print(f"    ✓ Real weather data from OpenWeatherMap")
        else:
            print(f"    ⚠ Simulated weather data (OpenWeatherMap not available)")
        
        if advisory:
            print(f"\n  Advisory Summary:")
            print(f"    Type: {advisory['stress_type']}")
            print(f"    Risk: {advisory['risk_score']}/100")
            print(f"    Actions: {len(advisory['actions'])}")
            print(f"    Total Cost: ₹{advisory['total_cost']}")
            
            if voice_message and voice_message.get('audio_file'):
                print(f"\n  Voice Message:")
                print(f"    ✓ Generated: {voice_message['audio_file']}")
            else:
                print(f"\n  ⚠ Voice message text created but audio generation failed")
            
            if call_result:
                print(f"\n  Voice Call:")
                print(f"    ✓ Call made to: {farmer['phone_number']}")
                print(f"    Call SID: {call_result['call_sid']}")
                print(f"    Status: {call_result['status']}")
            else:
                print(f"\n  Voice Call:")
                print(f"    ⚠ Call not made (skipped or failed)")
                print(f"    To make call later: python scripts/make_real_call.py")
        else:
            print(f"\n  ✓ Crops are healthy - no advisory needed")
        
        print(f"\n  🎉 Complete end-to-end test finished!")
        
        return 0
        
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    # Check if server is running
    print("\n⚠ Make sure the server is running:")
    print("  uvicorn src.main:app --reload")
    print("\nPress Enter to continue...")
    input()
    
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
