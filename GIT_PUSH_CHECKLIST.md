# Git Push Checklist - Before Pushing to GitHub

## ⚠️ CRITICAL: Check for Sensitive Data

Before pushing, verify these files don't contain real credentials:

### 1. Check .env file
```powershell
# .env should NOT be in git (it's in .gitignore)
git status
# If .env appears, remove it:
git rm --cached .env
```

### 2. Verify .gitignore is working
```powershell
# These should NOT appear in git status:
# - .env
# - *.db (database files)
# - venv/ (virtual environment)
# - __pycache__/
# - *.log
```

### 3. Search for hardcoded secrets
```powershell
# Search for potential secrets in tracked files
git grep -i "password"
git grep -i "secret"
git grep -i "api_key"
git grep -i "token"
```

## Files That Should NOT Be Pushed

- ✗ `.env` - Contains all secrets
- ✗ `krishimitra.db` - Local database
- ✗ `venv/` - Virtual environment
- ✗ `__pycache__/` - Python cache
- ✗ `*.log` - Log files
- ✗ `.aws/` - AWS credentials

## Files That SHOULD Be Pushed

- ✓ `.env.example` - Template without secrets
- ✓ All `.py` source files
- ✓ `requirements.txt` and `requirements-aws.txt`
- ✓ All `.md` documentation files
- ✓ `.gitignore`
- ✓ `docker-compose.yml`, `Dockerfile`
- ✓ All test scripts in `scripts/`

## Pre-Push Commands

### Step 1: Check Git Status
```powershell
git status
```

Look for:
- Untracked files that should be added
- Files that shouldn't be there (.env, *.db, etc.)

### Step 2: Add Files
```powershell
# Add all files (gitignore will exclude sensitive ones)
git add .

# Or add specific files
git add src/
git add scripts/
git add *.md
git add requirements*.txt
```

### Step 3: Verify What Will Be Committed
```powershell
git status
git diff --cached
```

### Step 4: Commit
```powershell
git commit -m "feat: Complete KrishiMitra implementation with E2E testing

- Implemented complete farmer early warning system
- Added AWS Bedrock, Transcribe, and Polly integration
- Created Agentic AI system (Monitoring, Diagnostic, Advisory agents)
- Built voice chatbot service with Hindi support
- Added end-to-end integration tests
- Configured for phone number +918095666788
- Ready for Twilio voice call integration

Features:
- REST API with JWT authentication
- Satellite data analysis (NDVI calculation)
- Weather risk assessment
- AI-powered crop health monitoring
- Personalized advisory generation
- Multi-language voice support (10+ Indian languages)
- Complete test suite

Tech Stack:
- Python + FastAPI
- PostgreSQL/SQLite
- AWS Bedrock (Llama 3)
- AWS Transcribe + Polly
- Twilio (voice calls)
"
```

### Step 5: Push to GitHub
```powershell
# First time push
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git push -u origin main

# Subsequent pushes
git push
```

## Create .env.example

Before pushing, create a template .env file:

```powershell
# Copy .env to .env.example and remove real values
```

Example `.env.example` content:
```env
# Application
APP_NAME=KrishiMitra
ENVIRONMENT=development

# Database
DATABASE_URL=sqlite:///./krishimitra.db

# AWS Credentials
AWS_REGION=ap-south-1
AWS_ACCESS_KEY_ID=your_access_key_here
AWS_SECRET_ACCESS_KEY=your_secret_key_here

# Twilio
TWILIO_ACCOUNT_SID=your_account_sid
TWILIO_AUTH_TOKEN=your_auth_token
TWILIO_PHONE_NUMBER=your_twilio_number

# Security
JWT_SECRET_KEY=generate_random_secret_key
ENCRYPTION_KEY=generate_random_encryption_key

# API Keys (Optional - for production)
OPENWEATHERMAP_API_KEY=your_api_key
SENTINEL_HUB_CLIENT_ID=your_client_id
SENTINEL_HUB_CLIENT_SECRET=your_client_secret
```

## GitHub Repository Setup

### 1. Create Repository on GitHub
1. Go to https://github.com/new
2. Name: `krishimitra` or `ai-crop-early-warning`
3. Description: "AI-powered farmer early warning system with voice advisory in Indian languages"
4. Public or Private (your choice)
5. Don't initialize with README (you already have one)

### 2. Add Repository Secrets (for CI/CD)
If using GitHub Actions:
1. Go to Settings > Secrets and variables > Actions
2. Add secrets:
   - `AWS_ACCESS_KEY_ID`
   - `AWS_SECRET_ACCESS_KEY`
   - `TWILIO_ACCOUNT_SID`
   - `TWILIO_AUTH_TOKEN`

### 3. Add Topics/Tags
Add these topics to your repo:
- `agriculture`
- `ai`
- `machine-learning`
- `fastapi`
- `aws`
- `voice-assistant`
- `hindi`
- `farmer-advisory`
- `crop-monitoring`
- `early-warning-system`

## Post-Push Checklist

After pushing:

1. ✓ Verify repository on GitHub
2. ✓ Check no sensitive data is visible
3. ✓ Update README.md with:
   - Project description
   - Setup instructions
   - Demo screenshots/videos
   - License information
4. ✓ Add LICENSE file (MIT, Apache 2.0, etc.)
5. ✓ Enable GitHub Actions (if using CI/CD)
6. ✓ Add repository description and topics

## Common Issues

### Issue: .env file appears in git status
**Solution**:
```powershell
git rm --cached .env
git commit -m "Remove .env from tracking"
```

### Issue: Large files (database, models)
**Solution**:
```powershell
# Remove from git
git rm --cached krishimitra.db
git commit -m "Remove database file"

# Add to .gitignore if not already there
echo "*.db" >> .gitignore
```

### Issue: Accidentally pushed secrets
**Solution**:
1. Immediately rotate all exposed credentials
2. Remove from git history:
```powershell
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch .env" \
  --prune-empty --tag-name-filter cat -- --all
git push origin --force --all
```
3. Change all exposed credentials immediately!

## Security Best Practices

1. ✓ Never commit `.env` files
2. ✓ Use `.env.example` as template
3. ✓ Rotate credentials regularly
4. ✓ Use GitHub Secrets for CI/CD
5. ✓ Enable 2FA on GitHub account
6. ✓ Review commits before pushing
7. ✓ Use signed commits (optional)

## Ready to Push?

Run this final check:
```powershell
# 1. Check status
git status

# 2. Verify no secrets
git diff --cached | grep -i "secret\|password\|key"

# 3. If all clear, push!
git push
```

## Need Help?

- Git basics: https://git-scm.com/doc
- GitHub guides: https://guides.github.com/
- Removing sensitive data: https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository
