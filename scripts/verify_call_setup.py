#!/usr/bin/env python3
"""
Verify Voice Call Setup
Checks all prerequisites before making a call
"""
import sys
from pathlib import Path
import os

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

def check_env_var(var_name: str, required: bool = True) -> bool:
    """Check if environment variable is set"""
    value = os.getenv(var_name)
    if value and value != f"your_{var_name.lower()}":
        print(f"  ✓ {var_name}: {value[:20]}...")
        return True
    else:
        if required:
            print(f"  ✗ {var_name}: Not set or using placeholder")
        else:
            print(f"  ⚠ {var_name}: Not set (optional)")
        return not required


def check_twilio_credentials():
    """Check Twilio credentials"""
    print("\n" + "="*70)
    print("  Checking Twilio Credentials")
    print("="*70)
    
    from src.config.settings import settings
    
    checks = [
        check_env_var("TWILIO_ACCOUNT_SID"),
        check_env_var("TWILIO_AUTH_TOKEN"),
        check_env_var("TWILIO_PHONE_NUMBER"),
    ]
    
    if all(checks):
        print("\n  ✓ All Twilio credentials configured")
        return True
    else:
        print("\n  ✗ Missing Twilio credentials")
        print("\n  Add to .env file:")
        print("    TWILIO_ACCOUNT_SID=ACxxxxx")
        print("    TWILIO_AUTH_TOKEN=your_token")
        print("    TWILIO_PHONE_NUMBER=+1234567890")
        return False


def check_server_running():
    """Check if FastAPI server is running"""
    print("\n" + "="*70)
    print("  Checking FastAPI Server")
    print("="*70)
    
    import httpx
    
    try:
        response = httpx.get("http://localhost:8000/health", timeout=2)
        if response.status_code == 200:
            print("  ✓ Server is running on http://localhost:8000")
            return True
        else:
            print(f"  ✗ Server returned status {response.status_code}")
            return False
    except Exception as e:
        print(f"  ✗ Server not running: {e}")
        print("\n  Start server with:")
        print("    uvicorn src.main:app --reload")
        return False


def check_voice_endpoints():
    """Check if voice endpoints are available"""
    print("\n" + "="*70)
    print("  Checking Voice Endpoints")
    print("="*70)
    
    import httpx
    
    try:
        # Check if voice endpoint exists (will return 405 for GET, but that's ok)
        response = httpx.get("http://localhost:8000/voice/advisory", timeout=2)
        # 405 means endpoint exists but doesn't accept GET
        if response.status_code in [200, 405]:
            print("  ✓ Voice endpoints configured")
            return True
        else:
            print(f"  ✗ Voice endpoint returned {response.status_code}")
            return False
    except Exception as e:
        print(f"  ✗ Voice endpoints not accessible: {e}")
        return False


def check_ngrok():
    """Check if ngrok is available"""
    print("\n" + "="*70)
    print("  Checking ngrok")
    print("="*70)
    
    import subprocess
    
    try:
        # Try to run ngrok version
        result = subprocess.run(
            ["ngrok", "version"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            version = result.stdout.strip()
            print(f"  ✓ ngrok installed: {version}")
            return True
        else:
            print("  ✗ ngrok not working")
            return False
    except FileNotFoundError:
        print("  ✗ ngrok not found in PATH")
        print("\n  Install ngrok:")
        print("    1. Download from https://ngrok.com/download")
        print("    2. Extract to C:\\ngrok\\")
        print("    3. Run: C:\\ngrok\\ngrok.exe http 8000")
        return False
    except Exception as e:
        print(f"  ⚠ Could not check ngrok: {e}")
        print("\n  If ngrok is installed, you can run:")
        print("    ngrok http 8000")
        return False


def check_phone_number():
    """Check phone number format"""
    print("\n" + "="*70)
    print("  Checking Phone Number")
    print("="*70)
    
    phone = "+918095666788"
    
    if phone.startswith("+") and len(phone) >= 10:
        print(f"  ✓ Phone number: {phone}")
        print("  ⚠ Make sure this number is verified in Twilio Console")
        print("    (Required for trial accounts)")
        return True
    else:
        print(f"  ✗ Invalid phone number format: {phone}")
        return False


def check_aws_services():
    """Check AWS services configuration"""
    print("\n" + "="*70)
    print("  Checking AWS Services (Optional)")
    print("="*70)
    
    checks = [
        check_env_var("AWS_ACCESS_KEY_ID", required=False),
        check_env_var("AWS_SECRET_ACCESS_KEY", required=False),
        check_env_var("AWS_REGION", required=False),
    ]
    
    if all(checks):
        print("\n  ✓ AWS services configured")
        return True
    else:
        print("\n  ⚠ AWS services not fully configured")
        print("    (Not required for basic voice calls)")
        return True  # Not required


def print_summary(results: dict):
    """Print summary of checks"""
    print("\n" + "="*70)
    print("  Setup Verification Summary")
    print("="*70)
    
    all_passed = all(results.values())
    
    for check, passed in results.items():
        status = "✓" if passed else "✗"
        print(f"  {status} {check}")
    
    print("\n" + "="*70)
    
    if all_passed:
        print("  ✓ ALL CHECKS PASSED - Ready to make calls!")
        print("="*70)
        print("\n  Next steps:")
        print("    1. Start ngrok: ngrok http 8000")
        print("    2. Copy ngrok URL: https://abc123.ngrok.io")
        print("    3. Run: python scripts/make_real_call.py")
        print("    4. Enter webhook URL: https://abc123.ngrok.io/voice/advisory")
        print("    5. Confirm: yes")
        print("\n  See CALL_NOW_QUICKSTART.md for detailed instructions")
        return 0
    else:
        print("  ✗ SOME CHECKS FAILED - Fix issues above")
        print("="*70)
        print("\n  Common fixes:")
        print("    - Add Twilio credentials to .env")
        print("    - Start server: uvicorn src.main:app --reload")
        print("    - Install ngrok: https://ngrok.com/download")
        print("    - Verify phone in Twilio Console")
        return 1


def main():
    """Run all checks"""
    print("="*70)
    print("  KrishiMitra - Voice Call Setup Verification")
    print("="*70)
    
    results = {
        "Twilio Credentials": check_twilio_credentials(),
        "FastAPI Server": check_server_running(),
        "Voice Endpoints": check_voice_endpoints(),
        "ngrok": check_ngrok(),
        "Phone Number": check_phone_number(),
        "AWS Services": check_aws_services(),
    }
    
    return print_summary(results)


if __name__ == "__main__":
    sys.exit(main())
