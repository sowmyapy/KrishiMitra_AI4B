# Voice Call Alternatives for KrishiMitra (AISPL Account)

## Problem: AWS Connect Not Available

Your AWS account is managed by AISPL (Amazon Internet Services Private Limited), which is the Indian entity. AISPL accounts **cannot create AWS Connect instances** - this is a known limitation.

## Best Alternatives for Indian Farmers

### Option 1: Twilio (Recommended for Now) ⭐

**Pros:**
- Works immediately
- Indian phone numbers available
- Good documentation
- Reliable service
- No account restrictions

**Cons:**
- Higher cost (₹2-3 per minute vs ₹0.50-1)
- Need to verify phone numbers

**Setup Time:** 15 minutes

**Cost:** ₹60,000/month for 1000 farmers (2 min/call)

**Status:** Already integrated in your code!

---

### Option 2: Exotel (Indian Alternative) 🇮🇳

**Best for:** Indian startups, local support

**Pros:**
- Indian company (Bangalore-based)
- Cheaper than Twilio (₹1-1.50 per minute)
- Indian phone numbers
- Local support
- No AISPL restrictions
- Good for compliance

**Cons:**
- Less documentation than Twilio
- Smaller ecosystem

**Setup Time:** 30 minutes

**Cost:** ₹30,000-45,000/month for 1000 farmers

**Website:** https://exotel.com/

---

### Option 3: Knowlarity

**Best for:** Enterprise customers

**Pros:**
- Indian company
- Enterprise features
- Good for large scale
- Compliance ready

**Cons:**
- More expensive
- Enterprise focus (may have minimums)

**Website:** https://www.knowlarity.com/

---

### Option 4: AWS Chime SDK (Alternative AWS Service)

**Best for:** If you want to stay with AWS

**Pros:**
- Available on AISPL accounts
- AWS integration
- Lower cost than Twilio
- Programmable

**Cons:**
- More complex setup
- Need to build more infrastructure
- Limited Indian number support

**Setup Time:** 2-3 hours

**Cost:** ₹0.80-1.20 per minute

---

## Recommended Approach

### Phase 1: Development & Testing (Now)
**Use Twilio**
- Quick setup
- Test with your number
- Validate the workflow
- Cost: Minimal (testing only)

### Phase 2: Production Launch (1-3 months)
**Switch to Exotel**
- Better pricing for scale
- Indian company (easier support)
- Local compliance
- Cost: 50% less than Twilio

### Phase 3: Scale (6+ months)
**Evaluate AWS Chime SDK or negotiate with Exotel**
- Volume discounts
- Custom features
- Dedicated support

---

## Quick Start: Twilio Setup (15 minutes)

Since Twilio is already integrated, here's how to get started:

### Step 1: Create Twilio Account

1. Go to: https://www.twilio.com/try-twilio
2. Sign up with your email
3. Verify your email
4. Get $15 free credit

### Step 2: Get Credentials

1. Go to Console: https://console.twilio.com/
2. Copy:
   - Account SID
   - Auth Token
3. Add to `.env`:
```env
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=your_auth_token
```

### Step 3: Get Phone Number

1. Go to: Phone Numbers → Buy a number
2. Country: India (+91) or US (+1)
3. Capabilities: Voice ✓
4. Buy number (uses free credit)
5. Add to `.env`:
```env
TWILIO_PHONE_NUMBER=+1234567890
```

### Step 4: Verify Your Number

1. Go to: Phone Numbers → Verified Caller IDs
2. Click "Add a new number"
3. Enter: +918095666788
4. Verify via SMS code

### Step 5: Test

```powershell
python scripts/make_real_call.py
```

You'll receive a call with the Hindi advisory!

---

## Exotel Setup (30 minutes)

If you want to use Exotel instead:

### Step 1: Sign Up

1. Go to: https://exotel.com/
2. Click "Start Free Trial"
3. Fill business details
4. Verify documents (GST, PAN)

### Step 2: Get Credentials

1. Login to dashboard
2. Go to: Settings → API Settings
3. Copy:
   - API Key
   - API Token
   - Exotel SID
4. Add to `.env`:
```env
EXOTEL_API_KEY=your_api_key
EXOTEL_API_TOKEN=your_api_token
EXOTEL_SID=your_sid
```

### Step 3: Get Phone Number

1. Go to: Phone Numbers
2. Select Indian number
3. Note the number

### Step 4: Create Exotel Client

Create `src/services/exotel/exotel_client.py`:

```python
"""
Exotel client for voice calls (Indian alternative)
"""
import logging
import httpx
from typing import Dict
from src.config.settings import settings

logger = logging.getLogger(__name__)


class ExotelClient:
    """Client for Exotel voice calls"""
    
    def __init__(self):
        self.api_key = settings.exotel_api_key
        self.api_token = settings.exotel_api_token
        self.sid = settings.exotel_sid
        self.base_url = f"https://api.exotel.com/v1/Accounts/{self.sid}"
    
    async def make_call(
        self,
        to_number: str,
        audio_url: str,
        from_number: str = None
    ) -> Dict:
        """
        Make outbound call
        
        Args:
            to_number: Farmer's number (+918095666788)
            audio_url: Public URL of audio file
            from_number: Your Exotel number
        
        Returns:
            Call details
        """
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/Calls/connect",
                auth=(self.api_key, self.api_token),
                data={
                    "From": from_number or settings.exotel_phone_number,
                    "To": to_number,
                    "Url": audio_url,  # TwiML-like XML endpoint
                    "CallType": "trans"
                }
            )
            response.raise_for_status()
            
            logger.info(f"Call initiated to {to_number}")
            return response.json()
```

---

## Cost Comparison (1000 farmers/day, 2 min/call)

| Provider | Per Minute | Daily Cost | Monthly Cost | Notes |
|----------|-----------|------------|--------------|-------|
| **Twilio** | ₹2.50 | ₹5,000 | ₹150,000 | Easy setup |
| **Exotel** | ₹1.20 | ₹2,400 | ₹72,000 | Indian company |
| **Knowlarity** | ₹1.50 | ₹3,000 | ₹90,000 | Enterprise |
| **AWS Chime** | ₹1.00 | ₹2,000 | ₹60,000 | Complex setup |
| **AWS Connect** | ₹0.60 | ₹1,200 | ₹36,000 | ❌ Not available |

---

## My Recommendation

**For your situation:**

1. **Start with Twilio** (this week)
   - Already integrated
   - Test the complete workflow
   - Validate with real farmers
   - Cost: ~₹500 for testing

2. **Switch to Exotel** (next month)
   - 50% cost savings
   - Indian company
   - Better for compliance
   - Setup in parallel while using Twilio

3. **Negotiate volume pricing** (after 3 months)
   - Once you have 1000+ farmers
   - Get custom rates
   - Potentially ₹0.80-1.00 per minute

---

## AISPL Account Workaround (Advanced)

If you really want AWS Connect:

### Option A: Create US AWS Account
1. Create new AWS account with US address
2. Use US credit card
3. Set up AWS Connect there
4. Use API from India

**Cons:** Complex billing, compliance issues

### Option B: AWS Organizations
1. Create organization with US master account
2. Add AISPL account as member
3. Use Connect from US account

**Cons:** Complex setup, may not work

### Option C: Wait for AWS
AWS is working on enabling Connect for AISPL accounts. Check periodically.

---

## Next Steps

1. **Immediate:** Set up Twilio (15 min)
2. **This week:** Test with real calls
3. **Next week:** Evaluate Exotel
4. **Next month:** Switch to Exotel if satisfied

Need help with Twilio or Exotel setup? Let me know!
