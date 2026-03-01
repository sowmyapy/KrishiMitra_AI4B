# KrishiMitra System Flow Diagram

## Complete Workflow Visualization

```
┌─────────────────────────────────────────────────────────────────────┐
│                         KRISHIMITRA SYSTEM                          │
│                  AI-Powered Farmer Early Warning                    │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│ STEP 1: DATA COLLECTION (Every 3 days)                             │
└─────────────────────────────────────────────────────────────────────┘

    Sentinel Hub API          OpenWeatherMap API
    (Satellite Images)        (Weather Data)
           │                         │
           ├─────────────┬───────────┤
           │             │           │
           ▼             ▼           ▼
    ┌──────────┐  ┌──────────┐  ┌──────────┐
    │   NDVI   │  │ Moisture │  │  Weather │
    │  Values  │  │  Index   │  │   Data   │
    └──────────┘  └──────────┘  └──────────┘
           │             │           │
           └─────────────┴───────────┘
                     │
                     ▼
           ┌─────────────────┐
           │  Data Storage   │
           │  (PostgreSQL)   │
           └─────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│ STEP 2: MONITORING & ANALYSIS (Real-time)                          │
└─────────────────────────────────────────────────────────────────────┘

           ┌─────────────────┐
           │  Data Storage   │
           └────────┬────────┘
                    │
                    ▼
           ┌─────────────────┐
           │ NDVI Calculator │
           │  - Calculate    │
           │  - Interpret    │
           │  - Detect       │
           │    Anomalies    │
           └────────┬────────┘
                    │
                    ▼
           ┌─────────────────┐
           │Weather Analyzer │
           │  - Heat Risk    │
           │  - Drought Risk │
           │  - Frost Risk   │
           │  - Wind Risk    │
           └────────┬────────┘
                    │
                    ▼
           ┌─────────────────┐
           │ Stress Predictor│
           │  - ML Model     │
           │  - Risk Score   │
           └────────┬────────┘
                    │
                    ▼
                 [Data]

┌─────────────────────────────────────────────────────────────────────┐
│ STEP 3: AGENTIC AI SYSTEM (Intelligent Decision Making)            │
└─────────────────────────────────────────────────────────────────────┘

                 [Data]
                    │
                    ▼
    ┌───────────────────────────────────────┐
    │      MONITORING AGENT                 │
    │  ┌─────────────────────────────────┐  │
    │  │ 1. Detect NDVI anomaly          │  │
    │  │ 2. Check weather context        │  │
    │  │ 3. Assess threat level          │  │
    │  │ 4. Reduce false positives       │  │
    │  │ 5. Decide: Escalate or Monitor  │  │
    │  └─────────────────────────────────┘  │
    └───────────────┬───────────────────────┘
                    │
                    │ [Anomaly Detected]
                    ▼
    ┌───────────────────────────────────────┐
    │      DIAGNOSTIC AGENT                 │
    │  ┌─────────────────────────────────┐  │
    │  │ 1. Analyze symptoms             │  │
    │  │ 2. Check historical patterns    │  │
    │  │ 3. Identify root cause          │  │
    │  │ 4. Calculate risk score         │  │
    │  │ 5. Recommend investigation      │  │
    │  └─────────────────────────────────┘  │
    └───────────────┬───────────────────────┘
                    │
                    │ [Diagnosis]
                    ▼
    ┌───────────────────────────────────────┐
    │      ADVISORY AGENT                   │
    │  ┌─────────────────────────────────┐  │
    │  │ 1. Query knowledge base         │  │
    │  │ 2. Generate actions             │  │
    │  │ 3. Check farmer constraints     │  │
    │  │ 4. Estimate costs               │  │
    │  │ 5. Personalize for farmer       │  │
    │  └─────────────────────────────────┘  │
    └───────────────┬───────────────────────┘
                    │
                    │ [Advisory]
                    ▼
    ┌───────────────────────────────────────┐
    │   COMMUNICATION AGENT                 │
    │  ┌─────────────────────────────────┐  │
    │  │ 1. Select delivery method       │  │
    │  │ 2. Translate to local language  │  │
    │  │ 3. Schedule optimal time        │  │
    │  │ 4. Track delivery status        │  │
    │  └─────────────────────────────────┘  │
    └───────────────┬───────────────────────┘
                    │
                    ▼

┌─────────────────────────────────────────────────────────────────────┐
│ STEP 4: VOICE DELIVERY (Multi-channel)                             │
└─────────────────────────────────────────────────────────────────────┘

                [Advisory]
                    │
                    ├──────────────┬──────────────┐
                    │              │              │
                    ▼              ▼              ▼
           ┌─────────────┐  ┌──────────┐  ┌──────────┐
           │ Voice Call  │  │   SMS    │  │   App    │
           │  (Twilio)   │  │          │  │  Notif   │
           └──────┬──────┘  └────┬─────┘  └────┬─────┘
                  │              │             │
                  ▼              │             │
         ┌────────────────┐      │             │
         │  AWS Polly     │      │             │
         │  (Text-to-     │      │             │
         │   Speech)      │      │             │
         └────────┬───────┘      │             │
                  │              │             │
                  ▼              ▼             ▼
         ┌─────────────────────────────────────┐
         │         FARMER RECEIVES             │
         │         Advisory in Hindi           │
         └─────────────────────────────────────┘
                         │
                         ▼
         ┌─────────────────────────────────────┐
         │    FARMER RESPONDS (Optional)       │
         │    - Voice input via phone          │
         │    - Captured by AWS Transcribe     │
         └─────────────────────────────────────┘
                         │
                         ▼
         ┌─────────────────────────────────────┐
         │      LEARNING AGENT                 │
         │  - Track advisory effectiveness     │
         │  - Update knowledge base            │
         │  - Improve recommendations          │
         └─────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│ EXAMPLE: Water Stress Scenario                                     │
└─────────────────────────────────────────────────────────────────────┘

Day 1:  Satellite shows NDVI = 0.65 (healthy)
        Weather: Normal rainfall

Day 15: No rain for 14 days
        Temperature rising

Day 20: Satellite shows NDVI = 0.45 (stressed)
        Weather: Drought conditions
        
        ┌─────────────────────────────────────┐
        │ MONITORING AGENT DETECTS:           │
        │ - NDVI dropped 31% (0.65 → 0.45)   │
        │ - No rain for 20 days               │
        │ - High temperature (38°C)           │
        │ - Threat Level: HIGH                │
        │ - Action: ESCALATE                  │
        └─────────────────────────────────────┘
                         │
                         ▼
        ┌─────────────────────────────────────┐
        │ DIAGNOSTIC AGENT ANALYZES:          │
        │ - Root Cause: Water Stress          │
        │ - Contributing: Drought + Heat      │
        │ - Risk Score: 75/100                │
        │ - Confidence: 85%                   │
        └─────────────────────────────────────┘
                         │
                         ▼
        ┌─────────────────────────────────────┐
        │ ADVISORY AGENT RECOMMENDS:          │
        │ 1. Immediate irrigation (₹500)      │
        │    - Within 24 hours                │
        │    - High priority                  │
        │                                     │
        │ 2. Apply mulch (₹1250)              │
        │    - Within 3 days                  │
        │    - Medium priority                │
        │                                     │
        │ Total Cost: ₹1750                   │
        │ (Within farmer's ₹2000 budget)      │
        └─────────────────────────────────────┘
                         │
                         ▼
        ┌─────────────────────────────────────┐
        │ VOICE CALL TO FARMER:               │
        │                                     │
        │ "नमस्ते किसान भाई।                 │
        │  आपकी फसल में पानी की कमी है।      │
        │  कृपया 24 घंटे में सिंचाई करें।"   │
        │                                     │
        │ [Farmer confirms action]            │
        └─────────────────────────────────────┘

Day 25: Farmer irrigates field
        System tracks action

Day 30: Satellite shows NDVI = 0.60 (recovering)
        Advisory marked as successful
        Knowledge base updated

┌─────────────────────────────────────────────────────────────────────┐
│ KEY METRICS                                                         │
└─────────────────────────────────────────────────────────────────────┘

Response Time:     < 2 seconds (API)
                   < 5 minutes (Advisory generation)
                   < 15 minutes (Voice call delivery)

Accuracy:          85% prediction accuracy
                   95% STT accuracy (Hindi)
                   40% reduction in false positives

Cost:              < $1 per farmer per month
                   ₹1750 average advisory cost

Engagement:        60% increase vs SMS
                   85% compliance rate

Uptime:            99.5% availability target

┌─────────────────────────────────────────────────────────────────────┐
│ TECHNOLOGY STACK                                                    │
└─────────────────────────────────────────────────────────────────────┘

Backend:           Python + FastAPI
Database:          PostgreSQL + PostGIS
Cache:             Redis
Message Queue:     Apache Kafka
Vector DB:         ChromaDB

AI/ML:
  - LLM:           AWS Bedrock (Llama 3)
  - STT:           AWS Transcribe
  - TTS:           AWS Polly
  - Embeddings:    Sentence Transformers

Data Sources:
  - Satellite:     Sentinel Hub
  - Weather:       OpenWeatherMap
  - Voice:         Twilio

Infrastructure:
  - Cloud:         AWS (ECS, RDS, S3)
  - Monitoring:    Prometheus + Grafana
  - CI/CD:         GitHub Actions

┌─────────────────────────────────────────────────────────────────────┐
│ SUPPORTED LANGUAGES                                                 │
└─────────────────────────────────────────────────────────────────────┘

Hindi (hi)         Bengali (bn)        Telugu (te)
Marathi (mr)       Tamil (ta)          Gujarati (gu)
Kannada (kn)       Malayalam (ml)      Punjabi (pa)
Odia (or)

All with native voice support via AWS Polly!
