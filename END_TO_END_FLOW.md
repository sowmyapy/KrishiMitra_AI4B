# End-to-End Test Flow Diagram

## Complete KrishiMitra Workflow

```
┌─────────────────────────────────────────────────────────────────┐
│                    START END-TO-END TEST                        │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│  STEP 1: Register Farmer                                        │
│  ────────────────────────                                       │
│  • Phone: +918151910856                                         │
│  • Language: Hindi (hi)                                         │
│  • Location: Pune area                                          │
│  ✓ Farmer ID created in database                               │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│  STEP 2: Fetch Satellite Data                                   │
│  ─────────────────────────────                                  │
│  🛰️ Sentinel Hub API                                            │
│  • Coordinates: (13.2443, 77.7122)                              │
│  • Date range: Last 7 days                                      │
│  • Resolution: 256x256 pixels                                   │
│  • Bands: Red, NIR (for NDVI)                                   │
│  ✓ NDVI calculated: 0.55 (moderate vegetation)                 │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│  STEP 3: Fetch Weather Data                                     │
│  ────────────────────────────                                   │
│  🌤️ OpenWeatherMap API                                          │
│  • Current conditions                                           │
│  • 5-day forecast                                               │
│  ✓ Data: 38.5°C, 25% humidity, 15 m/s wind                     │
│  ⚠️ Risks detected: Heat stress, Drought conditions             │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│  STEP 4: AI Analysis & Advisory Generation                      │
│  ──────────────────────────────────────────                     │
│  🤖 AWS Bedrock (Claude)                                        │
│  • Analyze NDVI + Weather data                                  │
│  • Detect stress type: Water stress                            │
│  • Calculate risk score: 75/100                                 │
│  • Generate actionable recommendations                          │
│  ✓ Advisory created with 2 actions, ₹1750 total cost          │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│  STEP 5: Generate Voice Message                                 │
│  ───────────────────────────────                                │
│  🔊 AWS Polly (Text-to-Speech)                                  │
│  • Language: Hindi (hi-IN)                                      │
│  • Voice: Aditi (female, Indian)                                │
│  • Content: Advisory with actions and costs                     │
│  ✓ MP3 file generated: test_advisory_message.mp3               │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│  STEP 6: Make Voice Call                                        │
│  ────────────────────────                                       │
│  📞 Twilio Voice API                                            │
│  • From: +17752270557 (Twilio number)                          │
│  • To: +918151910856 (verified number)                         │
│  • Webhook: ngrok URL for TwiML                                 │
│  ✓ Call initiated → Phone rings → Message plays                │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                    TEST COMPLETE ✅                              │
│  ───────────────────────────────────────                        │
│  • Farmer receives actionable advisory in Hindi                 │
│  • Real satellite and weather data used                         │
│  • AI-powered analysis and recommendations                      │
│  • Voice call delivered successfully                            │
└─────────────────────────────────────────────────────────────────┘
```

## Data Flow

```
┌──────────────┐
│ Sentinel Hub │ ──┐
└──────────────┘   │
                   │
┌──────────────┐   │    ┌─────────────┐    ┌──────────────┐
│OpenWeatherMap│ ──┼───→│ AI Analysis │───→│ AWS Bedrock  │
└──────────────┘   │    │  (Advisory) │    │   (Claude)   │
                   │    └─────────────┘    └──────────────┘
┌──────────────┐   │                              ↓
│   Database   │ ──┘                       ┌──────────────┐
│ (Farmer Info)│                           │   Advisory   │
└──────────────┘                           │  (Actions +  │
                                           │    Costs)    │
                                           └──────────────┘
                                                  ↓
                                           ┌──────────────┐
                                           │  AWS Polly   │
                                           │ (Hindi TTS)  │
                                           └──────────────┘
                                                  ↓
                                           ┌──────────────┐
                                           │    Twilio    │
                                           │ (Voice Call) │
                                           └──────────────┘
                                                  ↓
                                           ┌──────────────┐
                                           │   Farmer's   │
                                           │    Phone     │
                                           └──────────────┘
```

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         YOUR COMPUTER                           │
│                                                                 │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │  Terminal 1  │  │  Terminal 2  │  │  Terminal 3  │         │
│  │              │  │              │  │              │         │
│  │   FastAPI    │  │    ngrok     │  │ Test Script  │         │
│  │   Server     │  │   Tunnel     │  │              │         │
│  │              │  │              │  │              │         │
│  │ Port: 8000   │  │ HTTPS Tunnel │  │  Triggers    │         │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘         │
│         │                 │                 │                 │
└─────────┼─────────────────┼─────────────────┼─────────────────┘
          │                 │                 │
          │                 │                 │
          └────────┬────────┘                 │
                   │                          │
                   ↓                          ↓
┌─────────────────────────────────────────────────────────────────┐
│                        EXTERNAL APIS                            │
│                                                                 │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │ Sentinel Hub │  │OpenWeatherMap│  │     AWS      │         │
│  │              │  │              │  │              │         │
│  │  Satellite   │  │   Weather    │  │  • Bedrock   │         │
│  │    Data      │  │    Data      │  │  • Polly     │         │
│  └──────────────┘  └──────────────┘  └──────────────┘         │
│                                                                 │
│  ┌──────────────┐                                              │
│  │    Twilio    │                                              │
│  │              │                                              │
│  │ Voice Calls  │ ──────────────────────────────┐             │
│  └──────────────┘                                │             │
└──────────────────────────────────────────────────┼─────────────┘
                                                   │
                                                   ↓
                                            ┌──────────────┐
                                            │   Farmer's   │
                                            │    Phone     │
                                            │              │
                                            │+918151910856 │
                                            └──────────────┘
```

## Timeline (Typical Test Run)

```
Time    Step                              Duration    Status
────────────────────────────────────────────────────────────────
00:00   Start test script                 -           ⏳
00:01   Register farmer                   1s          ✅
00:02   Fetch satellite data              3s          ✅
00:05   Fetch weather data                2s          ✅
00:07   AI analysis (Bedrock)             5s          ✅
00:12   Generate voice (Polly)            2s          ✅
00:14   Initiate call (Twilio)            1s          ✅
00:15   Phone rings                       -           📞
00:20   Farmer answers                    -           🎧
00:25   Message plays (Hindi)             45s         🔊
01:10   Call completes                    -           ✅
────────────────────────────────────────────────────────────────
Total: ~70 seconds (1 minute 10 seconds)
```

## Cost Breakdown (Per Test)

```
Service              Cost per Test    Free Tier
─────────────────────────────────────────────────────────
Sentinel Hub         $0.01           30,000 units/month
OpenWeatherMap       $0.00           1,000 calls/day
AWS Bedrock          $0.008          -
AWS Polly            $0.004          5M chars/month
Twilio Call          $0.02           $15 trial credit
─────────────────────────────────────────────────────────
TOTAL                ~$0.04          (~₹3.30)
```

## Success Metrics

```
✅ Farmer registered in database
✅ Real satellite data fetched (NDVI: 0.55)
✅ Real weather data fetched (38.5°C, 25% humidity)
✅ AI advisory generated (Risk: 75/100)
✅ Voice message created (Hindi, 45 seconds)
✅ Call initiated successfully
✅ Phone rings within 10 seconds
✅ Message plays clearly
✅ Call completes (duration: 45s)
```

## What Farmer Hears (Hindi)

```
🔊 "नमस्ते किसान भाई,

यह कृषि मित्र से एक महत्वपूर्ण सलाह है।

हमारे उपग्रह विश्लेषण से पता चला है कि 
आपकी फसल में पानी की कमी है।

तुरंत करें:
1. अगले 24 घंटों में सिंचाई करें - खर्च लगभग 500 रुपये
2. 3 दिनों में मल्चिंग करें - खर्च लगभग 1250 रुपये

कुल अनुमानित खर्च: 1750 रुपये

अधिक जानकारी के लिए हमें कॉल करें।
धन्यवाद।"
```

---

**Ready to run?** See `START_END_TO_END_TEST.md` for step-by-step instructions! 🚀
