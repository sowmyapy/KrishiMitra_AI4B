# Testing the Deployed KrishiMitra Application

## Frontend URL
http://krishimitra-frontend.s3-website.ap-south-1.amazonaws.com

## Backend URL
http://krishimitra-prod.eba-gz6myy8n.ap-south-1.elasticbeanstalk.com

## Test Steps

### 1. Register a Farmer
1. Open the frontend URL in your browser
2. Click "Add Farmer"
3. Fill in the form:
   - Phone: +918095666788
   - Language: Hindi
   - Timezone: Asia/Kolkata
4. Click "Register Farmer"

### 2. Add a Farm Plot
1. Click on the farmer you just created
2. Click "Add Plot"
3. Fill in the plot details:
   - Latitude: 12.9716 (Bangalore)
   - Longitude: 77.5946
   - Area: 2.5 hectares
   - Crop: rice
   - Planting Date: 2026-01-15
4. Click "Add Plot"

### 3. Generate Advisory
1. On the farmer detail page, click "Generate Advisory"
2. Wait for the advisory to be generated
3. You should see a Hindi advisory message

### 4. Test Voice Call (Optional)
1. Update Twilio webhook URL to point to the deployed backend
2. Call +17752270557 from +918095666788
3. You should hear the Hindi advisory

## Known Limitations

### Data Persistence
- SQLite database is stored on EC2 instance
- Data is wiped on each deployment
- For production, migrate to Amazon RDS

### LLM Generation
- AWS Bedrock calls are failing (IAM permissions needed)
- Falling back to Hindi/Telugu templates
- Templates are working correctly

### CORS
- Currently allowing all origins for prototype
- Tighten security before production use

## Troubleshooting

If you see "Error generating advisory":
1. Make sure the farmer has at least one plot
2. Check backend logs: `eb logs`
3. The fallback templates should still work even if LLM fails

If you see "Network Error":
1. Check that both frontend and backend are accessible
2. Clear browser cache and reload
3. Check browser console for specific error messages
