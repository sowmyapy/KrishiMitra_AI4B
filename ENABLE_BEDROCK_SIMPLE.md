# Enable AWS Bedrock Models - Simple Guide

## What You Need to Do

Enable model access in AWS Bedrock so you can use AI models. Takes 5 minutes.

---

## Step 1: Open AWS Bedrock Console

**Link**: https://console.aws.amazon.com/bedrock

**Important**: Make sure you're in **Asia Pacific (Mumbai) ap-south-1** region
- Look at top-right corner of AWS console
- Click the region dropdown
- Select "Asia Pacific (Mumbai) ap-south-1"

---

## Step 2: Go to Model Access

On the left sidebar, click **"Model access"**

You'll see a list of AI model providers (Anthropic, Amazon, Meta, etc.)

---

## Step 3: Click "Manage Model Access"

Click the orange button that says **"Manage model access"** or **"Edit"**

---

## Step 4: Enable Amazon Nova Models

Scroll down to find **"Amazon"** section

You'll see:
- ☐ Nova Micro
- ☐ Nova Lite ← **Check this one**
- ☐ Nova Pro
- ☐ Nova 2 Lite

**Check the box next to "Nova Lite"**

Why Nova Lite?
- ✅ Amazon's own model (no form required!)
- ✅ Works immediately
- ✅ Fast and cheap
- ✅ Good quality for farming advice

---

## Step 5: (Optional) Enable Claude Models

If you want better quality AI (requires filling a form):

Scroll to **"Anthropic"** section

Check these boxes:
- ☐ Claude 3 Haiku
- ☐ Claude 3.5 Sonnet v2 ← **Best quality**

**You'll need to fill a form**:
- Use case: "Agriculture"
- Description: "AI-powered farmer advisory system for crop monitoring"
- Industry: Agriculture

---

## Step 6: Save Changes

Click **"Save changes"** or **"Request model access"** button at the bottom

---

## Step 7: Wait for Approval

**For Amazon Nova**: Instant! ✅ Works immediately

**For Claude models**: 
- Usually instant
- Sometimes takes 5-15 minutes
- You'll see status change from "Pending" to "Access granted"

---

## Step 8: Verify Access

Go back to **"Model access"** page

You should see:
- ✅ Amazon Nova Lite: **Access granted**
- ✅ (Optional) Claude 3.5 Sonnet v2: **Access granted**

---

## Step 9: Test It!

Run the test script:

```powershell
python scripts/test_aws_integration.py
```

You should see:
```
✓ LLM: PASS
✓ STT: PASS
✓ TTS: PASS
```

All green checkmarks! 🎉

---

## Troubleshooting

### "I don't see Model Access in sidebar"

Make sure you're in the Bedrock console:
- URL should be: `console.aws.amazon.com/bedrock`
- Not in EC2, S3, or other services

### "Access still pending after 15 minutes"

For Claude models:
1. Refresh the page
2. Check your email for approval
3. Try a different region (us-east-1)
4. Contact AWS support

For Nova models:
- Should be instant
- If not working, check IAM permissions

### "I filled the form but still can't use Claude"

Wait 15 minutes, then:
1. Go back to Model access page
2. Check if status shows "Access granted"
3. Try the test script again

### "Error: Access Denied"

Your IAM user needs these permissions:
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

Ask your AWS administrator to add these permissions.

---

## What Models to Enable?

### For Testing (Start Here):
✅ **Amazon Nova Lite** - Instant access, free tier, good quality

### For Production (Later):
✅ **Claude 3.5 Sonnet v2** - Best quality, requires form
✅ **Claude 3 Haiku** - Faster, cheaper than Sonnet

### Cost Comparison (1 farmer, 1 month):

| Model | Cost | Quality | Speed |
|-------|------|---------|-------|
| Nova Lite | $0.50 | Good | Fast |
| Claude Haiku | $0.30 | Good | Very Fast |
| Claude Sonnet | $1.50 | Excellent | Medium |

All are under $2/month for testing! ✅

---

## Quick Visual Checklist

```
Step 1: Open Bedrock Console
   ↓
Step 2: Click "Model access" (left sidebar)
   ↓
Step 3: Click "Manage model access" (orange button)
   ↓
Step 4: Check ☑ "Amazon Nova Lite"
   ↓
Step 5: (Optional) Check ☑ "Claude 3.5 Sonnet v2" + Fill form
   ↓
Step 6: Click "Save changes"
   ↓
Step 7: Wait (instant for Nova, 15 min for Claude)
   ↓
Step 8: Verify "Access granted" status
   ↓
Step 9: Run test: python scripts/test_aws_integration.py
   ↓
✓ All tests pass! 🎉
```

---

## After Enabling

Once you see "Access granted":

1. **Test immediately**:
   ```powershell
   python scripts/test_aws_integration.py
   ```

2. **Start the app**:
   ```powershell
   python scripts/init_db.py
   uvicorn src.main:app --reload
   ```

3. **Open browser**:
   ```
   http://localhost:8000/docs
   ```

4. **Test with 1 farmer**:
   - Register a farmer
   - Send voice message
   - Get AI response!

---

## Summary

**Minimum to get started**:
- ✅ Enable Amazon Nova Lite (instant, no form)

**For better quality**:
- ✅ Enable Claude 3.5 Sonnet v2 (15 min, requires form)

**Total time**: 5 minutes (Nova) or 20 minutes (Nova + Claude)

**Cost**: ~$1-2/month for testing with 1 farmer

---

## Need Help?

**AWS Bedrock Console**: https://console.aws.amazon.com/bedrock

**AWS Documentation**: https://docs.aws.amazon.com/bedrock/

**Support**: Check TROUBLESHOOTING.md for common issues

---

That's it! Once you enable Nova Lite, you can start testing immediately! 🚀
