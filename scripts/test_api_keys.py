#!/usr/bin/env python3
"""
Test all API keys configuration
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.config.settings import settings

def test_api_keys():
    """Test all API keys are configured"""
    
    print("\n" + "="*70)
    print("  API Keys Configuration Test")
    print("="*70)
    
    results = {}
    
    # Test Sentinel Hub
    print("\n1. Sentinel Hub (Satellite Imagery)")
    print("-" * 70)
    try:
        if settings.sentinel_hub_client_id and settings.sentinel_hub_client_secret:
            print(f"   Client ID: {settings.sentinel_hub_client_id[:20]}...")
            print(f"   Client Secret: {settings.sentinel_hub_client_secret[:20]}...")
            print("   ✓ Configured")
            results['Sentinel Hub'] = True
        else:
            print("   ✗ Not configured")
            print("   Get key at: https://www.sentinel-hub.com/")
            results['Sentinel Hub'] = False
    except Exception as e:
        print(f"   ✗ Error: {e}")
        results['Sentinel Hub'] = False
    
    # Test OpenWeatherMap
    print("\n2. OpenWeatherMap (Weather Data)")
    print("-" * 70)
    try:
        if settings.openweathermap_api_key:
            print(f"   API Key: {settings.openweathermap_api_key[:20]}...")
            print("   ✓ Configured")
            results['OpenWeatherMap'] = True
        else:
            print("   ✗ Not configured")
            print("   Get key at: https://openweathermap.org/api")
            results['OpenWeatherMap'] = False
    except Exception as e:
        print(f"   ✗ Error: {e}")
        results['OpenWeatherMap'] = False
    
    # Test Twilio
    print("\n3. Twilio (Voice Calls)")
    print("-" * 70)
    try:
        if (settings.twilio_account_sid and 
            settings.twilio_auth_token and 
            settings.twilio_phone_number):
            print(f"   Account SID: {settings.twilio_account_sid[:20]}...")
            print(f"   Auth Token: {settings.twilio_auth_token[:20]}...")
            print(f"   Phone Number: {settings.twilio_phone_number}")
            print("   ✓ Configured")
            results['Twilio'] = True
        else:
            print("   ✗ Not configured")
            print("   Get account at: https://www.twilio.com/try-twilio")
            results['Twilio'] = False
    except Exception as e:
        print(f"   ✗ Error: {e}")
        results['Twilio'] = False
    
    # Test AWS
    print("\n4. AWS (Bedrock, Transcribe, Polly)")
    print("-" * 70)
    try:
        if settings.aws_access_key_id and settings.aws_secret_access_key:
            print(f"   Access Key ID: {settings.aws_access_key_id[:20]}...")
            print(f"   Secret Key: {settings.aws_secret_access_key[:20]}...")
            print(f"   Region: {settings.aws_region}")
            print("   ✓ Configured")
            results['AWS'] = True
        else:
            print("   ✗ Not configured")
            results['AWS'] = False
    except Exception as e:
        print(f"   ✗ Error: {e}")
        results['AWS'] = False
    
    # Summary
    print("\n" + "="*70)
    print("  Summary")
    print("="*70)
    
    for service, configured in results.items():
        status = "✓ PASS" if configured else "✗ FAIL"
        print(f"  {service}: {status}")
    
    passed = sum(results.values())
    total = len(results)
    
    print(f"\n  Configured: {passed}/{total}")
    
    if passed == total:
        print("\n  ✓ All API keys configured!")
        print("\n  Next steps:")
        print("    1. Run: python scripts/test_real_farmer.py")
        print("    2. Or: python scripts/make_real_call.py")
        return 0
    else:
        print("\n  ⚠ Some API keys missing")
        print("\n  See GET_API_KEYS_GUIDE.md for setup instructions")
        return 1


if __name__ == "__main__":
    exit_code = test_api_keys()
    sys.exit(exit_code)
