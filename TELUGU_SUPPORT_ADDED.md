# Telugu Language Support Added

## Changes Made

### 1. Voice Webhook Error Handling (`src/api/voice.py`)
- Added comprehensive error handling to prevent "application error" messages
- Added detailed logging to track webhook execution
- Returns graceful error messages instead of crashing
- Logs all Twilio form data for debugging

### 2. Telugu Advisory Text (`src/api/advisories.py`)
- Added full Telugu translation for advisory generation
- Supports all stress types in Telugu:
  - తీవ్రమైన ఒత్తిడి (Severe Stress)
  - నీటి కొరత (Water Stress)
  - వేడి ఒత్తిడి (Heat Stress)
  - మితమైన ఒత్తిడి (Moderate Stress)
  - సాధారణ ఒత్తిడి (General Stress)
  - ఆరోగ్యకరమైన (Healthy)

### 3. Telugu Advisory Content
Full advisory includes:
- Greeting: "నమస్కారం రైతు గారు" (Hello Farmer)
- Crop analysis with NDVI, temperature, humidity
- Status and risk score
- Immediate actions with costs in Telugu
- Weather information
- Closing: "ధన్యవాదాలు" (Thank you)

## How to Test

### Step 1: Restart Backend
```powershell
# Stop backend (Ctrl+C or stop script)
.\stop_all.ps1

# Start backend again
.\start_all.ps1
```

Or just restart backend:
```powershell
python -m uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

### Step 2: Update Farmer Language
1. Go to http://localhost:3000
2. Navigate to Farmers → Select a farmer
3. Click "Edit" button
4. Change language to "Telugu (తెలుగు)"
5. Click "Update"

### Step 3: Generate New Advisory
1. Click "Generate Advisory" button
2. Wait for success message
3. The advisory will be created in Telugu

### Step 4: Make Voice Call
1. Click "Make Voice Call" button
2. The farmer will receive a call
3. The call will be in Telugu with Telugu text-to-speech

## What You'll Hear

The voice call will say (in Telugu):
1. Greeting: "నమస్కారం, ఇది కృషి మిత్ర" (Hello, this is KrishiMitra)
2. Advisory content in Telugu
3. Replay prompt: "సందేశాన్ని మళ్లీ వినడానికి 1 నొక్కండి" (Press 1 to replay)
4. Goodbye: "ధన్యవాదాలు. నమస్కారం" (Thank you. Goodbye)

## Supported Languages

| Language | Code | Advisory | Voice | Status |
|----------|------|----------|-------|--------|
| Hindi | hi | ✅ | ✅ | Fully Supported |
| English | en | ✅ | ✅ | Fully Supported |
| Telugu | te | ✅ | ✅ | Fully Supported |
| Tamil | ta | ⚠️ | ✅ | Voice only (uses English advisory) |
| Marathi | mr | ⚠️ | ✅ | Voice only (uses English advisory) |

## Adding More Languages

To add Tamil or Marathi advisory text, add another `elif` block in `src/api/advisories.py`:

```python
elif farmer.preferred_language == "ta":  # Tamil
    stress_desc = {
        "severe_stress": "கடுமையான அழுத்தம்",
        "water_stress": "நீர் பற்றாக்குறை",
        # ... etc
    }.get(stress_type, "அழுத்தம்")
    
    advisory_text = f"""
வணக்கம் விவசாயி,
# ... Tamil content
"""
```

## Troubleshooting

### Still getting "application error"?
- Check backend logs for detailed error messages
- Verify backend was restarted after code changes
- Check ngrok is running and URL is correct in .env

### Advisory still in English?
- Make sure you generated a NEW advisory after changing language
- Old advisories remain in their original language
- Check farmer's language was actually updated (refresh page)

### Voice call not in Telugu?
- Verify the advisory text is in Telugu (check Advisories page)
- Make sure Twilio supports Telugu (te-IN) - it does!
- Check backend logs for language detection

## Technical Details

### Advisory Generation Flow:
1. User clicks "Generate Advisory"
2. Backend fetches farmer's `preferred_language` from database
3. Generates advisory text in that language
4. Saves to database with language-specific content

### Voice Call Flow:
1. User clicks "Make Voice Call"
2. Twilio initiates call to farmer's phone
3. Twilio calls webhook: `/api/v1/voice/advisory`
4. Webhook fetches farmer by phone number
5. Gets farmer's `preferred_language`
6. Retrieves latest advisory (already in Telugu)
7. Generates TwiML with Telugu language code (te-IN)
8. Twilio reads Telugu text with Telugu TTS
9. Farmer hears advisory in Telugu!

## Files Modified

- `src/api/voice.py` - Better error handling
- `src/api/advisories.py` - Telugu advisory text generation

## Next Steps

To add more languages:
1. Add translation in `src/api/advisories.py`
2. Verify Twilio supports the language
3. Test with a farmer who speaks that language
4. Update this documentation

Enjoy your multilingual agricultural advisory system! 🌾
