# KrishiMitra 🌾

**AI-Powered Agricultural Advisory System for Indian Farmers**

[![AWS](https://img.shields.io/badge/AWS-Deployed-orange)](http://krishimitra-prod.eba-gz6myy8n.ap-south-1.elasticbeanstalk.com)
[![Frontend](https://img.shields.io/badge/Frontend-Live-green)](http://krishimitra-frontend.s3-website.ap-south-1.amazonaws.com)
[![Python](https://img.shields.io/badge/Python-3.11-blue)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-Latest-teal)](https://fastapi.tiangolo.com/)

## 🎯 Overview

KrishiMitra is a production-ready AI-powered agricultural advisory system that helps farmers make data-driven decisions using satellite imagery, weather data, and AI-generated insights delivered in their local language (Hindi/Telugu) via voice calls.

**Live Demo**: 
- Frontend: http://krishimitra-frontend.s3-website.ap-south-1.amazonaws.com
- Backend API: http://krishimitra-prod.eba-gz6myy8n.ap-south-1.elasticbeanstalk.com

## ✨ Key Features

- 🛰️ **Real-Time Satellite Monitoring**: Crop health analysis using Sentinel Hub satellite imagery
- 🌤️ **Weather Intelligence**: Live weather data and forecasts from OpenWeather API
- 🤖 **AI-Powered Advisories**: Personalized recommendations using AWS Bedrock (Amazon Nova Lite)
- 📞 **Voice Call Delivery**: Automated voice calls in Hindi/Telugu via Twilio
- 🗣️ **Multi-Language Support**: Hindi and Telugu with easy expansion to more languages
- 📊 **Analytics Dashboard**: Real-time monitoring and insights
- ☁️ **Cloud-Native**: Fully deployed on AWS infrastructure
- 🔄 **Auto-Monitoring**: Continuous crop health tracking with alerts

## 🏗️ Architecture

### Technology Stack

**Frontend**
- React 18 with TypeScript
- Material-UI (MUI) for components
- React Router for navigation
- Axios for API calls
- Deployed on AWS S3 with static website hosting

**Backend**
- FastAPI (Python 3.11)
- SQLite database (production-ready for prototype)
- Pydantic for data validation
- Uvicorn ASGI server
- Deployed on AWS Elastic Beanstalk

**AI & ML Services**
- **LLM**: AWS Bedrock (Amazon Nova Lite in us-east-1)
- **Satellite Data**: Sentinel Hub API
- **Weather Data**: OpenWeather API
- **Voice Calls**: Twilio
- **Text-to-Speech**: Google TTS (gTTS) with Hindi/Telugu support

**AWS Services**
- **Elastic Beanstalk**: Backend hosting (Python 3.11 on Amazon Linux 2023)
- **S3**: Frontend hosting + audio file storage
- **Bedrock**: AI-powered advisory generation
- **IAM**: Access management and security

### Deployment Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                         AWS Cloud                            │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌──────────────────┐         ┌──────────────────┐          │
│  │   S3 Bucket      │         │ Elastic Beanstalk│          │
│  │   (Frontend)     │◄────────┤   (Backend API)  │          │
│  │                  │         │                  │          │
│  │  React + MUI     │         │  FastAPI + SQLite│          │
│  └──────────────────┘         └────────┬─────────┘          │
│                                        │                     │
│                                        ▼                     │
│                              ┌──────────────────┐            │
│                              │  AWS Bedrock     │            │
│                              │  (Nova Lite)     │            │
│                              │  us-east-1       │            │
│                              └──────────────────┘            │
│                                                               │
└───────────────────────────────┬───────────────────────────────┘
                                │
                    ┌───────────┴───────────┐
                    │                       │
            ┌───────▼────────┐     ┌───────▼────────┐
            │  Sentinel Hub  │     │  OpenWeather   │
            │  (Satellite)   │     │  (Weather API) │
            └────────────────┘     └────────────────┘
                    │                       │
                    └───────────┬───────────┘
                                │
                        ┌───────▼────────┐
                        │     Twilio     │
                        │  (Voice Calls) │
                        └────────────────┘
```

## 📁 Project Structure

```
krishimitra/
├── src/
│   ├── api/                    # REST API endpoints
│   │   ├── advisories.py       # Advisory generation endpoints
│   │   ├── farmers.py          # Farmer management
│   │   ├── monitoring.py       # Crop monitoring endpoints
│   │   └── voice.py            # Voice call webhooks
│   ├── services/               # Core business services
│   │   ├── agents/             # AI advisory agent
│   │   ├── aws/                # AWS Bedrock integration
│   │   ├── communication/      # Voice & TTS services
│   │   ├── data_ingestion/     # Satellite & weather data
│   │   └── monitoring/         # Crop health analysis
│   ├── models/                 # SQLAlchemy data models
│   ├── config/                 # Configuration & settings
│   └── main.py                 # FastAPI application entry
├── frontend/                   # React frontend application
│   ├── src/
│   │   ├── pages/              # React pages
│   │   ├── components/         # Reusable components
│   │   └── api/                # API client
│   └── public/                 # Static assets
├── scripts/                    # Utility scripts
├── tests/                      # Test suites
├── .elasticbeanstalk/          # EB deployment config
├── requirements.txt            # Python dependencies
├── Procfile                    # EB startup command
└── README.md                   # This file
```

## 🚀 Getting Started

### Prerequisites

- Python 3.11+
- Node.js 18+ (for frontend development)
- AWS Account with Bedrock access
- Twilio Account (for voice calls)
- API Keys: Sentinel Hub, OpenWeather

### Quick Start - Local Development

```bash
# 1. Clone the repository
git clone <repository-url>
cd krishimitra

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\Activate.ps1

# 3. Install dependencies
pip install -r requirements.txt

# 4. Setup environment variables
cp .env.example .env
# Edit .env with your API keys

# 5. Initialize database
python scripts/init_db.py

# 6. Run backend
uvicorn src.main:app --reload

# 7. Run frontend (separate terminal)
cd frontend
npm install
npm run dev
```

Access the application:
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

### Quick Start - Use Live Deployment

Simply visit the live application:
- **Frontend**: http://krishimitra-frontend.s3-website.ap-south-1.amazonaws.com
- **API**: http://krishimitra-prod.eba-gz6myy8n.ap-south-1.elasticbeanstalk.com/docs

Test farmer: +918095666788 (Hindi)

## 📞 Voice Call Feature

KrishiMitra delivers AI-generated advisories via voice calls in Hindi and Telugu.

### How It Works

1. **Generate Advisory**: System analyzes satellite data, weather, and crop conditions
2. **AI Processing**: AWS Bedrock generates personalized recommendations
3. **Voice Synthesis**: Google TTS converts text to speech in local language
4. **Call Delivery**: Twilio initiates voice call to farmer's phone
5. **Interactive**: Farmer can replay advisory by pressing 1

### Making a Test Call

From the live frontend:
1. Visit http://krishimitra-frontend.s3-website.ap-south-1.amazonaws.com
2. Click on a farmer (e.g., +918095666788)
3. Click "Generate Advisory" button
4. Click "Make Voice Call" button
5. Farmer receives call with advisory in Hindi

### Voice Call Features

- ✅ Real voice calls via Twilio
- ✅ Hindi and Telugu language support
- ✅ AI-generated personalized advisories
- ✅ Interactive replay option
- ✅ Call recording and logging
- ✅ Fallback templates if AI unavailable

## 📚 Documentation

### Essential Guides
- [**AWS_DEPLOYMENT_STATUS.md**](AWS_DEPLOYMENT_STATUS.md) - Current deployment status and URLs
- [**DEMO_VIDEO_GUIDE.md**](DEMO_VIDEO_GUIDE.md) - How to create a demo video
- [**TESTING_GUIDE.md**](TESTING_GUIDE.md) - Testing instructions
- [**ENABLE_BEDROCK_GUIDE.md**](ENABLE_BEDROCK_GUIDE.md) - AWS Bedrock setup
- [**TEST_DEPLOYED_APP.md**](TEST_DEPLOYED_APP.md) - Testing the live deployment

### Quick References
- [**QUICK_START.md**](QUICK_START.md) - Quick start guide
- [**RUN_ME.md**](RUN_ME.md) - How to run locally
- [**STARTUP_SCRIPTS_README.md**](STARTUP_SCRIPTS_README.md) - Startup scripts guide

### Deployment Scripts
- `deploy_to_aws.ps1` - Deploy backend to Elastic Beanstalk
- `deploy_frontend_simple.ps1` - Deploy frontend to S3
- `start_all.ps1` - Start all services locally
- `stop_all.ps1` - Stop all services

## 🌟 Key Features Demonstrated

### 1. Farmer Management
- Register farmers with phone numbers and language preferences
- Manage farm plots with geo-coordinates
- Track crop types and cultivation areas

### 2. AI-Powered Advisories
- Real-time satellite imagery analysis
- Weather-based recommendations
- Crop-specific advice in local languages
- Irrigation and fertilizer guidance

### 3. Voice Call Delivery
- Automated voice calls via Twilio
- Text-to-speech in Hindi/Telugu
- Interactive replay functionality
- Call status tracking

### 4. Monitoring Dashboard
- Real-time crop health monitoring
- Weather alerts and forecasts
- Advisory history and analytics
- System performance metrics

## 🎯 Production Deployment

### Current Status
- ✅ Backend: Deployed on AWS Elastic Beanstalk
- ✅ Frontend: Deployed on AWS S3
- ✅ Database: SQLite (suitable for prototype)
- ✅ AI: AWS Bedrock (Amazon Nova Lite)
- ✅ Voice: Twilio integration active
- ✅ Monitoring: CloudWatch enabled

### Environment Details
- **Region**: ap-south-1 (Mumbai)
- **Backend URL**: http://krishimitra-prod.eba-gz6myy8n.ap-south-1.elasticbeanstalk.com
- **Frontend URL**: http://krishimitra-frontend.s3-website.ap-south-1.amazonaws.com
- **Platform**: Python 3.11 on Amazon Linux 2023
- **Instance**: t3.medium

### Known Limitations
- SQLite database (data resets on deployment)
- Bedrock daily quota limits
- Hindi/Telugu only (expandable to more languages)
- Prototype-level error handling

## 💡 Future Enhancements

- 🔄 Migrate to Amazon RDS for persistent database
- 🌍 Add support for 10+ Indian languages
- 📱 Mobile app for farmers
- 🔬 Computer vision for pest detection
- 🤝 Integration with government schemes
- 📊 Advanced analytics and ML models
- 🔔 SMS and WhatsApp notifications
- 🌐 Multi-region deployment


## 📊 Technical Achievements

- ✅ Full-stack application deployed on AWS
- ✅ AI-powered advisory generation with AWS Bedrock
- ✅ Real-time satellite data integration
- ✅ Multi-language support (Hindi/Telugu)
- ✅ Voice call delivery system
- ✅ Responsive React frontend
- ✅ RESTful API with FastAPI
- ✅ Production-ready deployment

## 🏆 Hackathon Highlights

**Built for**: AWS AI for Bharat Hackathon 2026

**Key Differentiators**:
- 🌾 Addresses real agricultural challenges in India
- 🗣️ Language accessibility for non-English speakers
- 📞 Voice-first approach for low-literacy users
- ☁️ Fully leverages AWS services
- 🚀 Production-ready and scalable
- 💰 Cost-effective solution

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Team

Built with ❤️ for Indian farmers

## 📧 Contact

For questions or support, please open an issue on GitHub.

---

**Status**: ✅ Production Deployed
**Version**: 1.0.0
**Last Updated**: March 8, 2026
**Deployed**: AWS ap-south-1 (Mumbai)
