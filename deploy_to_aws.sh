#!/bin/bash
# Quick AWS deployment script for KrishiMitra

set -e

echo "=========================================="
echo "  KrishiMitra - AWS Deployment"
echo "=========================================="
echo ""

# Check prerequisites
echo "Checking prerequisites..."

if ! command -v aws &> /dev/null; then
    echo "❌ AWS CLI not found. Install: https://aws.amazon.com/cli/"
    exit 1
fi

if ! command -v docker &> /dev/null; then
    echo "❌ Docker not found. Install: https://www.docker.com/"
    exit 1
fi

echo "✅ Prerequisites OK"
echo ""

# Get AWS account ID
ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
REGION="ap-south-1"

echo "AWS Account: $ACCOUNT_ID"
echo "Region: $REGION"
echo ""

# Create ECR repository
echo "Creating ECR repository..."
aws ecr create-repository \
    --repository-name krishimitra-app \
    --region $REGION \
    --image-scanning-configuration scanOnPush=true \
    || echo "Repository already exists"

# Login to ECR
echo "Logging in to ECR..."
aws ecr get-login-password --region $REGION | \
    docker login --username AWS --password-stdin \
    $ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com

# Build Docker image
echo "Building Docker image..."
docker build -t krishimitra-app:latest .

# Tag image
echo "Tagging image..."
docker tag krishimitra-app:latest \
    $ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com/krishimitra-app:latest

# Push to ECR
echo "Pushing to ECR..."
docker push $ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com/krishimitra-app:latest

echo ""
echo "=========================================="
echo "  Docker Image Pushed Successfully!"
echo "=========================================="
echo ""
echo "Image URI: $ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com/krishimitra-app:latest"
echo ""
echo "Next steps:"
echo "1. Deploy with Terraform: cd infrastructure/terraform && terraform apply"
echo "2. Or use Elastic Beanstalk: eb init && eb create"
echo ""
