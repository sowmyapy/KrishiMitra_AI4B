# Dataset Recommendations for KrishiMitra

## Current Issue
Both farmers get the same advisory because:
- NDVI is hardcoded to `0.55` instead of calculated from satellite data
- Weather data is fetched but not fully utilized in decision logic
- No historical data or crop-specific models

## Recommended Datasets

### 1. Satellite Imagery (Already Integrated)
**Source**: Sentinel Hub (Sentinel-2)
**Current Status**: ✅ Integrated but not fully utilized
**Data Available**:
- NDVI (Normalized Difference Vegetation Index)
- Moisture Index (SWIR bands)
- RGB imagery
- 10m resolution
- 5-day revisit time

**How to Use Better**:
```python
# Calculate actual NDVI from satellite data
import numpy as np
from PIL import Image
import io

# Parse TIFF data
image = Image.open(io.BytesIO(satellite_data['data']))
ndvi_array = np.array(image)[:, :, 0]  # First band is NDVI
ndvi_mean = np.mean(ndvi_array)
ndvi_std = np.std(ndvi_array)
ndvi_min = np.min(ndvi_array)
ndvi_max = np.max(ndvi_array)
```

### 2. Weather Data (Already Integrated)
**Source**: OpenWeatherMap
**Current Status**: ✅ Integrated
**Data Available**:
- Temperature
- Humidity
- Precipitation
- Wind speed
- Pressure

**Enhancement**: Add historical weather data for trend analysis

### 3. Soil Data
**Source**: SoilGrids (https://soilgrids.org/)
**API**: REST API available
**Data Available**:
- Soil pH
- Organic carbon content
- Bulk density
- Clay/Sand/Silt content
- Cation exchange capacity
- 250m resolution

**Integration Example**:
```python
async def fetch_soil_data(lat: float, lon: float):
    url = f"https://rest.isric.org/soilgrids/v2.0/properties/query"
    params = {
        "lon": lon,
        "lat": lat,
        "property": ["phh2o", "soc", "clay", "sand"],
        "depth": ["0-5cm", "5-15cm"],
        "value": "mean"
    }
    # Returns soil properties for the location
```

### 4. Crop-Specific Data
**Source**: FAO Crop Calendar (http://www.fao.org/agriculture/seed/cropcalendar/)
**Data Available**:
- Planting dates by region
- Growing seasons
- Harvest periods
- Crop water requirements
- Suitable temperature ranges

**Use Case**: Validate farmer's planting dates and provide season-specific advice

### 5. Historical Crop Yield Data
**Source**: 
- **India**: ICRISAT (https://data.icrisat.org/)
- **Global**: FAO STAT (https://www.fao.org/faostat/)

**Data Available**:
- District-level crop yields
- Production statistics
- Area under cultivation
- Historical trends

**Use Case**: Benchmark farmer's expected yield against regional averages

### 6. Pest and Disease Data
**Source**: 
- **India**: ICAR (Indian Council of Agricultural Research)
- **Global**: CABI Crop Protection Compendium

**Data Available**:
- Common pests by crop and region
- Disease outbreak patterns
- Seasonal pest activity
- Treatment recommendations

**Use Case**: Predict pest/disease risk based on weather and crop stage

### 7. Market Price Data
**Source**: 
- **India**: Agmarknet (https://agmarknet.gov.in/)
- **API**: Available through government portals

**Data Available**:
- Daily mandi prices
- Commodity trends
- Demand forecasts

**Use Case**: Advise farmers on optimal harvest timing for better prices

### 8. Irrigation Data
**Source**: 
- **India**: India-WRIS (Water Resources Information System)
- **Global**: FAO AQUASTAT

**Data Available**:
- Groundwater levels
- Reservoir storage
- Irrigation infrastructure
- Water availability

**Use Case**: Provide water-saving irrigation schedules

## Implementation Priority

### Phase 1: Fix Current Issues (Immediate)
1. ✅ Calculate actual NDVI from satellite data
2. ✅ Use weather data more effectively
3. ✅ Add crop-specific thresholds

### Phase 2: Add Core Datasets (1-2 weeks)
1. Soil data integration (SoilGrids)
2. Historical weather trends
3. Crop calendar validation

### Phase 3: Advanced Features (1 month)
1. Pest/disease prediction models
2. Market price integration
3. Yield forecasting

### Phase 4: ML Models (2-3 months)
1. Train crop-specific stress detection models
2. Personalized recommendations based on farmer history
3. Predictive analytics for optimal interventions

## Sample Enhanced Advisory Logic

```python
# Enhanced decision logic using multiple data sources
def generate_enhanced_advisory(
    ndvi_mean: float,
    ndvi_trend: float,  # Change over last 2 weeks
    temperature: float,
    humidity: float,
    rainfall: float,
    soil_moisture: float,
    crop_type: str,
    crop_stage: str,
    soil_ph: float,
    historical_yield: float
):
    advisories = []
    risk_score = 0
    
    # NDVI-based stress detection
    if ndvi_mean < 0.4:
        risk_score += 30
        advisories.append({
            "type": "severe_stress",
            "action": "Immediate irrigation and nutrient check",
            "priority": 1
        })
    elif ndvi_mean < 0.6 and ndvi_trend < -0.05:
        risk_score += 20
        advisories.append({
            "type": "declining_health",
            "action": "Monitor closely, prepare for intervention",
            "priority": 2
        })
    
    # Weather-based recommendations
    if temperature > 35 and humidity < 30:
        risk_score += 25
        advisories.append({
            "type": "heat_stress",
            "action": "Increase irrigation frequency, apply mulch",
            "priority": 1
        })
    
    # Soil-based recommendations
    if soil_ph < 5.5 or soil_ph > 8.0:
        risk_score += 15
        advisories.append({
            "type": "soil_imbalance",
            "action": f"Adjust soil pH (current: {soil_ph})",
            "priority": 3
        })
    
    # Crop stage-specific advice
    if crop_stage == "flowering" and rainfall < 10:
        risk_score += 20
        advisories.append({
            "type": "critical_stage_water",
            "action": "Critical stage - ensure adequate water",
            "priority": 1
        })
    
    return {
        "risk_score": min(risk_score, 100),
        "advisories": sorted(advisories, key=lambda x: x["priority"])
    }
```

## Data Storage Strategy

### Option 1: PostgreSQL with PostGIS (Recommended)
- Store spatial data efficiently
- Support for geospatial queries
- Good for historical data

### Option 2: TimescaleDB
- Optimized for time-series data
- Perfect for weather and NDVI trends
- Built on PostgreSQL

### Option 3: Hybrid Approach
- PostgreSQL for structured data (farmers, plots, advisories)
- S3 for satellite imagery
- Redis for caching frequently accessed data
- TimescaleDB for time-series analytics

## Cost Optimization

### Free/Low-Cost Data Sources
1. ✅ Sentinel Hub - Free tier: 30,000 requests/month
2. ✅ OpenWeatherMap - Free tier: 1,000 calls/day
3. ✅ SoilGrids - Free REST API
4. ✅ FAO Data - Free public datasets
5. ✅ Agmarknet - Free government data

### Caching Strategy
- Cache satellite data for 5 days (Sentinel-2 revisit time)
- Cache weather data for 1 hour
- Cache soil data indefinitely (rarely changes)
- Cache crop calendar data for season

## Next Steps

1. **Immediate**: Fix NDVI calculation in `src/api/advisories.py`
2. **This Week**: Add soil data integration
3. **Next Week**: Implement crop-specific thresholds
4. **Month 1**: Build ML models for stress prediction
5. **Month 2**: Add market price integration
6. **Month 3**: Deploy predictive analytics

## Sample Dataset Integration Code

See `DATASET_INTEGRATION_EXAMPLES.md` for complete code examples of:
- Soil data fetching
- Historical weather analysis
- Crop calendar validation
- Market price integration
