# 🚀 Test Farmer Registration Fix - Quick Start

## ✅ Implementation Complete!

The farmer registration bug has been fixed. The form now creates both farmer AND plot records.

## What Changed

**Before:** Only farmer created, plot data discarded ❌
**After:** Both farmer and plot created ✅

## Quick Test (5 minutes)

### Step 1: Start Backend (if not running)

```bash
python -m uvicorn src.main:app --reload
```

### Step 2: Frontend Already Running ✅

Frontend dev server is running on http://localhost:3000

### Step 3: Test Registration

1. **Open**: http://localhost:3000/farmers/new

2. **Fill Form**:
   - Phone: `+918151910856`
   - Language: `Hindi (हिंदी)`
   - Click map to set location (or use GPS button)
   - Area: `2.5`
   - Crops: Select `Rice` and `Wheat`
   - Date: `2024-01-15`

3. **Open DevTools**: Press F12 → Network tab

4. **Submit**: Click "Register Farmer"

5. **Verify**:
   - ✅ See TWO POST requests:
     - `POST /farmers/`
     - `POST /farmers/{farmer_id}/plots`
   - ✅ Success message appears
   - ✅ Redirected to farmers list

## Expected Network Requests

### Request 1: Create Farmer
```
POST http://localhost:8000/farmers/
{
  "phone_number": "+918151910856",
  "preferred_language": "hi",
  "timezone": "Asia/Kolkata"
}
```

### Request 2: Create Plot
```
POST http://localhost:8000/farmers/{farmer_id}/plots
{
  "latitude": 28.6139,
  "longitude": 77.2090,
  "area_hectares": 2.5,
  "crop_types": ["Rice", "Wheat"],
  "planting_date": "2024-01-15"
}
```

## Troubleshooting

### Issue: 401 Unauthorized

**Cause**: Backend requires JWT authentication

**Solution**: Temporarily disable auth in backend:

Edit `src/api/farmers.py`:
```python
# Comment out auth dependencies for testing
@router.post("/", response_model=FarmerResponse)
async def create_farmer(
    farmer_data: FarmerCreate,
    db: Session = Depends(get_db),
    # current_user: dict = Depends(get_current_user)  # Comment this
):
```

### Issue: CORS Error

**Solution**: Already configured in `src/main.py` ✅

### Issue: Frontend Not Loading

**Solution**: 
```bash
cd frontend
npm run dev
```

## Database Verification

After successful registration:

```sql
-- Check farmer
SELECT * FROM farmers WHERE phone_number = '+918151910856';

-- Check plot (should exist now!)
SELECT * FROM farm_plots WHERE farmer_id = '<farmer_id_from_above>';
```

## Test Scenarios

### ✅ Happy Path
- Fill all fields → Submit → Both records created

### ⚠️ Duplicate Phone
- Use same phone twice → Error: "Phone number already registered"

### ⚠️ Invalid Data
- Empty fields → Validation errors shown
- Invalid coordinates → Error message

## Success Indicators

✅ Two POST requests in Network tab
✅ Success message: "Farmer registered successfully!"
✅ Redirected to /farmers list
✅ Both farmer and plot in database

## Files Changed

- `frontend/src/hooks/useFarmers.ts` - Added useCreatePlot hook
- `frontend/src/pages/FarmerRegistration.tsx` - Sequential API calls

## Documentation

- **Complete Guide**: `FARMER_REGISTRATION_FIX_COMPLETE.md`
- **Verification Steps**: `FARMER_REGISTRATION_FIX_VERIFICATION.md`
- **Spec Files**: `.kiro/specs/complete-farmer-registration-flow/`

## Status

🎉 **Ready to Test!**

The fix is implemented and the dev server is running. Just open http://localhost:3000/farmers/new and test the registration flow!

---

**Need Help?** Check `FARMER_REGISTRATION_FIX_COMPLETE.md` for detailed information.
