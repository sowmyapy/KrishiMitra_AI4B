# Get API Keys - Complete Step-by-Step Guide

## Overview

You need 3 API keys for real farmer testing:
1. **Sentinel Hub** - Satellite imagery (FREE trial)
2. **OpenWeatherMap** - Weather data (FREE tier)
3. **Twilio** - Voice calls ($15 FREE credit)

Total time: ~30 minutes

---

## 1. Sentinel Hub (Satellite Imagery)

### What You Get
- Free trial: 1 month
- 10,000 processing units/month
- Access to Sentinel-2 satellite data
- 10m resolution imagery

### Step-by-Step Instructions

#### Step 1: Sign Up (5 minutes)

1. **Go to**: https://www.sentinel-hub.com/
2. **Click**: "Try now" or "Sign up"
3. **Fill in**:
   - Email: your.email@example.com
   - Password: (create strong password)
   - Name: Your Name
   - Company: (optional, can put "Individual" or "Research")
4. **Click**: "Create account"
5. **Verify email**: Check inbox and click verification link

#### Step 2: Create OAuth Client (5 minutes)

1. **Login** to Sentinel Hub
2. **Go to**: Dashboard (top right, click your name)
3. **Click**: "User settings" (gear icon)
4. **Navigate to**: "OAuth clients" tab on left sidebar
5. **Click**: "Create new OAuth client" button
6. **Fill in**:
   - Name: `KrishiMitra`
   - Description: `Farmer early warning system`
   - Redirect URIs: Leave empty (not needed for server-to-server)
7. **Click**: "Create"
8. **IMPORTANT**: Copy these immediately (shown only once):
   ```
   Client ID: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
   Client Secret: xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
   ```

#### Step 3: Add to .env File

Open your `.env` file and add:

```env
SENTINEL_HUB_CLIENT_ID=your_client_id_here
SENTINEL_HUB_CLIENT_SECRET=your_client_secret_here
```

#### Step 4: Test Connection

```powershell
.\venv\Scripts\Activate.ps1
python -c "from src.services.data_ingestion.satellite_client import SatelliteDataClient; print('✓ Sentinel Hub configured')"
```

### Troubleshooting

**Issue**: Can't find OAuth clients
- **Solution**: Make sure you're logged in, look for "User settings" or "Configuration"

**Issue**: Lost client secret
- **Solution**: Delete the client and create a new one

**Issue**: API quota exceeded
- **Solution**: Check usage in dashboard, wait for monthly reset

---

## 2. OpenWeatherMap (Weather Data)

### What You Get
- Free tier: Forever free
- 60 calls/minute
- 1,000,000 calls/month
- Current weather + 7-day forecast

### Step-by-Step Instructions

#### Step 1: Sign Up (3 minutes)

1. **Go to**: https://openweathermap.org/api
2. **Click**: "Sign Up" (top right)
3. **Fill in**:
   - Username: your_username
   - Email: your.email@example.com
   - Password: (create password)
   - Age verification: Check box
   - Terms: Check box
4. **Click**: "Create Account"
5. **Verify email**: Check inbox and click verification link

#### Step 2: Get API Key (2 minutes)

1. **Login** to OpenWeatherMap
2. **Go to**: https://home.openweathermap.org/api_keys
   - Or click your username > "My API keys"
3. **You'll see**: Default API key already created
4. **Copy the key**: 
   ```
   API Key: xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
   ```
5. **Note**: Key activation takes ~10 minutes (but usually works immediately)

#### Step 3: Add to .env File

Open your `.env` file and add:

```env
OPENWEATHERMAP_API_KEY=your_api_key_here
```

#### Step 4: Test Connection

```powershell
.\venv\Scripts\Activate.ps1
python -c "from src.services.data_ingestion.weather_client import WeatherClient; print('✓ OpenWeatherMap configured')"
```

### Troubleshooting

**Issue**: API key not working
- **Solution**: Wait 10-15 minutes for activation, then try again

**Issue**: 401 Unauthorized
- **Solution**: Check API key is copied correctly (no extra spaces)

**Issue**: Rate limit exceeded
- **Solution**: Free tier allows 60 calls/minute, wait a minute and retry

---

## 3. Twilio (Voice Calls)

### What You Get
- Free trial: $15 credit
- ~880 calls to India
- SMS capability
- Phone number included

### Step-by-Step Instructions

#### Step 1: Sign Up (5 minutes)

1. **Go to**: https://www.twilio.com/try-twilio
2. **Click**: "Sign up"
3. **Fill in**:
   - Email: your.email@example.com
   - Password: (create strong password)
4. **Click**: "Start your free trial"
5. **Verify email**: Check inbox and click link
6. **Verify phone**: 
   - Enter your phone: +918095666788
   - Receive SMS code
   - Enter code

#### Step 2: Get Account Credentials (3 minutes)

1. **After signup**: You'll see the Console Dashboard
2. **Find these on dashboard**:
   ```
   Account SID: ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
   Auth Token: Click "Show" to reveal
   ```
3. **Copy both values**

#### Step 3: Get a Phone Number (5 minutes)

1. **In Console**: Click "Get a Trial Number" button
   - Or go to: Phone Numbers > Manage > Buy a number
2. **For trial**: Twilio assigns you a number automatically
3. **Click**: "Choose this number"
4. **Copy**: Your Twilio phone number
   ```
   Phone Number: +1234567890
   ```

#### Step 4: Verify Your Phone Number (2 minutes)

**IMPORTANT**: Trial accounts can only call verified numbers

1. **Go to**: Phone Numbers > Manage > Verified Caller IDs
   - Or: https://console.twilio.com/us1/develop/phone-numbers/manage/verified
2. **Click**: "Add a new number" (red + button)
3. **Enter**: +918095666788
4. **Click**: "Text you instead" (if SMS is easier)
5. **Enter code**: From SMS
6. **Click**: "Submit"
7. **Status**: Should show "Verified" ✓

#### Step 5: Add to .env File

Open your `.env` file and add:

```env
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=your_auth_token_here
TWILIO_PHONE_NUMBER=+1234567890
```

#### Step 6: Test Connection

```powershell
.\venv\Scripts\Activate.ps1
python -c "from twilio.rest import Client; from src.config.settings import settings; client = Client(settings.twilio_account_sid, settings.twilio_auth_token); print('✓ Twilio configured')"
```

### Troubleshooting

**Issue**: Can't find Account SID
- **Solution**: Go to Console home, it's at the top of the page

**Issue**: Phone number not verified
- **Solution**: Go to Verified Caller IDs and add +918095666788

**Issue**: Trial account limitations
- **Solution**: Trial can only call verified numbers. Verify your number first.

**Issue**: Can't make calls
- **Solution**: Check you have trial credit ($15), verify destination number

---

## Complete .env File Example

After getting all keys, your `.env` should look like:

```env
# Application
APP_NAME=KrishiMitra
ENVIRONMENT=development

# Database
DATABASE_URL=sqlite:///./krishimitra.db

# AWS (Already configured)
AWS_REGION=ap-south-1
AWS_ACCESS_KEY_ID=your_existing_key
AWS_SECRET_ACCESS_KEY=your_existing_secret

# Sentinel Hub (NEW)
SENTINEL_HUB_CLIENT_ID=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
SENTINEL_HUB_CLIENT_SECRET=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# OpenWeatherMap (NEW)
OPENWEATHERMAP_API_KEY=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# Twilio (NEW)
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_PHONE_NUMBER=+1234567890

# LLM Provider
LLM_PROVIDER=bedrock
USE_AWS_SERVICES=True

# Security (Already configured)
JWT_SECRET_KEY=your_existing_secret
ENCRYPTION_KEY=your_existing_key
```

---

## Verify All Keys Work

Run this test script:

```powershell
.\venv\Scripts\Activate.ps1
python scripts/test_api_keys.py
```

Create `scripts/test_api_keys.py`:

```python
#!/usr/bin/env python3
"""Test all API keys"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.config.settings import settings

print("Testing API Keys...")
print("="*50)

# Test Sentinel Hub
try:
    assert settings.sentinel_hub_client_id
    assert settings.sentinel_hub_client_secret
    print("✓ Sentinel Hub: Configured")
except:
    print("✗ Sentinel Hub: Not configured")

# Test OpenWeatherMap
try:
    assert settings.openweathermap_api_key
    print("✓ OpenWeatherMap: Configured")
except:
    print("✗ OpenWeatherMap: Not configured")

# Test Twilio
try:
    assert settings.twilio_account_sid
    assert settings.twilio_auth_token
    assert settings.twilio_phone_number
    print("✓ Twilio: Configured")
except:
    print("✗ Twilio: Not configured")

# Test AWS
try:
    assert settings.aws_access_key_id
    assert settings.aws_secret_access_key
    print("✓ AWS: Configured")
except:
    print("✗ AWS: Not configured")

print("="*50)
print("Configuration check complete!")
```

---

## Cost Summary

### Free Tier Limits

**Sentinel Hub**:
- Free: 1 month trial
- Then: ~$0.01 per processing unit
- Typical usage: 100-200 units/farmer/month = $1-2/month

**OpenWeatherMap**:
- Free: Forever (1M calls/month)
- Typical usage: 100 calls/farmer/month = FREE

**Twilio**:
- Free: $15 trial credit
- Then: $0.0085/minute to India
- Typical usage: 2 min/call × 4 calls/month = $0.068/farmer/month

**Total Cost**: ~$1-2/farmer/month (well within budget!)

---

## Security Best Practices

1. **Never commit .env to git**
   ```powershell
   # Verify .env is in .gitignore
   git status | Select-String ".env"
   # Should only show .env.example
   ```

2. **Rotate keys regularly**
   - Every 90 days for production
   - Immediately if compromised

3. **Use environment variables**
   - Never hardcode keys in code
   - Always use settings.py

4. **Monitor usage**
   - Check dashboards weekly
   - Set up billing alerts
   - Watch for unusual activity

---

## Next Steps

After getting all API keys:

1. **Update .env file** with all keys
2. **Test configuration**: `python scripts/test_api_keys.py`
3. **Run real farmer test**: `python scripts/test_real_farmer.py`
4. **Make test call**: `python scripts/make_real_call.py`

---

## Support Links

- **Sentinel Hub**: https://www.sentinel-hub.com/faq/
- **OpenWeatherMap**: https://openweathermap.org/faq
- **Twilio**: https://support.twilio.com/

## Quick Reference

| Service | Sign Up | Dashboard | Docs |
|---------|---------|-----------|------|
| Sentinel Hub | [Link](https://www.sentinel-hub.com/) | [Link](https://apps.sentinel-hub.com/dashboard/) | [Link](https://docs.sentinel-hub.com/) |
| OpenWeatherMap | [Link](https://openweathermap.org/api) | [Link](https://home.openweathermap.org/) | [Link](https://openweathermap.org/api/one-call-api) |
| Twilio | [Link](https://www.twilio.com/try-twilio) | [Link](https://console.twilio.com/) | [Link](https://www.twilio.com/docs/voice) |

---

Good luck! You're now ready to test with real satellite and weather data! 🛰️🌦️📞
