# Push to GitHub - Quick Commands

## Quick Start (Copy & Paste)

```powershell
# 1. Check what will be committed
git status

# 2. Add all files (gitignore will protect secrets)
git add .

# 3. Verify no sensitive files
git status | Select-String ".env"
# Should only show .env.example, NOT .env

# 4. Commit with message
git commit -m "feat: Complete KrishiMitra AI farmer advisory system

- Full-stack FastAPI application with JWT auth
- AWS Bedrock + Transcribe + Polly integration  
- Agentic AI system for crop monitoring
- Voice advisory in 10+ Indian languages
- End-to-end testing suite
- Ready for production deployment"

# 5. Create GitHub repo (if not done)
# Go to https://github.com/new and create repository

# 6. Push to GitHub
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git push -u origin main
```

## If Repository Already Exists

```powershell
# Just push
git push
```

## Verify Before Pushing

```powershell
# Check for secrets in staged files
git diff --cached | Select-String -Pattern "secret|password|key|token" -CaseSensitive:$false

# List files to be committed
git diff --cached --name-only

# Should NOT include:
# - .env (only .env.example is OK)
# - *.db files
# - venv/ folder
# - __pycache__/ folders
```

## What Gets Pushed

### ✓ Will Be Pushed (Good)
- All Python source code (`src/`, `scripts/`)
- Documentation (all `.md` files)
- Configuration templates (`.env.example`)
- Requirements files (`requirements*.txt`)
- Docker files (`Dockerfile`, `docker-compose.yml`)
- GitHub Actions (`.github/workflows/`)
- Infrastructure code (`infrastructure/`)

### ✗ Will NOT Be Pushed (Protected by .gitignore)
- `.env` - Your secrets
- `venv/` - Virtual environment
- `*.db` - Database files
- `__pycache__/` - Python cache
- `*.log` - Log files
- `.aws/` - AWS credentials

## After Pushing

1. **Verify on GitHub**:
   - Go to your repository URL
   - Check no `.env` file is visible
   - Verify README.md displays correctly

2. **Add Repository Details**:
   - Description: "AI-powered farmer early warning system with voice advisory"
   - Topics: `agriculture`, `ai`, `fastapi`, `aws`, `voice-assistant`, `hindi`
   - Website: Your demo URL (if deployed)

3. **Update README** (optional):
   - Add demo screenshots
   - Add setup instructions
   - Add contribution guidelines

## Common Commands

```powershell
# Check current branch
git branch

# Check remote
git remote -v

# View commit history
git log --oneline -10

# Undo last commit (keep changes)
git reset --soft HEAD~1

# Undo last commit (discard changes)
git reset --hard HEAD~1

# Update from remote
git pull

# Create new branch
git checkout -b feature/new-feature

# Switch branch
git checkout main
```

## Troubleshooting

### Problem: .env file appears in git status

```powershell
# Remove from staging
git reset HEAD .env

# Or remove from git entirely
git rm --cached .env
```

### Problem: Accidentally committed .env

```powershell
# Remove from last commit
git reset --soft HEAD~1
git reset HEAD .env
git commit -m "Your commit message"

# If already pushed - ROTATE ALL CREDENTIALS IMMEDIATELY!
```

### Problem: Large files error

```powershell
# Remove large file
git rm --cached path/to/large/file

# Add to .gitignore
echo "path/to/large/file" >> .gitignore
```

### Problem: Merge conflicts

```powershell
# Pull latest changes
git pull

# Resolve conflicts in files
# Then:
git add .
git commit -m "Resolve merge conflicts"
git push
```

## Security Reminder

Before pushing, always verify:
1. ✓ No `.env` file in git status
2. ✓ No database files (`.db`, `.sqlite3`)
3. ✓ No API keys in code
4. ✓ No passwords in comments
5. ✓ `.gitignore` is working

## Ready to Push?

Run this final check:
```powershell
# 1. Status check
git status

# 2. Search for secrets
git diff --cached | Select-String "AWS_SECRET|TWILIO_AUTH|JWT_SECRET"

# 3. If nothing found, you're good to go!
git push
```

## Your Repository Info

After creating on GitHub, update these:
- Repository URL: `https://github.com/YOUR_USERNAME/krishimitra`
- Clone command: `git clone https://github.com/YOUR_USERNAME/krishimitra.git`

## Next Steps After Push

1. Set up GitHub Actions for CI/CD
2. Add branch protection rules
3. Enable Dependabot for security updates
4. Add collaborators (if team project)
5. Create issues for future features
6. Set up project board for tracking

Good luck with your push! 🚀
