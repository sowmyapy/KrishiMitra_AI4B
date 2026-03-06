# Voice Call Fix Summary

## Issue
"Failed to initiate call" error when clicking "Make Voice Call" button

## Root Cause
The `/api/v1/voice/call/{farmer_id}` endpoint was calling `voice_service.initiate_call()` with incorrect parameters:
- **Wrong**: `advisory_id` and `language` parameters
- **Correct**: `callback_url`, `farmer_id`, and `call_type` parameters

## Fix Applied

### 1. Updated Voice Call Endpoint (`src/api/voice.py`)
Changed the `initiate_call` method call to use correct parameters:

```python
# Before (WRONG)
call_result = await voice_service.initiate_call(
    to_number=farmer.phone_number,
    advisory_id=str(advisory.advisory_id),
    language=farmer.preferred_language
)

# After (CORRECT)
call_result = await voice_service.initiate_call(
    to_number=farmer.phone_number,
    callback_url=callback_url,
    farmer_id=str(farmer_id),
    call_type="advisory"
)
```

### 2. Added NGROK_URL to .env
Added the ngrok URL to environment variables for proper webhook configuration:
```
NGROK_URL=https://emma-autecologic-gregg.ngrok-free.dev
```

### 3. Improved Frontend Error Messages
Updated the frontend to show detailed error messages including the Call SID on success.

## How Voice Calls Work

1. **User clicks "Make Voice Call"** on farmer detail page
2. **Frontend sends POST** to `/api/v1/voice/call/{farmer_id}`
3. **Backend checks**:
   - Farmer exists
   - Farmer has at least one advisory
4. **Backend initiates Twilio call** with:
   - `to_number`: Farmer's phone number
   - `callback_url`: Ngrok webhook URL (`/api/v1/voice/advisory`)
   - `farmer_id`: For tracking
   - `call_type`: "advisory"
5. **Twilio calls farmer** and requests TwiML from webhook
6. **Webhook returns TwiML** with advisory message in farmer's language
7. **Farmer hears advisory** and can press 1 to replay

## Testing

### Test from UI
1. Go to: http://localhost:3000/farmers
2. Click eye icon on any farmer
3. Generate an advisory first (if not already done)
4. Click "Make Voice Call"
5. Should see: "Voice call initiated! Call SID: CAxxxx..."
6. Farmer's phone will ring and deliver advisory in Hindi

### Test from API
```bash
# Generate advisory first
curl -X POST http://localhost:8000/api/v1/voice/call/fc008579-7fcb-4f31-8ab8-837ef8d44f83

# Expected response
{
  "status": "success",
  "call_sid": "CA0aa2a9bc543ca9f977ef4d6d0f6f9654",
  "message": "Call initiated to +918151910856"
}
```

## Requirements
- ✅ Ngrok tunnel running
- ✅ Twilio credentials configured
- ✅ Farmer has at least one advisory
- ✅ Phone number is verified in Twilio (for trial accounts)

## Verified Phone Numbers
- +918151910856 ✅ (Farmer: fc008579-7fcb-4f31-8ab8-837ef8d44f83)
- +918095666788 ✅ (Farmer: aa25b281-8515-4be1-a8de-25b244b403b5)

## Status
✅ **FIXED** - Voice calls now working from UI and API
