# KrishiMitra - Windows Quick Start Guide

## Step-by-Step Setup for Windows

### 1. Check System Requirements

```powershell
# Check Python version (should be 3.10+)
python --version

# Check if Docker is installed
docker --version
docker-compose --version

# Check if Git is installed
git --version
```

If Docker is not installed, download from: https://www.docker.com/products/docker-desktop/

### 2. Create Virtual Environment

```powershell
# Create virtual environment
python -m venv venv

# Activate virtual environment
.\venv\Scripts\Activate.ps1

# If you get execution policy error, run:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### 3. Install Dependencies

```powershell
# Upgrade pip
python -m pip install --upgrade pip

# Install project dependencies
pip install -r requirements.txt
```

This will take a few minutes as it installs all required packages.

### 4. Configure Environment

```powershell
# Copy example environment file
Copy-Item .env.example .env

# Open .env in your editor
notepad .env
```

**Minimum required configuration for local development:**

```env
# Database (will be provided by Docker)
DATABASE_URL=postgresql://krishimitra:krishimitra_dev_password@localhost:5432/krishimitra

# Redis (will be provided by Docker)
REDIS_URL=redis://localhost:6379/0

# Kafka (will be provided by Docker)
KAFKA_BOOTSTRAP_SERVERS=localhost:9092

# Security (generate random strings for local dev)
JWT_SECRET_KEY=your-secret-key-here-change-this
ENCRYPTION_KEY=your-32-character-encryption-key

# AWS (use dummy values for local dev, or your actual credentials)
AWS_ACCESS_KEY_ID=your-aws-key
AWS_SECRET_ACCESS_KEY=your-aws-secret
AWS_REGION=us-east-1
S3_BUCKET_SATELLITE=your-satellite-bucket
S3_BUCKET_AUDIO=your-audio-bucket

# API Keys (use dummy values for local dev, or get real keys)
OPENAI_API_KEY=your-openai-key
TWILIO_ACCOUNT_SID=your-twilio-sid
TWILIO_AUTH_TOKEN=your-twilio-token
TWILIO_PHONE_NUMBER=+1234567890
ELEVENLABS_API_KEY=your-elevenlabs-key
SENTINEL_HUB_CLIENT_ID=your-sentinel-id
SENTINEL_HUB_CLIENT_SECRET=your-sentinel-secret
OPENWEATHERMAP_API_KEY=your-weather-key
```

### 5. Start Infrastructure Services

```powershell
# Start PostgreSQL, Redis, Kafka, and ChromaDB
docker-compose up -d

# Wait about 10 seconds for services to start
Start-Sleep -Seconds 10

# Check if services are running
docker ps
```

You should see 4 containers running:
- krishimitra-postgres
- krishimitra-redis
- krishimitra-kafka
- krishimitra-chromadb

### 6. Initialize Database

```powershell
# Create database tables using Alembic
alembic upgrade head

# Or use the init script
python scripts/init_db.py
```

### 7. (Optional) Seed Sample Data

```powershell
# Add sample farmers and farm plots for testing
python scripts/seed_data.py
```

### 8. Run the Application

```powershell
# Start the FastAPI server
python src/main.py
```

You should see:
```
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### 9. Test the Application

Open your browser and visit:

- **API Root**: http://localhost:8000
- **API Documentation**: http://localhost:8000/api/v1/docs
- **Health Check**: http://localhost:8000/health

Or use PowerShell:
```powershell
# Test root endpoint
Invoke-RestMethod -Uri http://localhost:8000

# Test health endpoint
Invoke-RestMethod -Uri http://localhost:8000/health
```

### 10. Using Helper Script

For convenience, use the PowerShell helper script:

```powershell
# Show all available commands
.\setup.ps1 help

# Run the application
.\setup.ps1 run

# Run tests
.\setup.ps1 test

# Check code quality
.\setup.ps1 lint

# Format code
.\setup.ps1 format
```

## Common Issues and Solutions

### Issue: "Execution Policy" Error

**Error**: `cannot be loaded because running scripts is disabled`

**Solution**:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Issue: Docker Services Not Starting

**Solution**:
```powershell
# Check Docker Desktop is running
# Restart Docker Desktop if needed

# Check service logs
docker-compose logs postgres
docker-compose logs redis
docker-compose logs kafka

# Restart services
docker-compose down
docker-compose up -d
```

### Issue: Port Already in Use

**Error**: `port is already allocated`

**Solution**: Edit `docker-compose.yml` and change the port mappings:
```yaml
ports:
  - "5433:5432"  # PostgreSQL (changed from 5432)
  - "6380:6379"  # Redis (changed from 6379)
```

Then update `.env` with the new ports.

### Issue: Database Connection Error

**Solution**:
```powershell
# Check if PostgreSQL is running
docker ps | Select-String postgres

# Check PostgreSQL logs
docker logs krishimitra-postgres

# Verify DATABASE_URL in .env matches Docker settings
```

### Issue: Module Import Errors

**Solution**:
```powershell
# Make sure virtual environment is activated
.\venv\Scripts\Activate.ps1

# Reinstall dependencies
pip install -r requirements.txt
```

## Development Workflow

### Daily Development

```powershell
# 1. Activate virtual environment
.\venv\Scripts\Activate.ps1

# 2. Start Docker services (if not running)
docker-compose up -d

# 3. Run the application
python src/main.py

# Or use the helper script
.\setup.ps1 run
```

### Making Changes

```powershell
# 1. Create a feature branch
git checkout -b feature/your-feature

# 2. Make your changes

# 3. Run tests
.\setup.ps1 test

# 4. Format code
.\setup.ps1 format

# 5. Check code quality
.\setup.ps1 lint

# 6. Commit changes
git add .
git commit -m "feat: your feature description"
```

### Database Changes

```powershell
# 1. Modify models in src/models/

# 2. Create migration
alembic revision --autogenerate -m "Add new field"

# 3. Review migration in alembic/versions/

# 4. Apply migration
alembic upgrade head

# 5. If needed, rollback
alembic downgrade -1
```

## Stopping Services

```powershell
# Stop the application
# Press Ctrl+C in the terminal running the app

# Stop Docker services
docker-compose down

# Stop and remove volumes (WARNING: deletes all data)
docker-compose down -v
```

## Next Steps

1. Review [design.md](design.md) for system architecture
2. Review [requirements.md](requirements.md) for features
3. Check [tasks.md](tasks.md) for implementation roadmap
4. Start implementing Phase 2: Data Ingestion & Processing

## Getting Help

- Check [SETUP.md](SETUP.md) for detailed setup instructions
- Check [CONTRIBUTING.md](CONTRIBUTING.md) for contribution guidelines
- Review error logs in the terminal
- Check Docker logs: `docker-compose logs`

---

**Happy Coding!** 🚀
