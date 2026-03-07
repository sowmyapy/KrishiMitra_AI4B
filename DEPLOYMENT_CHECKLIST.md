# KrishiMitra - AWS Deployment Checklist

## Pre-Deployment Verification

### Local Testing
- [x] Backend running on http://localhost:8000
- [x] Frontend running on http://localhost:3000
- [x] Farmer registration working
- [x] Advisory generation working (Hindi)
- [x] Voice calls working (Hindi)
- [x] Database has test data

### API Keys Ready
- [x] Twilio Account SID: AC675ef23df325351b1b8f8a7b6e67635c
- [x] Twilio Auth Token: (in .env)
- [x] Twilio Phone: +17752270557
- [x] Sentinel Hub Client ID: (in .env)
- [x] Sentinel Hub Secret: (in .env)
- [x] OpenWeatherMap API Key: (in .env)
- [x] AWS Access Key: (in .env)
- [x] AWS Secret Key: (in .env)

## Deployment Steps

### Step 1: Choose Deployment Method

**Option A: Elastic Beanstalk (Recommended for prototype)**
- [ ] Install EB CLI: `pip install awsebcli`
- [ ] Run: `eb init -p python-3.10 krishimitra --region ap-south-1`
- [ ] Run: `eb create krishimitra-prod --instance-type t3.small`
- [ ] Set environment variables (see DEPLOY_NOW.md)
- [ ] Deploy: `eb deploy`
- [ ] Get URL: `eb status`

**Option B: ECS Fargate (Production-ready)**
- [ ] Run: `.\deploy_to_aws.ps1`
- [ ] Deploy Terraform: `cd infrastructure/terraform && terraform apply`
- [ ] Get ALB URL from Terraform output

### Step 2: Update Twilio Webhook

- [ ] Go to: https://console.twilio.com/
- [ ] Navigate to: Phone Numbers > Manage > Active numbers
- [ ] Click: +17752270557
- [ ] Update Voice webhook URL to: `https://your-aws-url/api/v1/voice/advisory`
- [ ] Method: HTTP POST
- [ ] Save

### Step 3: Deploy Frontend

**Option A: AWS Amplify**
- [ ] `cd frontend`
- [ ] `npm install -g @aws-amplify/cli`
- [ ] `amplify init`
- [ ] `amplify add hosting`
- [ ] Update API URL in `src/api/client.ts`
- [ ] `amplify publish`

**Option B: S3 + CloudFront**
- [ ] Update API URL in `frontend/src/api/client.ts`
- [ ] `npm run build`
- [ ] Create S3 bucket
- [ ] Upload: `aws s3 sync dist/ s3://your-bucket`
- [ ] Enable website hosting

### Step 4: Database Migration (if using RDS)

- [ ] Create RDS PostgreSQL instance
- [ ] Update DATABASE_URL environment variable
- [ ] Run migrations: `alembic upgrade head`
- [ ] Import test data if needed

### Step 5: Test Deployment

- [ ] Health check: `curl https://your-aws-url/health`
- [ ] API docs: `https://your-aws-url/api/v1/docs`
- [ ] Open UI: `https://your-frontend-url`
- [ ] Register test farmer
- [ ] Generate advisory
- [ ] Make voice call
- [ ] Verify Hindi message received

## Post-Deployment

### Monitoring
- [ ] Set up CloudWatch alarms for errors
- [ ] Configure log retention (7 days recommended)
- [ ] Set up cost alerts

### Security
- [ ] Enable HTTPS (use AWS Certificate Manager)
- [ ] Configure CORS properly
- [ ] Review security groups
- [ ] Enable CloudTrail for audit logs

### Optimization
- [ ] Configure auto-scaling policies
- [ ] Set up CloudFront caching
- [ ] Enable RDS automated backups
- [ ] Configure S3 lifecycle policies

## Rollback Plan

If deployment fails:

**Elastic Beanstalk:**
```powershell
eb abort  # Cancel ongoing deployment
eb deploy --version previous  # Rollback to previous version
```

**ECS Fargate:**
```powershell
# Rollback via Terraform
terraform apply -target=aws_ecs_service.app -var="image_tag=previous"
```

## Support Resources

- AWS Deployment Guide: `AWS_DEPLOYMENT.md`
- Quick Deploy Guide: `DEPLOY_NOW.md`
- Terraform configs: `infrastructure/terraform/`
- Docker setup: `Dockerfile`

## Estimated Timeline

- Elastic Beanstalk: 15-30 minutes
- ECS Fargate: 1-2 hours
- Frontend (Amplify): 10 minutes
- Frontend (S3): 5 minutes

## Estimated Costs

**Prototype (EB + S3):**
- ~$42/month

**Production (ECS + RDS + Redis):**
- ~$570/month

---

**Ready?** Start with: `DEPLOY_NOW.md`
