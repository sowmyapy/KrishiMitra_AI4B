# Deploy KrishiMitra to AWS - Quick Start

## Current Status

✅ **Working Features:**
- Farmer registration with farm plots
- Satellite data integration (Sentinel Hub)
- Weather data integration (OpenWeatherMap)
- Advisory generation with Hindi support
- Voice calls in Hindi (Twilio TTS)
- Web UI for management

✅ **Tested:**
- Hindi voice calls working
- Advisory generation working (with fallback templates)
- Farmer: +918095666788

## Fastest Deployment Path

### Method 1: AWS Elastic Beanstalk (15 minutes)

**Why this method:**
- Simplest AWS deployment
- Automatic load balancing
- Auto-scaling built-in
- ~$25/month for prototype

**Steps:**

1. **Install EB CLI**
```powershell
pip install awsebcli
```

2. **Initialize EB**
```powershell
eb init -p python-3.10 krishimitra --region ap-south-1
```

3. **Create environment**
```powershell
eb create krishimitra-prod --instance-type t3.small --single
```

4. **Set environment variables**
```powershell
eb setenv `
  TWILIO_ACCOUNT_SID=AC675ef23df325351b1b8f8a7b6e67635c `
  TWILIO_AUTH_TOKEN=61a4ec1e7a793f1acf07fa88f70bac60 `
  TWILIO_PHONE_NUMBER=+17752270557 `
  SENTINEL_HUB_CLIENT_ID=5337ed74-d518-4795-b31a-3b5546d0cefd `
  SENTINEL_HUB_CLIENT_SECRET=Qr5BFDXmoS3sfJ9ozaZtdV2glPKigxqh `
  OPENWEATHERMAP_API_KEY=9cb097bad8ee1c0e5e6e3f4a0b3ebc5b `
  AWS_REGION=ap-south-1 `
  LLM_PROVIDER=bedrock `
  USE_AWS_SERVICES=True `
  DATABASE_URL=sqlite:///./krishimitra.db
```

5. **Deploy**
```powershell
eb deploy
```

6. **Get URL**
```powershell
eb status
# Copy the CNAME URL
```

7. **Update Twilio webhook**
- Go to: https://console.twilio.com/
- Navigate to: Phone Numbers > Manage > Active numbers
- Click your number: +17752270557
- Update webhook URL to: `https://your-eb-url.elasticbeanstalk.com/api/v1/voice/advisory`
- Save

8. **Test**
- Open: `https://your-eb-url.elasticbeanstalk.com`
- Register farmer, generate advisory, make call

**Done!** Your app is live on AWS.

---

### Method 2: Docker + ECS Fargate (Production-ready)

**Why this method:**
- More control and scalability
- Better for production
- ~$150/month with RDS + Redis

**Quick steps:**

1. **Run deployment script**
```powershell
.\deploy_to_aws.ps1
```

2. **Deploy infrastructure**
```powershell
cd infrastructure/terraform
terraform init
terraform apply
```

3. **Get ALB URL from Terraform output**
```powershell
terraform output alb_dns_name
```

4. **Update Twilio webhook** to ALB URL

---

## Frontend Deployment

### Option 1: AWS Amplify (Easiest)

```powershell
cd frontend
npm install -g @aws-amplify/cli
amplify init
amplify add hosting
amplify publish
```

### Option 2: S3 + CloudFront

```powershell
cd frontend
npm run build

# Create S3 bucket
aws s3 mb s3://krishimitra-ui-$RANDOM --region ap-south-1

# Upload
aws s3 sync dist/ s3://krishimitra-ui-$RANDOM --acl public-read

# Enable website hosting
aws s3 website s3://krishimitra-ui-$RANDOM --index-document index.html
```

---

## Post-Deployment

### Update Frontend API URL

Edit `frontend/src/api/client.ts`:
```typescript
const API_BASE_URL = 'https://your-aws-url.com/api/v1';
```

Rebuild and redeploy frontend.

### Test End-to-End

1. Open UI: `https://your-frontend-url.com`
2. Register farmer with Hindi language
3. Add farm plot
4. Generate advisory
5. Make voice call
6. Verify call received with Hindi message

---

## Troubleshooting

### EB deployment fails

```powershell
eb logs
# Check for errors
```

### Voice calls not working

1. Check Twilio webhook URL is correct
2. Check backend logs: `eb logs`
3. Verify ngrok is NOT needed (AWS has public URL)

### Database issues

For production, switch from SQLite to RDS:

```powershell
# Create RDS
aws rds create-db-instance `
  --db-instance-identifier krishimitra-db `
  --db-instance-class db.t3.micro `
  --engine postgres `
  --master-username admin `
  --master-user-password YourSecurePassword123 `
  --allocated-storage 20 `
  --region ap-south-1

# Update DATABASE_URL
eb setenv DATABASE_URL=postgresql://admin:YourSecurePassword123@endpoint:5432/krishimitra
```

---

## Cost Estimate

**Prototype (Elastic Beanstalk):**
- EB instance (t3.small): $25/month
- S3 storage: $2/month
- Data transfer: $5/month
- Twilio (100 calls): $10/month
- **Total: ~$42/month**

**Production (ECS + RDS):**
- ECS Fargate: $150/month
- RDS PostgreSQL: $200/month
- ElastiCache Redis: $100/month
- S3 + CloudFront: $20/month
- Twilio (1000 calls): $100/month
- **Total: ~$570/month**

---

## Need Help?

- Detailed guide: `AWS_DEPLOYMENT.md`
- Terraform configs: `infrastructure/terraform/`
- Docker setup: `Dockerfile`

**Ready to deploy?** Run: `.\deploy_to_aws.ps1`
