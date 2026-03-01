# Quick start script for KrishiMitra (Windows PowerShell)

Write-Host "🌾 KrishiMitra Quick Start" -ForegroundColor Cyan
Write-Host "==========================" -ForegroundColor Cyan
Write-Host ""

# Check Python version
Write-Host "Checking Python version..." -ForegroundColor Yellow
$pythonVersion = python --version 2>&1
Write-Host "✓ $pythonVersion" -ForegroundColor Green
Write-Host ""

# Create virtual environment if it doesn't exist
if (-not (Test-Path "venv")) {
    Write-Host "Creating virtual environment..." -ForegroundColor Yellow
    python -m venv venv
    Write-Host "✓ Virtual environment created" -ForegroundColor Green
} else {
    Write-Host "✓ Virtual environment exists" -ForegroundColor Green
}
Write-Host ""

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
& .\venv\Scripts\Activate.ps1
Write-Host "✓ Virtual environment activated" -ForegroundColor Green
Write-Host ""

# Install dependencies
Write-Host "Installing dependencies..." -ForegroundColor Yellow
pip install -q --upgrade pip
pip install -q -r requirements.txt
Write-Host "✓ Dependencies installed" -ForegroundColor Green
Write-Host ""

# Setup environment
if (-not (Test-Path ".env")) {
    Write-Host "Setting up environment..." -ForegroundColor Yellow
    Copy-Item ".env.test" ".env"
    Write-Host "✓ Created .env file (using test configuration)" -ForegroundColor Green
    Write-Host "⚠️  For production, update .env with real API keys" -ForegroundColor Yellow
} else {
    Write-Host "✓ .env file exists" -ForegroundColor Green
}
Write-Host ""

# Initialize database
Write-Host "Initializing database..." -ForegroundColor Yellow
python scripts/init_db.py
Write-Host "✓ Database initialized" -ForegroundColor Green
Write-Host ""

# Seed sample data
Write-Host "Seeding sample data..." -ForegroundColor Yellow
python scripts/seed_data.py
Write-Host "✓ Sample data created" -ForegroundColor Green
Write-Host ""

Write-Host "==========================" -ForegroundColor Cyan
Write-Host "✅ Setup complete!" -ForegroundColor Green
Write-Host ""
Write-Host "To start the application:" -ForegroundColor Cyan
Write-Host "  python src/main.py"
Write-Host ""
Write-Host "Or visit the API documentation:" -ForegroundColor Cyan
Write-Host "  http://localhost:8000/api/v1/docs"
Write-Host ""
Write-Host "For full setup with Docker services:" -ForegroundColor Cyan
Write-Host "  docker-compose up -d"
Write-Host "  python src/main.py"
Write-Host ""
