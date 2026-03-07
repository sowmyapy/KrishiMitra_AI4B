# Deploy KrishiMitra Hindi Prototype to AWS

Quick deployment guide for the working Hindi voice advisory system.

## What's Working Now

✅ Farmer registration with plots
✅ Satellite data integration (Sentinel Hub)
✅ Weather data integration (OpenWeatherMap)
✅ Advisory generation (with LLM fallback)
✅ Voice calls in Hindi (Twilio + simplified templates)
✅ Web UI for farmer management

## Prerequisites

1. AWS Account with admin access
2. AWS CLI installed and configured
3. Docker installed
4. Your current API keys:
   - Twilio (working)
   - Sentinel Hub (working)
   - OpenWeatherMap (working)
   - AWS credentials (working)

## Deployment Options

### Option A: Quick Deploy with Elastic Beanstalk (Recommended for Prototype)

Fastest way to get your app running on AWS.

**Step 1: Install EB CLI**
```bash
pip install awsebcli
```

**Step 2: Initialize EB**
```bash
eb init -p python-3.10 krishimitra --region ap-south-1
```

**Step 3: Create environment**
```bash
eb create krishimitra-prod --instance-type t3.small
```

**Step 4: Set environment variables**
```bash
eb setenv \
  TWILIO_ACCOUNT_SID=AC675ef23df325351b1b8f8a7b6e67635c \
  TWILIO_AUTH_TOKEN=61a4ec1e7a793f1acf07fa88f70bac60 \
  TWILIO_PHONE_NUMBER=+17752270557 \
  SENTINEL_HUB_CLIENT_ID=5337ed74-d518-4795-b31a-3b5546d0cefd \
  SENTINEL_HUB_CLIENT_SECRET=Qr5BFDXmoS3sfJ9ozaZtdV2glPKigxqh \
  OPENWEATHERMAP_API_KEY=9cb097bad8ee1c0e5e6e3f4a0b3ebc5b \
  AWS_REGION=ap-south-1 \
  LLM_PROVIDER=bedrock \
  USE_AWS_SERVICES=True
```

**Step 5: Deploy**
```bash
eb deploy
```

**Step 6: Get URL**
```bash
eb status
# Note the CNAME - this is your public URL
```

**Step 7: Update Twilio webhook**
- Go to Twilio Console
- Update webhook URL to: `https://your-eb-url.elasticbeanstalk.com/api/v1/voice/advisory`

**Cost**: ~$25/month (t3.small instance)

### Option B: Deploy with ECS Fargate (Production-Ready)

More scalable but requires more setup.

**Step 1: Build Docker image**
```bash
docker build -t krishimitra-app .
```

**Step 2: Create ECR repository**
```bash
aws ecr create-repository --repository-name krishimitra-app --region ap-south-1
```

**Step 3: Push image**
```bash
aws ecr get-login-password --region ap-south-1 | docker login --username AWS --password-stdin <account-id>.dkr.ecr.ap-south-1.amazonaws.com

docker tag krishimitra-app:latest <account-id>.dkr.ecr.ap-south-1.amazonaws.com/krishimitra-app:latest

docker push <account-id>.dkr.ecr.ap-south-1.amazonaws.com/krishimitra-app:latest
```

**Step 4: Deploy with Terraform**
```bash
cd infrastructure/terraform
terraform init
terraform plan
terraform apply
```

**Cost**: ~$150/month (Fargate + RDS + Redis)

## Database Migration

### For Elastic Beanstalk

EB uses SQLite by default. For production, switch to RDS:

**Step 1: Create RDS PostgreSQL**
```bash
aws rds create-db-instance \
  --db-instance-identifier krishimitra-db \
  --db-instance-class db.t3.micro \
  --engine postgres \
  --master-username admin \
  --master-user-password YourPassword123 \
  --allocated-storage 20 \
  --region ap-south-1
```

**Step 2: Update DATABASE_URL**
```bash
eb setenv DATABASE_URL=postgresql://admin:YourPassword123@endpoint:5432/krishimitra
```

**Step 3: Run migrations**
```bash
eb ssh
cd /var/app/current
source /var/app/venv/*/bin/activate
alembic upgrade head
```

### For ECS Fargate

RDS is created automatically by Terraform. Migrations run as ECS task.

## Frontend Deployment

### Option 1: S3 + CloudFront (Recommended)

**Step 1: Build frontend**
```bash
cd frontend
npm run build
```

**Step 2: Create S3 bucket**
```bash
aws s3 mb s3://krishimitra-ui --region ap-south-1
aws s3 website s3://krishimitra-ui --index-document index.html
```

**Step 3: Upload**
```bash
aws s3 sync dist/ s3://krishimitra-ui --delete
```

**Step 4: Create CloudFront distribution**
```bash
aws cloudfront create-distribution \
  --origin-domain-name krishimitra-ui.s3.ap-south-1.amazonaws.com \
  --default-root-object index.html
```

**Cost**: ~$5/month

### Option 2: Amplify Hosting

**Step 1: Install Amplify CLI**
```bash
npm install -g @aws-amplify/cli
amplify configure
```

**Step 2: Initialize**
```bash
cd frontend
amplify init
```

**Step 3: Add hosting**
```bash
amplify add hosting
amplify publish
```

**Cost**: ~$15/month

## Post-Deployment Checklist

- [ ] Update Twilio webhook URL to AWS endpoint
- [ ] Test farmer registration via UI
- [ ] Generate advisory for test farmer
- [ ] Make test voice call in Hindi
- [ ] Verify advisory is delivered correctly
- [ ] Set up CloudWatch alarms for errors
- [ ] Configure auto-scaling policies
- [ ] Set up daily database backups
- [ ] Document the deployment URL

## Quick Test After Deployment

```bash
# Get your deployment URL
DEPLOY_URL="https://your-app-url.com"

# Test health
curl $DEPLOY_URL/health

# Test API docs
curl $DEPLOY_URL/api/v1/docs

# Register test farmer (via UI)
# Generate advisory (via UI)
# Make voice call (via UI)
```

## Troubleshooting

### Issue: Voice calls not working

**Check 1: Webhook URL**
```bash
# Verify Twilio webhook is set to your AWS URL
curl https://api.twilio.com/2010-04-01/Accounts/$TWILIO_SID/IncomingPhoneNumbers.json \
  -u $TWILIO_SID:$TWILIO_TOKEN
```

**Check 2: Backend logs**
```bash
# For EB
eb logs

# For ECS
aws logs tail /aws/ecs/krishimitra-production --follow
```

### Issue: LLM rate limits

Your Bedrock is hitting rate limits. Solutions:

1. **Wait for quota reset** (hourly)
2. **Request quota increase** in AWS Console
3. **Use fallback templates** (already implemented)

### Issue: Database connection errors

```bash
# Check RDS security group allows ECS tasks
aws ec2 describe-security-groups --group-ids sg-xxx

# Verify DATABASE_URL is correct
eb printenv | grep DATABASE_URL
```

## Next Steps

1. **Domain Setup**: Point your domain to AWS deployment
2. **SSL Certificate**: Use AWS Certificate Manager (free)
3. **Monitoring**: Set up CloudWatch dashboards
4. **Backups**: Configure automated RDS snapshots
5. **Scaling**: Configure auto-scaling based on load

## Estimated Costs (Prototype)

- Elastic Beanstalk (t3.small): $25/month
- RDS PostgreSQL (db.t3.micro): $15/month
- S3 + CloudFront: $5/month
- Twilio (100 calls/month): $10/month
- AWS Bedrock (limited usage): $5/month

**Total**: ~$60/month for prototype

---

**Need help?** Check AWS_DEPLOYMENT.md for detailed infrastructure setup.
