# KrishiMitra - Complete AWS Deployment Guide

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                         AWS Cloud                           │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────────┐         ┌──────────────┐                │
│  │   Route 53   │────────→│  CloudFront  │                │
│  │     DNS      │         │     CDN      │                │
│  └──────────────┘         └──────┬───────┘                │
│                                  │                          │
│                    ┌─────────────┴─────────────┐           │
│                    │                           │           │
│            ┌───────▼────────┐         ┌───────▼────────┐  │
│            │   S3 Bucket    │         │   API Gateway  │  │
│            │  (Frontend)    │         │                │  │
│            │  React Build   │         └───────┬────────┘  │
│            └────────────────┘                 │           │
│                                       ┌───────▼────────┐  │
│                                       │   Lambda or    │  │
│                                       │   ECS/Fargate  │  │
│                                       │   (Backend)    │  │
│                                       └───────┬────────┘  │
│                                               │           │
│                    ┌──────────────────────────┼──────┐    │
│                    │                          │      │    │
│            ┌───────▼────────┐      ┌─────────▼──┐   │    │
│            │   RDS/Aurora   │      │  Bedrock   │   │    │
│            │   PostgreSQL   │      │   Polly    │   │    │
│            └────────────────┘      │ Transcribe │   │    │
│                                    └────────────┘   │    │
│                                                     │    │
│            ┌────────────────┐      ┌──────────────▼┐    │
│            │   S3 Bucket    │      │  Sentinel Hub │    │
│            │  (Satellite)   │      │ OpenWeather   │    │
│            └────────────────┘      └───────────────┘    │
│                                                          │
└──────────────────────────────────────────────────────────┘
```

## Deployment Options

### Option 1: Serverless (Recommended for MVP)
- **Frontend**: S3 + CloudFront
- **Backend**: Lambda + API Gateway
- **Database**: RDS Aurora Serverless
- **Cost**: ~$50-100/month

### Option 2: Container-Based (Recommended for Production)
- **Frontend**: S3 + CloudFront
- **Backend**: ECS Fargate
- **Database**: RDS PostgreSQL
- **Cost**: ~$150-300/month

### Option 3: EC2-Based (Traditional)
- **Frontend**: S3 + CloudFront
- **Backend**: EC2 instances
- **Database**: RDS PostgreSQL
- **Cost**: ~$100-200/month

## Part 1: Frontend Deployment (S3 + CloudFront)

### Step 1: Build Frontend

```bash
cd frontend

# Update .env for production
cat > .env.production << EOF
VITE_API_BASE_URL=https://api.your-domain.com
VITE_APP_NAME=KrishiMitra
EOF

# Build
npm run build
```

### Step 2: Create S3 Bucket

```bash
# Install AWS CLI if not already installed
# Download from: https://aws.amazon.com/cli/

# Configure AWS CLI
aws configure
# Enter:
# - AWS Access Key ID
# - AWS Secret Access Key
# - Default region: ap-south-1
# - Default output format: json

# Create S3 bucket
aws s3 mb s3://krishimitra-frontend --region ap-south-1

# Enable static website hosting
aws s3 website s3://krishimitra-frontend \
  --index-document index.html \
  --error-document index.html

# Upload build files
cd frontend/dist
aws s3 sync . s3://krishimitra-frontend --delete

# Set bucket policy for public read
aws s3api put-bucket-policy \
  --bucket krishimitra-frontend \
  --policy '{
    "Version": "2012-10-17",
    "Statement": [{
      "Sid": "PublicReadGetObject",
      "Effect": "Allow",
      "Principal": "*",
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::krishimitra-frontend/*"
    }]
  }'
```

### Step 3: Create CloudFront Distribution

```bash
# Create CloudFront distribution
aws cloudfront create-distribution \
  --origin-domain-name krishimitra-frontend.s3.ap-south-1.amazonaws.com \
  --default-root-object index.html
```

Or use AWS Console:
1. Go to CloudFront → Create Distribution
2. Origin Domain: Select your S3 bucket
3. Origin Access: Public
4. Default Root Object: index.html
5. Custom Error Response: 404 → /index.html (for React Router)
6. Create Distribution

**Note the CloudFront URL**: `https://d1234567890.cloudfront.net`

### Step 4: Configure Custom Domain (Optional)

1. **Register domain** in Route 53 or use existing
2. **Request SSL certificate** in ACM (us-east-1 region for CloudFront)
3. **Add CNAME** to CloudFront distribution
4. **Create Route 53 record** pointing to CloudFront

## Part 2: Backend Deployment

### Option A: Lambda + API Gateway (Serverless)

#### Step 1: Prepare Backend for Lambda

Create `lambda_handler.py`:

```python
from mangum import Mangum
from src.main import app

handler = Mangum(app)
```

Update `requirements.txt`:

```txt
# Add to existing requirements
mangum==0.17.0
```

#### Step 2: Package Backend

```bash
# Create deployment package
mkdir lambda_package
cd lambda_package

# Copy application code
cp -r ../src .
cp ../lambda_handler.py .

# Install dependencies
pip install -r ../requirements-aws.txt -t .

# Create ZIP
zip -r ../krishimitra-backend.zip .
```

#### Step 3: Create Lambda Function

```bash
# Create Lambda function
aws lambda create-function \
  --function-name krishimitra-backend \
  --runtime python3.11 \
  --role arn:aws:iam::YOUR_ACCOUNT_ID:role/lambda-execution-role \
  --handler lambda_handler.handler \
  --zip-file fileb://krishimitra-backend.zip \
  --timeout 30 \
  --memory-size 512 \
  --environment Variables="{
    DATABASE_URL=postgresql://user:pass@rds-endpoint/krishimitra,
    AWS_REGION=ap-south-1,
    TWILIO_ACCOUNT_SID=your_sid,
    TWILIO_AUTH_TOKEN=your_token
  }"
```

#### Step 4: Create API Gateway

1. Go to API Gateway → Create API → HTTP API
2. Add integration → Lambda
3. Select your Lambda function
4. Configure routes:
   - `ANY /{proxy+}` → Lambda function
5. Deploy API
6. Note the API URL: `https://abc123.execute-api.ap-south-1.amazonaws.com`

### Option B: ECS Fargate (Container-Based)

#### Step 1: Create Dockerfile

Create `Dockerfile` in project root:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements-aws.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements-aws.txt

# Copy application code
COPY src/ ./src/
COPY alembic/ ./alembic/
COPY alembic.ini .

# Expose port
EXPOSE 8000

# Run application
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

#### Step 2: Build and Push to ECR

```bash
# Create ECR repository
aws ecr create-repository \
  --repository-name krishimitra-backend \
  --region ap-south-1

# Get login token
aws ecr get-login-password --region ap-south-1 | \
  docker login --username AWS --password-stdin \
  YOUR_ACCOUNT_ID.dkr.ecr.ap-south-1.amazonaws.com

# Build image
docker build -t krishimitra-backend .

# Tag image
docker tag krishimitra-backend:latest \
  YOUR_ACCOUNT_ID.dkr.ecr.ap-south-1.amazonaws.com/krishimitra-backend:latest

# Push to ECR
docker push YOUR_ACCOUNT_ID.dkr.ecr.ap-south-1.amazonaws.com/krishimitra-backend:latest
```

#### Step 3: Create ECS Cluster and Service

```bash
# Create ECS cluster
aws ecs create-cluster \
  --cluster-name krishimitra-cluster \
  --region ap-south-1

# Create task definition (save as task-definition.json)
{
  "family": "krishimitra-backend",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "512",
  "memory": "1024",
  "containerDefinitions": [{
    "name": "krishimitra-backend",
    "image": "YOUR_ACCOUNT_ID.dkr.ecr.ap-south-1.amazonaws.com/krishimitra-backend:latest",
    "portMappings": [{
      "containerPort": 8000,
      "protocol": "tcp"
    }],
    "environment": [
      {"name": "DATABASE_URL", "value": "postgresql://..."},
      {"name": "AWS_REGION", "value": "ap-south-1"}
    ],
    "logConfiguration": {
      "logDriver": "awslogs",
      "options": {
        "awslogs-group": "/ecs/krishimitra-backend",
        "awslogs-region": "ap-south-1",
        "awslogs-stream-prefix": "ecs"
      }
    }
  }]
}

# Register task definition
aws ecs register-task-definition \
  --cli-input-json file://task-definition.json

# Create service
aws ecs create-service \
  --cluster krishimitra-cluster \
  --service-name krishimitra-backend-service \
  --task-definition krishimitra-backend \
  --desired-count 1 \
  --launch-type FARGATE \
  --network-configuration "awsvpcConfiguration={
    subnets=[subnet-xxx],
    securityGroups=[sg-xxx],
    assignPublicIp=ENABLED
  }"
```

#### Step 4: Create Application Load Balancer

1. Go to EC2 → Load Balancers → Create ALB
2. Configure:
   - Name: krishimitra-alb
   - Scheme: Internet-facing
   - Listeners: HTTP (80), HTTPS (443)
   - Availability Zones: Select 2+
3. Create Target Group:
   - Target type: IP
   - Protocol: HTTP
   - Port: 8000
   - Health check: /
4. Register ECS service with target group

## Part 3: Database Setup

### Option A: RDS Aurora Serverless (Recommended)

```bash
# Create Aurora Serverless cluster
aws rds create-db-cluster \
  --db-cluster-identifier krishimitra-db \
  --engine aurora-postgresql \
  --engine-mode serverless \
  --master-username admin \
  --master-user-password YOUR_PASSWORD \
  --database-name krishimitra \
  --scaling-configuration MinCapacity=2,MaxCapacity=4,AutoPause=true \
  --vpc-security-group-ids sg-xxx \
  --db-subnet-group-name default
```

### Option B: RDS PostgreSQL

```bash
# Create RDS instance
aws rds create-db-instance \
  --db-instance-identifier krishimitra-db \
  --db-instance-class db.t3.micro \
  --engine postgres \
  --master-username admin \
  --master-user-password YOUR_PASSWORD \
  --allocated-storage 20 \
  --vpc-security-group-ids sg-xxx \
  --db-subnet-group-name default \
  --backup-retention-period 7 \
  --publicly-accessible false
```

### Run Migrations

```bash
# Update DATABASE_URL in .env
DATABASE_URL=postgresql://admin:password@rds-endpoint/krishimitra

# Run migrations
alembic upgrade head
```

## Part 4: Environment Variables

### Backend Environment Variables

```bash
# Lambda/ECS environment variables
DATABASE_URL=postgresql://admin:password@rds-endpoint/krishimitra
AWS_REGION=ap-south-1
AWS_ACCESS_KEY_ID=your_key
AWS_SECRET_ACCESS_KEY=your_secret
SENTINEL_HUB_CLIENT_ID=your_id
SENTINEL_HUB_CLIENT_SECRET=your_secret
OPENWEATHERMAP_API_KEY=your_key
TWILIO_ACCOUNT_SID=your_sid
TWILIO_AUTH_TOKEN=your_token
TWILIO_PHONE_NUMBER=+17752270557
JWT_SECRET_KEY=your_secret_key
```

### Frontend Environment Variables

```bash
# .env.production
VITE_API_BASE_URL=https://api.your-domain.com
VITE_APP_NAME=KrishiMitra
```

## Part 5: CI/CD Pipeline (GitHub Actions)

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy to AWS

on:
  push:
    branches: [main]

jobs:
  deploy-frontend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'
      
      - name: Install dependencies
        run: |
          cd frontend
          npm install
      
      - name: Build
        run: |
          cd frontend
          npm run build
        env:
          VITE_API_BASE_URL: ${{ secrets.API_URL }}
      
      - name: Deploy to S3
        run: |
          cd frontend/dist
          aws s3 sync . s3://krishimitra-frontend --delete
        env:
          AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
          AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          AWS_REGION: ap-south-1
      
      - name: Invalidate CloudFront
        run: |
          aws cloudfront create-invalidation \
            --distribution-id ${{ secrets.CLOUDFRONT_ID }} \
            --paths "/*"

  deploy-backend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v2
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: ap-south-1
      
      - name: Login to ECR
        run: |
          aws ecr get-login-password --region ap-south-1 | \
            docker login --username AWS --password-stdin \
            ${{ secrets.AWS_ACCOUNT_ID }}.dkr.ecr.ap-south-1.amazonaws.com
      
      - name: Build and push Docker image
        run: |
          docker build -t krishimitra-backend .
          docker tag krishimitra-backend:latest \
            ${{ secrets.AWS_ACCOUNT_ID }}.dkr.ecr.ap-south-1.amazonaws.com/krishimitra-backend:latest
          docker push ${{ secrets.AWS_ACCOUNT_ID }}.dkr.ecr.ap-south-1.amazonaws.com/krishimitra-backend:latest
      
      - name: Update ECS service
        run: |
          aws ecs update-service \
            --cluster krishimitra-cluster \
            --service krishimitra-backend-service \
            --force-new-deployment
```

## Part 6: Cost Optimization

### Estimated Monthly Costs

| Service | Configuration | Cost |
|---------|--------------|------|
| S3 (Frontend) | 1GB storage, 10K requests | $0.50 |
| CloudFront | 10GB transfer | $1.00 |
| Lambda | 1M requests, 512MB | $5.00 |
| RDS Aurora Serverless | 2-4 ACU | $30-60 |
| API Gateway | 1M requests | $3.50 |
| Bedrock | 1M tokens | $10-20 |
| Polly | 1M characters | $4.00 |
| **Total (Serverless)** | | **$54-94/month** |

### Cost Optimization Tips

1. **Use Aurora Serverless** with auto-pause
2. **Enable CloudFront caching** (reduce origin requests)
3. **Use S3 Intelligent-Tiering** for satellite data
4. **Set Lambda reserved concurrency** to control costs
5. **Use AWS Budgets** to set alerts
6. **Enable Cost Explorer** to track spending

## Part 7: Monitoring & Logging

### CloudWatch Setup

```bash
# Create log groups
aws logs create-log-group --log-group-name /aws/lambda/krishimitra-backend
aws logs create-log-group --log-group-name /ecs/krishimitra-backend

# Create CloudWatch dashboard
# Go to CloudWatch → Dashboards → Create dashboard
# Add widgets for:
# - Lambda invocations
# - API Gateway requests
# - RDS connections
# - Error rates
```

### Set Up Alarms

```bash
# High error rate alarm
aws cloudwatch put-metric-alarm \
  --alarm-name krishimitra-high-errors \
  --alarm-description "Alert when error rate is high" \
  --metric-name Errors \
  --namespace AWS/Lambda \
  --statistic Sum \
  --period 300 \
  --threshold 10 \
  --comparison-operator GreaterThanThreshold
```

## Part 8: Security

### Security Checklist

- ✅ Use HTTPS everywhere (CloudFront + ALB)
- ✅ Enable WAF on CloudFront
- ✅ Use Secrets Manager for sensitive data
- ✅ Enable VPC for RDS (private subnets)
- ✅ Use IAM roles (not access keys)
- ✅ Enable CloudTrail for audit logs
- ✅ Set up Security Groups properly
- ✅ Enable RDS encryption at rest
- ✅ Use Parameter Store for config

## Part 9: Testing Deployment

```bash
# Test frontend
curl https://your-cloudfront-url.cloudfront.net

# Test backend
curl https://api.your-domain.com/

# Test farmer registration
curl -X POST https://api.your-domain.com/api/v1/farmers/ \
  -H "Content-Type: application/json" \
  -d '{
    "phone_number": "+918151910856",
    "preferred_language": "hi",
    "timezone": "Asia/Kolkata"
  }'
```

## Part 10: Domain Setup

### Configure Custom Domain

1. **Register domain** in Route 53
2. **Request SSL certificate** in ACM (us-east-1 for CloudFront)
3. **Add to CloudFront**:
   - Alternate domain names: www.your-domain.com, your-domain.com
   - SSL certificate: Select your ACM certificate
4. **Create Route 53 records**:
   - A record (Alias) → CloudFront distribution
   - CNAME www → CloudFront distribution

## Quick Deploy Script

Create `deploy.sh`:

```bash
#!/bin/bash

echo "Deploying KrishiMitra to AWS..."

# Build frontend
cd frontend
npm run build

# Deploy to S3
aws s3 sync dist/ s3://krishimitra-frontend --delete

# Invalidate CloudFront
aws cloudfront create-invalidation \
  --distribution-id YOUR_DISTRIBUTION_ID \
  --paths "/*"

# Build and deploy backend (if using ECS)
cd ..
docker build -t krishimitra-backend .
docker tag krishimitra-backend:latest \
  YOUR_ACCOUNT_ID.dkr.ecr.ap-south-1.amazonaws.com/krishimitra-backend:latest
docker push YOUR_ACCOUNT_ID.dkr.ecr.ap-south-1.amazonaws.com/krishimitra-backend:latest

# Update ECS service
aws ecs update-service \
  --cluster krishimitra-cluster \
  --service krishimitra-backend-service \
  --force-new-deployment

echo "Deployment complete!"
echo "Frontend: https://your-cloudfront-url.cloudfront.net"
echo "Backend: https://api.your-domain.com"
```

## Troubleshooting

### Frontend not loading
- Check S3 bucket policy
- Verify CloudFront distribution status
- Check browser console for errors

### API not responding
- Check Lambda/ECS logs in CloudWatch
- Verify security groups allow traffic
- Check API Gateway configuration

### Database connection errors
- Verify RDS security group
- Check DATABASE_URL format
- Ensure Lambda/ECS has VPC access

---

**Deployment complete!** Your KrishiMitra application is now live on AWS! 🚀
