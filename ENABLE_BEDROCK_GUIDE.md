# Enable AWS Bedrock for KrishiMitra

## Current Status
- Bedrock calls are failing due to missing IAM permissions
- Application is using Hindi/Telugu fallback templates (working correctly)
- To enable AI-generated advisories, follow these steps

## Prerequisites
- AWS Console access
- Elastic Beanstalk environment running (krishimitra-prod)

## Step 1: Find the IAM Instance Profile

1. Go to AWS Elastic Beanstalk Console:
   https://ap-south-1.console.aws.amazon.com/elasticbeanstalk/home?region=ap-south-1#/environment/dashboard?environmentId=e-jzpm3k8squ

2. Click on "Configuration" in the left sidebar

3. Find the "Security" section and click "Edit"

4. Note the "IAM instance profile" name (usually something like `aws-elasticbeanstalk-ec2-role`)

## Step 2: Add Bedrock Permissions to IAM Role

1. Go to IAM Console:
   https://console.aws.amazon.com/iam/home?region=ap-south-1#/roles

2. Search for the instance profile name from Step 1

3. Click on the role name

4. Click "Add permissions" → "Attach policies"

5. Search for and attach: `AmazonBedrockFullAccess`
   - Or create a custom policy with minimal permissions (see below)

6. Click "Attach policy"

## Step 3: Request Model Access (If Needed)

1. Go to Bedrock Console:
   https://ap-south-1.console.aws.amazon.com/bedrock/home?region=ap-south-1#/modelaccess

2. Click "Manage model access"

3. Enable access for: **Meta Llama 3 8B Instruct**
   - Model ID: `meta.llama3-8b-instruct-v1:0`
   - This model is available immediately without approval

4. Click "Save changes"

## Step 4: Verify Permissions

After adding permissions, the application should automatically start using Bedrock (no restart needed).

Test by generating an advisory from the UI - you should see more natural, context-aware Hindi text instead of the simple template.

## Alternative: Custom IAM Policy (Minimal Permissions)

Instead of `AmazonBedrockFullAccess`, you can create a custom policy with minimal permissions:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "bedrock:InvokeModel"
      ],
      "Resource": [
        "arn:aws:bedrock:ap-south-1::foundation-model/meta.llama3-8b-instruct-v1:0"
      ]
    }
  ]
}
```

## Troubleshooting

### Check if Bedrock is working:
```powershell
# View recent logs
eb logs --all

# Look for "LLM generated advisory" (success) or "LLM generation failed" (still failing)
```

### Common Issues:

1. **Model not available in region**
   - Meta Llama 3 is available in ap-south-1 (Mumbai)
   - If not, change region or use a different model

2. **IAM permissions not propagated**
   - Wait 1-2 minutes after adding permissions
   - Try generating another advisory

3. **Rate limits**
   - Meta Llama 3 has strict rate limits on free tier
   - Consider using Amazon Nova or Titan models instead

## Alternative Models

If Meta Llama 3 doesn't work, you can switch to other models by updating `src/services/aws/bedrock_client.py`:

### Amazon Nova Lite (Recommended for production)
```python
self.model_id = "amazon.nova-lite-v1:0"
self.model_type = "nova"
```

### Amazon Titan Text Express
```python
self.model_id = "amazon.titan-text-express-v1"
self.model_type = "titan"
```

After changing the model, commit and deploy:
```powershell
git add src/services/aws/bedrock_client.py
git commit -m "Switch to Amazon Nova model"
eb deploy
```

## Cost Considerations

### Bedrock Pricing (ap-south-1)
- Meta Llama 3 8B: $0.0003 per 1K input tokens, $0.0006 per 1K output tokens
- Amazon Nova Lite: $0.00006 per 1K input tokens, $0.00024 per 1K output tokens
- Amazon Titan Text Express: $0.0008 per 1K input tokens, $0.0016 per 1K output tokens

For 1000 advisories/month (~500 tokens each):
- Meta Llama 3: ~$0.45/month
- Amazon Nova Lite: ~$0.15/month
- Amazon Titan: ~$1.20/month

## Next Steps

1. Add Bedrock permissions to IAM role (Step 2 above)
2. Request model access if needed (Step 3 above)
3. Test advisory generation from UI
4. Monitor logs to confirm Bedrock is working: `eb logs`

Once Bedrock is working, you'll see much more natural, context-aware advisories in Hindi that adapt to the specific crop conditions and weather data.
