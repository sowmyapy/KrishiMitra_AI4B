# Enable AWS Bedrock - One-Time Setup

You need to fill out a use case form to use Anthropic Claude models. This is a one-time setup that takes 5 minutes.

## Error You're Seeing

```
Model use case details have not been submitted for this account. 
Fill out the Anthropic use case details form before using the model.
```

## How to Fix (5 minutes)

### Step 1: Go to AWS Bedrock Console

Open: https://console.aws.amazon.com/bedrock

Make sure you're in the **ap-south-1** region (Mumbai)

### Step 2: Click "Model Access"

In the left sidebar, click **"Model access"**

### Step 3: Click "Manage Model Access"

Click the orange **"Manage model access"** button

### Step 4: Find Anthropic Models

Scroll down to find **"Anthropic"** section

You'll see:
- Claude 3 Haiku
- Claude 3 Sonnet  
- Claude 3.5 Sonnet
- Claude 3.5 Sonnet v2 ← **Check this one**
- Claude 3.7 Sonnet

### Step 5: Check the Box

Check the box next to **"Claude 3.5 Sonnet v2"**

### Step 6: Fill Out Use Case Form

A form will appear asking:
- **Use case**: Select "Agriculture" or "Other"
- **Description**: Enter something like:
  ```
  Agricultural early warning system for crop monitoring and farmer advisory.
  Provides AI-powered recommendations to farmers via voice calls in local languages.
  ```
- **Company/Organization**: Your name or organization
- **Industry**: Agriculture

### Step 7: Submit

Click **"Request model access"** or **"Submit"**

### Step 8: Wait (15 minutes)

AWS will review your request. Usually approved within:
- **Instant**: For most use cases
- **15 minutes**: Maximum wait time

You'll see status change from "Pending" to "Access granted"

### Step 9: Test Again

After approval, run:

```powershell
python scripts/test_aws_integration.py
```

You should now see:
```
✓ LLM: PASS
✓ STT: PASS  
✓ TTS: PASS
```

## Alternative: Use Claude 3 Haiku (No Form Required)

If you don't want to wait, you can use Claude 3 Haiku which doesn't require the form:

1. Edit `src/services/aws/bedrock_client.py`
2. Change model_id to:
   ```python
   self.model_id = "apac.anthropic.claude-3-haiku-20240307-v1:0"
   ```
3. Test again

**Note**: Haiku is faster and cheaper but slightly less capable than Sonnet.

## Cost Comparison

| Model | Input (per 1M tokens) | Output (per 1M tokens) | Quality |
|-------|----------------------|------------------------|---------|
| Claude 3 Haiku | $0.25 | $1.25 | Good |
| Claude 3.5 Sonnet v2 | $3.00 | $15.00 | Excellent |

For testing with 1 farmer: Both cost <$1/month

## Troubleshooting

### "Still getting error after 15 minutes"

Try:
1. Refresh the Bedrock console page
2. Check if status shows "Access granted"
3. Wait another 5 minutes
4. Try a different region (us-east-1)

### "Form not appearing"

Make sure you:
1. Are logged in as IAM user with admin permissions
2. Are in the correct region (ap-south-1)
3. Have billing enabled on your account

### "Access denied"

Check IAM permissions. Your user needs:
```json
{
  "Effect": "Allow",
  "Action": [
    "bedrock:InvokeModel",
    "bedrock:GetFoundationModel",
    "bedrock:ListFoundationModels"
  ],
  "Resource": "*"
}
```

## What's Working Now

Even without Bedrock, you have:

✅ **AWS Transcribe** - Speech-to-text working  
✅ **AWS Polly** - Text-to-speech working  
✅ **Database** - SQLite ready  
✅ **API** - FastAPI ready  

You can test everything except AI conversations!

## Quick Test Without Bedrock

You can still test the application without Bedrock:

```powershell
# Skip Bedrock test
python scripts/init_db.py
uvicorn src.main:app --reload
```

Then use the API at http://localhost:8000/docs

The voice chatbot will fail, but all other endpoints work!

## Summary

1. Go to: https://console.aws.amazon.com/bedrock
2. Click: Model access → Manage model access
3. Check: Claude 3.5 Sonnet v2
4. Fill form: Agriculture use case
5. Wait: 15 minutes
6. Test: `python scripts/test_aws_integration.py`

That's it! 🎉
