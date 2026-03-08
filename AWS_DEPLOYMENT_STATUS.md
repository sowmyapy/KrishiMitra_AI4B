# AWS Deployment Status

## Current Status: ✅ DEPLOYMENT SUCCESSFUL

The backend has been successfully deployed to AWS Elastic Beanstalk and is fully operational!

## Deployment Summary

### Backend (Elastic Beanstalk) ✅
- **Application Name**: krishimitra
- **Environment**: krishimitra-prod
- **Platform**: Python 3.11 on Amazon Linux 2023
- **Instance Type**: t3.medium
- **Region**: ap-south-1 (Mumbai)
- **Backend URL**: http://krishimitra-prod.eba-gz6myy8n.ap-south-1.elasticbeanstalk.com
- **Health Status**: Green ✅
- **Deployed Version**: app-a341-260307_221452617646 (Language codes + CORS + DB tables fixed)

### Frontend (S3 Static Website) ✅
- **S3 Bucket**: krishimitra-frontend
- **Region**: ap-south-1 (Mumbai)
- **Frontend URL**: http://krishimitra-frontend.s3-website.ap-south-1.amazonaws.com
- **Status**: Live and accessible ✅

### Working Endpoints ✅
- **Frontend UI**: http://krishimitra-frontend.s3-website.ap-south-1.amazonaws.com
- Backend Root: http://krishimitra-prod.eba-gz6myy8n.ap-south-1.elasticbeanstalk.com/
- Backend Health: http://krishimitra-prod.eba-gz6myy8n.ap-south-1.elasticbeanstalk.com/health
- Voice Advisory: http://krishimitra-prod.eba-gz6myy8n.ap-south-1.elasticbeanstalk.com/api/v1/voice/advisory
- **Farmer Registration**: ✅ Tested and working (created farmer ID: 57a69bd5-5122-4616-9df6-b656ce93f03e)

## Issues Fixed During Deployment

### 1. Pydantic Settings Validation ✅
**Problem**: Settings class had required fields without defaults
**Solution**: Added default values to all fields in `src/config/settings.py`

### 2. Missing Python Package ✅
**Problem**: `pythonjsonlogger` module not found
**Solution**: Made JSON logging optional with try/except import

### 3. Log Directory Missing ✅
**Problem**: Application tried to create log file in non-existent directory
**Solution**: Added `os.makedirs('logs', exist_ok=True)` with error handling

### 4. PostgreSQL Dependency ✅
**Problem**: `.ebextensions/01_packages.config` tried to install `postgresql-devel`
**Solution**: Removed postgresql-devel (not needed for SQLite)

### 5. Heavy Dependencies ✅
**Problem**: TensorFlow and ML libraries caused disk space issues
**Solution**: Created minimal `requirements.txt` with only essential packages

### 6. CORS Configuration ✅
**Problem**: Frontend on S3 couldn't call backend API due to CORS blocking
**Solution**: Simplified CORS to allow all origins for prototype (`allow_origins=["*"]`)

### 7. Database Tables Not Created ✅
**Problem**: SQLite database tables didn't exist in production, causing 500 errors
**Solution**: Modified startup to create tables on every startup (appropriate for SQLite prototype)

### 8. Language Code Mismatch ✅
**Problem**: Advisory generation checked for "hi" but frontend sent "hindi", causing English fallback
**Solution**: Updated language code handling to accept both "hi"/"hindi" and "te"/"telugu"

### 9. Hardcoded Frontend URLs ✅
**Problem**: Frontend pages had hardcoded localhost:8000 URLs instead of using environment variable
**Solution**: Created getApiUrl() helper and updated all pages to use production backend URL

## Important Notes

### SQLite Data Persistence ⚠️
**Current Setup**: Using SQLite database stored on EC2 instance
**Limitation**: Database is wiped on each deployment (eb deploy)
**Impact**: All farmers, plots, and advisories are lost when you redeploy
**For Production**: Use Amazon RDS (PostgreSQL) for persistent data storage

### AWS Bedrock LLM ⚠️
**Current Status**: LLM calls are failing, using fallback Hindi templates
**Likely Cause**: IAM role needs Bedrock permissions
**Impact**: Advisory text uses simple templates instead of AI-generated content
**Fallback**: Hindi/Telugu templates are working correctly

## Next Steps

### 1. Update Twilio Webhook URL
Update your Twilio phone number (+17752270557) webhook URL to:
```
http://krishimitra-prod.eba-gz6myy8n.ap-south-1.elasticbeanstalk.com/api/v1/voice/advisory
```

**Steps**:
1. Go to Twilio Console: https://console.twilio.com/
2. Navigate to Phone Numbers → Manage → Active Numbers
3. Click on +17752270557
4. Under "Voice Configuration":
   - A Call Comes In: Webhook
   - URL: `http://krishimitra-prod.eba-gz6myy8n.ap-south-1.elasticbeanstalk.com/api/v1/voice/advisory`
   - HTTP Method: POST
5. Save

### 2. Test Voice Call
Call +17752270557 from +918095666788 to test the Hindi advisory system

### 3. Enable HTTPS (Optional but Recommended)
Currently using HTTP. To enable HTTPS:
1. Go to EB Console → Configuration → Load Balancer
2. Add HTTPS listener on port 443
3. Upload or create SSL certificate
4. Update Twilio webhook to use `https://` instead of `http://`

### 4. Monitor Application
- View logs: `eb logs --all`
- Check status: `eb status`
- View in AWS Console: https://ap-south-1.console.aws.amazon.com/elasticbeanstalk/home?region=ap-south-1#/environment/dashboard?environmentId=e-jzpm3k8squ

## Cost Estimate

### Backend (Elastic Beanstalk)
- t3.medium instance: ~$0.0416/hour = ~$30/month
- Data transfer: Minimal for prototype
- **Backend subtotal**: ~$30-35/month

### Frontend (S3 Static Website)
- S3 storage: ~$0.023/GB/month (~$0.50/month for typical frontend)
- S3 requests: ~$0.005/1000 requests (~$1/month for moderate traffic)
- Data transfer: First 100GB free, then $0.09/GB
- **Frontend subtotal**: ~$2-5/month

### Total Estimated Cost
**~$35-40/month** for the complete application

To reduce costs:
- Use t3.small for backend ($15/month) once stable
- Stop environment when not in use: `eb terminate`
- Use AWS Free Tier eligible services where possible

## Deployment Commands Reference

### Backend Commands
```powershell
# Check status
eb status

# View logs
eb logs --all

# Update environment variables
eb setenv KEY=value KEY2=value2

# Deploy new version
eb deploy

# Terminate environment (to save costs)
eb terminate krishimitra-prod

# Recreate environment
eb create krishimitra-prod --instance-type t3.medium --single
```

### Frontend Commands
```powershell
# Update frontend
.\deploy_frontend_simple.ps1

# Or manually:
cd frontend
npx vite build
cd ..
aws s3 sync frontend/dist/ s3://krishimitra-frontend/ --delete
```

## Files Modified for Deployment

1. `src/config/settings.py` - Added default values for all fields
2. `src/config/logging_config.py` - Made pythonjsonlogger optional, added logs directory creation
3. `requirements.txt` - Minimal dependencies for deployment
4. `.ebextensions/01_packages.config` - Removed postgresql-devel

## Environment Variables Set

All environment variables have been configured via `eb setenv`:
- AWS credentials (AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION)
- Twilio credentials (TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_PHONE_NUMBER)
- Sentinel Hub credentials (SENTINEL_HUB_CLIENT_ID, SENTINEL_HUB_CLIENT_SECRET)
- OpenWeatherMap API key
- S3 bucket names
- LLM provider settings (LLM_PROVIDER=bedrock, USE_AWS_SERVICES=True)
- Security keys (JWT_SECRET_KEY, ENCRYPTION_KEY)
- Database URL (DATABASE_URL=sqlite:///./krishimitra.db)

## Important URLs

- **Application URL**: http://krishimitra-prod.eba-gz6myy8n.ap-south-1.elasticbeanstalk.com
- **EB Console**: https://ap-south-1.console.aws.amazon.com/elasticbeanstalk/home?region=ap-south-1#/environment/dashboard?environmentId=e-jzpm3k8squ
- **S3 Bucket**: elasticbeanstalk-ap-south-1-520578320427

## Troubleshooting

If issues occur:
1. Check logs: `eb logs --all`
2. Check health: `eb status`
3. Restart app: `eb deploy` (redeploys current version)
4. Check environment variables: `eb printenv`

## Support Resources

- [EB Python Documentation](https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/create-deploy-python-apps.html)
- [EB Environment Variables](https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/environments-cfg-softwaresettings.html)
- [Troubleshooting EB](https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/troubleshooting.html)
