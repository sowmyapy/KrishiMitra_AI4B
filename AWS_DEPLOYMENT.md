# KrishiMitra - AWS Deployment Guide

## Architecture Overview

KrishiMitra is deployed on AWS using the following managed services:

### Compute & Containers
- **ECS Fargate**: Serverless container orchestration for the FastAPI application
- **Lambda**: Background jobs (satellite ingestion, weather updates, predictions)
- **SageMaker**: ML model training and deployment

### Data Storage
- **RDS PostgreSQL**: Primary database with PostGIS extension
- **ElastiCache Redis**: Caching layer for performance
- **S3**: Object storage for satellite tiles, audio files, and ML models
- **Amazon MSK**: Managed Kafka for event streaming

### Networking & Security
- **VPC**: Isolated network with public/private/database subnets
- **ALB**: Application Load Balancer with SSL/TLS
- **CloudFront**: CDN for global content delivery
- **WAF**: Web Application Firewall for security
- **Secrets Manager**: Secure storage for API keys and credentials
- **KMS**: Encryption key management

### Monitoring & Logging
- **CloudWatch**: Logs, metrics, and alarms
- **X-Ray**: Distributed tracing
- **CloudTrail**: Audit logging

### AI/ML Services
- **Bedrock**: Alternative to OpenAI for LLM (optional)
- **Transcribe**: Speech-to-text (alternative to Whisper)
- **Polly**: Text-to-speech (alternative to ElevenLabs)
- **Rekognition**: Image analysis for satellite data

## Prerequisites

1. AWS Account with appropriate permissions
2. AWS CLI configured
3. Terraform installed (>= 1.0)
4. Docker installed
5. Domain name for the application

## Deployment Steps

### 1. Setup AWS CLI

```bash
# Configure AWS credentials
aws configure

# Verify access
aws sts get-caller-identity
```

### 2. Create S3 Backend for Terraform State

```bash
# Create S3 bucket for Terraform state
aws s3 mb s3://krishimitra-terraform-state --region ap-south-1

# Enable versioning
aws s3api put-bucket-versioning \
  --bucket krishimitra-terraform-state \
  --versioning-configuration Status=Enabled

# Create DynamoDB table for state locking
aws dynamodb create-table \
  --table-name krishimitra-terraform-locks \
  --attribute-definitions AttributeName=LockID,AttributeType=S \
  --key-schema AttributeName=LockID,KeyType=HASH \
  --billing-mode PAY_PER_REQUEST \
  --region ap-south-1
```

### 3. Store Secrets in AWS Secrets Manager

```bash
# JWT Secret
aws secretsmanager create-secret \
  --name krishimitra/production/jwt-secret \
  --secret-string "your-strong-random-jwt-secret-key" \
  --region ap-south-1

# OpenAI API Key
aws secretsmanager create-secret \
  --name krishimitra/production/openai-api-key \
  --secret-string "sk-your-openai-key" \
  --region ap-south-1

# Twilio Credentials
aws secretsmanager create-secret \
  --name krishimitra/production/twilio-sid \
  --secret-string "your-twilio-account-sid" \
  --region ap-south-1

aws secretsmanager create-secret \
  --name krishimitra/production/twilio-token \
  --secret-string "your-twilio-auth-token" \
  --region ap-south-1

# ElevenLabs API Key
aws secretsmanager create-secret \
  --name krishimitra/production/elevenlabs-key \
  --secret-string "your-elevenlabs-key" \
  --region ap-south-1
```

### 4. Build and Push Docker Image

```bash
# Login to ECR
aws ecr get-login-password --region ap-south-1 | \
  docker login --username AWS --password-stdin \
  <account-id>.dkr.ecr.ap-south-1.amazonaws.com

# Build Docker image
docker build -t krishimitra-app .

# Tag image
docker tag krishimitra-app:latest \
  <account-id>.dkr.ecr.ap-south-1.amazonaws.com/krishimitra-app:latest

# Push to ECR
docker push <account-id>.dkr.ecr.ap-south-1.amazonaws.com/krishimitra-app:latest
```

### 5. Deploy Infrastructure with Terraform

```bash
cd infrastructure/terraform

# Initialize Terraform
terraform init

# Review plan
terraform plan -out=tfplan

# Apply infrastructure
terraform apply tfplan

# Save outputs
terraform output > outputs.txt
```

### 6. Run Database Migrations

```bash
# Get RDS endpoint from Terraform outputs
RDS_ENDPOINT=$(terraform output -raw rds_endpoint)

# Run migrations using ECS task
aws ecs run-task \
  --cluster krishimitra-production \
  --task-definition krishimitra-migration \
  --launch-type FARGATE \
  --network-configuration "awsvpcConfiguration={subnets=[subnet-xxx],securityGroups=[sg-xxx]}" \
  --overrides '{"containerOverrides":[{"name":"app","command":["alembic","upgrade","head"]}]}'
```

### 7. Verify Deployment

```bash
# Get ALB DNS name
ALB_DNS=$(terraform output -raw alb_dns_name)

# Test health endpoint
curl https://$ALB_DNS/health

# Test API
curl https://$ALB_DNS/api/v1/docs
```

## AWS Service Configuration

### Speech and LLM Provider Selection

KrishiMitra supports two provider configurations:

**Option 1: OpenAI + ElevenLabs (Default)**
- LLM: OpenAI GPT-4
- STT: OpenAI Whisper
- TTS: ElevenLabs
- Embeddings: OpenAI text-embedding-3-small

**Option 2: AWS Native Services**
- LLM: AWS Bedrock (Claude v2 or Titan)
- STT: AWS Transcribe
- TTS: AWS Polly
- Embeddings: AWS Bedrock Titan Embeddings

To switch between providers, set environment variables:

```bash
# Use AWS services
export USE_AWS_SERVICES=True
export LLM_PROVIDER=bedrock

# Or use OpenAI (default)
export USE_AWS_SERVICES=False
export LLM_PROVIDER=openai
```

### Using AWS Bedrock for LLM

The application automatically uses Bedrock when `USE_AWS_SERVICES=True`:

```python
# src/services/llm_factory.py handles provider selection
from src.services.llm_factory import get_llm

llm = get_llm()  # Returns BedrockProvider or OpenAIProvider
response = await llm.generate_completion(messages)
```

**Enable Bedrock Models:**

```bash
# Enable Claude v2 in AWS Console
# Go to Bedrock > Model access > Request model access
# Select: anthropic.claude-v2, amazon.titan-text-express-v1, amazon.titan-embed-text-v1

# Or use AWS CLI
aws bedrock list-foundation-models --region ap-south-1
```

### Using AWS Transcribe for Speech-to-Text

The application automatically uses Transcribe when `USE_AWS_SERVICES=True`:

```python
# src/services/speech_factory.py handles provider selection
from src.services.speech_factory import get_stt

stt = get_stt()  # Returns TranscribeSTTProvider or WhisperSTTProvider
result = await stt.transcribe(audio_data, language="hi")
```

**Supported Languages:**
- Hindi (hi-IN)
- Bengali (bn-IN)
- Telugu (te-IN)
- Marathi (mr-IN)
- Tamil (ta-IN)
- Gujarati (gu-IN)
- Kannada (kn-IN)
- Malayalam (ml-IN)
- Punjabi (pa-IN)
- English (en-IN)

### Using AWS Polly for Text-to-Speech

The application automatically uses Polly when `USE_AWS_SERVICES=True`:

```python
# src/services/speech_factory.py handles provider selection
from src.services.speech_factory import get_tts

tts = get_tts()  # Returns PollyTTSProvider or ElevenLabsTTSProvider
audio = await tts.synthesize(text, language="hi")
```

**Available Voices:**
- Hindi: Aditi (female, neural)
- English (India): Raveena (female, neural)

**Note:** AWS Polly has limited Indian language support compared to ElevenLabs. For production with multiple Indian languages, consider using ElevenLabs or a hybrid approach.

### IAM Permissions Required

Add these permissions to your ECS task role:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "bedrock:InvokeModel",
        "bedrock:InvokeModelWithResponseStream"
      ],
      "Resource": [
        "arn:aws:bedrock:*::foundation-model/anthropic.claude-v2",
        "arn:aws:bedrock:*::foundation-model/amazon.titan-*"
      ]
    },
    {
      "Effect": "Allow",
      "Action": [
        "transcribe:StartTranscriptionJob",
        "transcribe:GetTranscriptionJob"
      ],
      "Resource": "*"
    },
    {
      "Effect": "Allow",
      "Action": [
        "polly:SynthesizeSpeech"
      ],
      "Resource": "*"
    },
    {
      "Effect": "Allow",
      "Action": [
        "s3:GetObject",
        "s3:PutObject",
        "s3:DeleteObject"
      ],
      "Resource": [
        "arn:aws:s3:::${S3_BUCKET_AUDIO}/*"
      ]
    }
  ]
}
```

### Cost Comparison

**OpenAI + ElevenLabs (per 10,000 farmers/month):**
- OpenAI GPT-4: ~$300
- OpenAI Whisper: ~$100
- ElevenLabs TTS: ~$200
- Total: ~$600/month

**AWS Native Services (per 10,000 farmers/month):**
- Bedrock Claude v2: ~$250
- Transcribe: ~$80
- Polly: ~$40
- Total: ~$370/month

**Recommendation:** Use AWS native services for cost savings, but consider ElevenLabs for better Indian language TTS quality.

### Using AWS Transcribe (Alternative to Whisper)

```python
# Update src/services/communication/speech_to_text.py
import boto3

transcribe_client = boto3.client('transcribe', region_name='ap-south-1')

# Start transcription job
response = transcribe_client.start_transcription_job(
    TranscriptionJobName='job-name',
    Media={'MediaFileUri': 's3://bucket/audio.mp3'},
    MediaFormat='mp3',
    LanguageCode='hi-IN'
)
```

### Using AWS Polly (Alternative to ElevenLabs)

```python
# Update src/services/communication/text_to_speech.py
import boto3

polly_client = boto3.client('polly', region_name='ap-south-1')

response = polly_client.synthesize_speech(
    Text='Your text here',
    OutputFormat='mp3',
    VoiceId='Aditi',  # Hindi voice
    LanguageCode='hi-IN'
)
```

### Using Amazon MSK (Managed Kafka)

```python
# Update Kafka configuration
KAFKA_BOOTSTRAP_SERVERS = os.getenv('MSK_BOOTSTRAP_BROKERS')

# MSK uses IAM authentication
from aws_msk_iam_sasl_signer import MSKAuthTokenProvider

class MSKTokenProvider:
    def token(self):
        token, _ = MSKAuthTokenProvider.generate_auth_token('ap-south-1')
        return token

producer = KafkaProducer(
    bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
    security_protocol='SASL_SSL',
    sasl_mechanism='OAUTHBEARER',
    sasl_oauth_token_provider=MSKTokenProvider()
)
```

## Cost Optimization

### 1. Use Spot Instances for Batch Processing

```hcl
# In ECS task definition
capacity_provider_strategy {
  capacity_provider = "FARGATE_SPOT"
  weight           = 1
  base             = 0
}
```

### 2. S3 Lifecycle Policies

Already configured in Terraform:
- Satellite tiles: Archive to Glacier after 90 days, delete after 365 days
- Audio recordings: Delete after 90 days

### 3. RDS Auto-Scaling

```hcl
resource "aws_appautoscaling_target" "rds" {
  max_capacity       = 15
  min_capacity       = 2
  resource_id        = "cluster:${aws_rds_cluster.main.cluster_identifier}"
  scalable_dimension = "rds:cluster:ReadReplicaCount"
  service_namespace  = "rds"
}
```

### 4. Lambda Reserved Concurrency

```hcl
resource "aws_lambda_function" "satellite_ingestion" {
  reserved_concurrent_executions = 5
}
```

## Monitoring & Alerts

### CloudWatch Alarms

```bash
# High CPU alarm
aws cloudwatch put-metric-alarm \
  --alarm-name krishimitra-high-cpu \
  --alarm-description "Alert when CPU exceeds 80%" \
  --metric-name CPUUtilization \
  --namespace AWS/ECS \
  --statistic Average \
  --period 300 \
  --threshold 80 \
  --comparison-operator GreaterThanThreshold \
  --evaluation-periods 2

# High error rate alarm
aws cloudwatch put-metric-alarm \
  --alarm-name krishimitra-high-errors \
  --alarm-description "Alert when error rate exceeds 5%" \
  --metric-name 5XXError \
  --namespace AWS/ApplicationELB \
  --statistic Sum \
  --period 60 \
  --threshold 10 \
  --comparison-operator GreaterThanThreshold \
  --evaluation-periods 2
```

### CloudWatch Dashboard

```bash
aws cloudwatch put-dashboard \
  --dashboard-name KrishiMitra-Production \
  --dashboard-body file://cloudwatch-dashboard.json
```

## Disaster Recovery

### 1. RDS Automated Backups

- Configured for 7-day retention
- Multi-AZ deployment for high availability
- Point-in-time recovery enabled

### 2. S3 Cross-Region Replication

```hcl
resource "aws_s3_bucket_replication_configuration" "satellite" {
  bucket = module.s3.satellite_bucket_id
  
  rule {
    id     = "replicate-to-backup-region"
    status = "Enabled"
    
    destination {
      bucket        = aws_s3_bucket.backup.arn
      storage_class = "STANDARD_IA"
    }
  }
}
```

### 3. Backup Strategy

- Database: Daily automated backups, 7-day retention
- S3: Versioning enabled, cross-region replication
- Configuration: Terraform state in S3 with versioning

## Security Best Practices

1. **Network Security**
   - Private subnets for application and database
   - Security groups with least privilege
   - VPC endpoints for AWS services

2. **Data Encryption**
   - RDS encryption at rest with KMS
   - S3 encryption with SSE-S3 or SSE-KMS
   - TLS 1.3 for data in transit

3. **Access Control**
   - IAM roles with least privilege
   - Secrets Manager for sensitive data
   - MFA for AWS console access

4. **Compliance**
   - CloudTrail for audit logging
   - Config for compliance monitoring
   - GuardDuty for threat detection

## Scaling Strategy

### Horizontal Scaling

- ECS auto-scaling based on CPU/memory
- RDS read replicas for read-heavy workloads
- ElastiCache cluster mode for Redis

### Vertical Scaling

- Increase ECS task CPU/memory
- Upgrade RDS instance class
- Increase Lambda memory allocation

## Estimated Monthly Costs

Based on 10,000 farmers:

- **ECS Fargate**: $150 (3 tasks, 1GB RAM, 0.5 vCPU)
- **RDS PostgreSQL**: $200 (db.t3.medium, Multi-AZ)
- **ElastiCache Redis**: $100 (cache.t3.medium, 2 nodes)
- **Amazon MSK**: $300 (3 brokers, kafka.t3.small)
- **S3**: $50 (satellite tiles + audio)
- **Lambda**: $100 (background jobs)
- **Data Transfer**: $50
- **CloudWatch**: $30

**Total**: ~$980/month (~$0.10 per farmer/month)

## Troubleshooting

### Check ECS Task Logs

```bash
aws logs tail /aws/ecs/krishimitra-production --follow
```

### Check Lambda Logs

```bash
aws logs tail /aws/lambda/krishimitra-satellite-ingestion --follow
```

### Connect to RDS

```bash
# Create bastion host or use Systems Manager Session Manager
aws ssm start-session --target i-xxxxx

# Connect to RDS
psql -h $RDS_ENDPOINT -U krishimitra_admin -d krishimitra
```

### Debug ECS Task

```bash
# Describe task
aws ecs describe-tasks \
  --cluster krishimitra-production \
  --tasks <task-arn>

# Check task stopped reason
aws ecs describe-tasks \
  --cluster krishimitra-production \
  --tasks <task-arn> \
  --query 'tasks[0].stoppedReason'
```

## Next Steps

1. Configure custom domain with Route 53
2. Set up CI/CD pipeline with CodePipeline
3. Implement blue-green deployment
4. Configure WAF rules
5. Set up cost alerts
6. Implement automated testing in staging environment

---

For support, contact the DevOps team or refer to AWS documentation.
