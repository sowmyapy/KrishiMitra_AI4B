# 📱 Visual Quick Guide - Make Your First Call

## The 3-Terminal Setup

```
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│  TERMINAL 1: Server                                             │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │ PS> uvicorn src.main:app --reload                         │ │
│  │                                                            │ │
│  │ INFO: Uvicorn running on http://127.0.0.1:8000           │ │
│  │ INFO: Application startup complete                        │ │
│  │                                                            │ │
│  │ ✓ KEEP THIS RUNNING                                       │ │
│  └───────────────────────────────────────────────────────────┘ │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│  TERMINAL 2: ngrok                                              │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │ PS> C:\ngrok\ngrok.exe http 8000                          │ │
│  │                                                            │ │
│  │ Session Status    online                                  │ │
│  │ Forwarding        https://abc123.ngrok.io -> localhost    │ │
│  │                                                            │ │
│  │ ✓ COPY THIS URL: https://abc123.ngrok.io                 │ │
│  │ ✓ KEEP THIS RUNNING                                       │ │
│  └───────────────────────────────────────────────────────────┘ │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│  TERMINAL 3: Call Script                                        │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │ PS> python scripts/make_real_call.py                      │ │
│  │                                                            │ │
│  │ Enter webhook URL:                                        │ │
│  │ > https://abc123.ngrok.io/voice/advisory                  │ │
│  │                                                            │ │
│  │ Proceed with call? (yes/no):                              │ │
│  │ > yes                                                      │ │
│  │                                                            │ │
│  │ ✓ Call initiated!                                         │ │
│  └───────────────────────────────────────────────────────────┘ │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## What Happens Next

```
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│  YOUR PHONE: +918095666788                                      │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │                                                            │ │
│  │              📞 Incoming Call                              │ │
│  │                                                            │ │
│  │         From: +918095666788                                │ │
│  │                                                            │ │
│  │         [Answer]  [Decline]                                │ │
│  │                                                            │ │
│  └───────────────────────────────────────────────────────────┘ │
│                                                                 │
│  ✓ ANSWER THE CALL                                              │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

         ↓ You answer ↓

┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│  YOU HEAR (in Hindi):                                           │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │                                                            │ │
│  │  🔊 "नमस्ते। यह कृषि मित्र है।"                           │ │
│  │     (Hello. This is KrishiMitra.)                          │ │
│  │                                                            │ │
│  │  🔊 "आपकी फसल में पानी की कमी के संकेत दिख रहे हैं।"     │ │
│  │     (Your crop shows water shortage signs.)                │ │
│  │                                                            │ │
│  │  🔊 "जोखिम स्कोर 75 प्रतिशत है।"                          │ │
│  │     (Risk score is 75 percent.)                            │ │
│  │                                                            │ │
│  │  🔊 "पहला: अगले 24 घंटे में सिंचाई करें..."               │ │
│  │     (First: Irrigate within 24 hours...)                   │ │
│  │                                                            │ │
│  │  🔊 "दूसरा: 3 दिन में मल्चिंग करें..."                    │ │
│  │     (Second: Apply mulching within 3 days...)              │ │
│  │                                                            │ │
│  │  🔊 "कुल अनुमानित लागत 1750 रुपये है।"                    │ │
│  │     (Total estimated cost is 1750 rupees.)                 │ │
│  │                                                            │ │
│  │  🔊 "संदेश दोबारा सुनने के लिए 1 दबाएं।"                 │ │
│  │     (Press 1 to replay the message.)                       │ │
│  │                                                            │ │
│  └───────────────────────────────────────────────────────────┘ │
│                                                                 │
│  ✓ CLEAR AUDIO                                                  │
│  ✓ HINDI LANGUAGE                                               │
│  ✓ ACTIONABLE ADVICE                                            │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

         ↓ Optional: Press 1 ↓

┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│  IF YOU PRESS 1:                                                │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │                                                            │ │
│  │  🔊 Message replays from the beginning                     │ │
│  │                                                            │ │
│  │  (Same advisory message plays again)                       │ │
│  │                                                            │ │
│  └───────────────────────────────────────────────────────────┘ │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

         ↓ Call ends ↓

┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│  TERMINAL 1 (Server Logs):                                      │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │ INFO: 127.0.0.1 - "POST /voice/advisory HTTP/1.1" 200    │ │
│  │ INFO: Advisory call webhook: CAxxxxx, status: completed   │ │
│  └───────────────────────────────────────────────────────────┘ │
│                                                                 │
│  TERMINAL 2 (ngrok Logs):                                       │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │ POST /voice/advisory           200 OK                     │ │
│  └───────────────────────────────────────────────────────────┘ │
│                                                                 │
│  TERMINAL 3 (Script Output):                                    │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │ ✓ Call initiated successfully!                            │ │
│  │ Call SID: CAxxxxx                                         │ │
│  │ Status: completed                                         │ │
│  │ Duration: 58 seconds                                      │ │
│  └───────────────────────────────────────────────────────────┘ │
│                                                                 │
│  ✓ SUCCESS!                                                     │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## Step-by-Step Checklist

```
□ Step 1: Open PowerShell Terminal 1
  └─ Run: uvicorn src.main:app --reload
  └─ Wait for: "Uvicorn running on http://127.0.0.1:8000"
  └─ ✓ Keep running

□ Step 2: Open PowerShell Terminal 2
  └─ Run: C:\ngrok\ngrok.exe http 8000
  └─ Copy: https://abc123.ngrok.io
  └─ ✓ Keep running

□ Step 3: Open PowerShell Terminal 3
  └─ Run: python scripts/make_real_call.py
  └─ Enter: https://abc123.ngrok.io/voice/advisory
  └─ Type: yes

□ Step 4: Answer Your Phone
  └─ Phone: +918095666788 rings
  └─ Answer the call
  └─ Listen to Hindi advisory

□ Step 5: Verify Success
  └─ Heard greeting in Hindi
  └─ Heard water stress advisory
  └─ Heard cost estimates (₹1750)
  └─ Audio was clear
  └─ Call ended cleanly

✓ All steps complete? SUCCESS! 🎉
```

## Common Mistakes to Avoid

```
❌ WRONG: Using HTTP URL
   http://abc123.ngrok.io/voice/advisory
   
✓ RIGHT: Using HTTPS URL
   https://abc123.ngrok.io/voice/advisory

─────────────────────────────────────────

❌ WRONG: Forgetting /voice/advisory
   https://abc123.ngrok.io
   
✓ RIGHT: Including full path
   https://abc123.ngrok.io/voice/advisory

─────────────────────────────────────────

❌ WRONG: Closing ngrok too early
   (Call will fail if ngrok stops)
   
✓ RIGHT: Keep all 3 terminals running
   Until call completes

─────────────────────────────────────────

❌ WRONG: Not answering the phone
   (Call will timeout)
   
✓ RIGHT: Answer within 30 seconds
   Listen to the full message
```

## Troubleshooting Visual Guide

```
PROBLEM: ngrok not found
┌─────────────────────────────────────┐
│ PS> ngrok http 8000                 │
│ ngrok: command not found            │
└─────────────────────────────────────┘
         ↓
SOLUTION: Use full path
┌─────────────────────────────────────┐
│ PS> C:\ngrok\ngrok.exe http 8000    │
│ Session Status    online            │
└─────────────────────────────────────┘

═══════════════════════════════════════

PROBLEM: Server not running
┌─────────────────────────────────────┐
│ Connection refused                  │
└─────────────────────────────────────┘
         ↓
SOLUTION: Start server
┌─────────────────────────────────────┐
│ PS> uvicorn src.main:app --reload   │
│ INFO: Uvicorn running...            │
└─────────────────────────────────────┘

═══════════════════════════════════════

PROBLEM: No audio on call
┌─────────────────────────────────────┐
│ Call connects but silent            │
└─────────────────────────────────────┘
         ↓
CHECK: All 3 terminals running?
┌─────────────────────────────────────┐
│ ✓ Terminal 1: Server running        │
│ ✓ Terminal 2: ngrok running         │
│ ✓ Terminal 3: Script completed      │
└─────────────────────────────────────┘
```

## Success Indicators

```
✓ Terminal 1 shows:
  INFO: "POST /voice/advisory HTTP/1.1" 200 OK

✓ Terminal 2 shows:
  POST /voice/advisory           200 OK

✓ Terminal 3 shows:
  ✓ Call initiated successfully!
  Call SID: CAxxxxx

✓ Your phone:
  Rings within 5 seconds
  Clear Hindi audio
  Complete message plays
  Call ends cleanly

✓ All indicators present = SUCCESS! 🎉
```

## Quick Reference Card

```
┌─────────────────────────────────────────────────────────┐
│                                                         │
│  KRISHIMITRA VOICE CALL - QUICK REFERENCE               │
│                                                         │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  Terminal 1: Server                                     │
│  uvicorn src.main:app --reload                          │
│                                                         │
│  Terminal 2: ngrok                                      │
│  C:\ngrok\ngrok.exe http 8000                           │
│  Copy: https://abc123.ngrok.io                          │
│                                                         │
│  Terminal 3: Call                                       │
│  python scripts/make_real_call.py                       │
│  Webhook: https://abc123.ngrok.io/voice/advisory        │
│  Confirm: yes                                           │
│                                                         │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  Phone: +918095666788                                   │
│  Language: Hindi (hi)                                   │
│  Duration: ~2 minutes                                   │
│  Cost: ~₹1.40 per call                                  │
│                                                         │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  Help: START_HERE_VOICE_CALLS.md                        │
│  Quick: CALL_NOW_QUICKSTART.md                          │
│  Verify: python scripts/verify_call_setup.py            │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

## Ready to Start?

**Option 1: Verify First** (Recommended)
```powershell
python scripts/verify_call_setup.py
```

**Option 2: Jump Right In**
```powershell
# See START_HERE_VOICE_CALLS.md
```

**Option 3: Quick Start**
```powershell
# See CALL_NOW_QUICKSTART.md
```

---

**Need help?** Check [START_HERE_VOICE_CALLS.md](START_HERE_VOICE_CALLS.md)

**Ready to call?** Let's go! 📞🌾
