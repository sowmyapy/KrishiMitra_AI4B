# Quick AWS deployment script for KrishiMitra (PowerShell)

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "  KrishiMitra - AWS Deployment" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""

# Check prerequisites
Write-Host "Checking prerequisites..." -ForegroundColor Yellow

try {
    $awsVersion = aws --version 2>&1
    Write-Host "[OK] AWS CLI found: $awsVersion" -ForegroundColor Green
} catch {
    Write-Host "[ERROR] AWS CLI not found. Install: https://aws.amazon.com/cli/" -ForegroundColor Red
    exit 1
}

try {
    $dockerVersion = docker --version 2>&1
    Write-Host "[OK] Docker found: $dockerVersion" -ForegroundColor Green
} catch {
    Write-Host "[ERROR] Docker not found. Install: https://www.docker.com/" -ForegroundColor Red
    exit 1
}

Write-Host ""

# Get AWS account ID
$ACCOUNT_ID = aws sts get-caller-identity --query Account --output text
$REGION = "ap-south-1"

Write-Host "AWS Account: $ACCOUNT_ID" -ForegroundColor Cyan
Write-Host "Region: $REGION" -ForegroundColor Cyan
Write-Host ""

# Create ECR repository
Write-Host "Creating ECR repository..." -ForegroundColor Yellow
aws ecr create-repository `
    --repository-name krishimitra-app `
    --region $REGION `
    --image-scanning-configuration scanOnPush=true `
    2>$null

if ($LASTEXITCODE -ne 0) {
    Write-Host "[INFO] Repository already exists" -ForegroundColor Gray
}

# Login to ECR
Write-Host "Logging in to ECR..." -ForegroundColor Yellow
$ecrPassword = aws ecr get-login-password --region $REGION
$ecrPassword | docker login --username AWS --password-stdin "$ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com"

# Build Docker image
Write-Host "Building Docker image..." -ForegroundColor Yellow
docker build -t krishimitra-app:latest .

# Tag image
Write-Host "Tagging image..." -ForegroundColor Yellow
docker tag krishimitra-app:latest "$ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com/krishimitra-app:latest"

# Push to ECR
Write-Host "Pushing to ECR..." -ForegroundColor Yellow
docker push "$ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com/krishimitra-app:latest"

Write-Host ""
Write-Host "==========================================" -ForegroundColor Green
Write-Host "  Docker Image Pushed Successfully!" -ForegroundColor Green
Write-Host "==========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Image URI: $ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com/krishimitra-app:latest" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "1. Deploy with Terraform: cd infrastructure/terraform && terraform apply" -ForegroundColor White
Write-Host "2. Or use Elastic Beanstalk: eb init && eb create" -ForegroundColor White
Write-Host ""
