# How to Restart the Backend

## The backend crashed because of the code changes. Here's how to restart it:

### Step 1: Open a new terminal/PowerShell

### Step 2: Navigate to project directory
```bash
cd C:\Users\Sowmya\OneDrive\projects\ai_crop_system
```

### Step 3: Activate virtual environment
```bash
.\venv\Scripts\activate
```

### Step 4: Start the backend
```bash
python -m uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

## What Changed?

The advisory generation now:
1. **Uses location-based NDVI simulation** (different for Bangalore vs Chennai)
2. **Considers crop types** (rice needs more humidity, wheat prefers cooler temps)
3. **Uses actual weather data** for each location
4. **Generates specific recommendations** based on stress level

## Expected Results

### Farmer 1 (Bangalore - wheat, rice)
- Location: 12.9716, 77.5946
- Simulated NDVI: ~0.53-0.63 (inland, better vegetation)
- Advisory: Likely "healthy" or "general_stress"
- Recommendations: Regular monitoring, less urgent actions

### Farmer 2 (Chennai - rice, sugarcane)  
- Location: 13.0827, 80.2707
- Simulated NDVI: ~0.42-0.52 (coastal, drier)
- Advisory: Likely "moderate_stress" or "water_stress"
- Recommendations: More urgent irrigation, higher risk score

## Test After Restart

1. Go to: http://localhost:3000/farmers
2. Click eye icon on Bangalore farmer (+918151910856)
3. Generate advisory - note the NDVI and recommendations
4. Go back and click eye icon on Chennai farmer (+918095666788)
5. Generate advisory - should be DIFFERENT from Bangalore farmer
6. Compare:
   - Different NDVI values
   - Different stress types
   - Different risk scores
   - Different recommendations

## Optional: Install numpy and Pillow for Real NDVI

If you want to use actual satellite data instead of simulation:

```bash
# In activated virtual environment
pip install numpy Pillow

# Restart backend
python -m uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

This will calculate real NDVI from Sentinel-2 satellite imagery!
