# Bugfix Requirements Document

## Introduction

The farmer registration form in the UI collects complete farmer and plot data but only creates the farmer record upon submission. The plot data (latitude, longitude, area_hectares, crop_types, planting_date) is collected from the user but never sent to the backend, resulting in farmers being created without their associated plots. This breaks the registration flow and leaves the system in an incomplete state.

## Bug Analysis

### Current Behavior (Defect)

1.1 WHEN a user submits the registration form with complete farmer and plot data THEN the system only sends farmer data (phone_number, preferred_language, timezone) to POST /farmers/ and discards the plot data

1.2 WHEN the farmer is successfully created THEN the system does not make a subsequent API call to POST /farmers/{farmer_id}/plots with the collected plot data

1.3 WHEN the registration completes THEN the farmer record exists in the database but has no associated plot records despite the user providing plot information

### Expected Behavior (Correct)

2.1 WHEN a user submits the registration form with complete farmer and plot data THEN the system SHALL first create the farmer via POST /farmers/ and then automatically create the plot via POST /farmers/{farmer_id}/plots using the collected plot data

2.2 WHEN the farmer creation succeeds THEN the system SHALL immediately submit the plot data (latitude, longitude, area_hectares, crop_types, planting_date) to create the associated plot record

2.3 WHEN both farmer and plot are successfully created THEN the system SHALL display a success message and redirect to the farmers list with the complete registration

2.4 WHEN either the farmer creation or plot creation fails THEN the system SHALL display an appropriate error message indicating which step failed

### Unchanged Behavior (Regression Prevention)

3.1 WHEN the registration form is rendered THEN the system SHALL CONTINUE TO collect all farmer fields (phone_number, preferred_language, timezone) and plot fields (latitude, longitude, area_hectares, crop_types, planting_date)

3.2 WHEN form validation runs THEN the system SHALL CONTINUE TO validate all fields using the existing Zod schema

3.3 WHEN the MapPicker component is used THEN the system SHALL CONTINUE TO correctly capture latitude and longitude coordinates

3.4 WHEN API calls are made to farmer endpoints THEN the system SHALL CONTINUE TO include JWT authentication (Bearer token) in request headers

3.5 WHEN a user navigates to the farmers list THEN the system SHALL CONTINUE TO display all registered farmers with their details
