# KrishiMitra - Development Setup Guide

> **Windows Users**: See [QUICKSTART_WINDOWS.md](QUICKSTART_WINDOWS.md) for Windows-specific setup instructions.

## Prerequisites

- Python 3.10+
- Docker & Docker Compose
- Git

## Quick Start

### 1. Clone and Setup Environment

```bash
# Clone the repository
git clone <repository-url>
cd krishimitra

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Environment Variables

```bash
# Copy example environment file
cp .env.example .env

# Edit .env with your credentials
# Required: Database, AWS, API keys for external services
```

### 3. Start Infrastructure Services

```bash
# Start PostgreSQL, Redis, Kafka, ChromaDB
docker-compose up -d

# Wait for services to be ready (about 10 seconds)
```

### 4. Initialize Database

```bash
# Create initial migration
alembic revision --autogenerate -m "Initial migration"

# Apply migrations
alembic upgrade head

# Or use the init script
python scripts/init_db.py
```

### 5. Run the Application

```bash
# Development mode with auto-reload
python src/main.py

# Or using uvicorn directly
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

### 6. Access the Application

- API: http://localhost:8000
- API Documentation: http://localhost:8000/api/v1/docs
- Health Check: http://localhost:8000/health

## Using Make Commands

If you have Make installed, you can use convenient shortcuts:

```bash
# Setup everything
make dev-setup

# Run application
make run

# Database operations
make db-migrate      # Create new migration
make db-upgrade      # Apply migrations
make db-downgrade    # Rollback migration

# Testing
make test           # Run tests with coverage
make lint           # Run linters
make format         # Format code

# Docker
make docker-up      # Start services
make docker-down    # Stop services
make docker-logs    # View logs

# Cleanup
make clean          # Remove cache files
```

## Database Migrations

### Create a New Migration

```bash
# Auto-generate migration from model changes
alembic revision --autogenerate -m "Add new field to farmer model"

# Create empty migration (for data migrations)
alembic revision -m "Seed initial data"
```

### Apply Migrations

```bash
# Upgrade to latest
alembic upgrade head

# Upgrade by one version
alembic upgrade +1

# Downgrade by one version
alembic downgrade -1

# View migration history
alembic history

# View current version
alembic current
```

## Testing

### Run All Tests

```bash
pytest
```

### Run Specific Test Types

```bash
# Unit tests only
pytest -m unit

# Integration tests only
pytest -m integration

# With coverage report
pytest --cov=src --cov-report=html
```

### Run Specific Test File

```bash
pytest tests/test_main.py -v
```

## Code Quality

### Linting

```bash
# Check code with ruff
ruff check src/ tests/

# Auto-fix issues
ruff check --fix src/ tests/

# Type checking with mypy
mypy src/
```

### Formatting

```bash
# Format with ruff
ruff format src/ tests/

# Or use black
black src/ tests/
```

## Development Workflow

### 1. Create a New Feature

```bash
# Create feature branch
git checkout -b feature/your-feature-name

# Make changes to code
# Update models if needed

# Create migration if models changed
alembic revision --autogenerate -m "Add feature X"

# Apply migration
alembic upgrade head

# Run tests
pytest

# Format and lint
make format
make lint
```

### 2. Before Committing

```bash
# Run all checks
make test
make lint

# Ensure all tests pass
# Ensure no linting errors
```

## Troubleshooting

### Database Connection Issues

```bash
# Check if PostgreSQL is running
docker ps | grep postgres

# View PostgreSQL logs
docker logs krishimitra-postgres

# Restart PostgreSQL
docker-compose restart postgres
```

### Redis Connection Issues

```bash
# Check if Redis is running
docker ps | grep redis

# Test Redis connection
docker exec -it krishimitra-redis redis-cli ping
```

### Kafka Issues

```bash
# Check if Kafka is running
docker ps | grep kafka

# View Kafka logs
docker logs krishimitra-kafka

# List Kafka topics
docker exec -it krishimitra-kafka kafka-topics --list --bootstrap-server localhost:9092
```

### Migration Issues

```bash
# View current migration status
alembic current

# View migration history
alembic history

# Rollback to specific version
alembic downgrade <revision_id>

# Reset database (WARNING: destroys all data)
python scripts/init_db.py --drop
alembic upgrade head
```

### Port Conflicts

If ports are already in use, modify `docker-compose.yml`:

```yaml
# Change port mappings
ports:
  - "5433:5432"  # PostgreSQL
  - "6380:6379"  # Redis
  - "9093:9092"  # Kafka
```

Then update `.env` with new ports.

## Environment Variables Reference

See `.env.example` for all available configuration options.

### Required Variables

- `DATABASE_URL`: PostgreSQL connection string
- `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`: AWS credentials
- `OPENAI_API_KEY`: OpenAI API key
- `TWILIO_ACCOUNT_SID`, `TWILIO_AUTH_TOKEN`: Twilio credentials
- `JWT_SECRET_KEY`: Secret key for JWT tokens
- `ENCRYPTION_KEY`: Encryption key for sensitive data

### Optional Variables

- `REDIS_URL`: Redis connection string (default: localhost)
- `KAFKA_BOOTSTRAP_SERVERS`: Kafka servers (default: localhost:9092)
- `ENABLE_AGENTIC_AI`: Enable/disable Agentic AI features
- `ENABLE_VOICE_CHATBOT`: Enable/disable Voice Chatbot

## Next Steps

1. Review the [Design Document](design.md) for system architecture
2. Review the [Requirements Document](requirements.md) for feature specifications
3. Check [Tasks](tasks.md) for implementation roadmap
4. Start implementing Phase 2: Data Ingestion & Processing

## Support

For issues or questions:
- Check existing documentation
- Review error logs in `logs/` directory
- Check Docker container logs
- Consult the team

---

**Last Updated**: 2024-01-15
