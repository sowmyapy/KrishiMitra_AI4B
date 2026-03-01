# Setup Webhook URL - Quick Start

## What You Need

Your script is ready to make calls! You just need a public webhook URL so Twilio can communicate with your app.

## Quick Setup (5 minutes)

### Step 1: Install ngrok

**Windows PowerShell**:
```powershell
# Download ngrok
# Go to: https://ngrok.com/download
# Download Windows ZIP
# Extract to a folder (e.g., C:\ngrok)
```

**Or use Chocolatey** (if installed):
```powershell
choco install ngrok
```

### Step 2: Start Your Server

Open PowerShell terminal 1:
```powershell
cd C:\Users\Sowmya\OneDrive\projects\ai_crop_system
.\venv\Scripts\Activate.ps1
uvicorn src.main:app --reload
```

Keep this running!

### Step 3: Start ngrok

Open PowerShell terminal 2:
```powershell
# If ngrok is in C:\ngrok
cd C:Program Files\ngrok
.\ngrok.exe http 8000

# Or if ngrok is in PATH
ngrok http 8000
```

You'll see output like:
```
Forwarding  https://abc123.ngrok.io -> http://localhost:8000
```

**Copy the HTTPS URL**: `https://abc123.ngrok.io`

### Step 4: Make the Call

Open PowerShell terminal 3:
```powershell
cd C:\Users\Sowmya\OneDrive\projects\ai_crop_system
.\venv\Scripts\Activate.ps1
python scripts/make_real_call.py
```

When prompted:
```
Enter your webhook URL (or press Enter to skip): https://abc123.ngrok.io/voice/advisory
```

Type `yes` to confirm the call.

## What Happens Next

1. Script calls Twilio API
2. Twilio calls your phone: +918095666788
3. You answer the call
4. You hear the Hindi advisory message
5. Call completes

## Troubleshooting

### ngrok not found

**Solution**: Add ngrok to PATH or use full path:
```powershell
C:\ngrok\ngrok.exe http 8000
```

### Server not running

**Error**: Connection refused

**Solution**: Make sure `uvicorn src.main:app --reload` is running in terminal 1

### Twilio credentials missing

**Check .env file** has:
```env
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=your_auth_token_here
TWILIO_PHONE_NUMBER=+1234567890
```

### Phone number not verified

**For Twilio trial accounts**:
1. Go to: https://console.twilio.com/
2. Navigate to: Phone Numbers > Verified Caller IDs
3. Add +918095666788
4. Verify via SMS code

## Alternative: Test Without Webhook

If you want to test the TwiML generation without making a call:

```powershell
python scripts/make_real_call.py
# Press Enter when asked for webhook URL
```

This will:
- Generate the Hindi advisory message
- Create the TwiML
- Show you what would be sent
- Skip the actual call

## Next: Add Voice Endpoints

After successful test, you'll want to add proper voice endpoints to handle Twilio callbacks. But for now, this basic setup will work for testing!

## Quick Reference

**3 Terminals Needed**:
1. Server: `uvicorn src.main:app --reload`
2. ngrok: `ngrok http 8000`
3. Script: `python scripts/make_real_call.py`

**Webhook URL Format**:
```
https://[your-ngrok-id].ngrok.io/voice/advisory
```

Ready to receive your first AI-powered farming advisory call! 📞🌾
