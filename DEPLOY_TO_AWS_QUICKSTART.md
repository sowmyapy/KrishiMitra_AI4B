# Deploy KrishiMitra to AWS - Quick Start

## 🚀 Fastest Way to Deploy

This guide will get your KrishiMitra application (frontend + backend + farmer registration) deployed to AWS in under 1 hour.

## Prerequisites

- ✅ AWS Account
- ✅ AWS CLI installed and configured
- ✅ Node.js 18+ installed
- ✅ Docker installed (for backend)
- ✅ Git repository

## Architecture

```
User → CloudFront (Frontend) → API Gateway → Lambda/ECS (Backend) → RDS (Database)
                                                    ↓
                                            AWS Services (Bedrock, Polly, etc.)
```

## Step-by-Step Deployment

### Step 1: Configure AWS CLI (5 minutes)

```bash
# Install AWS CLI
# Windows: Download from https://aws.amazon.com/cli/
# Mac: brew install awscli
# Linux: sudo apt install awscli

# Configure
aws configure
# Enter:
# - AWS Access Key ID: [Your key]
# - AWS Secret Access Key: [Your secret]
# - Default region: ap-south-1
# - Default output format: json

# Verify
aws sts get-caller-identity
```

### Step 2: Deploy Frontend (10 minutes)

```bash
# Navigate to project
cd C:\Users\Sowmya\OneDrive\projects\ai_crop_system

# Build frontend
cd frontend
npm install
npm run build

# Create S3 bucket
aws s3 mb s3://krishimitra-frontend-$(date +%s) --region ap-south-1

# Note the bucket name, then upload
aws s3 sync dist/ s3://YOUR-BUCKET-NAME --delete

# Enable website hosting
aws s3 website s3://YOUR-BUCKET-NAME \
  --index-document index.html \
  --error-document index.html

# Make public
aws s3api put-bucket-policy \
  --bucket YOUR-BUCKET-NAME \
  --policy '{
    "Version": "2012-10-17",
    "Statement": [{
      "Sid": "PublicReadGetObject",
      "Effect": "Allow",
      "Principal": "*",
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::YOUR-BUCKET-NAME/*"
    }]
  }'

# Get website URL
echo "Frontend URL: http://YOUR-BUCKET-NAME.s3-website.ap-south-1.amazonaws.com"
```

### Step 3: Create Database (10 minutes)

```bash
# Create RDS PostgreSQL instance
aws rds create-db-instance \
  --db-instance-identifier krishimitra-db \
  --db-instance-class db.t3.micro \
  --engine postgres \
  --engine-version 15.3 \
  --master-username admin \
  --master-user-password YourSecurePassword123! \
  --allocated-storage 20 \
  --db-name krishimitra \
  --publicly-accessible true \
  --backup-retention-period 7 \
  --region ap-south-1

# Wait for database to be available (5-10 minutes)
aws rds wait db-instance-available \
  --db-instance-identifier krishimitra-db

# Get endpoint
aws rds describe-db-instances \
  --db-instance-identifier krishimitra-db \
  --query 'DBInstances[0].Endpoint.Address' \
  --output text

# Note the endpoint: krishimitra-db.xxxxx.ap-south-1.rds.amazonaws.com
```

### Step 4: Deploy Backend with Lambda (15 minutes)

```bash
# Go back to project root
cd C:\Users\Sowmya\OneDrive\projects\ai_crop_system

# Install mangum for Lambda
pip install mangum

# Create lambda handler
cat > lambda_handler.py << 'EOF'
from mangum import Mangum
from src.main import app

handler = Mangum(app)
EOF

# Create deployment package
mkdir lambda_package
cd lambda_package

# Copy code
cp -r ../src .
cp ../lambda_handler.py .
cp ../alembic.ini .
cp -r ../alembic .

# Install dependencies
pip install -r ../requirements-aws.txt -t . --platform manylinux2014_x86_64 --only-binary=:all:

# Create ZIP (this may take a few minutes)
# Windows PowerShell:
Compress-Archive -Path * -DestinationPath ../krishimitra-backend.zip -Force

# Linux/Mac:
# zip -r ../krishimitra-backend.zip .

cd ..

# Create IAM role for Lambda
aws iam create-role \
  --role-name krishimitra-lambda-role \
  --assume-role-policy-document '{
    "Version": "2012-10-17",
    "Statement": [{
      "Effect": "Allow",
      "Principal": {"Service": "lambda.amazonaws.com"},
      "Action": "sts:AssumeRole"
    }]
  }'

# Attach policies
aws iam attach-role-policy \
  --role-name krishimitra-lambda-role \
  --policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole

aws iam attach-role-policy \
  --role-name krishimitra-lambda-role \
  --policy-arn arn:aws:iam::aws:policy/AmazonBedrockFullAccess

# Get account ID
ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)

# Create Lambda function
aws lambda create-function \
  --function-name krishimitra-backend \
  --runtime python3.11 \
  --role arn:aws:iam::${ACCOUNT_ID}:role/krishimitra-lambda-role \
  --handler lambda_handler.handler \
  --zip-file fileb://krishimitra-backend.zip \
  --timeout 30 \
  --memory-size 1024 \
  --environment Variables="{
    DATABASE_URL=postgresql://admin:YourSecurePassword123!@YOUR-RDS-ENDPOINT/krishimitra,
    AWS_REGION=ap-south-1,
    TWILIO_ACCOUNT_SID=YOUR_TWILIO_ACCOUNT_SID,
    TWILIO_AUTH_TOKEN=YOUR_TWILIO_AUTH_TOKEN,
    TWILIO_PHONE_NUMBER=YOUR_TWILIO_PHONE_NUMBER,
    SENTINEL_HUB_CLIENT_ID=YOUR_SENTINEL_HUB_CLIENT_ID,
    SENTINEL_HUB_CLIENT_SECRET=YOUR_SENTINEL_HUB_CLIENT_SECRET,
    OPENWEATHERMAP_API_KEY=YOUR_OPENWEATHERMAP_API_KEY,
    JWT_SECRET_KEY=your_secret_key_change_in_production
  }" \
  --region ap-south-1

# Create function URL (simpler than API Gateway for MVP)
aws lambda create-function-url-config \
  --function-name krishimitra-backend \
  --auth-type NONE \
  --cors '{
    "AllowOrigins": ["*"],
    "AllowMethods": ["*"],
    "AllowHeaders": ["*"],
    "MaxAge": 86400
  }'

# Get function URL
aws lambda get-function-url-config \
  --function-name krishimitra-backend \
  --query 'FunctionUrl' \
  --output text

# Note the URL: https://xxxxx.lambda-url.ap-south-1.on.aws/
```

### Step 5: Run Database Migrations (5 minutes)

```bash
# Update .env with RDS endpoint
DATABASE_URL=postgresql://admin:YourSecurePassword123!@YOUR-RDS-ENDPOINT/krishimitra

# Run migrations locally (connects to RDS)
alembic upgrade head

# Or run migrations via Lambda
aws lambda invoke \
  --function-name krishimitra-backend \
  --payload '{"rawPath": "/migrate"}' \
  response.json
```

### Step 6: Update Frontend with Backend URL (5 minutes)

```bash
# Update frontend .env
cd frontend
cat > .env.production << EOF
VITE_API_BASE_URL=https://YOUR-LAMBDA-URL.lambda-url.ap-south-1.on.aws
VITE_APP_NAME=KrishiMitra
EOF

# Rebuild
npm run build

# Redeploy to S3
aws s3 sync dist/ s3://YOUR-BUCKET-NAME --delete
```

### Step 7: Test Deployment (5 minutes)

```bash
# Test frontend
curl http://YOUR-BUCKET-NAME.s3-website.ap-south-1.amazonaws.com

# Test backend health
curl https://YOUR-LAMBDA-URL.lambda-url.ap-south-1.on.aws/

# Test farmer registration
curl -X POST https://YOUR-LAMBDA-URL.lambda-url.ap-south-1.on.aws/api/v1/farmers/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer test_token" \
  -d '{
    "phone_number": "+918151910856",
    "preferred_language": "hi",
    "timezone": "Asia/Kolkata"
  }'
```

## URLs After Deployment

- **Frontend**: `http://YOUR-BUCKET-NAME.s3-website.ap-south-1.amazonaws.com`
- **Backend**: `https://YOUR-LAMBDA-URL.lambda-url.ap-south-1.on.aws`
- **Database**: `YOUR-RDS-ENDPOINT:5432`

## Cost Estimate

| Service | Monthly Cost |
|---------|-------------|
| S3 (Frontend) | $0.50 |
| Lambda (Backend) | $5-10 |
| RDS t3.micro | $15-20 |
| Data Transfer | $1-5 |
| **Total** | **$21-35/month** |

## Optional: Add CloudFront (CDN)

```bash
# Create CloudFront distribution
aws cloudfront create-distribution \
  --origin-domain-name YOUR-BUCKET-NAME.s3.ap-south-1.amazonaws.com \
  --default-root-object index.html

# Get distribution domain
# Note: Takes 15-20 minutes to deploy
```

## Optional: Custom Domain

1. **Register domain** in Route 53
2. **Request SSL certificate** in ACM (us-east-1 region)
3. **Add to CloudFront** distribution
4. **Create Route 53 A record** pointing to CloudFront

## Troubleshooting

### Lambda timeout errors
```bash
# Increase timeout
aws lambda update-function-configuration \
  --function-name krishimitra-backend \
  --timeout 60
```

### Database connection errors
```bash
# Check security group allows Lambda access
# Get Lambda security group
aws lambda get-function \
  --function-name krishimitra-backend \
  --query 'Configuration.VpcConfig.SecurityGroupIds'

# Update RDS security group to allow Lambda SG
```

### CORS errors
```bash
# Update Lambda CORS
aws lambda update-function-url-config \
  --function-name krishimitra-backend \
  --cors '{
    "AllowOrigins": ["*"],
    "AllowMethods": ["*"],
    "AllowHeaders": ["*"]
  }'
```

## Monitoring

```bash
# View Lambda logs
aws logs tail /aws/lambda/krishimitra-backend --follow

# View Lambda metrics
aws cloudwatch get-metric-statistics \
  --namespace AWS/Lambda \
  --metric-name Invocations \
  --dimensions Name=FunctionName,Value=krishimitra-backend \
  --start-time 2025-03-01T00:00:00Z \
  --end-time 2025-03-01T23:59:59Z \
  --period 3600 \
  --statistics Sum
```

## Cleanup (if needed)

```bash
# Delete Lambda
aws lambda delete-function --function-name krishimitra-backend

# Delete S3 bucket
aws s3 rb s3://YOUR-BUCKET-NAME --force

# Delete RDS
aws rds delete-db-instance \
  --db-instance-identifier krishimitra-db \
  --skip-final-snapshot
```

## Next Steps

1. ✅ **Set up custom domain** (optional)
2. ✅ **Add CloudFront** for better performance
3. ✅ **Set up CI/CD** with GitHub Actions
4. ✅ **Enable monitoring** with CloudWatch
5. ✅ **Set up backups** for RDS
6. ✅ **Add WAF** for security

## Production Checklist

- [ ] Use custom domain with SSL
- [ ] Enable CloudFront
- [ ] Set up CloudWatch alarms
- [ ] Enable RDS backups
- [ ] Use Secrets Manager for credentials
- [ ] Set up VPC for Lambda and RDS
- [ ] Enable CloudTrail for audit logs
- [ ] Set up AWS Budgets for cost alerts
- [ ] Configure auto-scaling
- [ ] Set up staging environment

---

**Deployment complete!** Your KrishiMitra application is now live on AWS! 🎉

**Frontend**: http://YOUR-BUCKET-NAME.s3-website.ap-south-1.amazonaws.com
**Backend**: https://YOUR-LAMBDA-URL.lambda-url.ap-south-1.on.aws

Test the farmer registration form at: `/farmers/new`
