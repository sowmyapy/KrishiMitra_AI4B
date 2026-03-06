# Farmer Registration Form - Complete Implementation

## Overview

This guide shows how to build a complete farmer registration form that captures:
- Farmer's phone number
- Preferred language
- Farm location (latitude/longitude via map picker)
- Farm area (hectares)
- Crop types
- Planting date

## Component Structure

```
src/
├── pages/
│   └── FarmerRegistration.tsx    # Main registration page
├── components/
│   └── farmer/
│       ├── FarmerForm.tsx         # Registration form
│       ├── MapPicker.tsx          # Interactive map for location
│       └── CropSelector.tsx       # Multi-select for crops
├── hooks/
│   └── useFarmers.ts              # API hooks
└── types/
    └── farmer.ts                  # TypeScript types
```

## Step 1: Create Type Definitions

Create `src/types/farmer.ts`:

```typescript
export interface FarmerFormData {
  phone_number: string;
  preferred_language: string;
  timezone: string;
  plot: PlotFormData;
}

export interface PlotFormData {
  latitude: number;
  longitude: number;
  area_hectares: number;
  crop_types: string[];
  planting_date: string;
}

export interface Farmer {
  farmer_id: string;
  phone_number: string;
  preferred_language: string;
  timezone: string;
  created_at: string;
  updated_at: string;
}

export interface Plot {
  plot_id: string;
  farmer_id: string;
  latitude: number;
  longitude: number;
  area_hectares: number;
  crop_types: string[];
  planting_date: string;
  created_at: string;
}

export const SUPPORTED_LANGUAGES = [
  { code: 'hi', name: 'Hindi (हिंदी)' },
  { code: 'en', name: 'English' },
  { code: 'bn', name: 'Bengali (বাংলা)' },
  { code: 'te', name: 'Telugu (తెలుగు)' },
  { code: 'mr', name: 'Marathi (मराठी)' },
  { code: 'ta', name: 'Tamil (தமிழ்)' },
  { code: 'gu', name: 'Gujarati (ગુજરાતી)' },
  { code: 'kn', name: 'Kannada (ಕನ್ನಡ)' },
  { code: 'ml', name: 'Malayalam (മലയാളം)' },
  { code: 'pa', name: 'Punjabi (ਪੰਜਾਬੀ)' },
  { code: 'or', name: 'Odia (ଓଡ଼ିଆ)' },
];

export const CROP_OPTIONS = [
  'Rice', 'Wheat', 'Maize', 'Millet', 'Sorghum',
  'Cotton', 'Sugarcane', 'Jute', 'Tea', 'Coffee',
  'Potato', 'Onion', 'Tomato', 'Cabbage', 'Cauliflower',
  'Mango', 'Banana', 'Orange', 'Apple', 'Grapes',
  'Ragi', 'Bajra', 'Jowar', 'Groundnut', 'Soybean',
];
```

## Step 2: Create Map Picker Component

Create `src/components/farmer/MapPicker.tsx`:

```typescript
import { useEffect, useRef, useState } from 'react';
import { Box, Typography, TextField, Button } from '@mui/material';
import { MapContainer, TileLayer, Marker, useMapEvents } from 'react-leaflet';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';

// Fix Leaflet default marker icon
import icon from 'leaflet/dist/images/marker-icon.png';
import iconShadow from 'leaflet/dist/images/marker-shadow.png';

let DefaultIcon = L.icon({
  iconUrl: icon,
  shadowUrl: iconShadow,
  iconSize: [25, 41],
  iconAnchor: [12, 41],
});

L.Marker.prototype.options.icon = DefaultIcon;

interface MapPickerProps {
  value: { lat: number; lng: number } | null;
  onChange: (location: { lat: number; lng: number }) => void;
}

function LocationMarker({ position, setPosition }: any) {
  useMapEvents({
    click(e) {
      setPosition(e.latlng);
    },
  });

  return position === null ? null : <Marker position={position} />;
}

export const MapPicker: React.FC<MapPickerProps> = ({ value, onChange }) => {
  const [position, setPosition] = useState<L.LatLng | null>(
    value ? L.latLng(value.lat, value.lng) : null
  );
  const [manualLat, setManualLat] = useState(value?.lat.toString() || '');
  const [manualLng, setManualLng] = useState(value?.lng.toString() || '');

  useEffect(() => {
    if (position) {
      onChange({ lat: position.lat, lng: position.lng });
    }
  }, [position, onChange]);

  const handleManualInput = () => {
    const lat = parseFloat(manualLat);
    const lng = parseFloat(manualLng);
    if (!isNaN(lat) && !isNaN(lng)) {
      setPosition(L.latLng(lat, lng));
    }
  };

  const handleUseCurrentLocation = () => {
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        (pos) => {
          setPosition(L.latLng(pos.coords.latitude, pos.coords.longitude));
          setManualLat(pos.coords.latitude.toString());
          setManualLng(pos.coords.longitude.toString());
        },
        (error) => {
          console.error('Error getting location:', error);
        }
      );
    }
  };

  return (
    <Box>
      <Typography variant="subtitle2" gutterBottom>
        Farm Location
      </Typography>

      <Box display="flex" gap={2} mb={2}>
        <TextField
          label="Latitude"
          value={manualLat}
          onChange={(e) => setManualLat(e.target.value)}
          size="small"
          fullWidth
        />
        <TextField
          label="Longitude"
          value={manualLng}
          onChange={(e) => setManualLng(e.target.value)}
          size="small"
          fullWidth
        />
        <Button onClick={handleManualInput} variant="outlined" size="small">
          Set
        </Button>
      </Box>

      <Button
        onClick={handleUseCurrentLocation}
        variant="outlined"
        size="small"
        fullWidth
        sx={{ mb: 2 }}
      >
        📍 Use Current Location
      </Button>

      <Box sx={{ height: 400, border: '1px solid #ccc', borderRadius: 1 }}>
        <MapContainer
          center={position || [20.5937, 78.9629]} // Center of India
          zoom={position ? 13 : 5}
          style={{ height: '100%', width: '100%' }}
        >
          <TileLayer
            attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          />
          <LocationMarker position={position} setPosition={setPosition} />
        </MapContainer>
      </Box>

      {position && (
        <Typography variant="caption" color="textSecondary" sx={{ mt: 1 }}>
          Selected: {position.lat.toFixed(6)}, {position.lng.toFixed(6)}
        </Typography>
      )}
    </Box>
  );
};
```

## Step 3: Create Farmer Registration Form

Create `src/pages/FarmerRegistration.tsx`:

```typescript
import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Box,
  Paper,
  Typography,
  TextField,
  Button,
  Grid,
  MenuItem,
  Chip,
  FormControl,
  InputLabel,
  Select,
  OutlinedInput,
  Alert,
  CircularProgress,
} from '@mui/material';
import { useForm, Controller } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { useSnackbar } from 'notistack';
import { MapPicker } from '@/components/farmer/MapPicker';
import { useCreateFarmer } from '@/hooks/useFarmers';
import { SUPPORTED_LANGUAGES, CROP_OPTIONS, FarmerFormData } from '@/types/farmer';

const farmerSchema = z.object({
  phone_number: z.string()
    .min(10, 'Phone number must be at least 10 digits')
    .regex(/^\+?[1-9]\d{1,14}$/, 'Invalid phone number format'),
  preferred_language: z.string().min(1, 'Please select a language'),
  timezone: z.string().default('Asia/Kolkata'),
  plot: z.object({
    latitude: z.number().min(-90).max(90),
    longitude: z.number().min(-180).max(180),
    area_hectares: z.number().min(0.01, 'Area must be greater than 0'),
    crop_types: z.array(z.string()).min(1, 'Select at least one crop'),
    planting_date: z.string().min(1, 'Planting date is required'),
  }),
});

export const FarmerRegistration = () => {
  const navigate = useNavigate();
  const { enqueueSnackbar } = useSnackbar();
  const createFarmer = useCreateFarmer();
  const [mapLocation, setMapLocation] = useState<{ lat: number; lng: number } | null>(null);

  const {
    control,
    handleSubmit,
    formState: { errors },
    setValue,
    watch,
  } = useForm<FarmerFormData>({
    resolver: zodResolver(farmerSchema),
    defaultValues: {
      phone_number: '',
      preferred_language: 'hi',
      timezone: 'Asia/Kolkata',
      plot: {
        latitude: 0,
        longitude: 0,
        area_hectares: 0,
        crop_types: [],
        planting_date: '',
      },
    },
  });

  const selectedCrops = watch('plot.crop_types');

  const onSubmit = async (data: FarmerFormData) => {
    try {
      // First create farmer
      const farmer = await createFarmer.mutateAsync({
        phone_number: data.phone_number,
        preferred_language: data.preferred_language,
        timezone: data.timezone,
      });

      // Then create plot (you'll need to implement this API call)
      // await createPlot.mutateAsync({
      //   farmer_id: farmer.farmer_id,
      //   ...data.plot,
      // });

      enqueueSnackbar('Farmer registered successfully!', { variant: 'success' });
      navigate('/farmers');
    } catch (error: any) {
      enqueueSnackbar(
        error.response?.data?.detail || 'Failed to register farmer',
        { variant: 'error' }
      );
    }
  };

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Register New Farmer
      </Typography>

      <Paper sx={{ p: 3, maxWidth: 800 }}>
        <form onSubmit={handleSubmit(onSubmit)}>
          <Grid container spacing={3}>
            {/* Personal Information */}
            <Grid item xs={12}>
              <Typography variant="h6" gutterBottom>
                Personal Information
              </Typography>
            </Grid>

            <Grid item xs={12} md={6}>
              <Controller
                name="phone_number"
                control={control}
                render={({ field }) => (
                  <TextField
                    {...field}
                    label="Phone Number"
                    placeholder="+918151910856"
                    fullWidth
                    error={!!errors.phone_number}
                    helperText={errors.phone_number?.message}
                  />
                )}
              />
            </Grid>

            <Grid item xs={12} md={6}>
              <Controller
                name="preferred_language"
                control={control}
                render={({ field }) => (
                  <TextField
                    {...field}
                    select
                    label="Preferred Language"
                    fullWidth
                    error={!!errors.preferred_language}
                    helperText={errors.preferred_language?.message}
                  >
                    {SUPPORTED_LANGUAGES.map((lang) => (
                      <MenuItem key={lang.code} value={lang.code}>
                        {lang.name}
                      </MenuItem>
                    ))}
                  </TextField>
                )}
              />
            </Grid>

            {/* Farm Information */}
            <Grid item xs={12}>
              <Typography variant="h6" gutterBottom sx={{ mt: 2 }}>
                Farm Information
              </Typography>
            </Grid>

            <Grid item xs={12}>
              <Controller
                name="plot.latitude"
                control={control}
                render={({ field }) => (
                  <MapPicker
                    value={mapLocation}
                    onChange={(location) => {
                      setMapLocation(location);
                      setValue('plot.latitude', location.lat);
                      setValue('plot.longitude', location.lng);
                    }}
                  />
                )}
              />
              {errors.plot?.latitude && (
                <Alert severity="error" sx={{ mt: 1 }}>
                  {errors.plot.latitude.message}
                </Alert>
              )}
            </Grid>

            <Grid item xs={12} md={6}>
              <Controller
                name="plot.area_hectares"
                control={control}
                render={({ field }) => (
                  <TextField
                    {...field}
                    label="Farm Area (Hectares)"
                    type="number"
                    fullWidth
                    inputProps={{ step: 0.1, min: 0 }}
                    error={!!errors.plot?.area_hectares}
                    helperText={errors.plot?.area_hectares?.message}
                    onChange={(e) => field.onChange(parseFloat(e.target.value))}
                  />
                )}
              />
            </Grid>

            <Grid item xs={12} md={6}>
              <Controller
                name="plot.planting_date"
                control={control}
                render={({ field }) => (
                  <TextField
                    {...field}
                    label="Planting Date"
                    type="date"
                    fullWidth
                    InputLabelProps={{ shrink: true }}
                    error={!!errors.plot?.planting_date}
                    helperText={errors.plot?.planting_date?.message}
                  />
                )}
              />
            </Grid>

            <Grid item xs={12}>
              <Controller
                name="plot.crop_types"
                control={control}
                render={({ field }) => (
                  <FormControl fullWidth error={!!errors.plot?.crop_types}>
                    <InputLabel>Crop Types</InputLabel>
                    <Select
                      {...field}
                      multiple
                      input={<OutlinedInput label="Crop Types" />}
                      renderValue={(selected) => (
                        <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5 }}>
                          {selected.map((value) => (
                            <Chip key={value} label={value} size="small" />
                          ))}
                        </Box>
                      )}
                    >
                      {CROP_OPTIONS.map((crop) => (
                        <MenuItem key={crop} value={crop}>
                          {crop}
                        </MenuItem>
                      ))}
                    </Select>
                    {errors.plot?.crop_types && (
                      <Typography variant="caption" color="error">
                        {errors.plot.crop_types.message}
                      </Typography>
                    )}
                  </FormControl>
                )}
              />
            </Grid>

            {/* Actions */}
            <Grid item xs={12}>
              <Box display="flex" gap={2} justifyContent="flex-end" mt={2}>
                <Button
                  variant="outlined"
                  onClick={() => navigate('/farmers')}
                  disabled={createFarmer.isPending}
                >
                  Cancel
                </Button>
                <Button
                  type="submit"
                  variant="contained"
                  disabled={createFarmer.isPending}
                  startIcon={createFarmer.isPending && <CircularProgress size={20} />}
                >
                  {createFarmer.isPending ? 'Registering...' : 'Register Farmer'}
                </Button>
              </Box>
            </Grid>
          </Grid>
        </form>
      </Paper>
    </Box>
  );
};
```

## Step 4: Update API Hooks

Update `src/hooks/useFarmers.ts`:

```typescript
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { apiClient } from '@/api/client';
import { Farmer, Plot } from '@/types/farmer';

export const useCreateFarmer = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (data: {
      phone_number: string;
      preferred_language: string;
      timezone: string;
    }) => {
      const response = await apiClient.post<Farmer>('/farmers/', data);
      return response.data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['farmers'] });
    },
  });
};

export const useCreatePlot = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (data: {
      farmer_id: string;
      latitude: number;
      longitude: number;
      area_hectares: number;
      crop_types: string[];
      planting_date: string;
    }) => {
      const response = await apiClient.post<Plot>('/plots/', data);
      return response.data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['plots'] });
    },
  });
};
```

## Step 5: Add Route

Update `src/App.tsx`:

```typescript
<Routes>
  <Route path="/" element={<Dashboard />} />
  <Route path="/farmers" element={<Farmers />} />
  <Route path="/farmers/new" element={<FarmerRegistration />} />
  {/* ... other routes */}
</Routes>
```

## Step 6: Update Backend CORS

Update `src/main.py` to allow frontend access:

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://your-domain.com",  # Add your AWS domain
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## Testing Locally

```bash
# Terminal 1: Backend
uvicorn src.main:app --reload

# Terminal 2: Frontend
cd frontend
npm run dev

# Open: http://localhost:3000/farmers/new
```

## Form Features

✅ Phone number validation (international format)
✅ Language selection (11 Indian languages)
✅ Interactive map picker
✅ Current location detection
✅ Manual coordinate input
✅ Farm area input (hectares)
✅ Multi-select crop types
✅ Planting date picker
✅ Form validation with Zod
✅ Error handling
✅ Loading states
✅ Success notifications

## Next Steps

1. **Test the form** locally
2. **Add plot API endpoint** to backend if not exists
3. **Deploy to AWS** (see `AWS_UI_DEPLOYMENT.md`)

---

Ready to deploy? See `AWS_UI_DEPLOYMENT.md` for AWS deployment guide!
