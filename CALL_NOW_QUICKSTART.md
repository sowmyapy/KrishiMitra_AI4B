# Make Your First Voice Call - 5 Minute Quickstart

## What You'll Do

Make an actual voice call to your phone (+918095666788) with a Hindi farming advisory using Twilio and ngrok.

## Prerequisites Check

✓ Twilio credentials in `.env` (already configured)
✓ Server code ready (just updated with voice endpoints)
✓ Python environment activated

## Step-by-Step Instructions

### 1. Download ngrok (2 minutes)

**Option A: Direct Download**
1. Go to: https://ngrok.com/download
2. Click "Download for Windows"
3. Extract ZIP to `C:\ngrok\`

**Option B: Using Chocolatey** (if you have it)
```powershell
choco install ngrok
```

### 2. Open 3 PowerShell Terminals

You'll need 3 separate terminals running simultaneously.

#### Terminal 1: Start Server

```powershell
cd C:\Users\Sowmya\OneDrive\projects\ai_crop_system
.\venv\Scripts\Activate.ps1
uvicorn src.main:app --reload
```

Wait for:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
```

**Keep this running!**

#### Terminal 2: Start ngrok

```powershell
# If extracted to C:\ngrok
cd C:\ngrok
.\ngrok.exe http 8000

# Or if ngrok is in PATH
ngrok http 8000
```

You'll see:
```
Forwarding  https://abc123.ngrok.io -> http://localhost:8000
```

**Copy the HTTPS URL** (e.g., `https://abc123.ngrok.io`)

**Keep this running!**

#### Terminal 3: Make the Call

```powershell
cd C:\Users\Sowmya\OneDrive\projects\ai_crop_system
.\venv\Scripts\Activate.ps1
python scripts/make_real_call.py
```

### 3. Follow the Prompts

The script will show:
```
======================================================================
  KrishiMitra - Real Voice Call Test
======================================================================

Farmer Details:
  Phone: +918095666788
  Language: hi

Advisory Details:
  Type: water_stress
  Risk Score: 75/100
  Total Cost: ₹1750

...

Enter your webhook URL (or press Enter to skip):
```

**Type your ngrok URL** with `/voice/advisory` at the end:
```
https://abc123.ngrok.io/voice/advisory
```

Then confirm:
```
Proceed with call? (yes/no): yes
```

### 4. Answer Your Phone!

Within seconds, you'll receive a call on +918095666788.

You'll hear (in Hindi):
- Greeting from KrishiMitra
- Water stress alert (75% risk)
- Two recommended actions with costs
- Total estimated cost: ₹1750
- Option to press 1 to replay

## What Each Terminal Does

| Terminal | Purpose | Command |
|----------|---------|---------|
| 1 | FastAPI server | `uvicorn src.main:app --reload` |
| 2 | Public tunnel | `ngrok http 8000` |
| 3 | Call script | `python scripts/make_real_call.py` |

## Troubleshooting

### ngrok: command not found

**Solution**: Use full path
```powershell
C:\ngrok\ngrok.exe http 8000
```

### Server not running

**Error**: "Connection refused"

**Solution**: Make sure Terminal 1 is running with uvicorn

### Twilio error: Phone not verified

**For trial accounts only**:
1. Go to: https://console.twilio.com/
2. Phone Numbers > Verified Caller IDs
3. Add +918095666788
4. Verify via SMS

### Call connects but no audio

**Check**:
- ngrok is running (Terminal 2)
- Webhook URL is correct (includes `/voice/advisory`)
- Server logs show incoming request

### Call fails immediately

**Check Twilio Console**:
1. Go to: https://console.twilio.com/
2. Monitor > Logs > Calls
3. Click on your call
4. See detailed error message

## Expected Output

### Terminal 1 (Server)
```
INFO:     127.0.0.1:54321 - "POST /voice/advisory HTTP/1.1" 200 OK
```

### Terminal 2 (ngrok)
```
POST /voice/advisory           200 OK
```

### Terminal 3 (Script)
```
✓ Call initiated successfully!

Call Details:
  Call SID: CAxxxxxxxxxxxxx
  To: +918095666788
  From: +918095666788
  Status: queued
  
The call should arrive at +918095666788 shortly!
```

### Your Phone
- Incoming call from your Twilio number
- Hindi voice message about water stress
- Clear audio quality
- Option to press 1 to replay

## Cost

**Twilio Trial**: $15 free credit
**Per call**: ~$0.017 (₹1.40)
**Calls possible**: ~880 with trial credit

## Next Steps After Success

1. **Test with real farmer data**:
   ```powershell
   python scripts/test_real_farmer.py
   ```

2. **Add more advisory types**:
   - Pest alerts
   - Weather warnings
   - Harvest timing

3. **Implement call scheduling**:
   - Respect calling hours (9 AM - 7 PM)
   - Retry failed calls
   - Track farmer preferences

4. **Deploy to production**:
   - Use permanent webhook URL
   - Set up monitoring
   - Configure alerts

## Quick Reference Card

```
┌─────────────────────────────────────────────┐
│  Terminal 1: Server                         │
│  uvicorn src.main:app --reload              │
├─────────────────────────────────────────────┤
│  Terminal 2: ngrok                          │
│  ngrok http 8000                            │
│  Copy: https://abc123.ngrok.io             │
├─────────────────────────────────────────────┤
│  Terminal 3: Call Script                    │
│  python scripts/make_real_call.py           │
│  Webhook: https://abc123.ngrok.io/voice/... │
│  Confirm: yes                               │
└─────────────────────────────────────────────┘
```

## Success! 🎉

If you heard the Hindi advisory on your phone, congratulations! You've successfully integrated:
- ✓ FastAPI backend
- ✓ Twilio voice calls
- ✓ AWS Polly text-to-speech
- ✓ Real-time webhook handling
- ✓ Multi-language support

Your KrishiMitra voice calling system is now operational!

## Support

**Need help?**
- Check server logs (Terminal 1)
- Check ngrok logs (Terminal 2)
- Check Twilio Console logs
- Review `MAKE_REAL_CALL_GUIDE.md` for detailed troubleshooting

**Ready to scale?**
- See `VOICE_CALL_ALTERNATIVES.md` for production options
- Consider Exotel for 50% cost savings in India
- Set up proper call scheduling and monitoring
