# Complete Farmer Registration Flow Bugfix Design

## Overview

The farmer registration form currently collects complete farmer and plot data but only creates the farmer record, discarding the plot data. This design outlines the fix to implement sequential API calls: first creating the farmer via POST /farmers/, then immediately creating the associated plot via POST /farmers/{farmer_id}/plots. The fix will be implemented in the frontend React component and React Query hooks, ensuring both records are created atomically from the user's perspective with proper error handling at each step.

## Glossary

- **Bug_Condition (C)**: The condition that triggers the bug - when a user submits the registration form with complete farmer and plot data
- **Property (P)**: The desired behavior when C(X) holds - both farmer and plot records are created successfully via sequential API calls
- **Preservation**: Existing form validation, MapPicker functionality, JWT authentication, and UI navigation that must remain unchanged
- **FarmerRegistration**: The React component in `frontend/src/pages/FarmerRegistration.tsx` that handles the registration form
- **useCreateFarmer**: The React Query hook in `frontend/src/hooks/useFarmers.ts` that handles farmer creation API calls
- **Sequential API Calls**: The pattern of making a second API call (plot creation) only after the first API call (farmer creation) succeeds, using the farmer_id from the first response
- **FarmerFormData**: The TypeScript interface containing both farmer fields (phone_number, preferred_language, timezone) and nested plot fields (latitude, longitude, area_hectares, crop_types, planting_date)

## Bug Details

### Fault Condition

The bug manifests when a user completes the registration form with all farmer and plot information and clicks the "Register Farmer" button. The `onSubmit` handler in FarmerRegistration.tsx only sends farmer data to the backend, completely ignoring the collected plot data (latitude, longitude, area_hectares, crop_types, planting_date) that exists in the form state.

**Formal Specification:**
```
FUNCTION isBugCondition(input)
  INPUT: input of type FarmerFormData
  OUTPUT: boolean
  
  RETURN input.phone_number IS_VALID
         AND input.preferred_language IS_VALID
         AND input.timezone IS_VALID
         AND input.plot.latitude IS_VALID
         AND input.plot.longitude IS_VALID
         AND input.plot.area_hectares > 0
         AND input.plot.crop_types.length > 0
         AND input.plot.planting_date IS_VALID
         AND formSubmitted = true
END FUNCTION
```

### Examples

- **Example 1**: User enters phone "+918151910856", language "hi", timezone "Asia/Kolkata", selects location (lat: 28.6139, lng: 77.2090), area 2.5 hectares, crops ["Rice", "Wheat"], planting date "2024-01-15", and submits. Expected: Both farmer and plot created. Actual: Only farmer created, plot data discarded.

- **Example 2**: User completes all form fields including map location selection via MapPicker, then clicks "Register Farmer". Expected: Farmer created with farmer_id, then plot created with that farmer_id. Actual: Only POST /farmers/ is called, plot data never sent to backend.

- **Example 3**: User fills form with multiple crops ["Cotton", "Sugarcane", "Groundnut"] and area 5.2 hectares. Expected: Plot record created with crop_types array and area_hectares. Actual: Form submission succeeds but plot table remains empty for this farmer.

- **Edge Case**: User submits form but farmer creation fails (e.g., duplicate phone number). Expected: Error displayed, no plot creation attempted. Actual: Currently works correctly (no plot call made), but after fix must ensure plot creation is not attempted when farmer creation fails.

## Expected Behavior

### Preservation Requirements

**Unchanged Behaviors:**
- Form validation using Zod schema must continue to validate all fields before submission
- MapPicker component must continue to capture and update latitude/longitude coordinates correctly
- JWT Bearer token authentication must continue to be included in all API request headers
- Form UI rendering with all farmer and plot input fields must remain unchanged
- Navigation to /farmers list page after successful registration must remain unchanged
- Error snackbar display for API failures must continue to work
- Loading state with CircularProgress during submission must continue to work
- Cancel button navigation back to /farmers must remain unchanged

**Scope:**
All inputs and interactions that do NOT involve the form submission flow should be completely unaffected by this fix. This includes:
- Form field rendering and validation
- MapPicker interaction and coordinate selection
- Crop selection dropdown with multi-select chips
- Date picker for planting date
- Language selection dropdown
- Phone number input formatting
- Real-time form validation errors

## Hypothesized Root Cause

Based on the bug description and code analysis, the root cause is clear:

1. **Incomplete onSubmit Handler**: The `onSubmit` function in FarmerRegistration.tsx (lines 67-81) only calls `createFarmer.mutateAsync()` with farmer data (phone_number, preferred_language, timezone) and completely ignores the `data.plot` object that contains all the collected plot information.

2. **Missing Plot Creation Hook**: There is no React Query hook for creating plots. The `useFarmers.ts` file only exports `useFarmers`, `useFarmer`, and `useCreateFarmer` hooks, but no `useCreatePlot` hook that would call POST /farmers/{farmer_id}/plots.

3. **No Sequential Call Logic**: The current implementation has no logic to chain API calls - it doesn't wait for the farmer creation response to get the farmer_id, then use that farmer_id to create the plot.

4. **Form Data Structure Mismatch**: While the form correctly collects plot data in the `FarmerFormData` structure with a nested `plot` object, this data is never extracted and sent to the backend plot creation endpoint.

## Correctness Properties

Property 1: Fault Condition - Complete Registration Creates Both Records

_For any_ form submission where all farmer fields (phone_number, preferred_language, timezone) and all plot fields (latitude, longitude, area_hectares, crop_types, planting_date) are valid, the fixed registration flow SHALL first create the farmer record via POST /farmers/, then immediately create the plot record via POST /farmers/{farmer_id}/plots using the returned farmer_id, resulting in both records existing in the database.

**Validates: Requirements 2.1, 2.2, 2.3**

Property 2: Preservation - Form Validation and UI Behavior

_For any_ user interaction with the registration form that does NOT involve final form submission (field editing, validation, map selection, navigation), the fixed code SHALL produce exactly the same behavior as the original code, preserving all existing form validation, MapPicker functionality, JWT authentication, and UI rendering.

**Validates: Requirements 3.1, 3.2, 3.3, 3.4, 3.5**

## Fix Implementation

### Changes Required

**File 1**: `frontend/src/hooks/useFarmers.ts`

**New Hook**: `useCreatePlot`

**Specific Changes**:
1. **Add useCreatePlot Hook**: Create a new React Query mutation hook that accepts farmer_id and plot data, calls POST /farmers/{farmer_id}/plots, and returns the created plot
   - Import PlotFormData type from @/types/farmer
   - Use useMutation with mutationFn that calls apiClient.post
   - Include farmer_id in the URL path: `/farmers/${farmerId}/plots`
   - Send plot data in request body: { latitude, longitude, area_hectares, crop_types, planting_date }
   - Invalidate ['farmers'] query cache on success to refresh farmer list

2. **Export New Hook**: Add useCreatePlot to the module exports so it can be imported in FarmerRegistration.tsx

**File 2**: `frontend/src/pages/FarmerRegistration.tsx`

**Function**: `onSubmit`

**Specific Changes**:
1. **Import useCreatePlot Hook**: Add useCreatePlot to the imports from @/hooks/useFarmers

2. **Initialize Plot Creation Hook**: Call `const createPlot = useCreatePlot()` alongside the existing createFarmer hook

3. **Implement Sequential API Calls**: Modify the onSubmit handler to:
   - First call `createFarmer.mutateAsync()` with farmer data and await the response
   - Extract farmer_id from the farmer creation response
   - Then call `createPlot.mutateAsync()` with farmer_id and plot data from `data.plot`
   - Only navigate to /farmers and show success message after BOTH calls succeed

4. **Add Error Handling for Each Step**: Wrap each API call in try-catch to display specific error messages:
   - If farmer creation fails: "Failed to create farmer: [error detail]"
   - If plot creation fails: "Farmer created but plot creation failed: [error detail]"
   - This helps users and developers understand which step failed

5. **Update Loading State**: The existing `createFarmer.isPending` check should be updated to `createFarmer.isPending || createPlot.isPending` to show loading state during both API calls

## Testing Strategy

### Validation Approach

The testing strategy follows a two-phase approach: first, surface counterexamples that demonstrate the bug on unfixed code by verifying plot data is NOT sent to the backend, then verify the fix works correctly by confirming both farmer and plot are created, and finally ensure existing form behavior is preserved.

### Exploratory Fault Condition Checking

**Goal**: Surface counterexamples that demonstrate the bug BEFORE implementing the fix. Confirm that plot data is collected but never sent to the backend.

**Test Plan**: Manually test the registration form on UNFIXED code by filling all fields, submitting, then checking the database and network requests to verify only POST /farmers/ is called and plot table remains empty.

**Test Cases**:
1. **Complete Form Submission Test**: Fill all farmer and plot fields, submit form, check browser DevTools Network tab (will show only POST /farmers/ call, no plot creation call)
2. **Database Verification Test**: After successful registration, query the farm_plots table for the created farmer_id (will return empty result set)
3. **Form Data Inspection Test**: Add console.log in onSubmit to verify data.plot contains all collected plot information (will show plot data exists in form state but is ignored)
4. **Multiple Crops Test**: Submit form with 3+ crops selected (will show crops are collected but never sent to backend)

**Expected Counterexamples**:
- Network tab shows only one POST request to /farmers/, no request to /farmers/{farmer_id}/plots
- Database query shows farmer record exists but no associated plot records
- Form state contains complete plot data but onSubmit handler only uses farmer fields

### Fix Checking

**Goal**: Verify that for all inputs where the bug condition holds (complete form submission), the fixed function produces the expected behavior (both records created).

**Pseudocode:**
```
FOR ALL input WHERE isBugCondition(input) DO
  result := onSubmit_fixed(input)
  ASSERT farmerCreated(result.farmer_id)
  ASSERT plotCreated(result.farmer_id, input.plot)
  ASSERT result.plot.farmer_id = result.farmer_id
END FOR
```

**Test Plan**: After implementing the fix, test the registration flow with various valid inputs to verify both API calls are made and both records are created.

**Test Cases**:
1. **Sequential API Calls Test**: Submit form, verify Network tab shows POST /farmers/ followed by POST /farmers/{farmer_id}/plots with correct farmer_id
2. **Database Verification Test**: After registration, query both farmers and farm_plots tables to verify both records exist with matching farmer_id
3. **Response Data Test**: Verify the plot creation request includes all collected data: latitude, longitude, area_hectares, crop_types array, planting_date
4. **Success Flow Test**: Verify success message displays and navigation to /farmers occurs only after both API calls succeed

### Preservation Checking

**Goal**: Verify that for all inputs where the bug condition does NOT hold (form interactions without submission), the fixed function produces the same result as the original function.

**Pseudocode:**
```
FOR ALL input WHERE NOT isBugCondition(input) DO
  ASSERT onSubmit_original(input) = onSubmit_fixed(input)
END FOR
```

**Testing Approach**: Property-based testing is recommended for preservation checking because:
- It generates many test cases automatically across the input domain
- It catches edge cases that manual unit tests might miss
- It provides strong guarantees that behavior is unchanged for all non-submission interactions

**Test Plan**: Observe behavior on UNFIXED code first for form validation, MapPicker, and other interactions, then verify these behaviors continue working identically after the fix.

**Test Cases**:
1. **Form Validation Preservation**: Test invalid inputs (empty phone, invalid coordinates, zero area) and verify validation errors display correctly before and after fix
2. **MapPicker Preservation**: Click map to select location, verify latitude/longitude update in form state identically before and after fix
3. **Crop Selection Preservation**: Select multiple crops, verify chips display and form state updates identically before and after fix
4. **Cancel Button Preservation**: Click Cancel button, verify navigation to /farmers works identically before and after fix
5. **Authentication Preservation**: Verify JWT token is included in Authorization header for all API calls before and after fix

### Unit Tests

- Test useCreatePlot hook calls correct endpoint with correct data structure
- Test onSubmit handler makes sequential API calls in correct order
- Test error handling displays appropriate messages for farmer creation failure vs plot creation failure
- Test loading state is active during both API calls
- Test navigation only occurs after both API calls succeed

### Property-Based Tests

- Generate random valid form data and verify both farmer and plot are created with matching farmer_id
- Generate random crop combinations (1-5 crops) and verify crop_types array is correctly sent to backend
- Generate random coordinates within valid ranges and verify latitude/longitude are correctly sent to plot endpoint
- Test that form validation continues to work across many random invalid input combinations

### Integration Tests

- Test full registration flow from form render to database record creation
- Test error recovery: if plot creation fails, verify farmer record exists and appropriate error is shown
- Test that registered farmers appear in the farmers list with their plot information
- Test that JWT authentication works for both API calls in the sequential flow
