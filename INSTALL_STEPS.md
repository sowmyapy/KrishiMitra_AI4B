# Installation Steps - AWS Only

Follow these steps exactly to get KrishiMitra running with AWS services.

## Current Status

✅ AWS CLI installed and configured  
✅ AWS credentials working  
✅ Bedrock models available (Claude 3.5 Sonnet v2)  
✅ Transcribe service available  
✅ Polly service available  
⏳ Python dependencies - IN PROGRESS  

## Step-by-Step Instructions

### Step 1: Create Virtual Environment (if not done)

Open **regular PowerShell** (not Kiro terminal):

```powershell
cd C:\Users\Sowmya\OneDrive\projects\ai_crop_system

# Create virtual environment
python -m venv venv

# Activate it
.\venv\Scripts\Activate.ps1

# Upgrade pip
python -m pip install --upgrade pip
```

### Step 2: Install AWS-Only Dependencies

```powershell
# Install from requirements-aws.txt (no OpenAI packages)
pip install -r requirements-aws.txt
```

This will install:
- FastAPI, Uvicorn (web framework)
- SQLAlchemy, Alembic (database)
- Boto3 (AWS SDK)
- Anthropic, LangChain, ChromaDB (AI/ML)
- Twilio (phone calls)
- All other dependencies EXCEPT openai-whisper and elevenlabs

**Expected time**: 5-10 minutes

### Step 3: Create S3 Bucket

```powershell
# Create bucket for audio files
aws s3 mb s3://krishimitra-audio-ap-south-1 --region ap-south-1
```

If bucket already exists, that's fine - you'll see a message saying so.

### Step 4: Configure Environment Variables

Edit your `.env` file and set these values:

```env
# AWS Configuration
AWS_REGION=ap-south-1
S3_BUCKET_AUDIO=krishimitra-audio-ap-south-1

# Provider Selection (USE AWS ONLY)
LLM_PROVIDER=bedrock
USE_AWS_SERVICES=True

# Database (SQLite for testing)
DATABASE_URL=sqlite:///./krishimitra.db

# JWT Secret (generate random string)
JWT_SECRET_KEY=your-random-secret-key-here
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

**You DO NOT need**:
- ❌ OPENAI_API_KEY
- ❌ ELEVENLABS_API_KEY  
- ❌ WEATHER_API_KEY (not needed for AWS testing)
- ❌ TWILIO_* keys (not needed for AWS testing)
- ❌ SENTINEL_HUB_* keys (not needed for AWS testing)

### Step 5: Test AWS Integration

```powershell
# Run the test script
python scripts/test_aws_integration.py
```

This will test:
1. ✅ AWS Bedrock - Generate text with Claude 3.5 Sonnet
2. ✅ AWS Bedrock - Generate embeddings with Titan
3. ✅ AWS Transcribe - Convert Hindi speech to text
4. ✅ AWS Polly - Convert Hindi text to speech

**Expected output**: All tests should pass with green checkmarks.

### Step 6: Run the Application

```powershell
# Start FastAPI server
uvicorn src.main:app --reload
```

Visit: http://localhost:8000/docs

You should see the API documentation (Swagger UI).

## Troubleshooting

### Issue: `aws` command not found in Kiro terminal

**Solution**: Use regular PowerShell for AWS commands. AWS CLI works in regular PowerShell but may not be in Kiro terminal's PATH.

### Issue: `pip install` fails on openai-whisper

**Solution**: Use `requirements-aws.txt` instead of `requirements.txt`. This skips the problematic openai-whisper package.

### Issue: ModuleNotFoundError: No module named 'pkg_resources'

**Solution**: This is caused by openai-whisper. Use `requirements-aws.txt` to avoid it.

### Issue: Bedrock model not found

**Solution**: 
1. Check model access: `aws bedrock list-foundation-models --region ap-south-1`
2. Enable models at: https://console.aws.amazon.com/bedrock
3. Go to "Model access" and request access to Claude models

### Issue: S3 bucket creation fails

**Solution**: 
- Bucket names must be globally unique
- Try: `krishimitra-audio-<your-account-id>`
- Or use existing bucket

## What's Next?

Once AWS integration is working:

1. **Commit to Git**:
   ```powershell
   git init
   git add .
   git commit -m "Initial commit: KrishiMitra with AWS integration"
   git remote add origin https://github.com/yourusername/krishimitra.git
   git push -u origin main
   ```

2. **Add more features**:
   - Weather API integration
   - Twilio voice calls
   - Satellite data ingestion

3. **Deploy to AWS**:
   - See `AWS_DEPLOYMENT.md` for deployment guide
   - Use ECS/Fargate for containerized deployment

## Cost Estimate

For 10,000 farmers using AWS services:

| Service | Usage | Cost/Month |
|---------|-------|------------|
| Bedrock (Claude 3.5 Sonnet) | 100k requests | $150 |
| Transcribe | 50k minutes | $120 |
| Polly | 50k characters | $100 |
| **Total** | | **$370** |

**Per farmer**: $0.037/month (much cheaper than OpenAI!)

## Support

If you encounter issues:
1. Check the error message carefully
2. Verify AWS credentials: `aws sts get-caller-identity`
3. Check Python version: `python --version` (should be 3.11+)
4. Check virtual environment is activated: `(venv)` should appear in prompt
