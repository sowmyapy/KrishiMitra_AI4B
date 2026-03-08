#!/usr/bin/env python3
"""
Make Real Voice Call to Farmer
This script actually calls your phone number with the advisory
"""
import asyncio
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.config.settings import settings
from src.services.communication.voice_call_service import VoiceCallService


async def make_advisory_call():
    """Make actual advisory call"""

    print("="*70)
    print("  KrishiMitra - Real Voice Call Test")
    print("="*70)

    # Farmer details
    farmer_phone = "+918151910856"  # Change this to your desired number
    farmer_language = "hi"

    # Advisory details
    advisory = {
        "stress_type": "water_stress",
        "risk_score": 75,
        "actions": [
            {
                "action": "immediate_irrigation",
                "description": "अगले 24 घंटे में सिंचाई करें",
                "cost": 500,
                "timeframe": "24 hours"
            },
            {
                "action": "mulching",
                "description": "3 दिन में मल्चिंग करें",
                "cost": 1250,
                "timeframe": "3 days"
            }
        ],
        "total_estimated_cost": 1750
    }

    print("\nFarmer Details:")
    print(f"  Phone: {farmer_phone}")
    print(f"  Language: {farmer_language}")

    print("\nAdvisory Details:")
    print(f"  Type: {advisory['stress_type']}")
    print(f"  Risk Score: {advisory['risk_score']}/100")
    print(f"  Total Cost: ₹{advisory['total_estimated_cost']}")

    # Create advisory message in Hindi
    advisory_message = f"""
    नमस्ते। यह कृषि मित्र है।

    आपकी फसल में पानी की कमी के संकेत दिख रहे हैं।
    जोखिम स्कोर {advisory['risk_score']} प्रतिशत है।

    तुरंत करने योग्य कार्य:

    पहला: अगले 24 घंटे में सिंचाई करें। लागत लगभग 500 रुपये।

    दूसरा: 3 दिन में मल्चिंग करें। लागत लगभग 1250 रुपये।

    कुल अनुमानित लागत 1750 रुपये है।

    कृपया जल्द से जल्द कार्रवाई करें।
    धन्यवाद।
    """

    print("\nMessage (Hindi):")
    print(advisory_message)

    # Check Twilio configuration
    print("\n" + "="*70)
    print("  Checking Twilio Configuration")
    print("="*70)

    try:
        print(f"  Twilio Account SID: {settings.twilio_account_sid[:10]}...")
        print(f"  Twilio Phone Number: {settings.twilio_phone_number}")
        print("  ✓ Twilio configured")
    except Exception as e:
        print(f"  ✗ Twilio not configured: {e}")
        print("\n  Please set in .env:")
        print("    TWILIO_ACCOUNT_SID=your_account_sid")
        print("    TWILIO_AUTH_TOKEN=your_auth_token")
        print("    TWILIO_PHONE_NUMBER=your_twilio_number")
        return 1

    # Initialize voice service
    try:
        voice_service = VoiceCallService()
        print("  ✓ Voice service initialized")
    except Exception as e:
        print(f"  ✗ Failed to initialize voice service: {e}")
        return 1

    # Generate TwiML
    print("\n" + "="*70)
    print("  Generating TwiML")
    print("="*70)

    twiml = voice_service.generate_advisory_twiml(
        advisory_text=advisory_message,
        language="hi",
        allow_replay=True
    )

    print(f"  ✓ TwiML generated ({len(twiml)} bytes)")
    print("\n  TwiML Preview:")
    print(f"  {twiml[:300]}...")

    # Important note about webhook
    print("\n" + "="*70)
    print("  IMPORTANT: Webhook URL Required")
    print("="*70)

    print("""
  To make actual calls, Twilio needs a public webhook URL.

  Options:

  1. Use ngrok (recommended for testing):
     - Install ngrok: https://ngrok.com/download
     - Run: ngrok http 8000
     - Copy the HTTPS URL (e.g., https://abc123.ngrok.io)
     - Use: https://abc123.ngrok.io/voice/advisory

  2. Deploy to production:
     - Deploy your app to AWS/Heroku/etc.
     - Use your production URL

  3. Use Twilio TwiML Bins (simple testing):
     - Go to Twilio Console > TwiML Bins
     - Create a new bin with the TwiML above
     - Use the bin URL
    """)

    # Ask for webhook URL
    print("\n" + "="*70)
    print("  Ready to Make Call")
    print("="*70)

    webhook_url = input("\nEnter your webhook URL (or press Enter to skip): ").strip()

    if not webhook_url:
        print("\n  ⚠ No webhook URL provided")
        print("  Skipping actual call")
        print("\n  To test without webhook, you can:")
        print("  1. Save the TwiML to a Twilio TwiML Bin")
        print("  2. Use Twilio Console to make a test call")
        return 0

    # Confirm call
    print(f"\n  About to call: {farmer_phone}")
    print(f"  Using webhook: {webhook_url}")
    confirm = input("\n  Proceed with call? (yes/no): ").strip().lower()

    if confirm != "yes":
        print("\n  Call cancelled")
        return 0

    # Make the call
    print("\n" + "="*70)
    print("  Making Call")
    print("="*70)

    try:
        call_result = await voice_service.initiate_call(
            to_number=farmer_phone,
            callback_url=webhook_url,
            farmer_id="test_farmer",
            call_type="advisory"
        )

        print("\n  ✓ Call initiated successfully!")
        print("\n  Call Details:")
        print(f"    Call SID: {call_result['call_sid']}")
        print(f"    To: {call_result['to_number']}")
        print(f"    From: {call_result['from_number']}")
        print(f"    Status: {call_result['status']}")
        print(f"    Initiated: {call_result['initiated_at']}")

        print(f"\n  The call should arrive at {farmer_phone} shortly!")
        print("  You will hear the advisory in Hindi.")

        # Wait a bit and check status
        print("\n  Waiting 10 seconds to check call status...")
        await asyncio.sleep(10)

        status = await voice_service.get_call_status(call_result['call_sid'])
        print("\n  Call Status Update:")
        print(f"    Status: {status['status']}")
        if status['duration']:
            print(f"    Duration: {status['duration']} seconds")

        return 0

    except Exception as e:
        print(f"\n  ✗ Failed to make call: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(make_advisory_call())
    sys.exit(exit_code)
