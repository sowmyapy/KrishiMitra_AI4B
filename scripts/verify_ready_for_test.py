#!/usr/bin/env python3
"""
Verify system is ready for end-to-end test with voice call
"""
import os
import sys
from pathlib import Path

from dotenv import load_dotenv

sys.path.insert(0, str(Path(__file__).parent.parent))

# Load environment variables
load_dotenv()

def check_env_var(name, required=True):
    """Check if environment variable is set"""
    value = os.getenv(name)
    if not value or value.startswith("your_"):
        if required:
            print(f"  ✗ {name}: NOT SET")
            return False
        else:
            print(f"  ⚠ {name}: Not set (optional)")
            return True
    else:
        # Mask sensitive values
        if len(value) > 10:
            masked = value[:4] + "..." + value[-4:]
        else:
            masked = "***"
        print(f"  ✓ {name}: {masked}")
        return True


def main():
    """Run all checks"""
    print("\n" + "="*70)
    print("  KrishiMitra - Pre-Test Verification")
    print("="*70)

    all_good = True

    # Check 1: Twilio Configuration
    print("\n1. Twilio Configuration (REQUIRED for voice calls)")
    print("-" * 70)

    twilio_ok = True
    twilio_ok &= check_env_var("TWILIO_ACCOUNT_SID")
    twilio_ok &= check_env_var("TWILIO_AUTH_TOKEN")
    twilio_ok &= check_env_var("TWILIO_PHONE_NUMBER")

    if twilio_ok:
        phone = os.getenv("TWILIO_PHONE_NUMBER")
        if phone == "+17752270557":
            print(f"  ✓ Using correct Twilio number: {phone}")
        else:
            print(f"  ⚠ Twilio number: {phone}")
            print("    Expected: +17752270557")
            twilio_ok = False

    all_good &= twilio_ok

    # Check 2: AWS Configuration
    print("\n2. AWS Configuration (REQUIRED for voice generation)")
    print("-" * 70)

    aws_ok = True
    aws_ok &= check_env_var("AWS_ACCESS_KEY_ID")
    aws_ok &= check_env_var("AWS_SECRET_ACCESS_KEY")
    aws_ok &= check_env_var("AWS_REGION")

    if aws_ok:
        region = os.getenv("AWS_REGION")
        if region == "ap-south-1":
            print(f"  ✓ Using India region: {region}")
        else:
            print(f"  ⚠ AWS region: {region}")
            print("    Recommended for India: ap-south-1")

    all_good &= aws_ok

    # Check 3: Sentinel Hub Configuration
    print("\n3. Sentinel Hub Configuration (for satellite data)")
    print("-" * 70)

    sentinel_ok = True
    sentinel_ok &= check_env_var("SENTINEL_HUB_CLIENT_ID")
    sentinel_ok &= check_env_var("SENTINEL_HUB_CLIENT_SECRET")

    if not sentinel_ok:
        print("  ⚠ Test will use simulated satellite data")

    # Check 4: OpenWeatherMap Configuration
    print("\n4. OpenWeatherMap Configuration (for weather data)")
    print("-" * 70)

    weather_ok = check_env_var("OPENWEATHERMAP_API_KEY")

    if not weather_ok:
        print("  ⚠ Test will use simulated weather data")

    # Check 5: Test Script Configuration
    print("\n5. Test Script Configuration")
    print("-" * 70)

    test_script = Path("scripts/test_real_farmer.py")
    if test_script.exists():
        print(f"  ✓ Test script found: {test_script}")

        # Read and check configuration
        content = test_script.read_text()

        if 'FARMER_PHONE = "+918151910856"' in content:
            print("  ✓ Farmer phone: +918151910856")
        else:
            print("  ⚠ Farmer phone may need updating")

        if 'PLOT_LATITUDE = 13.2443' in content:
            print("  ⚠ Using default coordinates (13.2443, 77.7122)")
            print("    Update lines 22-28 with your actual farm location")
        else:
            print("  ✓ Custom coordinates configured")
    else:
        print(f"  ✗ Test script not found: {test_script}")
        all_good = False

    # Check 6: Server Status
    print("\n6. Server Status")
    print("-" * 70)

    try:
        import asyncio

        import httpx

        async def check_server():
            try:
                async with httpx.AsyncClient() as client:
                    response = await client.get("http://127.0.0.1:8000/", timeout=2.0)
                    return response.status_code == 200
            except:
                return False

        server_running = asyncio.run(check_server())

        if server_running:
            print("  ✓ Server is running on http://127.0.0.1:8000")
        else:
            print("  ✗ Server is NOT running")
            print("    Start with: uvicorn src.main:app --reload")
            all_good = False
    except ImportError:
        print("  ⚠ Cannot check server status (httpx not available)")

    # Check 7: Phone Verification
    print("\n7. Phone Number Verification (CRITICAL!)")
    print("-" * 70)
    print("  ⚠ For Twilio trial accounts, you MUST verify +918151910856")
    print("    1. Go to: https://console.twilio.com/us1/develop/phone-numbers/manage/verified")
    print("    2. Add and verify: +918151910856")
    print("    3. Complete SMS or voice verification")
    print("\n  Have you verified the phone number? (This check is manual)")

    # Summary
    print("\n" + "="*70)
    print("  VERIFICATION SUMMARY")
    print("="*70)

    if all_good and twilio_ok and aws_ok:
        print("\n  ✅ READY FOR TESTING!")
        print("\n  Next steps:")
        print("    1. Verify phone number in Twilio (if not done)")
        print("    2. Update farm coordinates in scripts/test_real_farmer.py")
        print("    3. Start server: uvicorn src.main:app --reload")
        print("    4. Start ngrok: ngrok http 8000")
        print("    5. Run test: python scripts/test_real_farmer.py")
        print("\n  See: START_END_TO_END_TEST.md for detailed instructions")
        return 0
    else:
        print("\n  ⚠ SOME ISSUES FOUND")
        print("\n  Required fixes:")

        if not twilio_ok:
            print("    - Configure Twilio credentials in .env")
        if not aws_ok:
            print("    - Configure AWS credentials in .env")
        if not all_good:
            print("    - Check errors above")

        print("\n  Optional improvements:")
        if not sentinel_ok:
            print("    - Add Sentinel Hub credentials for real satellite data")
        if not weather_ok:
            print("    - Add OpenWeatherMap API key for real weather data")

        print("\n  See: API_KEYS_GUIDE.md for setup instructions")
        return 1


if __name__ == "__main__":
    exit_code = main()

    print("\n" + "="*70)
    input("Press Enter to exit...")
    sys.exit(exit_code)
