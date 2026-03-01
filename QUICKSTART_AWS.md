# Quick Start Guide - AWS Only Setup

This guide helps you quickly set up KrishiMitra using AWS services exclusively (Bedrock, Transcribe, Polly).

## Prerequisites

1. **Python 3.11+** installed
2. **AWS CLI** installed and configured
3. **AWS Account** with access to:
   - Amazon Bedrock (Claude models)
   - Amazon Transcribe
   - Amazon Polly
   - Amazon S3

## Step 1: Verify AWS CLI

Open PowerShell and verify AWS CLI is working:

```powershell
aws --version
aws sts get-caller-identity
```

If AWS CLI is not recognized in Kiro terminal, use regular PowerShell for AWS commands.

## Step 2: Verify AWS Services

Check that you have access to required AWS services:

```powershell
# Check Bedrock models (should show Claude models)
aws bedrock list-foundation-models --region ap-south-1 | Select-String "claude"

# Check Transcribe is available
aws transcribe list-language-models --region ap-south-1

# Check Polly voices
aws polly describe-voices --region ap-south-1 --language-code hi-IN
```

## Step 3: Create S3 Bucket for Audio Files

```powershell
# Replace 'your-bucket-name' with a unique bucket name
aws s3 mb s3://krishimitra-audio-ap-south-1 --region ap-south-1
```

## Step 4: Create Virtual Environment

```powershell
# Create virtual environment
python -m venv venv

# Activate it
.\venv\Scripts\Activate.ps1

# Upgrade pip
python -m pip install --upgrade pip
```

## Step 5: Install AWS-Only Dependencies

```powershell
# Install minimal AWS dependencies
pip install -r requirements-aws.txt
```

This installs only the packages needed for AWS integration, skipping problematic OpenAI packages.

## Step 6: Configure Environment Variables

Create a `.env` file with minimal AWS configuration:

```env
# AWS Configuration
AWS_REGION=ap-south-1
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
S3_BUCKET_AUDIO=krishimitra-audio-ap-south-1

# Provider Selection
LLM_PROVIDER=bedrock
USE_AWS_SERVICES=True

# Database (for local testing, use SQLite)
DATABASE_URL=sqlite:///./krishimitra.db

# Redis (optional for testing)
REDIS_URL=redis://localhost:6379/0

# JWT Secret (generate a random string)
JWT_SECRET_KEY=your-secret-key-here
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

**Note**: You don't need Weather API keys, Twilio keys, or Sentinel Hub keys for AWS integration testing.

## Step 7: Test AWS Integration

Run the AWS integration test script:

```powershell
python scripts/test_aws_integration.py
```

This will test:
- AWS Bedrock (Claude 3.5 Sonnet)
- AWS Transcribe (Hindi speech-to-text)
- AWS Polly (Hindi text-to-speech)

## Step 8: Run the Application

```powershell
# Start the FastAPI server
uvicorn src.main:app --reload
```

Visit `http://localhost:8000/docs` to see the API documentation.

## Troubleshooting

### AWS CLI not found in Kiro terminal
- Use regular PowerShell for AWS commands
- AWS CLI works in regular PowerShell but may not be in PATH for Kiro terminal

### pip install fails on openai-whisper
- Use `requirements-aws.txt` instead of `requirements.txt`
- This skips OpenAI-specific packages

### ModuleNotFoundError: No module named 'pkg_resources'
- This is caused by openai-whisper package
- Use `requirements-aws.txt` to avoid this issue

### Bedrock model not found
- Verify you have access to Claude models in your AWS region
- Check with: `aws bedrock list-foundation-models --region ap-south-1`

## Next Steps

Once AWS integration is working:

1. **Commit your code to Git** (see Git setup guide below)
2. **Deploy to AWS** (see AWS_DEPLOYMENT.md)
3. **Add full dependencies** when needed (Weather API, Twilio, etc.)

## Git Setup

```powershell
# Initialize git (if not already done)
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit: KrishiMitra with AWS integration"

# Add remote (replace with your repository URL)
git remote add origin https://github.com/yourusername/krishimitra.git

# Push to GitHub
git push -u origin main
```

## Cost Estimation

For 10,000 farmers with AWS services:
- **Bedrock (Claude 3.5 Sonnet)**: ~$150/month
- **Transcribe**: ~$120/month
- **Polly**: ~$100/month
- **Total**: ~$370/month (~$0.037/farmer/month)

Much cheaper than OpenAI alternatives!
