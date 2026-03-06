"""
Quick test script to verify farmer update endpoint works without authentication
"""
import requests
import json

# Get list of farmers
response = requests.get("http://localhost:8000/api/v1/farmers/")
print("GET /farmers/ status:", response.status_code)

if response.status_code == 200:
    farmers = response.json()
    if farmers:
        farmer = farmers[0]
        farmer_id = farmer['farmer_id']
        print(f"\nTesting with farmer: {farmer['phone_number']} (ID: {farmer_id})")
        print(f"Current language: {farmer['preferred_language']}")
        
        # Try to update the farmer
        update_data = {
            "phone_number": farmer['phone_number'],
            "preferred_language": "te",  # Change to Telugu
            "timezone": farmer['timezone']
        }
        
        print(f"\nAttempting to update to Telugu...")
        update_response = requests.put(
            f"http://localhost:8000/api/v1/farmers/{farmer_id}",
            json=update_data,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"PUT /farmers/{farmer_id} status:", update_response.status_code)
        
        if update_response.status_code == 200:
            print("✅ SUCCESS! Farmer updated successfully")
            updated_farmer = update_response.json()
            print(f"New language: {updated_farmer['preferred_language']}")
        else:
            print("❌ FAILED!")
            print("Response:", update_response.text)
            
            if "Not authenticated" in update_response.text or update_response.status_code == 401:
                print("\n⚠️  Authentication is still enabled!")
                print("Please restart the backend server:")
                print("  1. Stop the backend (Ctrl+C)")
                print("  2. Start it again: python -m uvicorn src.main:app --reload")
    else:
        print("No farmers found in database")
else:
    print("Failed to get farmers:", response.text)
    print("\n⚠️  Make sure the backend is running:")
    print("  python -m uvicorn src.main:app --reload")
