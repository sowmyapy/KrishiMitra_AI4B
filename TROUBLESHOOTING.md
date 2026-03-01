# Troubleshooting Guide

Common issues and quick fixes.

## pip install Issues

### ❌ "ModuleNotFoundError: No module named 'pkg_resources'"

**Cause**: openai-whisper package issue

**Fix**: Use requirements-aws.txt instead
```powershell
pip install -r requirements-aws.txt
```

### ❌ pip install hangs or takes forever

**Fix**: Upgrade pip first
```powershell
python -m pip install --upgrade pip
pip install -r requirements-aws.txt
```

### ❌ "ERROR: Could not find a version that satisfies the requirement"

**Fix**: Check Python version (need 3.11+)
```powershell
python --version
# Should show Python 3.11 or higher
```

---

## AWS Issues

### ❌ "aws: The term 'aws' is not recognized"

**Cause**: AWS CLI not in PATH for Kiro terminal

**Fix**: Use regular PowerShell for AWS commands
```powershell
# Open regular PowerShell (not Kiro terminal)
aws sts get-caller-identity
```

### ❌ "Unable to locate credentials"

**Fix**: Configure AWS credentials
```powershell
aws configure
# Enter: Access Key ID, Secret Access Key, Region (ap-south-1)
```

### ❌ "Bedrock model not found"

**Fix**: Enable models in AWS Console
1. Go to: https://console.aws.amazon.com/bedrock
2. Click "Model access"
3. Request access to Claude models
4. Wait 2-5 minutes for approval

### ❌ "Access Denied" for Bedrock

**Fix**: Check IAM permissions
```powershell
# Check your user/role has bedrock:InvokeModel permission
aws iam get-user
```

---

## Database Issues

### ❌ "OperationalError: no such table"

**Fix**: Initialize database
```powershell
python scripts/init_db.py
```

### ❌ "Database is locked"

**Fix**: Close other connections or delete database
```powershell
# Stop the server first (Ctrl+C)
# Then delete and recreate
rm krishimitra.db
python scripts/init_db.py
```

### ❌ "Connection refused" (PostgreSQL)

**Fix**: Use SQLite for testing
```env
# In .env file
DATABASE_URL=sqlite:///./krishimitra.db
```

---

## Server Issues

### ❌ "Port 8000 already in use"

**Fix**: Use different port or kill existing process
```powershell
# Option 1: Use different port
uvicorn src.main:app --reload --port 8001

# Option 2: Find and kill process using port 8000
netstat -ano | findstr :8000
taskkill /PID <process_id> /F
```

### ❌ "ModuleNotFoundError: No module named 'src'"

**Fix**: Run from project root directory
```powershell
# Make sure you're in the project root
cd C:\Users\Sowmya\OneDrive\projects\ai_crop_system
uvicorn src.main:app --reload
```

### ❌ Server starts but crashes immediately

**Fix**: Check logs for specific error
```powershell
# Run with verbose logging
uvicorn src.main:app --reload --log-level debug
```

---

## API Testing Issues

### ❌ "404 Not Found" when accessing /docs

**Fix**: Make sure server is running and use correct URL
```
Correct: http://localhost:8000/docs
Wrong: http://localhost:8000/api/v1/docs
```

### ❌ "422 Unprocessable Entity"

**Cause**: Invalid request data

**Fix**: Check request format matches schema
```json
// Correct format for farmer registration
{
  "name": "Test Farmer",
  "phone": "+919876543210",
  "language": "hi",
  "location": {
    "latitude": 28.6139,
    "longitude": 77.2090
  }
}
```

### ❌ "500 Internal Server Error"

**Fix**: Check server logs for details
```powershell
# Server logs show in terminal where uvicorn is running
# Look for ERROR or CRITICAL messages
```

---

## External API Issues

### ❌ Twilio: "Unable to create record"

**Cause**: Phone number not verified (trial account)

**Fix**: Verify phone number in Twilio console
1. Go to: https://console.twilio.com/
2. Phone Numbers → Verified Caller IDs
3. Add and verify your phone number

### ❌ Weather API: "Invalid API key"

**Cause**: API key not activated yet

**Fix**: Wait 10 minutes after signup
```powershell
# Test API key
curl "https://api.openweathermap.org/data/2.5/weather?q=Delhi&appid=YOUR_API_KEY"
```

### ❌ Sentinel Hub: "Authentication failed"

**Fix**: Check credentials are correct
```env
# Make sure you have all three:
SENTINEL_HUB_CLIENT_ID=your_client_id
SENTINEL_HUB_CLIENT_SECRET=your_client_secret
SENTINEL_HUB_INSTANCE_ID=your_instance_id
```

---

## Virtual Environment Issues

### ❌ "cannot be loaded because running scripts is disabled"

**Fix**: Enable script execution
```powershell
# Run as Administrator
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### ❌ Virtual environment not activating

**Fix**: Use full path
```powershell
C:\Users\Sowmya\OneDrive\projects\ai_crop_system\venv\Scripts\Activate.ps1
```

### ❌ "pip: command not found" in venv

**Fix**: Reinstall virtual environment
```powershell
# Delete old venv
rm -r venv

# Create new one
python -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
```

---

## Import Errors

### ❌ "ImportError: cannot import name 'X' from 'Y'"

**Fix**: Reinstall dependencies
```powershell
pip install -r requirements-aws.txt --force-reinstall
```

### ❌ "No module named 'pydantic'"

**Fix**: Install missing package
```powershell
pip install pydantic pydantic-settings
```

---

## Performance Issues

### ❌ API responses very slow

**Cause**: First request to AWS Bedrock is slow (cold start)

**Fix**: This is normal. Subsequent requests are faster.

### ❌ High AWS costs

**Fix**: Check CloudWatch for usage
```powershell
# Check costs
aws ce get-cost-and-usage \
  --time-period Start=2024-01-01,End=2024-01-31 \
  --granularity MONTHLY \
  --metrics BlendedCost
```

---

## Testing Issues

### ❌ test_aws_integration.py fails

**Fix**: Check each service individually
```powershell
# Test Bedrock only
python -c "from src.services.aws.bedrock_client import BedrockClient; import asyncio; asyncio.run(BedrockClient().generate_text('test'))"

# Test Polly only
python -c "from src.services.aws.polly_client import PollyClient; import asyncio; asyncio.run(PollyClient().synthesize_speech('test'))"
```

### ❌ "RuntimeError: Event loop is closed"

**Fix**: Use Python 3.11+ (better async support)
```powershell
python --version
# Should be 3.11 or higher
```

---

## Configuration Issues

### ❌ ".env file not found"

**Fix**: Create from example
```powershell
cp .env.example .env
# Then edit .env with your values
```

### ❌ "Settings validation error"

**Fix**: Check .env format
```env
# Correct format (no quotes, no spaces around =)
AWS_REGION=ap-south-1
LLM_PROVIDER=bedrock

# Wrong format
AWS_REGION = "ap-south-1"  # Don't use quotes or spaces
```

---

## Git Issues

### ❌ "fatal: not a git repository"

**Fix**: Initialize git
```powershell
git init
```

### ❌ ".env file committed to git"

**Fix**: Remove from git (keep local file)
```powershell
git rm --cached .env
git commit -m "Remove .env from git"
```

---

## Quick Diagnostic Commands

```powershell
# Check Python version
python --version

# Check pip packages
pip list

# Check AWS credentials
aws sts get-caller-identity

# Check AWS Bedrock access
aws bedrock list-foundation-models --region ap-south-1

# Check if port is in use
netstat -ano | findstr :8000

# Check database exists
ls krishimitra.db

# Check .env file
cat .env

# Test imports
python -c "import fastapi; import boto3; import pydantic; print('All imports OK')"
```

---

## Still Having Issues?

1. **Check logs**: Server logs show detailed errors
2. **Read error message**: Usually tells you what's wrong
3. **Google the error**: Often has solutions
4. **Check AWS Console**: See if services are enabled
5. **Restart everything**: Sometimes fixes weird issues

```powershell
# Nuclear option: Restart everything
# 1. Stop server (Ctrl+C)
# 2. Deactivate venv
deactivate

# 3. Reactivate venv
.\venv\Scripts\Activate.ps1

# 4. Restart server
uvicorn src.main:app --reload
```

---

## Common Error Messages Decoded

| Error | Meaning | Fix |
|-------|---------|-----|
| "ModuleNotFoundError" | Package not installed | `pip install <package>` |
| "OperationalError" | Database issue | Run `init_db.py` |
| "ValidationError" | Wrong data format | Check request schema |
| "ConnectionError" | Can't reach service | Check internet/credentials |
| "TimeoutError" | Request took too long | Check AWS region/network |
| "PermissionError" | No access rights | Check IAM permissions |
| "FileNotFoundError" | File missing | Check file path |

---

## Emergency Reset

If everything is broken:

```powershell
# 1. Stop all processes
# Press Ctrl+C in all terminals

# 2. Delete virtual environment
rm -r venv

# 3. Delete database
rm krishimitra.db

# 4. Recreate everything
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements-aws.txt
python scripts/init_db.py
uvicorn src.main:app --reload
```

This should fix 90% of issues! 🔧
