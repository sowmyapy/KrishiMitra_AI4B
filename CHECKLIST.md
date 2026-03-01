# Installation Checklist

Use this checklist to track your progress.

## Pre-Installation ✅ DONE

- [x] Python 3.11+ installed
- [x] AWS CLI installed
- [x] AWS credentials configured (`aws configure`)
- [x] Verified Bedrock access (Claude models available)
- [x] Verified Transcribe access
- [x] Verified Polly access

## Installation Steps ⏳ IN PROGRESS

- [ ] **Step 1**: Create virtual environment
  ```powershell
  python -m venv venv
  .\venv\Scripts\Activate.ps1
  python -m pip install --upgrade pip
  ```

- [ ] **Step 2**: Install dependencies
  ```powershell
  pip install -r requirements-aws.txt
  ```
  Expected: 5-10 minutes, no errors

- [ ] **Step 3**: Create S3 bucket
  ```powershell
  aws s3 mb s3://krishimitra-audio-ap-south-1 --region ap-south-1
  ```
  Expected: Bucket created or "bucket already exists" message

- [ ] **Step 4**: Configure .env file
  - Set `LLM_PROVIDER=bedrock`
  - Set `USE_AWS_SERVICES=True`
  - Set `S3_BUCKET_AUDIO=krishimitra-audio-ap-south-1`
  - Set `AWS_REGION=ap-south-1`
  - Set `DATABASE_URL=sqlite:///./krishimitra.db`
  - Set `JWT_SECRET_KEY=<random-string>`

- [ ] **Step 5**: Test AWS integration
  ```powershell
  python scripts/test_aws_integration.py
  ```
  Expected: All 4 tests pass with green checkmarks

- [ ] **Step 6**: Run the application
  ```powershell
  uvicorn src.main:app --reload
  ```
  Expected: Server starts, visit http://localhost:8000/docs

## Get API Keys (For Full Application)

- [ ] **Twilio** (15 minutes)
  - Sign up: https://www.twilio.com/try-twilio
  - Get: Account SID, Auth Token, Phone Number
  - Add to .env
  - See: API_KEYS_GUIDE.md for details

- [ ] **Weather API** (5 minutes)
  - Sign up: https://openweathermap.org/api
  - Get: API Key
  - Add to .env
  - See: API_KEYS_GUIDE.md for details

- [ ] **Sentinel Hub** (20 minutes)
  - Sign up: https://www.sentinel-hub.com/
  - Get: Client ID, Client Secret
  - Add to .env
  - See: API_KEYS_GUIDE.md for details

## Post-Installation (Optional)

- [ ] Commit code to Git
  ```powershell
  git init
  git add .
  git commit -m "Initial commit: KrishiMitra with AWS integration"
  ```

- [ ] Push to GitHub
  ```powershell
  git remote add origin https://github.com/yourusername/krishimitra.git
  git push -u origin main
  ```

- [ ] Deploy to AWS (see AWS_DEPLOYMENT.md)

## Common Issues

### ❌ pip install fails on openai-whisper
**Solution**: Use `requirements-aws.txt` instead of `requirements.txt`

### ❌ AWS CLI not found in Kiro terminal
**Solution**: Use regular PowerShell for AWS commands

### ❌ ModuleNotFoundError: No module named 'pkg_resources'
**Solution**: This is from openai-whisper. Use `requirements-aws.txt`

### ❌ Bedrock model not found
**Solution**: Enable models at https://console.aws.amazon.com/bedrock → Model access

## Need Help?

See these files:
- **API_KEYS_GUIDE.md** - How to get all API keys (Twilio, Weather, Sentinel Hub)
- **QUICK_REFERENCE.md** - Quick reference card
- **INSTALL_STEPS.md** - Detailed step-by-step guide
- **QUICKSTART_AWS.md** - Quick reference
- **NEXT_STEPS.md** - What to do after installation
- **AWS_INTEGRATION_SUMMARY.md** - AWS services details

## Current Step

👉 **You are here**: Step 2 - Install dependencies

**Next command to run**:
```powershell
# Make sure virtual environment is activated first
.\venv\Scripts\Activate.ps1

# Then install dependencies
pip install -r requirements-aws.txt
```
