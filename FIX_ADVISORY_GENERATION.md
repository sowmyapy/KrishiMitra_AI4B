# Fix Advisory Generation - Missing Dependencies

## Issue
Backend crashed when trying to generate advisory with the new NDVI calculation code.

## Root Cause
Missing Python packages:
- `numpy` - for array calculations
- `Pillow` (PIL) - for image processing

## Solution

### Option 1: Install Missing Packages (Recommended)
```bash
# Activate virtual environment
.\venv\Scripts\activate

# Install required packages
pip install numpy Pillow

# Restart backend
python -m uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

### Option 2: Use Simplified Version (Temporary)
If you want to test immediately without installing packages, I can provide a simplified version that:
- Uses location-based NDVI simulation (different for each farmer)
- Uses weather data for differentiation
- Doesn't require numpy/Pillow

## Why Advisories Were the Same Before

The old code had:
```python
# Hardcoded NDVI - same for everyone!
ndvi_mean = 0.55

# Simple logic - same result
stress_type = "general_stress"
risk_score = 75.0
```

## New Enhanced Logic

The new code:
1. **Calculates actual NDVI** from satellite imagery
2. **Uses location-specific data** (Bangalore vs Chennai have different conditions)
3. **Considers crop types** (rice vs wheat have different needs)
4. **Uses weather data** (temperature, humidity)
5. **Generates specific recommendations** based on stress level

## Expected Results After Fix

### Farmer 1 (Bangalore - wheat, rice)
- Location: 12.9716, 77.5946
- Expected NDVI: ~0.55-0.60 (inland, better vegetation)
- Weather: Moderate temperature
- Advisory: Likely "general_stress" or "healthy"

### Farmer 2 (Chennai - rice, sugarcane)
- Location: 13.0827, 80.2707
- Expected NDVI: ~0.45-0.50 (coastal, drier)
- Weather: Higher temperature, lower humidity
- Advisory: Likely "moderate_stress" or "water_stress"

## Next Steps

1. Install numpy and Pillow
2. Restart backend
3. Generate advisories for both farmers
4. Compare the different recommendations
