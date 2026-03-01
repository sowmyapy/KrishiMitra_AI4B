# API Keys Setup - Quick Checklist

## ✅ Checklist

Use this to track your progress:

### 1. Sentinel Hub (Satellite Data)
- [ ] Go to https://www.sentinel-hub.com/
- [ ] Sign up for free trial
- [ ] Create OAuth client
- [ ] Copy Client ID
- [ ] Copy Client Secret
- [ ] Add to `.env` file
- [ ] Test: `python scripts/test_api_keys.py`

**Time**: 10 minutes  
**Cost**: FREE (1 month trial)

---

### 2. OpenWeatherMap (Weather Data)
- [ ] Go to https://openweathermap.org/api
- [ ] Sign up for free account
- [ ] Get API key from dashboard
- [ ] Copy API key
- [ ] Add to `.env` file
- [ ] Wait 10 minutes for activation
- [ ] Test: `python scripts/test_api_keys.py`

**Time**: 5 minutes  
**Cost**: FREE forever

---

### 3. Twilio (Voice Calls)
- [ ] Go to https://www.twilio.com/try-twilio
- [ ] Sign up for trial
- [ ] Verify your email
- [ ] Verify your phone (+918095666788)
- [ ] Get Account SID
- [ ] Get Auth Token
- [ ] Get Twilio phone number
- [ ] Verify your phone as caller ID
- [ ] Add all to `.env` file
- [ ] Test: `python scripts/test_api_keys.py`

**Time**: 15 minutes  
**Cost**: $15 FREE credit

---

## Quick Commands

### Test All Keys
```powershell
.\venv\Scripts\Activate.ps1
python scripts/test_api_keys.py
```

### Update .env File
```powershell
notepad .env
```

Add these lines:
```env
# Sentinel Hub
SENTINEL_HUB_CLIENT_ID=your_client_id_here
SENTINEL_HUB_CLIENT_SECRET=your_client_secret_here

# OpenWeatherMap
OPENWEATHERMAP_API_KEY=your_api_key_here

# Twilio
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=your_token_here
TWILIO_PHONE_NUMBER=+1234567890
```

---

## Priority Order

If you want to test incrementally:

### Priority 1: OpenWeatherMap (Easiest)
- Takes 5 minutes
- Works immediately
- Enables weather analysis

### Priority 2: Twilio (For Voice Calls)
- Takes 15 minutes
- Enables actual phone calls
- Most impressive demo feature

### Priority 3: Sentinel Hub (Most Complex)
- Takes 10 minutes
- Enables real satellite data
- Can work with simulated data initially

---

## Verification Steps

After adding each key:

1. **Save .env file**
2. **Run test**:
   ```powershell
   python scripts/test_api_keys.py
   ```
3. **Check output** for ✓ marks

---

## What Each Key Enables

| API Key | Enables | Without It |
|---------|---------|------------|
| Sentinel Hub | Real satellite NDVI data | Uses simulated data |
| OpenWeatherMap | Real weather conditions | Uses simulated data |
| Twilio | Actual voice calls | Call simulation only |
| AWS | Voice TTS/STT, LLM | Already configured ✓ |

---

## Troubleshooting

### Can't find where to add keys?

Open `.env` file in your project root:
```powershell
notepad .env
```

### Keys not working?

1. Check for typos
2. Remove extra spaces
3. Ensure no quotes around values
4. Restart server after changes

### Still having issues?

See detailed guide: `GET_API_KEYS_GUIDE.md`

---

## After Setup

Once all keys are configured:

1. **Test configuration**:
   ```powershell
   python scripts/test_api_keys.py
   ```

2. **Run real farmer test**:
   ```powershell
   python scripts/test_real_farmer.py
   ```

3. **Make test call**:
   ```powershell
   python scripts/make_real_call.py
   ```

---

## Time & Cost Summary

| Service | Setup Time | Cost |
|---------|------------|------|
| Sentinel Hub | 10 min | FREE (1 month) |
| OpenWeatherMap | 5 min | FREE (forever) |
| Twilio | 15 min | $15 credit FREE |
| **Total** | **30 min** | **FREE** |

---

## Support

Need help? Check:
- `GET_API_KEYS_GUIDE.md` - Detailed instructions with screenshots
- `API_KEYS_GUIDE.md` - Original guide
- Service documentation links in guides

---

Ready to get started? Begin with OpenWeatherMap (easiest)! 🚀
