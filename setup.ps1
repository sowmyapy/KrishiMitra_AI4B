# KrishiMitra - Windows Setup Script
# PowerShell equivalent of Makefile commands

param(
    [Parameter(Position=0)]
    [string]$Command = "help"
)

function Show-Help {
    Write-Host "KrishiMitra - Development Commands" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Setup:" -ForegroundColor Yellow
    Write-Host "  .\setup.ps1 install       Install dependencies"
    Write-Host "  .\setup.ps1 dev-setup     Setup development environment"
    Write-Host ""
    Write-Host "Database:" -ForegroundColor Yellow
    Write-Host "  .\setup.ps1 db-init       Initialize database tables"
    Write-Host "  .\setup.ps1 db-migrate    Create new migration"
    Write-Host "  .\setup.ps1 db-upgrade    Apply migrations"
    Write-Host "  .\setup.ps1 db-downgrade  Rollback last migration"
    Write-Host ""
    Write-Host "Development:" -ForegroundColor Yellow
    Write-Host "  .\setup.ps1 run           Run development server"
    Write-Host "  .\setup.ps1 test          Run tests"
    Write-Host "  .\setup.ps1 lint          Run linters"
    Write-Host "  .\setup.ps1 format        Format code"
    Write-Host ""
    Write-Host "Docker:" -ForegroundColor Yellow
    Write-Host "  .\setup.ps1 docker-up     Start all services"
    Write-Host "  .\setup.ps1 docker-down   Stop all services"
    Write-Host "  .\setup.ps1 docker-logs   View service logs"
    Write-Host ""
    Write-Host "Utilities:" -ForegroundColor Yellow
    Write-Host "  .\setup.ps1 check         Check system requirements"
    Write-Host "  .\setup.ps1 seed          Seed database with sample data"
    Write-Host "  .\setup.ps1 clean         Remove cache and temp files"
}

function Install-Dependencies {
    Write-Host "Installing dependencies..." -ForegroundColor Cyan
    pip install -r requirements.txt
}

function Setup-DevEnvironment {
    Write-Host "Setting up development environment..." -ForegroundColor Cyan
    
    # Copy .env.example to .env if it doesn't exist
    if (-not (Test-Path ".env")) {
        Copy-Item ".env.example" ".env"
        Write-Host "✓ Created .env file (edit with your credentials)" -ForegroundColor Green
    } else {
        Write-Host "✓ .env file already exists" -ForegroundColor Green
    }
    
    # Start Docker services
    Write-Host "Starting Docker services..." -ForegroundColor Cyan
    docker-compose up -d
    
    Write-Host "Waiting for services to be ready..." -ForegroundColor Cyan
    Start-Sleep -Seconds 10
    
    # Apply migrations
    Write-Host "Applying database migrations..." -ForegroundColor Cyan
    alembic upgrade head
    
    Write-Host "✓ Development environment ready!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Next steps:" -ForegroundColor Yellow
    Write-Host "  1. Edit .env with your API keys and credentials"
    Write-Host "  2. Run: .\setup.ps1 run"
}

function Initialize-Database {
    Write-Host "Initializing database..." -ForegroundColor Cyan
    python scripts/init_db.py
}

function Create-Migration {
    $message = Read-Host "Enter migration message"
    Write-Host "Creating migration: $message" -ForegroundColor Cyan
    alembic revision --autogenerate -m "$message"
}

function Upgrade-Database {
    Write-Host "Applying migrations..." -ForegroundColor Cyan
    alembic upgrade head
}

function Downgrade-Database {
    Write-Host "Rolling back last migration..." -ForegroundColor Cyan
    alembic downgrade -1
}

function Start-Application {
    Write-Host "Starting KrishiMitra..." -ForegroundColor Cyan
    python src/main.py
}

function Run-Tests {
    Write-Host "Running tests..." -ForegroundColor Cyan
    pytest tests/ -v --cov=src --cov-report=html
}

function Run-Linters {
    Write-Host "Running linters..." -ForegroundColor Cyan
    ruff check src/ tests/
    mypy src/
}

function Format-Code {
    Write-Host "Formatting code..." -ForegroundColor Cyan
    ruff format src/ tests/
    ruff check --fix src/ tests/
}

function Start-Docker {
    Write-Host "Starting Docker services..." -ForegroundColor Cyan
    docker-compose up -d
    Write-Host "Waiting for services to be ready..." -ForegroundColor Cyan
    Start-Sleep -Seconds 10
    Write-Host "✓ Services started" -ForegroundColor Green
}

function Stop-Docker {
    Write-Host "Stopping Docker services..." -ForegroundColor Cyan
    docker-compose down
}

function Show-DockerLogs {
    Write-Host "Showing Docker logs (Ctrl+C to exit)..." -ForegroundColor Cyan
    docker-compose logs -f
}

function Check-Requirements {
    Write-Host "Checking system requirements..." -ForegroundColor Cyan
    python scripts/check_requirements.py
}

function Seed-Database {
    Write-Host "Seeding database with sample data..." -ForegroundColor Cyan
    python scripts/seed_data.py
}

function Clean-Project {
    Write-Host "Cleaning project..." -ForegroundColor Cyan
    
    # Remove __pycache__ directories
    Get-ChildItem -Path . -Recurse -Directory -Filter "__pycache__" | Remove-Item -Recurse -Force
    
    # Remove .pyc and .pyo files
    Get-ChildItem -Path . -Recurse -File -Include "*.pyc", "*.pyo" | Remove-Item -Force
    
    # Remove cache directories
    $cacheDirs = @(".pytest_cache", ".mypy_cache", ".ruff_cache", "htmlcov")
    foreach ($dir in $cacheDirs) {
        if (Test-Path $dir) {
            Remove-Item -Path $dir -Recurse -Force
        }
    }
    
    # Remove coverage files
    if (Test-Path ".coverage") {
        Remove-Item ".coverage" -Force
    }
    
    Write-Host "✓ Project cleaned" -ForegroundColor Green
}

# Main command dispatcher
switch ($Command.ToLower()) {
    "help" { Show-Help }
    "install" { Install-Dependencies }
    "dev-setup" { Setup-DevEnvironment }
    "db-init" { Initialize-Database }
    "db-migrate" { Create-Migration }
    "db-upgrade" { Upgrade-Database }
    "db-downgrade" { Downgrade-Database }
    "run" { Start-Application }
    "test" { Run-Tests }
    "lint" { Run-Linters }
    "format" { Format-Code }
    "docker-up" { Start-Docker }
    "docker-down" { Stop-Docker }
    "docker-logs" { Show-DockerLogs }
    "check" { Check-Requirements }
    "seed" { Seed-Database }
    "clean" { Clean-Project }
    default {
        Write-Host "Unknown command: $Command" -ForegroundColor Red
        Write-Host ""
        Show-Help
    }
}
