# KrishiMitra UI Setup Script for Windows
# Run this script to automatically set up the frontend

Write-Host "========================================" -ForegroundColor Green
Write-Host "  KrishiMitra UI Setup" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""

# Check if Node.js is installed
Write-Host "Checking Node.js installation..." -ForegroundColor Yellow
try {
    $nodeVersion = node --version
    Write-Host "✓ Node.js $nodeVersion found" -ForegroundColor Green
} catch {
    Write-Host "✗ Node.js not found. Please install Node.js 18+ from https://nodejs.org" -ForegroundColor Red
    exit 1
}

# Check if npm is installed
try {
    $npmVersion = npm --version
    Write-Host "✓ npm $npmVersion found" -ForegroundColor Green
} catch {
    Write-Host "✗ npm not found" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "Creating frontend project..." -ForegroundColor Yellow

# Create frontend directory if it doesn't exist
if (Test-Path "frontend") {
    Write-Host "⚠ frontend directory already exists" -ForegroundColor Yellow
    $response = Read-Host "Do you want to continue? This will overwrite files (y/n)"
    if ($response -ne "y") {
        Write-Host "Setup cancelled" -ForegroundColor Red
        exit 0
    }
} else {
    # Create Vite project
    npm create vite@latest frontend -- --template react-ts
}

# Navigate to frontend directory
Set-Location frontend

Write-Host ""
Write-Host "Installing dependencies..." -ForegroundColor Yellow
Write-Host "This may take a few minutes..." -ForegroundColor Gray

# Install all dependencies
npm install

# Install UI framework
npm install @mui/material @emotion/react @emotion/styled @mui/icons-material

# Install routing
npm install react-router-dom

# Install API client
npm install axios

# Install data fetching
npm install @tanstack/react-query

# Install forms
npm install react-hook-form @hookform/resolvers zod

# Install maps
npm install leaflet react-leaflet
npm install -D @types/leaflet

# Install charts
npm install recharts

# Install date handling
npm install date-fns

# Install notifications
npm install notistack

# Install i18n
npm install react-i18next i18next

# Install dev dependencies
npm install -D @types/node

Write-Host ""
Write-Host "✓ Dependencies installed" -ForegroundColor Green

# Create directory structure
Write-Host ""
Write-Host "Creating directory structure..." -ForegroundColor Yellow

$directories = @(
    "src/api",
    "src/components/common",
    "src/components/dashboard",
    "src/components/farmer",
    "src/components/advisory",
    "src/pages",
    "src/hooks",
    "src/contexts",
    "src/utils",
    "src/types",
    "public/assets"
)

foreach ($dir in $directories) {
    New-Item -ItemType Directory -Force -Path $dir | Out-Null
}

Write-Host "✓ Directory structure created" -ForegroundColor Green

# Create .env file
Write-Host ""
Write-Host "Creating .env file..." -ForegroundColor Yellow

$envContent = @"
VITE_API_BASE_URL=http://localhost:8000
VITE_APP_NAME=KrishiMitra
VITE_GOOGLE_MAPS_API_KEY=
"@

Set-Content -Path ".env" -Value $envContent

Write-Host "✓ .env file created" -ForegroundColor Green

# Create .env.example
Set-Content -Path ".env.example" -Value $envContent

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "  Setup Complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "1. Copy configuration files from UI_SETUP_GUIDE.md" -ForegroundColor White
Write-Host "2. Create components from UI_DEVELOPMENT_GUIDE.md" -ForegroundColor White
Write-Host "3. Start development server:" -ForegroundColor White
Write-Host "   npm run dev" -ForegroundColor Cyan
Write-Host ""
Write-Host "The UI will be available at: http://localhost:3000" -ForegroundColor Green
Write-Host ""
Write-Host "Make sure the backend is running on: http://localhost:8000" -ForegroundColor Yellow
Write-Host ""

# Ask if user wants to start dev server
$startServer = Read-Host "Do you want to start the development server now? (y/n)"
if ($startServer -eq "y") {
    Write-Host ""
    Write-Host "Starting development server..." -ForegroundColor Green
    Write-Host "Press Ctrl+C to stop" -ForegroundColor Gray
    Write-Host ""
    npm run dev
}
