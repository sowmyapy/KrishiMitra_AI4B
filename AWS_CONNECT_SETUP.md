# AWS Connect Setup for KrishiMitra Voice Calls

You've chosen **Option C: AWS Connect** for production voice calls. This is the best choice for scalability and cost-effectiveness in India.

## Why AWS Connect?

- **Cost**: ~₹0.50-1.00 per minute (cheaper than Twilio)
- **Scalability**: Handles thousands of concurrent calls
- **Indian Numbers**: Can call Indian numbers from Singapore region
- **Integration**: Native AWS integration with Polly, Lambda, S3
- **Reliability**: 99.9% uptime SLA
- **No Setup Fees**: Pay only for usage

## Important: Region Limitation

**AWS Connect is NOT available in Mumbai (ap-south-1)**

Available regions for Indian calling:
1. **Singapore (ap-southeast-1)** ← Recommended
   - Closest to India (~3000 km)
   - Low latency (~50-100ms)
   - Can call +91 numbers
   - May have +91 or +65 caller ID

2. **US East (us-east-1)** ← Alternative
   - More features
   - Higher latency (~200-300ms)
   - Can call +91 numbers
   - Usually +1 caller ID

**Impact**: Farmers will see international caller ID, but call quality is good.

## Architecture Overview

```
┌─────────────────┐
│  KrishiMitra    │
│  Application    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  AWS Lambda     │ ← Trigger outbound call
│  (Call Trigger) │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  AWS Connect    │ ← Make call to farmer
│  Contact Flow   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  AWS Polly      │ ← Play Hindi advisory
│  (TTS)          │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Farmer Phone   │ ← Receives call
│  +918095666788  │
└─────────────────┘
```

## Step-by-Step Setup

### Step 1: Create AWS Connect Instance (15 minutes)

**IMPORTANT: AWS Connect Region Selection**

AWS Connect is NOT available in Mumbai (ap-south-1). For calling Indian numbers, use:
- **Recommended**: `ap-southeast-1` (Singapore) - Closest to India, low latency
- **Alternative**: `us-east-1` (N. Virginia) - More features, slightly higher latency

Both regions support calling Indian (+91) numbers.

1. **Go to AWS Console**
   - Navigate to: https://console.aws.amazon.com/connect/
   - **Region: `ap-southeast-1` (Singapore)** ← Use this!

2. **Create Instance**
   - Click "Add an instance"
   - Access URL: `krishimitra` (becomes krishimitra.my.connect.aws)
   - Identity management: "Store users in Amazon Connect"
   - Administrator: Create new admin user
   - Telephony: Enable "Outbound calls" ✓
   - Data storage: Use default S3 buckets
   - Click "Create instance"

3. **Wait for Creation** (2-3 minutes)

**Note**: Even though the instance is in Singapore, you can:
- Call Indian phone numbers (+91)
- Use Indian voice (Aditi) from Polly
- Experience minimal latency (~50-100ms)

### Step 2: Claim Phone Number (5 minutes)

1. **Open Connect Instance**
   - Click on your instance name
   - Click "Login as administrator"

2. **Claim Number**
   - Go to: Routing → Phone numbers
   - Click "Claim a number"
   - **Country: India (+91)** ← Available in Singapore region!
   - Type: DID (Direct Inward Dialing)
   - Select available number
   - Click "Claim"
   
   **If Indian numbers not available:**
   - Try claiming a Singapore number (+65)
   - You can still call Indian numbers
   - Farmers will see international caller ID
   - Alternative: Use Twilio for Indian caller ID, AWS Connect for call handling

3. **Note Your Number**
   - Example: +91-80-XXXX-XXXX
   - This is your outbound caller ID

### Step 3: Create Contact Flow (10 minutes)

1. **Go to Contact Flows**
   - Routing → Contact flows
   - Click "Create contact flow"
   - Name: "KrishiMitra Advisory Call"

2. **Build Flow**
   
   **Flow Design:**
   ```
   Entry Point
      ↓
   Set Voice (Aditi - Hindi)
      ↓
   Get Customer Input (Press 1 to hear again, 2 to end)
      ↓
   Play Prompt (S3 audio file)
      ↓
   Check Input
      ├─ 1 → Loop back to Play Prompt
      ├─ 2 → End Call
      └─ Timeout → End Call
   ```

3. **Configure Blocks**

   **Block 1: Set Voice**
   - Type: "Set voice"
   - Language: Hindi (hi-IN)
   - Voice: Aditi

   **Block 2: Get Customer Input**
   - Type: "Get customer input"
   - Text-to-speech: "सलाह दोबारा सुनने के लिए 1 दबाएं, कॉल समाप्त करने के लिए 2 दबाएं"
   - Timeout: 5 seconds

   **Block 3: Play Prompt**
   - Type: "Play prompt"
   - Source: S3
   - S3 URL: `s3://krishimitra-audio/advisories/{advisory_id}.mp3`

   **Block 4: Check Input**
   - Type: "Check contact attributes"
   - Attribute: "Stored customer input"
   - Conditions:
     - Equals "1" → Go to Play Prompt
     - Equals "2" → Go to Disconnect
     - No match → Go to Disconnect

4. **Save and Publish**
   - Click "Save"
   - Click "Publish"

### Step 4: Create Lambda Function (15 minutes)

1. **Go to Lambda Console**
   - https://console.aws.amazon.com/lambda/
   - **Region: ap-southeast-1 (Singapore)** ← Same as Connect instance

2. **Create Function**
   - Name: `krishimitra-make-call`
   - Runtime: Python 3.11
   - Architecture: x86_64
   - Permissions: Create new role

3. **Add Code**

```python
import json
import boto3
import os
from datetime import datetime

connect = boto3.client('connect', region_name='ap-southeast-1')  # Singapore
s3 = boto3.client('s3', region_name='ap-south-1')  # Mumbai for S3

CONNECT_INSTANCE_ID = os.environ['CONNECT_INSTANCE_ID']
CONTACT_FLOW_ID = os.environ['CONTACT_FLOW_ID']
SOURCE_PHONE_NUMBER = os.environ['SOURCE_PHONE_NUMBER']
S3_BUCKET = os.environ['S3_BUCKET']

def lambda_handler(event, context):
    """
    Trigger outbound call via AWS Connect
    
    Event format:
    {
        "farmer_phone": "+918095666788",
        "advisory_id": "abc-123",
        "audio_data": "base64_encoded_mp3",
        "language": "hi"
    }
    """
    
    try:
        farmer_phone = event['farmer_phone']
        advisory_id = event['advisory_id']
        audio_data = event.get('audio_data')
        language = event.get('language', 'hi')
        
        # Upload audio to S3 if provided
        if audio_data:
            import base64
            audio_bytes = base64.b64decode(audio_data)
            
            s3_key = f"advisories/{advisory_id}.mp3"
            s3.put_object(
                Bucket=S3_BUCKET,
                Key=s3_key,
                Body=audio_bytes,
                ContentType='audio/mpeg'
            )
            
            audio_url = f"s3://{S3_BUCKET}/{s3_key}"
        else:
            audio_url = None
        
        # Start outbound call
        response = connect.start_outbound_voice_contact(
            DestinationPhoneNumber=farmer_phone,
            ContactFlowId=CONTACT_FLOW_ID,
            InstanceId=CONNECT_INSTANCE_ID,
            SourcePhoneNumber=SOURCE_PHONE_NUMBER,
            Attributes={
                'advisory_id': advisory_id,
                'audio_url': audio_url or '',
                'language': language,
                'timestamp': datetime.utcnow().isoformat()
            }
        )
        
        contact_id = response['ContactId']
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'success': True,
                'contact_id': contact_id,
                'farmer_phone': farmer_phone,
                'advisory_id': advisory_id
            })
        }
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({
                'success': False,
                'error': str(e)
            })
        }
```

4. **Configure Environment Variables**
   - `CONNECT_INSTANCE_ID`: Your Connect instance ID (from Singapore region)
   - `CONTACT_FLOW_ID`: Your contact flow ID
   - `SOURCE_PHONE_NUMBER`: Your claimed number (+91-XX or +65-XX)
   - `S3_BUCKET`: `krishimitra-audio-test-520578320427` (can be in Mumbai)

5. **Add Permissions**
   - Go to Configuration → Permissions
   - Click on the role name
   - Add inline policy:

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "connect:StartOutboundVoiceContact",
                "connect:StopContact"
            ],
            "Resource": "*"
        },
        {
            "Effect": "Allow",
            "Action": [
                "s3:PutObject",
                "s3:GetObject"
            ],
            "Resource": "arn:aws:s3:::krishimitra-audio-test-520578320427/*"
        }
    ]
}
```

6. **Test Lambda**
   - Click "Test"
   - Event name: "test-call"
   - Event JSON:
```json
{
    "farmer_phone": "+918095666788",
    "advisory_id": "test-123",
    "language": "hi"
}
```
   - Click "Test"

### Step 5: Update KrishiMitra Application

1. **Create AWS Connect Client**

Create `src/services/aws/connect_client.py`:

```python
"""
AWS Connect client for outbound voice calls
"""
import logging
import boto3
import base64
from typing import Dict, Optional
from botocore.exceptions import ClientError

from src.config.settings import settings

logger = logging.getLogger(__name__)


class ConnectClient:
    """Client for AWS Connect voice calls"""
    
    def __init__(self):
        self.lambda_client = boto3.client(
            'lambda',
            region_name=settings.aws_region
        )
        self.lambda_function = settings.aws_connect_lambda_function
        logger.info("AWS Connect client initialized")
    
    async def make_call(
        self,
        farmer_phone: str,
        advisory_id: str,
        audio_data: bytes,
        language: str = "hi"
    ) -> Dict:
        """
        Make outbound call to farmer
        
        Args:
            farmer_phone: Farmer's phone number (+918095666788)
            advisory_id: Unique advisory ID
            audio_data: MP3 audio bytes
            language: Language code
        
        Returns:
            Call result dictionary
        """
        try:
            # Encode audio as base64
            audio_base64 = base64.b64encode(audio_data).decode('utf-8')
            
            # Invoke Lambda function
            response = self.lambda_client.invoke(
                FunctionName=self.lambda_function,
                InvocationType='RequestResponse',
                Payload=json.dumps({
                    'farmer_phone': farmer_phone,
                    'advisory_id': advisory_id,
                    'audio_data': audio_base64,
                    'language': language
                })
            )
            
            # Parse response
            payload = json.loads(response['Payload'].read())
            body = json.loads(payload['body'])
            
            if body.get('success'):
                logger.info(
                    f"Call initiated: {farmer_phone}, "
                    f"contact_id={body['contact_id']}"
                )
                return {
                    'success': True,
                    'contact_id': body['contact_id'],
                    'farmer_phone': farmer_phone,
                    'advisory_id': advisory_id
                }
            else:
                raise Exception(body.get('error', 'Unknown error'))
                
        except ClientError as e:
            logger.error(f"Failed to make call: {e}")
            raise
    
    async def get_call_status(self, contact_id: str) -> Dict:
        """Get status of a call"""
        # AWS Connect doesn't have direct API for this
        # You'd need to query CloudWatch Logs or use Connect Streams
        return {
            'contact_id': contact_id,
            'status': 'unknown'
        }
```

2. **Update Settings**

Add to `src/config/settings.py`:

```python
# AWS Connect
aws_connect_instance_id: str = Field(default="", env="AWS_CONNECT_INSTANCE_ID")
aws_connect_contact_flow_id: str = Field(default="", env="AWS_CONNECT_CONTACT_FLOW_ID")
aws_connect_source_phone: str = Field(default="", env="AWS_CONNECT_SOURCE_PHONE")
aws_connect_lambda_function: str = Field(default="krishimitra-make-call", env="AWS_CONNECT_LAMBDA_FUNCTION")
```

3. **Update .env**

```env
# AWS Connect
AWS_CONNECT_INSTANCE_ID=your-instance-id
AWS_CONNECT_CONTACT_FLOW_ID=your-flow-id
AWS_CONNECT_SOURCE_PHONE=+91-80-XXXX-XXXX
AWS_CONNECT_LAMBDA_FUNCTION=krishimitra-make-call
```

4. **Update Voice Call Service**

Modify `src/services/communication/voice_call_service.py` to use Connect:

```python
from src.services.aws.connect_client import ConnectClient

class VoiceCallService:
    def __init__(self):
        self.connect_client = ConnectClient()
    
    async def make_advisory_call(
        self,
        farmer_phone: str,
        advisory_id: str,
        audio_data: bytes,
        language: str = "hi"
    ):
        """Make call using AWS Connect"""
        return await self.connect_client.make_call(
            farmer_phone=farmer_phone,
            advisory_id=advisory_id,
            audio_data=audio_data,
            language=language
        )
```

### Step 6: Test End-to-End

1. **Run Test Script**

```powershell
python scripts/test_real_farmer.py
```

2. **Make Real Call**

```powershell
python scripts/make_real_call.py
```

3. **You Should Receive**
   - Call from your AWS Connect number
   - Hindi advisory message
   - Option to replay (press 1) or end (press 2)

## Cost Estimation

### Per Call Costs
- **AWS Connect**: ₹0.50/minute
- **AWS Polly**: ₹0.016 per 1000 characters
- **AWS Lambda**: ₹0.0000002 per request
- **S3 Storage**: ₹0.023 per GB/month

### Example: 1000 Farmers/Day
- Average call: 2 minutes
- Daily cost: 1000 × 2 × ₹0.50 = ₹1,000
- Monthly cost: ₹30,000
- Per farmer/month: ₹30

**Much cheaper than Twilio (₹2-3 per minute)!**

## Production Checklist

- [ ] AWS Connect instance created
- [ ] Indian phone number claimed
- [ ] Contact flow published
- [ ] Lambda function deployed
- [ ] IAM permissions configured
- [ ] S3 bucket for audio files
- [ ] Environment variables set
- [ ] Test call successful
- [ ] Monitoring enabled (CloudWatch)
- [ ] Call logs configured

## Monitoring

### CloudWatch Metrics
- Total calls made
- Call duration
- Success/failure rate
- Audio playback errors

### CloudWatch Logs
- Lambda execution logs
- Connect contact flow logs
- Error tracking

## Troubleshooting

### Call Not Connecting
- Check phone number format (+91XXXXXXXXXX)
- Verify Connect instance is active
- Check Lambda permissions
- Review CloudWatch logs

### Audio Not Playing
- Verify S3 bucket permissions
- Check audio file format (MP3)
- Ensure contact flow has correct S3 URL
- Test audio file locally first

### High Costs
- Monitor call duration
- Set up billing alerts
- Use call queuing for batch processing
- Implement retry limits

## Next Steps

1. **Complete Setup** (follow steps above)
2. **Test with your number**
3. **Add more farmers**
4. **Monitor costs**
5. **Scale to production**

## Support

- AWS Connect Docs: https://docs.aws.amazon.com/connect/
- AWS Support: https://console.aws.amazon.com/support/
- KrishiMitra Issues: Create GitHub issue

Good luck with your AWS Connect setup! 📞
