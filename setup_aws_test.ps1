# KrishiMitra AWS Setup Script for Testing
# Run this script to set up AWS resources for testing

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "KrishiMitra AWS Setup for Testing" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# 1. Check AWS CLI
Write-Host "1. Checking AWS CLI..." -ForegroundColor Yellow
try {
    $identity = aws sts get-caller-identity | ConvertFrom-Json
    Write-Host "   ✓ AWS CLI configured" -ForegroundColor Green
    Write-Host "   Account: $($identity.Account)" -ForegroundColor Gray
    Write-Host "   User: $($identity.Arn)" -ForegroundColor Gray
} catch {
    Write-Host "   ✗ AWS CLI not configured" -ForegroundColor Red
    Write-Host "   Run: aws configure" -ForegroundColor Yellow
    exit 1
}

# 2. Create S3 bucket
Write-Host ""
Write-Host "2. Creating S3 bucket for audio files..." -ForegroundColor Yellow
$bucketName = "krishimitra-audio-test-$($identity.Account)"
try {
    aws s3 mb s3://$bucketName --region ap-south-1 2>$null
    Write-Host "   ✓ Bucket created: $bucketName" -ForegroundColor Green
} catch {
    Write-Host "   ℹ Bucket may already exist: $bucketName" -ForegroundColor Gray
}

# 3. Check Bedrock models
Write-Host ""
Write-Host "3. Checking Bedrock model access..." -ForegroundColor Yellow
try {
    $models = aws bedrock list-foundation-models --region ap-south-1 | ConvertFrom-Json
    $claudeModels = $models.modelSummaries | Where-Object { $_.modelId -like "*claude*" }
    $titanModels = $models.modelSummaries | Where-Object { $_.modelId -like "*titan-embed*" }
    
    if ($claudeModels.Count -gt 0) {
        Write-Host "   ✓ Claude models available: $($claudeModels.Count)" -ForegroundColor Green
    } else {
        Write-Host "   ✗ No Claude models available" -ForegroundColor Red
        Write-Host "   Enable at: https://console.aws.amazon.com/bedrock" -ForegroundColor Yellow
    }
    
    if ($titanModels.Count -gt 0) {
        Write-Host "   ✓ Titan embedding models available: $($titanModels.Count)" -ForegroundColor Green
    } else {
        Write-Host "   ⚠ No Titan embedding models found" -ForegroundColor Yellow
    }
} catch {
    Write-Host "   ✗ Error checking Bedrock models" -ForegroundColor Red
}

# 4. Update .env file
Write-Host ""
Write-Host "4. Updating .env file..." -ForegroundColor Yellow
if (Test-Path ".env") {
    Write-Host "   ℹ .env file already exists" -ForegroundColor Gray
} else {
    Copy-Item ".env.example" ".env"
    Write-Host "   ✓ Created .env from .env.example" -ForegroundColor Green
}

# Update .env with AWS settings
$envContent = Get-Content ".env" -Raw
$envContent = $envContent -replace "AWS_REGION=.*", "AWS_REGION=ap-south-1"
$envContent = $envContent -replace "S3_BUCKET_AUDIO=.*", "S3_BUCKET_AUDIO=$bucketName"
$envContent = $envContent -replace "LLM_PROVIDER=.*", "LLM_PROVIDER=bedrock"
$envContent = $envContent -replace "USE_AWS_SERVICES=.*", "USE_AWS_SERVICES=True"
$envContent | Set-Content ".env"
Write-Host "   ✓ Updated .env with AWS settings" -ForegroundColor Green

# 5. Summary
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Setup Complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "1. Activate virtual environment: .\venv\Scripts\Activate.ps1" -ForegroundColor White
Write-Host "2. Run integration test: python scripts/test_aws_integration.py" -ForegroundColor White
Write-Host ""
Write-Host "S3 Bucket: $bucketName" -ForegroundColor Gray
Write-Host "Region: ap-south-1" -ForegroundColor Gray
Write-Host ""
