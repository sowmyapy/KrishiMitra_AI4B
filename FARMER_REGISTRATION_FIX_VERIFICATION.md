# Farmer Registration Fix Verification

## Bug Fix Summary

Fixed the incomplete farmer registration flow where plot data was collected but never submitted to the backend.

## Changes Made

### 1. Added `useCreatePlot` Hook (`frontend/src/hooks/useFarmers.ts`)

```typescript
export const useCreatePlot = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (data: { farmerId: string; plotData: PlotFormData }) => {
      const response = await apiClient.post<Plot>(
        `/farmers/${data.farmerId}/plots`,
        {
          latitude: data.plotData.latitude,
          longitude: data.plotData.longitude,
          area_hectares: data.plotData.area_hectares,
          crop_types: data.plotData.crop_types,
          planting_date: data.plotData.planting_date,
        }
      );
      return response.data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['farmers'] });
    },
  });
};
```

### 2. Updated `FarmerRegistration` Component (`frontend/src/pages/FarmerRegistration.tsx`)

**Imported the new hook:**
```typescript
import { useCreateFarmer, useCreatePlot } from '@/hooks/useFarmers';
```

**Initialized the hook:**
```typescript
const createPlot = useCreatePlot();
```

**Implemented sequential API calls in `onSubmit`:**
```typescript
const onSubmit = async (data: FarmerFormData) => {
  try {
    // Step 1: Create farmer
    const farmer = await createFarmer.mutateAsync({
      phone_number: data.phone_number,
      preferred_language: data.preferred_language,
      timezone: data.timezone,
    });

    // Step 2: Create plot using the farmer_id from the response
    try {
      await createPlot.mutateAsync({
        farmerId: farmer.farmer_id,
        plotData: data.plot,
      });

      // Both farmer and plot created successfully
      enqueueSnackbar('Farmer registered successfully!', { variant: 'success' });
      navigate('/farmers');
    } catch (plotError: any) {
      // Farmer was created but plot creation failed
      enqueueSnackbar(
        `Farmer created but plot creation failed: ${plotError.response?.data?.detail || plotError.message}`,
        { variant: 'warning' }
      );
      navigate('/farmers');
    }
  } catch (farmerError: any) {
    // Farmer creation failed
    enqueueSnackbar(
      `Failed to create farmer: ${farmerError.response?.data?.detail || farmerError.message}`,
      { variant: 'error' }
    );
  }
};
```

**Updated loading states:**
```typescript
disabled={createFarmer.isPending || createPlot.isPending}
```

## Manual Verification Steps

### Before Fix (Bug Behavior)
1. Open browser DevTools Network tab
2. Navigate to http://localhost:3000/farmers/new
3. Fill in all form fields including plot data
4. Submit the form
5. **Observe**: Only ONE POST request to `/farmers/` is made
6. **Result**: Farmer created, but NO plot record exists

### After Fix (Expected Behavior)
1. Open browser DevTools Network tab
2. Navigate to http://localhost:3000/farmers/new
3. Fill in complete form:
   - Phone: `+918151910856`
   - Language: `Hindi (हिंदी)`
   - Click map to set location (or use GPS)
   - Area: `2.5` hectares
   - Crops: Select `Rice`, `Wheat`
   - Planting date: `2024-01-15`
4. Submit the form
5. **Observe**: TWO POST requests:
   - First: `POST /farmers/` with farmer data
   - Second: `POST /farmers/{farmer_id}/plots` with plot data
6. **Result**: Both farmer AND plot records created

## Expected API Calls

### Request 1: Create Farmer
```
POST http://localhost:8000/farmers/
Content-Type: application/json

{
  "phone_number": "+918151910856",
  "preferred_language": "hi",
  "timezone": "Asia/Kolkata"
}
```

**Response:**
```json
{
  "farmer_id": "uuid-here",
  "phone_number": "+918151910856",
  "preferred_language": "hi",
  "timezone": "Asia/Kolkata",
  "created_at": "2024-01-15T10:00:00Z"
}
```

### Request 2: Create Plot
```
POST http://localhost:8000/farmers/{farmer_id}/plots
Content-Type: application/json

{
  "latitude": 28.6139,
  "longitude": 77.2090,
  "area_hectares": 2.5,
  "crop_types": ["Rice", "Wheat"],
  "planting_date": "2024-01-15"
}
```

**Response:**
```json
{
  "plot_id": "uuid-here",
  "farmer_id": "uuid-here",
  "latitude": 28.6139,
  "longitude": 77.2090,
  "area_hectares": 2.5,
  "crop_types": ["Rice", "Wheat"],
  "planting_date": "2024-01-15",
  "created_at": "2024-01-15T10:00:01Z"
}
```

## Error Handling

### Scenario 1: Farmer Creation Fails
- **Trigger**: Duplicate phone number
- **Behavior**: Error message displayed, no plot creation attempted
- **Message**: "Failed to create farmer: Phone number already registered"

### Scenario 2: Plot Creation Fails
- **Trigger**: Invalid plot data or backend error
- **Behavior**: Farmer created, warning message displayed
- **Message**: "Farmer created but plot creation failed: [error detail]"
- **Note**: User still navigated to farmers list since farmer was created

### Scenario 3: Both Succeed
- **Behavior**: Success message displayed, navigate to farmers list
- **Message**: "Farmer registered successfully!"

## Preservation Verification

The following behaviors should remain UNCHANGED:

✅ Form validation with Zod schema
✅ MapPicker component captures lat/lng correctly
✅ Crop selection dropdown with multi-select
✅ Cancel button navigates to /farmers
✅ JWT Bearer token in Authorization header (if auth is enabled)
✅ Form fields render correctly
✅ Loading state with CircularProgress
✅ Real-time validation errors

## Database Verification

After successful registration, verify in the database:

```sql
-- Check farmer record
SELECT * FROM farmers WHERE phone_number = '+918151910856';

-- Check plot record (should exist now!)
SELECT * FROM farm_plots WHERE farmer_id = '<farmer_id_from_above>';
```

**Expected**: Both queries return records with matching `farmer_id`.

## Testing Checklist

- [ ] Backend server running on port 8000
- [ ] Frontend dev server running on port 3000
- [ ] Navigate to registration form
- [ ] Fill in all fields with valid data
- [ ] Open browser DevTools Network tab
- [ ] Submit form
- [ ] Verify TWO POST requests are made
- [ ] Verify success message appears
- [ ] Verify navigation to /farmers list
- [ ] Check database for both farmer and plot records
- [ ] Test error scenario: duplicate phone number
- [ ] Verify form validation still works
- [ ] Verify MapPicker still works
- [ ] Verify Cancel button still works

## Status

✅ **Fix Implemented**
- useCreatePlot hook created
- Sequential API calls implemented
- Error handling for each step
- Loading states updated

✅ **Code Changes Complete**
- `frontend/src/hooks/useFarmers.ts` - Added useCreatePlot hook
- `frontend/src/pages/FarmerRegistration.tsx` - Updated onSubmit handler

⏳ **Manual Testing Required**
- User should test the registration flow
- Verify both API calls are made
- Verify database records are created

## Next Steps

1. Start the backend server: `python -m uvicorn src.main:app --reload`
2. Frontend dev server should already be running on port 3000
3. Navigate to http://localhost:3000/farmers/new
4. Test the registration flow with the steps above
5. Verify in browser DevTools that both API calls are made
6. Check database to confirm both records exist

## Notes

- Authentication may be required for the API endpoints (JWT Bearer token)
- If auth is not set up, you may need to temporarily disable auth requirements in the backend
- The fix ensures plot data is no longer discarded during registration
- Error handling provides clear feedback for each step of the process
