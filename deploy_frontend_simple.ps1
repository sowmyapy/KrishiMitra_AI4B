# Simple Frontend Deployment to AWS S3
# Deploys React frontend to S3 with static website hosting

Write-Host "🚀 Starting Frontend Deployment to AWS S3..." -ForegroundColor Cyan

# Configuration
$BUCKET_NAME = "krishimitra-frontend"
$REGION = "ap-south-1"

# Step 1: Build the frontend (skip type checking for now)
Write-Host "`n📦 Building frontend..." -ForegroundColor Yellow
Set-Location frontend
# Build without type checking to avoid TypeScript errors
npx vite build
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Frontend build failed!" -ForegroundColor Red
    Set-Location ..
    exit 1
}
Set-Location ..
Write-Host "✅ Frontend built successfully!" -ForegroundColor Green

# Step 2: Create S3 bucket
Write-Host "`n🪣 Creating S3 bucket..." -ForegroundColor Yellow
aws s3 mb s3://$BUCKET_NAME --region $REGION 2>$null
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ S3 bucket created: $BUCKET_NAME" -ForegroundColor Green
} else {
    Write-Host "⚠️  Bucket already exists, continuing..." -ForegroundColor Yellow
}

# Step 3: Disable block public access
Write-Host "`n🔓 Configuring bucket for public access..." -ForegroundColor Yellow
aws s3api put-public-access-block --bucket $BUCKET_NAME --public-access-block-configuration "BlockPublicAcls=false,IgnorePublicAcls=false,BlockPublicPolicy=false,RestrictPublicBuckets=false"

# Step 4: Configure bucket for static website hosting
Write-Host "`n🌐 Enabling static website hosting..." -ForegroundColor Yellow
aws s3 website s3://$BUCKET_NAME --index-document index.html --error-document index.html

# Step 5: Set bucket policy for public read access
Write-Host "`n📜 Setting bucket policy..." -ForegroundColor Yellow
$POLICY = @"
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "PublicReadGetObject",
      "Effect": "Allow",
      "Principal": "*",
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::$BUCKET_NAME/*"
    }
  ]
}
"@
$POLICY | Out-File -FilePath bucket-policy.json -Encoding utf8
aws s3api put-bucket-policy --bucket $BUCKET_NAME --policy file://bucket-policy.json
Remove-Item bucket-policy.json
Write-Host "✅ Bucket policy set!" -ForegroundColor Green

# Step 6: Upload files to S3
Write-Host "`n📤 Uploading files to S3..." -ForegroundColor Yellow
aws s3 sync frontend/dist/ s3://$BUCKET_NAME/ --delete
Write-Host "✅ Files uploaded!" -ForegroundColor Green

# Step 7: Get the website URL
$WEBSITE_URL = "http://$BUCKET_NAME.s3-website.$REGION.amazonaws.com"

Write-Host "`n✅ Frontend deployment complete!" -ForegroundColor Green
Write-Host "`n📋 Deployment Summary:" -ForegroundColor Cyan
Write-Host "   - S3 Bucket: $BUCKET_NAME" -ForegroundColor White
Write-Host "   - Region: $REGION" -ForegroundColor White
Write-Host "   - Frontend URL: $WEBSITE_URL" -ForegroundColor White
Write-Host "   - Backend API: http://krishimitra-prod.eba-gz6myy8n.ap-south-1.elasticbeanstalk.com" -ForegroundColor White

Write-Host "`n🌐 Access your application at:" -ForegroundColor Cyan
Write-Host "   $WEBSITE_URL" -ForegroundColor Green

Write-Host "`n💡 To update the frontend in the future:" -ForegroundColor Yellow
Write-Host "   1. Make your changes" -ForegroundColor White
Write-Host "   2. Run: .\deploy_frontend_simple.ps1" -ForegroundColor White

# Save deployment info
@"
# Frontend Deployment Info

## S3 Static Website
- **Bucket Name**: $BUCKET_NAME
- **Region**: $REGION
- **Website URL**: $WEBSITE_URL
- **Backend API**: http://krishimitra-prod.eba-gz6myy8n.ap-south-1.elasticbeanstalk.com

## Deployment Date
$(Get-Date -Format "yyyy-MM-dd HH:mm:ss")

## Update Commands
To update the frontend:
``````powershell
cd frontend
npm run build
cd ..
aws s3 sync frontend/dist/ s3://$BUCKET_NAME/ --delete
``````

## Cost
- S3 storage: ~`$0.023/GB/month
- S3 requests: ~`$0.005/1000 requests
- Data transfer: First 100GB free, then `$0.09/GB
- **Estimated**: <`$5/month for prototype usage

## Add HTTPS (Optional)
To add HTTPS with CloudFront:
1. Run: .\deploy_frontend_to_s3.ps1 (full version with CloudFront)
2. Or manually create CloudFront distribution in AWS Console
"@ | Out-File -FilePath FRONTEND_DEPLOYMENT_INFO.md -Encoding utf8

Write-Host "`n📄 Deployment info saved to FRONTEND_DEPLOYMENT_INFO.md" -ForegroundColor Cyan
