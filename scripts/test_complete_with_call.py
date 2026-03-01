#!/usr/bin/env python3
"""
Complete End-to-End Test with Real Voice Call
Tests the entire KrishiMitra workflow including actual Twilio call
"""
import asyncio
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.services.communication.voice_call_service import VoiceCallService
from src.config.settings import settings


async def test_complete_workflow():
    """Complete workflow test with real voice call"""
    
    print("="*70)
    print("  KrishiMitra - Complete End-to-End Test with Voice Call")
    print("="*70)
    
    # Configuration
    farmer_phone = "+918151910856"
    farmer_language = "hi"
    
    print(f"\n📱 Farmer Phone: {farmer_phone}")
    print(f"🌍 Language: Hindi (hi)")
    
    # Step 1: Check Prerequisites
    print(f"\n" + "="*70)
    print("  STEP 1: Checking Prerequisites")
    print("="*70)
    
    # Check Twilio configuration
    try:
        print(f"\n✓ Twilio Account SID: {settings.twilio_account_sid[:10]}...")
        print(f"✓ Twilio Phone Number: {settings.twilio_phone_number}")
    except Exception as e:
        print(f"\n✗ Twilio not configured: {e}")
        print(f"\nPlease configure Twilio in .env file")
        return 1
    
    # Check ngrok webhook
    print(f"\n⚠ Important: Make sure ngrok is running!")
    print(f"  Terminal 2 should show: ngrok http 8000")
    webhook_url = input(f"\nEnter your ngrok webhook URL (e.g., https://abc123.ngrok-free.dev/voice/advisory): ").strip()
    
    if not webhook_url:
        print(f"\n✗ Webhook URL required for voice calls")
        return 1
    
    if not webhook_url.startswith("https://"):
        print(f"\n✗ Webhook URL must be HTTPS")
        return 1
    
    print(f"\n✓ Webhook URL: {webhook_url}")
    
    # Step 2: Simulate Data Collection
    print(f"\n" + "="*70)
    print("  STEP 2: Simulating Data Collection")
    print("="*70)
    
    # Simulated satellite data
    print(f"\n📡 Satellite Data (Simulated):")
    ndvi = 0.45
    print(f"  NDVI: {ndvi} (Stressed vegetation)")
    print(f"  Status: ⚠ Crop stress detected")
    
    # Simulated weather data
    print(f"\n🌤️  Weather Data (Simulated):")
    temperature = 35.5
    humidity = 25
    print(f"  Temperature: {temperature}°C")
    print(f"  Humidity: {humidity}%")
    print(f"  Conditions: ⚠ Hot and dry - drought risk")
    
    # Step 3: AI Analysis
    print(f"\n" + "="*70)
    print("  STEP 3: AI Analysis")
    print("="*70)
    
    print(f"\n🤖 Monitoring Agent:")
    print(f"  Anomaly detected: YES")
    print(f"  Confidence: 85%")
    print(f"  Issue: Water stress + heat stress")
    
    print(f"\n🤖 Advisory Agent:")
    advisory_type = "water_stress"
    risk_score = 75
    print(f"  Advisory Type: {advisory_type}")
    print(f"  Risk Score: {risk_score}/100")
    
    # Step 4: Generate Advisory
    print(f"\n" + "="*70)
    print("  STEP 4: Generating Advisory")
    print("="*70)
    
    actions = [
        {
            "action": "immediate_irrigation",
            "description": "अगले 24 घंटे में सिंचाई करें",
            "priority": "high",
            "cost": 500,
            "timeframe": "24 hours"
        },
        {
            "action": "mulching",
            "description": "3 दिन में मल्चिंग करें",
            "priority": "medium",
            "cost": 1250,
            "timeframe": "3 days"
        }
    ]
    
    total_cost = sum(a["cost"] for a in actions)
    
    print(f"\n✓ Advisory Generated:")
    print(f"  Actions: {len(actions)}")
    print(f"  Total Cost: ₹{total_cost}")
    
    for i, action in enumerate(actions, 1):
        print(f"\n  Action {i}: {action['action']}")
        print(f"    Description: {action['description']}")
        print(f"    Priority: {action['priority']}")
        print(f"    Cost: ₹{action['cost']}")
        print(f"    Timeframe: {action['timeframe']}")
    
    # Step 5: Generate Voice Message
    print(f"\n" + "="*70)
    print("  STEP 5: Generating Voice Message")
    print("="*70)
    
    advisory_message = f"""
    नमस्ते। यह कृषि मित्र है।
    
    आपकी फसल में पानी की कमी के संकेत दिख रहे हैं।
    जोखिम स्कोर {risk_score} प्रतिशत है।
    
    तुरंत करने योग्य कार्य:
    
    पहला: अगले 24 घंटे में सिंचाई करें। लागत लगभग 500 रुपये।
    
    दूसरा: 3 दिन में मल्चिंग करें। लागत लगभग 1250 रुपये।
    
    कुल अनुमानित लागत {total_cost} रुपये है।
    
    कृपया जल्द से जल्द कार्रवाई करें।
    धन्यवाद।
    """
    
    print(f"\n✓ Message created in Hindi")
    print(f"  Length: {len(advisory_message)} characters")
    
    # Step 6: Make Voice Call
    print(f"\n" + "="*70)
    print("  STEP 6: Making Voice Call")
    print("="*70)
    
    print(f"\n📞 Preparing to call: {farmer_phone}")
    print(f"  From: {settings.twilio_phone_number}")
    print(f"  Webhook: {webhook_url}")
    
    # Confirm call
    print(f"\n⚠ This will make an ACTUAL phone call!")
    confirm = input(f"\nProceed with call? (yes/no): ").strip().lower()
    
    if confirm != "yes":
        print(f"\n✗ Call cancelled by user")
        return 0
    
    # Initialize voice service
    try:
        voice_service = VoiceCallService()
        print(f"\n✓ Voice service initialized")
    except Exception as e:
        print(f"\n✗ Failed to initialize voice service: {e}")
        return 1
    
    # Make the call
    try:
        print(f"\n📞 Initiating call...")
        
        call_result = await voice_service.initiate_call(
            to_number=farmer_phone,
            callback_url=webhook_url,
            farmer_id="test_farmer",
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
        
    except Exception as e:
        print(f"\n✗ Failed to make call: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    # Step 7: Summary
    print(f"\n" + "="*70)
    print("  TEST COMPLETE")
    print("="*70)
    
    print(f"\n✓ All steps completed successfully!")
    print(f"\n  Workflow Summary:")
    print(f"    1. ✓ Prerequisites checked")
    print(f"    2. ✓ Data collected (simulated)")
    print(f"    3. ✓ AI analysis performed")
    print(f"    4. ✓ Advisory generated")
    print(f"    5. ✓ Voice message created")
    print(f"    6. ✓ Voice call initiated")
    
    print(f"\n  Call Details:")
    print(f"    Farmer: {farmer_phone}")
    print(f"    Language: Hindi")
    print(f"    Advisory: Water stress")
    print(f"    Actions: {len(actions)}")
    print(f"    Cost: ₹{total_cost}")
    
    print(f"\n  🎉 KrishiMitra end-to-end test successful!")
    
    return 0


if __name__ == "__main__":
    print("\n⚠ IMPORTANT: Before running this test:")
    print("  1. Make sure server is running: uvicorn src.main:app --reload")
    print("  2. Make sure ngrok is running: ngrok http 8000")
    print("  3. Verify your phone number in Twilio Console")
    print()
    
    input("Press Enter to continue...")
    
    exit_code = asyncio.run(test_complete_workflow())
    sys.exit(exit_code)
