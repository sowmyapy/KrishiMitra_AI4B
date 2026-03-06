# Testing Guide - Farmer Advisory System

## Current Status
✅ Backend running on http://localhost:8000
✅ Frontend running on http://localhost:3000
✅ Advisory generation endpoint fixed
✅ Voice call endpoint created
✅ Advisory display added to farmer detail page
✅ Both test farmers now have plots

## Test Farmers with Plots

### Farmer 1
**Farmer ID**: `fc008579-7fcb-4f31-8ab8-837ef8d44f83`
**Phone**: +918151910856
**Language**: Hindi (hi)
**Timezone**: Asia/Kolkata
**Plot ID**: `b18ef2b0-5ef6-46d1-bf50-a51b9959a388`
**Location**: Bangalore (12.9716, 77.5946)
**Crops**: wheat, rice
**Area**: 2.5 hectares

### Farmer 2
**Farmer ID**: `aa25b281-8515-4be1-a8de-25b244b403b5`
**Phone**: +918095666788
**Language**: Hindi (hi)
**Timezone**: Asia/Kolkata
**Plot ID**: `cf5214ef-9e12-4359-8a29-549c2cf9c826`
**Location**: Chennai (13.0827, 80.2707)
**Crops**: rice, sugarcane
**Area**: 3.0 hectares

## Testing Steps

### 1. View Farmer List
1. Go to: http://localhost:3000/farmers
2. You should see 3 farmers listed
3. Click the eye icon on any farmer

### 2. View Farmer Details
1. You should see:
   - Farmer information (phone, language, timezone)
   - Two action buttons: "Generate Advisory" and "Make Voice Call"
   - Farm plots section (placeholder)
   - Recent Advisories section (shows existing advisories or "No advisories yet")

### 3. Generate Advisory
1. Click the "Generate Advisory" button
2. Wait 10-15 seconds (fetching satellite and weather data)
3. You should see a success message: "Advisory generated successfully!"
4. The "Recent Advisories" section will automatically refresh and show the new advisory
5. Advisory details include:
   - Date created
   - Stress type (with colored chip)
   - Urgency level (with colored chip: CRITICAL=red, HIGH=orange, MEDIUM=blue, LOW=gray)
   - List of recommended actions with timing
   - Expiration date

### 4. View Advisory Details
The advisories table shows:
- **Date**: When the advisory was created
- **Stress Type**: Type of crop stress detected (WATER STRESS, HEAT STRESS, GENERAL STRESS)
- **Urgency**: Priority level (CRITICAL, HIGH, MEDIUM, LOW)
- **Actions**: Recommended actions with timing (e.g., "Monitor crop health (within 24 hours)")
- **Expires**: When the advisory expires (7 days from creation)

### 5. Make Voice Call
1. Click the "Make Voice Call" button
2. You should see: "Voice call initiated! The farmer will receive a call shortly."
3. The farmer's phone will receive a call
4. The call will deliver the advisory in Hindi

## API Endpoints (for manual testing)

### List Farmers
```bash
curl http://localhost:8000/api/v1/farmers/
```

### Get Specific Farmer
```bash
curl http://localhost:8000/api/v1/farmers/fc008579-7fcb-4f31-8ab8-837ef8d44f83
```

### Generate Advisory (Farmer 1)
```bash
curl -X POST http://localhost:8000/api/v1/advisories/generate/fc008579-7fcb-4f31-8ab8-837ef8d44f83
```

### Generate Advisory (Farmer 2)
```bash
curl -X POST http://localhost:8000/api/v1/advisories/generate/aa25b281-8515-4be1-a8de-25b244b403b5
```

### List Advisories for Farmer
```bash
curl http://localhost:8000/api/v1/advisories/farmer/fc008579-7fcb-4f31-8ab8-837ef8d44f83
```

### Initiate Voice Call
```bash
curl -X POST http://localhost:8000/api/v1/voice/call/fc008579-7fcb-4f31-8ab8-837ef8d44f83
```

## Known Issues Fixed
1. ✅ Advisory model mismatch - Fixed field names (farm_plot_id vs plot_id)
2. ✅ Missing plots - Created test plots for both farmers
3. ✅ Voice call endpoint - Added /voice/call/{farmer_id} endpoint
4. ✅ Advisory display - Added advisories table to farmer detail page
5. ✅ Auto-refresh - Advisories list refreshes after generating new advisory

## Features Implemented
- ✅ Generate advisories based on satellite and weather data
- ✅ Display advisories in a table with color-coded urgency levels
- ✅ Show recommended actions with timing and costs
- ✅ Initiate voice calls to deliver advisories
- ✅ Auto-refresh advisories after generation
- ✅ Error messages with details when generation fails

## Next Steps
- Add plot information display on farmer detail page
- Add advisory detail view (click to see full advisory text)
- Add filtering/sorting for advisories
- Add pagination for large advisory lists
- Test with multiple farmers and plots
- Add error handling for edge cases
