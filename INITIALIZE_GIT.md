# Initialize Git Repository - Step by Step

## Step 1: Initialize Git

```powershell
# Initialize git repository
git init

# Check status
git status
```

## Step 2: Configure Git (First Time Only)

```powershell
# Set your name
git config --global user.name "Your Name"

# Set your email
git config --global user.email "your.email@example.com"

# Verify configuration
git config --list
```

## Step 3: Add Files

```powershell
# Add all files (gitignore will protect secrets)
git add .

# Check what was added
git status
```

## Step 4: First Commit

```powershell
git commit -m "Initial commit: KrishiMitra AI Farmer Advisory System

Complete implementation with:
- FastAPI REST API with JWT authentication
- AWS Bedrock, Transcribe, Polly integration
- Agentic AI system (Monitoring, Diagnostic, Advisory agents)
- Voice chatbot with Hindi support
- End-to-end testing suite
- SQLite database with 12 tables
- Multi-language support (10+ Indian languages)
- Ready for Twilio voice call integration

Tech Stack: Python, FastAPI, AWS, PostgreSQL/SQLite"
```

## Step 5: Create GitHub Repository

1. Go to https://github.com/new
2. Repository name: `krishimitra` (or your choice)
3. Description: "AI-powered farmer early warning system with voice advisory in Indian languages"
4. Choose Public or Private
5. **DO NOT** check "Initialize with README" (you already have one)
6. Click "Create repository"

## Step 6: Connect to GitHub

```powershell
# Add remote (replace YOUR_USERNAME and YOUR_REPO)
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git

# Verify remote
git remote -v
```

## Step 7: Push to GitHub

```powershell
# Rename branch to main (if needed)
git branch -M main

# Push to GitHub
git push -u origin main
```

## Complete Command Sequence

Copy and paste these commands one by one:

```powershell
# 1. Initialize
git init

# 2. Configure (replace with your info)
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

# 3. Add files
git add .

# 4. Check status (verify no .env file)
git status

# 5. Commit
git commit -m "Initial commit: KrishiMitra AI Farmer Advisory System"

# 6. Create repo on GitHub (do this in browser)
# Then come back and run:

# 7. Add remote (replace YOUR_USERNAME/YOUR_REPO)
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git

# 8. Push
git branch -M main
git push -u origin main
```

## Verify Before Pushing

```powershell
# Check what will be pushed
git status

# Verify no secrets
git ls-files | Select-String ".env"
# Should only show .env.example, NOT .env
```

## If You See .env in Git

```powershell
# Remove it
git rm --cached .env

# Commit the removal
git commit -m "Remove .env from tracking"
```

## After Successful Push

Your code is now on GitHub! 🎉

Visit: `https://github.com/YOUR_USERNAME/YOUR_REPO`

## Next Steps

1. Add repository description and topics on GitHub
2. Enable GitHub Actions (if using CI/CD)
3. Add collaborators (if team project)
4. Share the repository link!

## Troubleshooting

### Error: "fatal: not a git repository"
**Solution**: Run `git init` first

### Error: "remote origin already exists"
**Solution**: 
```powershell
git remote remove origin
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
```

### Error: "failed to push some refs"
**Solution**:
```powershell
git pull origin main --rebase
git push -u origin main
```

### Error: "Permission denied (publickey)"
**Solution**: Use HTTPS instead of SSH, or set up SSH keys

## Need Help?

- Git documentation: https://git-scm.com/doc
- GitHub guides: https://guides.github.com/
- Git cheat sheet: https://education.github.com/git-cheat-sheet-education.pdf
