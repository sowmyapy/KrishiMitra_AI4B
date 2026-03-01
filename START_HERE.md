# START HERE - Test with 1 Farmer in 5 Minutes

No code changes needed. Just run these commands.

## ⚠️ Important: Enable Bedrock First (One-Time, 5 minutes)

You need to enable AWS Bedrock access first. See **ENABLE_BEDROCK.md** for instructions.

**Quick version**:
1. Go to: https://console.aws.amazon.com/bedrock
2. Click: Model access → Manage model access
3. Check: Claude 3.5 Sonnet v2
4. Fill form with "Agriculture" use case
5. Wait 15 minutes for approval

**Or skip for now** and test without AI conversations (Transcribe and Polly still work!)

---

## ✅ Step 1: Test AWS (30 seconds)

```powershell
python scripts/test_aws_integration.py
```

Should see 4 green checkmarks ✓

## ✅ Step 2: Setup Database (30 seconds)

```powershell
python scripts/init_db.py
```

## ✅ Step 3: Start Server (30 seconds)

```powershell
uvicorn src.main:app --reload
```

## ✅ Step 4: Open Browser (10 seconds)

Go to: **http://localhost:8000/docs**

## ✅ Step 5: Test with 1 Farmer (3 minutes)

### Register Farmer:
1. Click **POST /api/v1/farmers/register**
2. Click "Try it out"
3. Paste this:
```json
{
  "name": "Test Farmer",
  "phone": "+919876543210",
  "language": "hi",
  "location": {"latitude": 28.6139, "longitude": 77.2090}
}
```
4. Click "Execute"
5. Copy the `farmer_id`

### Test Voice Chat:
1. Click **POST /api/v1/voice/chat**
2. Click "Try it out"
3. Paste this (use your farmer_id):
```json
{
  "farmer_id": "paste_your_farmer_id_here",
  "text": "मेरी गेहूं की फसल में पीले पत्ते दिख रहे हैं"
}
```
4. Click "Execute"
5. See AI response in Hindi! 🎉

## Done! 🎉

You just tested:
- ✅ AWS Bedrock (AI conversations)
- ✅ AWS Polly (Voice generation)
- ✅ Farmer registration
- ✅ Voice chatbot
- ✅ Complete workflow

**Cost**: ~$1/month (mostly free tier)

## What Works Without External APIs?

Everything except:
- ❌ Actual phone calls (need Twilio)
- ❌ Real weather data (need Weather API)
- ❌ Real satellite images (need Sentinel Hub)

But you can test the complete logic via API! 🚀

## Add External APIs Later

When ready:
1. **Twilio** (15 min) - See API_KEYS_GUIDE.md
2. **Weather API** (5 min) - See API_KEYS_GUIDE.md
3. **Sentinel Hub** (20 min) - See API_KEYS_GUIDE.md

## Need Help?

- **TEST_NOW.md** - Detailed testing guide
- **SINGLE_FARMER_TEST.md** - Complete single farmer guide
- **API_KEYS_GUIDE.md** - How to get external API keys
- **TROUBLESHOOTING.md** - Common issues

---

**Current Status**: Ready to test with 1 farmer! 🎉
