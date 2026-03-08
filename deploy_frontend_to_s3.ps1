# Deploy Frontend to AWS S3 + CloudFront
# This script builds the React frontend and deploys it to S3 with CloudFront CDN

Write-Host "🚀 Starting Frontend Deployment to AWS..." -ForegroundColor Cyan

# Configuration
$BUCKET_NAME = "krishimitra-frontend"
$REGION = "ap-south-1"
$CLOUDFRONT_COMMENT = "KrishiMitra Frontend Distribution"

# Step 1: Build the frontend
Write-Host "`n📦 Building frontend..." -ForegroundColor Yellow
Set-Location frontend
npm run build
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Frontend build failed!" -ForegroundColor Red
    exit 1
}
Set-Location ..

# Step 2: Create S3 bucket
Write-Host "`n🪣 Creating S3 bucket..." -ForegroundColor Yellow
aws s3 mb s3://$BUCKET_NAME --region $REGION 2>$null
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ S3 bucket created: $BUCKET_NAME" -ForegroundColor Green
} else {
    Write-Host "⚠️  Bucket might already exist, continuing..." -ForegroundColor Yellow
}

# Step 3: Configure bucket for static website hosting
Write-Host "`n🌐 Configuring S3 for static website hosting..." -ForegroundColor Yellow
aws s3 website s3://$BUCKET_NAME --index-document index.html --error-document index.html

# Step 4: Update bucket policy for public read access
Write-Host "`n🔓 Setting bucket policy for public access..." -ForegroundColor Yellow
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

# Step 5: Upload files to S3
Write-Host "`n📤 Uploading files to S3..." -ForegroundColor Yellow
aws s3 sync frontend/dist/ s3://$BUCKET_NAME/ --delete --cache-control "public, max-age=31536000" --exclude "index.html"
aws s3 cp frontend/dist/index.html s3://$BUCKET_NAME/index.html --cache-control "public, max-age=0, must-revalidate"

# Step 6: Create CloudFront distribution
Write-Host "`n☁️  Creating CloudFront distribution..." -ForegroundColor Yellow
$DISTRIBUTION_CONFIG = @"
{
  "CallerReference": "krishimitra-$(Get-Date -Format 'yyyyMMddHHmmss')",
  "Comment": "$CLOUDFRONT_COMMENT",
  "Enabled": true,
  "Origins": {
    "Quantity": 1,
    "Items": [
      {
        "Id": "S3-$BUCKET_NAME",
        "DomainName": "$BUCKET_NAME.s3-website.$REGION.amazonaws.com",
        "CustomOriginConfig": {
          "HTTPPort": 80,
          "HTTPSPort": 443,
          "OriginProtocolPolicy": "http-only"
        }
      }
    ]
  },
  "DefaultRootObject": "index.html",
  "DefaultCacheBehavior": {
    "TargetOriginId": "S3-$BUCKET_NAME",
    "ViewerProtocolPolicy": "redirect-to-https",
    "AllowedMethods": {
      "Quantity": 2,
      "Items": ["GET", "HEAD"],
      "CachedMethods": {
        "Quantity": 2,
        "Items": ["GET", "HEAD"]
      }
    },
    "Compress": true,
    "ForwardedValues": {
      "QueryString": false,
      "Cookies": {
        "Forward": "none"
      }
    },
    "MinTTL": 0,
    "DefaultTTL": 86400,
    "MaxTTL": 31536000
  },
  "CustomErrorResponses": {
    "Quantity": 1,
    "Items": [
      {
        "ErrorCode": 404,
        "ResponsePagePath": "/index.html",
        "ResponseCode": "200",
        "ErrorCachingMinTTL": 300
      }
    ]
  }
}
"@
$DISTRIBUTION_CONFIG | Out-File -FilePath cloudfront-config.json -Encoding utf8

$DISTRIBUTION = aws cloudfront create-distribution --distribution-config file://cloudfront-config.json 2>&1
if ($LASTEXITCODE -eq 0) {
    $DISTRIBUTION_JSON = $DISTRIBUTION | ConvertFrom-Json
    $CLOUDFRONT_URL = $DISTRIBUTION_JSON.Distribution.DomainName
    $DISTRIBUTION_ID = $DISTRIBUTION_JSON.Distribution.Id
    
    Write-Host "`n✅ CloudFront distribution created!" -ForegroundColor Green
    Write-Host "   Distribution ID: $DISTRIBUTION_ID" -ForegroundColor Cyan
    Write-Host "   CloudFront URL: https://$CLOUDFRONT_URL" -ForegroundColor Cyan
    Write-Host "`n⏳ Note: CloudFront deployment takes 15-20 minutes to propagate globally" -ForegroundColor Yellow
    
    # Save deployment info
    @"
# Frontend Deployment Info

## S3 Bucket
- Bucket Name: $BUCKET_NAME
- Region: $REGION
- S3 Website URL: http://$BUCKET_NAME.s3-website.$REGION.amazonaws.com

## CloudFront CDN
- Distribution ID: $DISTRIBUTION_ID
- CloudFront URL: https://$CLOUDFRONT_URL
- Status: Deploying (takes 15-20 minutes)

## Access URLs
- S3 Direct: http://$BUCKET_NAME.s3-website.$REGION.amazonaws.com
- CloudFront (HTTPS): https://$CLOUDFRONT_URL

## Update Commands
To update the frontend:
``````powershell
cd frontend
npm run build
cd ..
aws s3 sync frontend/dist/ s3://$BUCKET_NAME/ --delete
aws cloudfront create-invalidation --distribution-id $DISTRIBUTION_ID --paths "/*"
``````
"@ | Out-File -FilePath FRONTEND_DEPLOYMENT_INFO.md -Encoding utf8
    
} else {
    Write-Host "⚠️  CloudFront creation failed or already exists" -ForegroundColor Yellow
    Write-Host "   You can access the site via S3: http://$BUCKET_NAME.s3-website.$REGION.amazonaws.com" -ForegroundColor Cyan
}

Remove-Item cloudfront-config.json -ErrorAction SilentlyContinue

Write-Host "`n✅ Frontend deployment complete!" -ForegroundColor Green
Write-Host "`n📋 Summary:" -ForegroundColor Cyan
Write-Host "   - S3 Bucket: $BUCKET_NAME" -ForegroundColor White
Write-Host "   - S3 URL: http://$BUCKET_NAME.s3-website.$REGION.amazonaws.com" -ForegroundColor White
if ($CLOUDFRONT_URL) {
    Write-Host "   - CloudFront URL: https://$CLOUDFRONT_URL (wait 15-20 min)" -ForegroundColor White
}
Write-Host "`n🔗 Backend API: http://krishimitra-prod.eba-gz6myy8n.ap-south-1.elasticbeanstalk.com" -ForegroundColor White
