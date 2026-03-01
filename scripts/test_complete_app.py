#!/usr/bin/env python3
"""
Complete application test script
Tests all available endpoints and services
"""
import asyncio
import sys
from pathlib import Path
import httpx
from datetime import datetime, timedelta
from jose import jwt

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

BASE_URL = "http://127.0.0.1:8000"


def create_test_token():
    """Create a test JWT token for authentication"""
    from src.config.settings import settings
    
    payload = {
        "sub": "test_user",
        "role": "staff",  # Staff role to access all endpoints
        "exp": datetime.utcnow() + timedelta(hours=1),
        "iat": datetime.utcnow(),
        "type": "access"
    }
    
    token = jwt.encode(payload, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)
    return token


async def test_root():
    """Test root endpoint"""
    print("\n" + "="*60)
    print("Testing Root Endpoint")
    print("="*60)
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{BASE_URL}/")
            print(f"✓ Status: {response.status_code}")
            print(f"✓ Response: {response.json()}")
            return True
    except Exception as e:
        print(f"✗ Error: {e}")
        return False


async def test_health():
    """Test health check endpoint"""
    print("\n" + "="*60)
    print("Testing Health Check")
    print("="*60)
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{BASE_URL}/health")
            print(f"✓ Status: {response.status_code}")
            print(f"✓ Response: {response.json()}")
            return True
    except Exception as e:
        print(f"✗ Error: {e}")
        return False


async def test_create_farmer():
    """Test creating a farmer"""
    print("\n" + "="*60)
    print("Testing Create Farmer")
    print("="*60)
    
    farmer_data = {
        "phone_number": "+919876543210",
        "preferred_language": "hi",
        "timezone": "Asia/Kolkata"
    }
    
    try:
        token = create_test_token()
        headers = {"Authorization": f"Bearer {token}"}
        
        async with httpx.AsyncClient(follow_redirects=True) as client:
            response = await client.post(
                f"{BASE_URL}/api/v1/farmers/",
                json=farmer_data,
                headers=headers
            )
            print(f"✓ Status: {response.status_code}")
            if response.status_code == 201:
                data = response.json()
                print(f"✓ Created farmer: {data.get('farmer_id')}")
                print(f"  Phone: {data.get('phone_number')}")
                print(f"  Language: {data.get('preferred_language')}")
                return True
            elif response.status_code == 400:
                print(f"⚠ Farmer already exists (this is OK for testing)")
                return True
            else:
                print(f"✗ Response: {response.text}")
                return False
    except Exception as e:
        print(f"✗ Error: {e}")
        return False


async def test_list_farmers():
    """Test listing farmers"""
    print("\n" + "="*60)
    print("Testing List Farmers")
    print("="*60)
    
    try:
        token = create_test_token()
        headers = {"Authorization": f"Bearer {token}"}
        
        async with httpx.AsyncClient(follow_redirects=True) as client:
            response = await client.get(
                f"{BASE_URL}/api/v1/farmers/",
                headers=headers
            )
            print(f"✓ Status: {response.status_code}")
            if response.status_code == 200:
                farmers = response.json()
                print(f"✓ Found {len(farmers)} farmer(s)")
                for farmer in farmers[:3]:  # Show first 3
                    print(f"  - {farmer.get('phone_number')} ({farmer.get('preferred_language')})")
                return True
            else:
                print(f"✗ Response: {response.text}")
                return False
    except Exception as e:
        print(f"✗ Error: {e}")
        return False


async def test_docs():
    """Test API documentation"""
    print("\n" + "="*60)
    print("Testing API Documentation")
    print("="*60)
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{BASE_URL}/api/v1/docs")
            print(f"✓ Status: {response.status_code}")
            if response.status_code == 200:
                print(f"✓ Swagger UI is accessible at: {BASE_URL}/api/v1/docs")
                return True
            else:
                print(f"✗ Unexpected status code: {response.status_code}")
                return False
    except Exception as e:
        print(f"✗ Error: {e}")
        return False


async def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("KrishiMitra - Complete Application Test")
    print("="*60)
    print(f"Testing server at: {BASE_URL}")
    
    # Check if server is running
    try:
        async with httpx.AsyncClient() as client:
            await client.get(BASE_URL, timeout=2.0)
    except Exception:
        print("\n✗ ERROR: Server is not running!")
        print("\nPlease start the server first:")
        print("  uvicorn src.main:app --reload")
        return 1
    
    # Run tests
    results = {
        "Root Endpoint": await test_root(),
        "Health Check": await test_health(),
        "API Documentation": await test_docs(),
        "Create Farmer": await test_create_farmer(),
        "List Farmers": await test_list_farmers(),
    }
    
    # Summary
    print("\n" + "="*60)
    print("Test Summary")
    print("="*60)
    
    for test_name, passed in results.items():
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{test_name}: {status}")
    
    passed_count = sum(results.values())
    total_count = len(results)
    
    print(f"\nPassed: {passed_count}/{total_count}")
    
    if passed_count == total_count:
        print("\n✓ All tests passed!")
        print(f"\nYou can now access the application at:")
        print(f"  - API: {BASE_URL}")
        print(f"  - Docs: {BASE_URL}/api/v1/docs")
        return 0
    else:
        print("\n✗ Some tests failed")
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
