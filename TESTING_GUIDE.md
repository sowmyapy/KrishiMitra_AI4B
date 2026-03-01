# KrishiMitra - Testing Guide

## Pre-Testing Checklist

### 1. Install Dependencies

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Setup Environment Variables

```bash
# Copy example env file
cp .env.example .env

# Edit .env and add your API keys:
# - DATABASE_URL (use local PostgreSQL or SQLite for testing)
# - AWS credentials (can use dummy values for local testing)
# - OpenAI API key (required for AI features)
# - Twilio credentials (required for voice features)
# - ElevenLabs API key (required for TTS)
```

### 3. Start Infrastructure Services

```bash
# Start Docker services (PostgreSQL, Redis, Kafka, ChromaDB)
docker-compose up -d

# Wait for services to be ready
sleep 10
```

### 4. Initialize Database

```bash
# Run database migrations
alembic upgrade head

# Or use init script
python scripts/init_db.py

# Seed sample data (optional)
python scripts/seed_data.py
```

## Quick Test Options

### Option 1: Basic API Test (No External Services)

For testing without external API keys, you can use SQLite and mock services:

```bash
# Set minimal .env
DATABASE_URL=sqlite:///./test.db
JWT_SECRET_KEY=test-secret-key-change-in-production
ENCRYPTION_KEY=test-encryption-key-32-bytes!!

# Run the app
python src/main.py
```

Visit: http://localhost:8000/api/v1/docs

### Option 2: Full Integration Test (With External Services)

Requires all API keys configured in .env:

```bash
# Ensure all services are running
docker-compose ps

# Run the app
python src/main.py
```

### Option 3: Run Unit Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test file
pytest tests/test_main.py -v
```

## Testing Endpoints

### 1. Health Check

```bash
curl http://localhost:8000/health
```

Expected response:
```json
{
  "status": "healthy",
  "version": "0.1.0"
}
```

### 2. API Documentation

Open in browser: http://localhost:8000/api/v1/docs

This provides interactive API documentation where you can test all endpoints.

### 3. Create a Farmer

```bash
curl -X POST http://localhost:8000/api/v1/farmers/ \
  -H "Content-Type: application/json" \
  -d '{
    "phone_number": "+919876543210",
    "preferred_language": "hi",
    "timezone": "Asia/Kolkata"
  }'
```

### 4. List Farmers

```bash
curl http://localhost:8000/api/v1/farmers/
```

## Common Issues & Solutions

### Issue 1: Database Connection Error

**Error**: `sqlalchemy.exc.OperationalError: could not connect to server`

**Solution**:
```bash
# Check if PostgreSQL is running
docker-compose ps

# Restart PostgreSQL
docker-compose restart postgres

# Or use SQLite for testing
DATABASE_URL=sqlite:///./test.db
```

### Issue 2: Missing API Keys

**Error**: `ValidationError: field required`

**Solution**: Add required API keys to .env file. For testing, you can use dummy values:
```bash
AWS_ACCESS_KEY_ID=test
AWS_SECRET_ACCESS_KEY=test
OPENAI_API_KEY=sk-test
TWILIO_ACCOUNT_SID=test
TWILIO_AUTH_TOKEN=test
TWILIO_PHONE_NUMBER=+1234567890
ELEVENLABS_API_KEY=test
SENTINEL_HUB_CLIENT_ID=test
SENTINEL_HUB_CLIENT_SECRET=test
OPENWEATHERMAP_API_KEY=test
S3_BUCKET_SATELLITE=test-bucket
S3_BUCKET_AUDIO=test-bucket
```

### Issue 3: Port Already in Use

**Error**: `OSError: [Errno 48] Address already in use`

**Solution**:
```bash
# Find process using port 8000
lsof -i :8000  # On Linux/Mac
netstat -ano | findstr :8000  # On Windows

# Kill the process or use different port
API_PORT=8001 python src/main.py
```

### Issue 4: Import Errors

**Error**: `ModuleNotFoundError: No module named 'src'`

**Solution**:
```bash
# Ensure you're in the project root
pwd

# Add project to PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$(pwd)"  # Linux/Mac
set PYTHONPATH=%PYTHONPATH%;%CD%  # Windows
```

## Testing Individual Components

### Test NDVI Calculator

```python
from src.services.monitoring.ndvi_calculator import NDVICalculator
import numpy as np

calculator = NDVICalculator()

# Test NDVI calculation
nir = np.array([0.8, 0.7, 0.9])
red = np.array([0.2, 0.3, 0.1])
ndvi = calculator.calculate_ndvi(nir, red)
print(f"NDVI: {ndvi}")
```

### Test Weather Analyzer

```python
from src.services.monitoring.weather_analyzer import WeatherAnalyzer

analyzer = WeatherAnalyzer()

current_weather = {
    "temperature": 35,
    "humidity": 40,
    "wind_speed": 20
}

forecast = [
    {"temp_max": 38, "temp_min": 25, "pop": 0.1}
]

weather_history = []

risks = analyzer.analyze_weather_risks(current_weather, forecast, weather_history)
print(f"Weather risks: {risks}")
```

### Test Stress Predictor

```python
from src.services.prediction.stress_predictor import StressPredictor

predictor = StressPredictor()

ndvi_data = {"mean": 0.3, "std": 0.1, "min": 0.2, "max": 0.4}
weather_data = {
    "temperature": 35,
    "humidity": 40,
    "rainfall_7day": 5,
    "rainfall_30day": 20,
    "wind_speed": 15,
    "heat_stress": {"risk_level": "high"},
    "drought": {"risk_level": "medium"},
    "frost": {"risk_level": "none"},
    "wind_damage": {"risk_level": "low"}
}

prediction = predictor.predict_stress(ndvi_data, weather_data)
print(f"Prediction: {prediction}")
```

## Performance Testing

### Load Test with Apache Bench

```bash
# Install Apache Bench
sudo apt-get install apache2-utils  # Linux
brew install httpd  # Mac

# Test health endpoint
ab -n 1000 -c 10 http://localhost:8000/health

# Expected: <200ms p95 response time
```

### Monitor Resource Usage

```bash
# Monitor Docker containers
docker stats

# Monitor Python process
top -p $(pgrep -f "python src/main.py")
```

## Next Steps After Testing

1. Review logs in `logs/` directory
2. Check API documentation at `/api/v1/docs`
3. Test with real farmer data
4. Configure production environment
5. Set up monitoring and alerts
6. Deploy to staging environment

## Getting Help

- Check logs: `tail -f logs/app.log`
- Run diagnostics: `python scripts/check_requirements.py`
- Review documentation: `README.md`, `SETUP.md`
- Check GitHub issues or contact team

---

**Note**: For production deployment, ensure all security measures are in place:
- Use strong JWT secret keys
- Enable HTTPS/TLS
- Configure proper CORS origins
- Set up rate limiting
- Enable audit logging
- Use production-grade database
