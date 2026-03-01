#!/usr/bin/env python3
"""
Test Sentinel Hub credentials
"""
import asyncio
import sys
from pathlib import Path
from datetime import datetime, timedelta

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.services.data_ingestion.satellite_client import SatelliteClient
from src.config.settings import settings


async def test_sentinel_hub():
    """Test Sentinel Hub connection and fetch sample data"""
    
    print("\n" + "="*70)
    print("  Sentinel Hub Credentials Test")
    print("="*70)
    
    # Check credentials are configured
    print("\n1. Checking Configuration")
    print("-" * 70)
    
    try:
        if not settings.sentinel_hub_client_id:
            print("✗ SENTINEL_HUB_CLIENT_ID not configured")
            print("  Add to .env file")
            return 1
        
        if not settings.sentinel_hub_client_secret:
            print("✗ SENTINEL_HUB_CLIENT_SECRET not configured")
            print("  Add to .env file")
            return 1
        
        print(f"✓ Client ID: {settings.sentinel_hub_client_id[:20]}...")
        print(f"✓ Client Secret: {settings.sentinel_hub_client_secret[:20]}...")
        
    except Exception as e:
        print(f"✗ Configuration error: {e}")
        return 1
    
    # Initialize client
    print("\n2. Initializing Sentinel Hub Client")
    print("-" * 70)
    
    try:
        client = SatelliteClient()
        print("✓ Client initialized")
    except Exception as e:
        print(f"✗ Failed to initialize client: {e}")
        return 1
    
    # Test authentication
    print("\n3. Testing Authentication")
    print("-" * 70)
    
    try:
        # This will trigger OAuth token fetch
        print("  Fetching OAuth token...")
        
        # Try to fetch a small tile (Pune, India area)
        bbox = (73.8567, 18.5204, 73.8667, 18.5304)  # ~1km x 1km
        
        print(f"  Location: Pune, India")
        print(f"  Bbox: {bbox}")
        print(f"  Date: Last 7 days")
        
        tile_data = await client.fetch_tile(
            bbox=bbox,
            date_from=datetime.utcnow() - timedelta(days=7),
            date_to=datetime.utcnow()
        )
        
        print(f"✓ Authentication successful!")
        print(f"✓ Tile data fetched")
        print(f"  Bbox: {tile_data['bbox']}")
        print(f"  Date range: {tile_data['date_from']} to {tile_data['date_to']}")
        print(f"  Image size: {tile_data['width']}x{tile_data['height']}")
        print(f"  Data size: {len(tile_data['data'])} bytes")
        
        print("\n" + "="*70)
        print("  ✓ SUCCESS: Sentinel Hub is working!")
        print("="*70)
        print("\n  You can now:")
        print("    - Fetch real satellite imagery")
        print("    - Calculate NDVI for any location")
        print("    - Monitor crop health")
        print("\n  Next: Run python scripts/test_api_keys.py")
        
        return 0
        
    except Exception as e:
        print(f"✗ Authentication failed: {e}")
        print(f"\n  Possible issues:")
        print(f"    1. Invalid Client ID or Secret")
        print(f"    2. Credentials not activated yet (wait a few minutes)")
        print(f"    3. No processing units remaining")
        print(f"    4. Network/firewall issues")
        print(f"\n  Check:")
        print(f"    - Sentinel Hub Dashboard: https://apps.sentinel-hub.com/dashboard/")
        print(f"    - Verify credentials are correct")
        print(f"    - Check processing units quota")
        
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(test_sentinel_hub())
    sys.exit(exit_code)
