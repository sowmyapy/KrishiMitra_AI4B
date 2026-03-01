# Voice Call Flow Diagram

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     Voice Call System Flow                       │
└─────────────────────────────────────────────────────────────────┘

1. INITIATE CALL
   ┌──────────────┐
   │ Your Script  │  python scripts/make_real_call.py
   │ (Terminal 3) │
   └──────┬───────┘
          │ HTTP POST
          ▼
   ┌──────────────┐
   │   Twilio     │  Makes outbound call
   │   API        │
   └──────┬───────┘
          │ Phone Call
          ▼
   ┌──────────────┐
   │ Your Phone   │  +918095666788 rings
   │              │
   └──────────────┘


2. CALL CONNECTED - WEBHOOK REQUEST
   ┌──────────────┐
   │ Your Phone   │  You answer the call
   │              │
   └──────┬───────┘
          │ Call Connected Event
          ▼
   ┌──────────────┐
   │   Twilio     │  Requests TwiML instructions
   │              │
   └──────┬───────┘
          │ HTTP POST
          ▼
   ┌──────────────┐
   │    ngrok     │  https://abc123.ngrok.io/voice/advisory
   │ (Terminal 2) │  Public tunnel
   └──────┬───────┘
          │ Forwards to localhost:8000
          ▼
   ┌──────────────┐
   │ FastAPI      │  POST /voice/advisory
   │ (Terminal 1) │  Generates TwiML response
   └──────┬───────┘
          │ Returns TwiML XML
          ▼
   ┌──────────────┐
   │    ngrok     │  Forwards response
   │              │
   └──────┬───────┘
          │ TwiML XML
          ▼
   ┌──────────────┐
   │   Twilio     │  Executes TwiML instructions
   │              │  - Say greeting
   └──────┬───────┘  - Say advisory
          │          - Gather input (press 1)
          │ Audio Stream
          ▼
   ┌──────────────┐
   │ Your Phone   │  You hear Hindi advisory
   │              │
   └──────────────┘


3. OPTIONAL: REPLAY (if you press 1)
   ┌──────────────┐
   │ Your Phone   │  Press 1 to replay
   │              │
   └──────┬───────┘
          │ DTMF tone "1"
          ▼
   ┌──────────────┐
   │   Twilio     │  Detects digit press
   │              │
   └──────┬───────┘
          │ HTTP POST
          ▼
   ┌──────────────┐
   │    ngrok     │  /voice/advisory/replay
   │              │
   └──────┬───────┘
          │
          ▼
   ┌──────────────┐
   │ FastAPI      │  POST /voice/advisory/replay
   │              │  Generates replay TwiML
   └──────┬───────┘
          │ Returns TwiML
          ▼
          ... (same flow as step 2)


4. CALL ENDS
   ┌──────────────┐
   │ Your Phone   │  Call ends
   │              │
   └──────┬───────┘
          │ Hangup
          ▼
   ┌──────────────┐
   │   Twilio     │  Sends status callback
   │              │
   └──────┬───────┘
          │ HTTP POST
          ▼
   ┌──────────────┐
   │    ngrok     │  /voice/advisory/status
   │              │
   └──────┬───────┘
          │
          ▼
   ┌──────────────┐
   │ FastAPI      │  POST /voice/advisory/status
   │              │  Logs call completion
   └──────────────┘
```

## Component Details

### Terminal 1: FastAPI Server
```
Role: Backend API server
Port: 8000 (localhost)
Endpoints:
  - POST /voice/advisory          (main webhook)
  - POST /voice/advisory/replay   (replay handler)
  - POST /voice/advisory/status   (status callback)
  - POST /voice/advisory/recording (recording callback)

What it does:
  1. Receives webhook from Twilio (via ngrok)
  2. Generates TwiML XML response
  3. Returns instructions to Twilio
  4. Logs call events
```

### Terminal 2: ngrok Tunnel
```
Role: Public HTTPS tunnel to localhost
Public URL: https://abc123.ngrok.io
Local: http://localhost:8000

What it does:
  1. Exposes local server to internet
  2. Provides HTTPS endpoint for Twilio
  3. Forwards requests to FastAPI
  4. Returns responses to Twilio
```

### Terminal 3: Call Script
```
Role: Initiates the call
Script: scripts/make_real_call.py

What it does:
  1. Reads Twilio credentials from .env
  2. Calls Twilio API to initiate call
  3. Provides webhook URL
  4. Monitors call status
```

## Data Flow

### Request: Initiate Call
```
Script → Twilio API
{
  "to": "+918095666788",
  "from": "+918095666788",
  "url": "https://abc123.ngrok.io/voice/advisory"
}
```

### Response: Call Initiated
```
Twilio API → Script
{
  "call_sid": "CAxxxxx",
  "status": "queued",
  "to": "+918095666788"
}
```

### Request: Webhook (Call Connected)
```
Twilio → ngrok → FastAPI
POST /voice/advisory
{
  "CallSid": "CAxxxxx",
  "From": "+918095666788",
  "To": "+918095666788",
  "CallStatus": "in-progress"
}
```

### Response: TwiML Instructions
```
FastAPI → ngrok → Twilio
<?xml version="1.0" encoding="UTF-8"?>
<Response>
  <Say language="hi-IN">नमस्ते, यह कृषि मित्र है।</Say>
  <Pause length="1"/>
  <Say language="hi-IN">आपकी फसल में पानी की कमी...</Say>
  <Gather numDigits="1" action="/voice/advisory/replay">
    <Say language="hi-IN">संदेश दोबारा सुनने के लिए 1 दबाएं।</Say>
  </Gather>
  <Say language="hi-IN">धन्यवाद। नमस्ते।</Say>
  <Hangup/>
</Response>
```

## Timeline

```
Time    Event                           Component
─────────────────────────────────────────────────────────
0:00    Script calls Twilio API         Terminal 3
0:01    Twilio initiates call           Twilio
0:02    Your phone rings                Your Phone
0:05    You answer                      Your Phone
0:06    Twilio requests TwiML           Twilio → ngrok
0:06    FastAPI generates TwiML         Terminal 1
0:07    Twilio receives TwiML           Twilio
0:08    You hear greeting               Your Phone
0:10    You hear advisory               Your Phone
0:50    Advisory complete               Your Phone
0:51    Prompt to press 1               Your Phone
0:56    (timeout or press 1)            Your Phone
0:57    Goodbye message                 Your Phone
0:58    Call ends                       Your Phone
0:59    Status callback sent            Twilio → FastAPI
1:00    Call logged                     Terminal 1
```

## Error Handling

### Scenario 1: ngrok not running
```
Twilio → https://abc123.ngrok.io/voice/advisory
         ❌ Connection refused
         
Result: Call fails, Twilio plays error message
```

### Scenario 2: FastAPI not running
```
Twilio → ngrok → http://localhost:8000/voice/advisory
                 ❌ Connection refused
                 
Result: Call fails, Twilio plays error message
```

### Scenario 3: Invalid TwiML
```
FastAPI → Invalid XML
          
Result: Twilio plays error message
```

### Scenario 4: All systems operational
```
Twilio → ngrok → FastAPI → TwiML
         ✓      ✓         ✓
         
Result: Call succeeds, you hear advisory
```

## Security Notes

### What's Exposed
- ngrok URL is public (anyone can access)
- Webhook endpoints are public
- No authentication on webhooks (by design)

### What's Protected
- Twilio credentials in .env (not exposed)
- AWS credentials in .env (not exposed)
- Database (local, not exposed)
- Server only accessible via ngrok tunnel

### Production Considerations
- Add Twilio signature verification
- Use permanent HTTPS domain
- Add rate limiting
- Implement authentication
- Monitor for abuse

## Monitoring

### What to Watch

**Terminal 1 (FastAPI)**:
```
INFO:     127.0.0.1:54321 - "POST /voice/advisory HTTP/1.1" 200 OK
```
✓ Webhook received and processed

**Terminal 2 (ngrok)**:
```
POST /voice/advisory           200 OK
```
✓ Request forwarded successfully

**Terminal 3 (Script)**:
```
✓ Call initiated successfully!
Call SID: CAxxxxx
Status: queued
```
✓ Call created in Twilio

**Twilio Console**:
- Go to: https://console.twilio.com/
- Monitor > Logs > Calls
- See real-time call status

## Success Indicators

✓ Terminal 1 shows POST requests
✓ Terminal 2 shows 200 OK responses
✓ Terminal 3 shows call initiated
✓ Your phone rings
✓ You hear Hindi advisory
✓ Audio is clear
✓ Call completes without errors

## Quick Debug Checklist

```
□ Terminal 1 running? (uvicorn)
□ Terminal 2 running? (ngrok)
□ ngrok URL copied correctly?
□ Webhook URL includes /voice/advisory?
□ Twilio credentials in .env?
□ Phone number verified in Twilio?
□ Sufficient Twilio credits?
□ Internet connection stable?
```

All checked? You're ready to make the call! 📞
