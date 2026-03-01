# Git Setup Guide

## Prerequisites

Before committing to Git, make sure:
- ✅ AWS integration tests pass (`python scripts/test_aws_integration.py`)
- ✅ Application runs successfully (`uvicorn src.main:app --reload`)
- ✅ No sensitive data in `.env` file (it's already in .gitignore)

## Step 1: Initialize Git Repository

```powershell
# Navigate to project directory
cd C:\Users\Sowmya\OneDrive\projects\ai_crop_system

# Initialize git (if not already done)
git init
```

## Step 2: Check What Will Be Committed

```powershell
# See what files will be added
git status
```

**Files that WILL be committed** (good):
- ✅ All `.py` files in `src/`
- ✅ `requirements.txt`, `requirements-aws.txt`
- ✅ Documentation files (`.md`)
- ✅ Configuration files (`pyproject.toml`, `alembic.ini`, etc.)
- ✅ Scripts in `scripts/`
- ✅ `.env.example` (template, no secrets)

**Files that WON'T be committed** (good, they're in .gitignore):
- ❌ `.env` (contains secrets)
- ❌ `venv/` (virtual environment)
- ❌ `__pycache__/` (Python cache)
- ❌ `*.db` (local database)
- ❌ `.aws/` (AWS credentials)

## Step 3: Add Files to Git

```powershell
# Add all files (respects .gitignore)
git add .

# Verify what's staged
git status
```

## Step 4: Create First Commit

```powershell
# Commit with descriptive message
git commit -m "Initial commit: KrishiMitra with AWS Bedrock integration

- Implemented FastAPI backend with REST APIs
- Integrated AWS Bedrock (Claude 3.5 Sonnet v2) for LLM
- Integrated AWS Transcribe for speech-to-text (10+ Indian languages)
- Integrated AWS Polly for text-to-speech (neural voices)
- Created Agentic AI system with 5 specialized agents
- Implemented voice chatbot service
- Added data ingestion layer (satellite, weather)
- Added monitoring and prediction services
- Created comprehensive documentation
- Cost optimized: $370/month for 10k farmers"
```

## Step 5: Create GitHub Repository

1. Go to https://github.com/new
2. Repository name: `krishimitra` (or your preferred name)
3. Description: "AI-powered agricultural early warning system with voice chatbot"
4. Choose: **Private** (recommended) or Public
5. **DO NOT** initialize with README, .gitignore, or license (we already have these)
6. Click "Create repository"

## Step 6: Connect to GitHub

GitHub will show you commands. Use these:

```powershell
# Add remote repository (replace with your URL)
git remote add origin https://github.com/yourusername/krishimitra.git

# Verify remote
git remote -v

# Push to GitHub
git branch -M main
git push -u origin main
```

## Step 7: Verify on GitHub

1. Go to your repository URL: `https://github.com/yourusername/krishimitra`
2. You should see all your files
3. Check that `.env` is NOT there (good!)
4. Check that `README.md` displays nicely

## Future Commits

After making changes:

```powershell
# See what changed
git status

# Add specific files
git add src/services/new_file.py

# Or add all changes
git add .

# Commit with message
git commit -m "Add new feature: XYZ"

# Push to GitHub
git push
```

## Branching Strategy (Optional)

For team development:

```powershell
# Create feature branch
git checkout -b feature/new-feature

# Make changes, commit
git add .
git commit -m "Implement new feature"

# Push feature branch
git push -u origin feature/new-feature

# Create Pull Request on GitHub
# After review, merge to main
```

## Common Git Commands

```powershell
# Check status
git status

# View commit history
git log --oneline

# View changes
git diff

# Undo changes (before commit)
git checkout -- filename.py

# Undo last commit (keep changes)
git reset --soft HEAD~1

# Pull latest changes
git pull

# Create new branch
git checkout -b branch-name

# Switch branches
git checkout main
```

## .gitignore Verification

Your `.gitignore` already protects:
- ✅ `.env` files (secrets)
- ✅ `venv/` (virtual environment)
- ✅ `__pycache__/` (Python cache)
- ✅ `*.db` (databases)
- ✅ `.aws/` (AWS credentials)
- ✅ `*.log` (log files)
- ✅ `*.pem`, `*.key` (private keys)

## Security Checklist

Before pushing to GitHub:

- [ ] `.env` is in .gitignore ✅
- [ ] No AWS credentials in code ✅
- [ ] No API keys in code ✅
- [ ] No passwords in code ✅
- [ ] `.env.example` has placeholder values only ✅

## Troubleshooting

### Issue: "fatal: not a git repository"
**Solution**: Run `git init` first

### Issue: "remote origin already exists"
**Solution**: 
```powershell
git remote remove origin
git remote add origin https://github.com/yourusername/krishimitra.git
```

### Issue: "failed to push some refs"
**Solution**: Pull first, then push:
```powershell
git pull origin main --rebase
git push
```

### Issue: Accidentally committed .env file
**Solution**:
```powershell
# Remove from git (keeps local file)
git rm --cached .env

# Commit the removal
git commit -m "Remove .env from git"

# Push
git push
```

## Next Steps

After pushing to GitHub:
1. ✅ Add repository description and topics on GitHub
2. ✅ Enable GitHub Actions for CI/CD (optional)
3. ✅ Add collaborators (if team project)
4. ✅ Set up branch protection rules (optional)
5. ✅ Deploy to AWS (see AWS_DEPLOYMENT.md)

## Repository Topics (Suggested)

Add these topics on GitHub for discoverability:
- `agriculture`
- `ai`
- `machine-learning`
- `aws-bedrock`
- `voice-assistant`
- `fastapi`
- `python`
- `satellite-imagery`
- `crop-monitoring`
- `early-warning-system`
