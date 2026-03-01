# Test Sentinel Hub Connection

Quick guide to test your Sentinel Hub credentials.

## Prerequisites

- Sentinel Hub credentials added to `.env` file
- Virtual environment activated
- Dependencies installed

## Run the Test

```powershell
python scripts/test_sentinel.py
```

## What It Tests

1. **Configuration Check**: Verifies credentials are in `.env`
2. **Client Initialization**: Creates Sentinel Hub client
3. **Authentication**: Fetches OAuth token
4. **Data Fetch**: Downloads a small satellite tile from Pune area (last 7 days)

## Expected Output

```
======================================================================
  Sentinel Hub Credentials Test
======================================================================

1. Checking Configuration
----------------------------------------------------------------------
✓ Client ID: 12345678-1234-1234...
✓ Client Secret: abcdefgh-abcd-abcd...

2. Initializing Sentinel Hub Client
----------------------------------------------------------------------
✓ Client initialized

3. Testing Authentication
----------------------------------------------------------------------
  Fetching OAuth token...
  Location: Pune, India
  Bbox: (73.8567, 18.5204, 73.8667, 18.5304)
  Date: Last 7 days
✓ Authentication successful!
✓ Tile data fetched
  Bbox: (73.8567, 18.5204, 73.8667, 18.5304)
  Date range: 2026-02-22 to 2026-03-01
  Image size: 512x512
  Data size: 3145728 bytes

======================================================================
  ✓ SUCCESS: Sentinel Hub is working!
======================================================================

  You can now:
    - Fetch real satellite imagery
    - Calculate NDVI for any location
    - Monitor crop health

  Next: Run python scripts/test_api_keys.py
```

## Troubleshooting

### Authentication Failed

**Possible causes:**
1. Invalid Client ID or Secret
2. Credentials not activated yet (wait a few minutes after signup)
3. No processing units remaining
4. Network/firewall issues

**Check:**
- Sentinel Hub Dashboard: https://apps.sentinel-hub.com/dashboard/
- Verify credentials are correct in `.env`
- Check processing units quota

### No Data Available

If authentication works but no data is returned:
- Try a different date range (last 30 days)
- Check cloud coverage (test uses max 30%)
- Verify the location has Sentinel-2 coverage

## Next Steps

After successful test:

1. **Test all API keys**: `python scripts/test_api_keys.py`
2. **Get remaining keys**: See `GET_API_KEYS_GUIDE.md`
3. **Test real farmer workflow**: `python scripts/test_real_farmer.py`
