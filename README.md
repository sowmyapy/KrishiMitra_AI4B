# KrishiMitra

**Empowering farmers with AI-driven insights, delivered by voice**

## Overview

KrishiMitra is an AI-powered agricultural early warning system that monitors crop health using satellite imagery and weather data. When potential issues are detected, the system proactively contacts farmers via voice calls in their local language, providing personalized, actionable advice through natural conversations.

## Key Features

- 🛰️ **Satellite Monitoring**: Continuous crop health monitoring using satellite imagery (NDVI, moisture levels)
- 🌤️ **Weather Integration**: Real-time weather data analysis and forecasting
- 🤖 **Agentic AI**: 5 specialized AI agents working together for intelligent decision-making
- 🎙️ **Voice Chatbot**: Natural speech conversations in 10+ Indian languages
- 📞 **Proactive Alerts**: Early warnings 3+ days before critical crop damage
- 💬 **24/7 Support**: Interactive voice assistant available anytime
- 📊 **Continuous Learning**: System improves automatically from farmer outcomes

## Architecture

- **Backend**: Python (FastAPI)
- **ML/AI**: TensorFlow, scikit-learn, OpenAI GPT-4 / AWS Bedrock
- **Databases**: PostgreSQL (PostGIS), Redis
- **Message Queue**: Apache Kafka / Amazon MSK
- **Voice**: Twilio, OpenAI Whisper / AWS Transcribe, ElevenLabs / AWS Polly
- **Cloud**: AWS (ECS Fargate, S3, RDS, Lambda, Bedrock)
- **Monitoring**: CloudWatch, Prometheus, Grafana

### Provider Flexibility

KrishiMitra supports multiple AI/ML providers:

**Option 1: OpenAI + ElevenLabs (Default)**
- LLM: OpenAI GPT-4
- STT: OpenAI Whisper
- TTS: ElevenLabs
- Best for: Development, highest quality

**Option 2: AWS Native Services**
- LLM: AWS Bedrock (Claude v2)
- STT: AWS Transcribe
- TTS: AWS Polly
- Best for: Production, cost optimization (38% savings)

**Option 3: Hybrid (Recommended)**
- LLM: AWS Bedrock
- STT: OpenAI Whisper
- TTS: ElevenLabs
- Best for: Balance of cost and quality

See [docs/PROVIDER_SELECTION_GUIDE.md](docs/PROVIDER_SELECTION_GUIDE.md) for details.

## Project Structure

```
krishimitra/
├── src/
│   ├── api/                 # REST API endpoints
│   ├── services/            # Core business services
│   │   ├── data_ingestion/  # Satellite & weather data collection
│   │   ├── monitoring/      # Crop health analysis
│   │   ├── prediction/      # ML-based stress prediction
│   │   ├── agents/          # Agentic AI system
│   │   └── communication/   # Voice & chatbot services
│   ├── models/              # Data models and schemas
│   ├── utils/               # Utility functions
│   └── config/              # Configuration management
├── tests/                   # Unit and integration tests
├── scripts/                 # Deployment and utility scripts
├── infrastructure/          # IaC (Terraform/CloudFormation)
├── docs/                    # Documentation
├── requirements.md          # Project requirements
├── design.md               # System design document
└── tasks.md                # Implementation tasks
```

## Getting Started

For detailed setup instructions, see [SETUP.md](SETUP.md).

### Quick Start - AWS Only (Recommended)

If you want to use AWS services exclusively (Bedrock, Transcribe, Polly):

**See [INSTALL_STEPS.md](INSTALL_STEPS.md) for detailed step-by-step instructions.**

```powershell
# 1. Create virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1

# 2. Install AWS-only dependencies (no OpenAI packages)
pip install -r requirements-aws.txt

# 3. Configure AWS
aws configure

# 4. Create S3 bucket
aws s3 mb s3://krishimitra-audio-ap-south-1 --region ap-south-1

# 5. Setup environment
cp .env.example .env
# Edit .env: Set LLM_PROVIDER=bedrock, USE_AWS_SERVICES=True

# 6. Test AWS integration
python scripts/test_aws_integration.py

# 7. Run application
uvicorn src.main:app --reload
```

### Quick Start - Full Setup (All Providers)

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Setup environment
cp .env.example .env
# Edit .env with your credentials

# 3. Start infrastructure
docker-compose up -d

# 4. Initialize database
alembic upgrade head

# 5. Run application
python src/main.py
```

Access the API at http://localhost:8000 and documentation at http://localhost:8000/api/v1/docs

### Prerequisites

**For AWS-Only Setup**:
- Python 3.11+
- AWS CLI configured
- AWS Account with Bedrock, Transcribe, Polly access

**For Full Setup**:
- Python 3.11+
- Docker & Docker Compose
- AWS Account
- API Keys: OpenAI, Twilio, Satellite Provider, Weather Provider

# Initialize database
python scripts/init_db.py

# Run migrations
alembic upgrade head

# Start the application
python src/main.py
```

### Development

```bash
# Run tests
pytest tests/

# Run with hot reload
uvicorn src.main:app --reload

# Run linting
flake8 src/
black src/

# Run type checking
mypy src/
```

## Documentation

- [**INSTALL_STEPS.md**](INSTALL_STEPS.md) - **Step-by-step AWS-only installation guide**
- [Requirements](requirements.md) - Detailed system requirements
- [Design](design.md) - System architecture and design
- [Tasks](tasks.md) - Implementation roadmap
- [AWS Deployment Guide](AWS_DEPLOYMENT.md) - Production deployment on AWS
- [AWS Integration Summary](AWS_INTEGRATION_SUMMARY.md) - AWS services integration details
- [AWS Quick Reference](docs/AWS_QUICK_REFERENCE.md) - Quick reference for AWS services
- [Provider Selection Guide](docs/PROVIDER_SELECTION_GUIDE.md) - Choosing between OpenAI and AWS
- [Testing Guide](TESTING_GUIDE.md) - Testing instructions
- [Windows Setup](QUICKSTART_WINDOWS.md) - Quick start for Windows users
- [AWS-Only Setup](QUICKSTART_AWS.md) - Quick start for AWS-only setup

## AWS Deployment

KrishiMitra is designed for AWS deployment with full support for AWS native services:

```bash
# Quick start with AWS services
export USE_AWS_SERVICES=True
export LLM_PROVIDER=bedrock
export AWS_REGION=ap-south-1

# Deploy infrastructure
cd infrastructure/terraform
terraform init
terraform apply

# Deploy application
docker build -t krishimitra .
docker push <ecr-repo>/krishimitra:latest
```

See [AWS_DEPLOYMENT.md](AWS_DEPLOYMENT.md) for complete deployment instructions.

### Cost Optimization

Using AWS native services reduces costs by 38%:
- OpenAI + ElevenLabs: ~$600/month (10k farmers)
- AWS Bedrock + Transcribe + Polly: ~$370/month (10k farmers)

See [AWS_INTEGRATION_SUMMARY.md](AWS_INTEGRATION_SUMMARY.md) for detailed cost analysis.

## Success Metrics

- **System Uptime**: 99.5%+
- **Response Latency**: <2 seconds (speech-to-speech)
- **Prediction Accuracy**: 85%+
- **Farmer Satisfaction**: 4.5+/5
- **Cost per Farmer**: <$1.00/month

## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Team

- Product Manager
- Backend Developers (3-4)
- ML Engineers (2)
- DevOps Engineer
- QA Engineers (2)
- Agricultural Domain Expert

## Contact

For questions or support, please contact: support@krishimitra.com

---

**Status**: Phase 1 - Foundation & Infrastructure (In Progress)
**Version**: 0.1.0
**Last Updated**: 2024-01-15
