# Installing Git on Windows

## Option 1: Download from Official Website (Recommended)

1. **Download Git for Windows**
   - Go to: https://git-scm.com/download/win
   - The download should start automatically
   - Or click "Click here to download manually"

2. **Run the Installer**
   - Double-click the downloaded `.exe` file
   - Click "Next" through the installation wizard
   - **Recommended settings:**
     - Use default installation directory
     - Select "Git from the command line and also from 3rd-party software"
     - Use "Use bundled OpenSSH"
     - Use "Use the OpenSSL library"
     - Checkout Windows-style, commit Unix-style line endings
     - Use MinTTY (default terminal)
     - Default pull behavior: Fast-forward or merge
     - Enable Git Credential Manager

3. **Verify Installation**
   ```powershell
   git --version
   ```
   Should show something like: `git version 2.43.0.windows.1`

## Option 2: Using Winget (Windows Package Manager)

If you have Windows 10/11 with winget installed:

```powershell
winget install --id Git.Git -e --source winget
```

## Option 3: Using Chocolatey

If you have Chocolatey installed:

```powershell
choco install git
```

## After Installation

1. **Configure Git with your details:**
   ```powershell
   git config --global user.name "Your Name"
   git config --global user.email "your.email@example.com"
   ```

2. **Verify configuration:**
   ```powershell
   git config --list
   ```

## Next Steps

Once Git is installed, you can initialize your repository:

```powershell
# Navigate to your project directory
cd C:\Users\Sowmya\OneDrive\projects\ai_crop_system

# Initialize Git repository
git init

# Add all files
git add .

# Create first commit
git commit -m "Initial commit: KrishiMitra - AI-powered farmer early warning system"

# (Optional) Add remote repository
git remote add origin https://github.com/yourusername/krishimitra.git

# (Optional) Push to remote
git push -u origin main
```

## Troubleshooting

**If git command not found after installation:**
- Close and reopen PowerShell/Terminal
- Or restart your computer
- Check if Git is in PATH: `$env:PATH -split ';' | Select-String git`

**If you need to add Git to PATH manually:**
1. Search for "Environment Variables" in Windows
2. Edit "Path" variable
3. Add: `C:\Program Files\Git\cmd`
4. Click OK and restart terminal
