# Call Me Now - Quick Start

## Your Phone Number

The system is now configured to call: **+918095666788**

## Quick Test (Without Actual Call)

Run the end-to-end test to see everything working:

```powershell
# Terminal 1: Start server
.\venv\Scripts\Activate.ps1
uvicorn src.main:app --reload

# Terminal 2: Run test
.\venv\Scripts\Activate.ps1
python scripts/test_end_to_end.py
```

This will:
- Create farmer with your number
- Analyze crop stress
- Generate advisory in Hindi
- Prepare voice message
- Show what would be said in the call

## Make Actual Call

To receive a real call on your phone:

### Step 1: Get Twilio Account (5 minutes)

1. Go to https://www.twilio.com/try-twilio
2. Sign up (free $15 credit)
3. Verify your number: +918095666788
4. Get a Twilio phone number

### Step 2: Add Credentials to .env

```env
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=your_auth_token
TWILIO_PHONE_NUMBER=+1234567890
```

### Step 3: Set Up ngrok (for webhook)

```powershell
# Download from https://ngrok.com/download
# Then run:
ngrok http 8000
```

Copy the HTTPS URL (e.g., `https://abc123.ngrok.io`)

### Step 4: Make the Call

```powershell
.\venv\Scripts\Activate.ps1
python scripts/make_real_call.py
```

Enter your ngrok URL when prompted:
```
https://abc123.ngrok.io/voice/advisory
```

Confirm with "yes" and your phone will ring!

## What You'll Hear

The call will say in Hindi:

> नमस्ते। यह कृषि मित्र है।
> 
> आपकी फसल में पानी की कमी के संकेत दिख रहे हैं।
> जोखिम स्कोर 75 प्रतिशत है।
> 
> तुरंत करने योग्य कार्य:
> पहला: अगले 24 घंटे में सिंचाई करें। लागत लगभग 500 रुपये।
> दूसरा: 3 दिन में मल्चिंग करें। लागत लगभग 1250 रुपये।
> 
> कुल अनुमानित लागत 1750 रुपये है।

**Translation**: "Hello, this is KrishiMitra. Your crop shows water shortage. Risk score 75%. Action 1: Irrigate within 24 hours, cost 500 rupees. Action 2: Apply mulch within 3 days, cost 1250 rupees. Total cost 1750 rupees."

## Cost

- **Per call**: ~₹1.40 (2 minutes)
- **Free trial**: $15 credit = ~880 calls
- **Perfect for testing!**

## Files Updated

- `scripts/test_end_to_end.py` - Now uses +918095666788
- `scripts/make_real_call.py` - New script for actual calls
- `MAKE_REAL_CALL_GUIDE.md` - Detailed instructions

## Troubleshooting

**No Twilio account?**
- Test runs in simulation mode
- Shows what would be said
- No actual call made

**Call not connecting?**
- Verify phone number in Twilio Console
- Check Twilio credits
- Verify ngrok URL is accessible

**Need help?**
- See MAKE_REAL_CALL_GUIDE.md for detailed steps
- Check Twilio Console > Logs for errors

## Next Steps

1. Test without calling (simulation mode)
2. Set up Twilio account
3. Make first test call
4. Verify you receive the advisory
5. Deploy to production!

Ready to test? Run:
```powershell
python scripts/test_end_to_end.py
```
