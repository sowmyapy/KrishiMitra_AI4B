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
import { useCreateFarmer, useCreatePlot } from '@/hooks/useFarmers';
import { SUPPORTED_LANGUAGES, CROP_OPTIONS } from '@/types/farmer';
import type { FarmerFormData } from '@/types/farmer';

const farmerSchema = z.object({
  phone_number: z.string()
    .min(10, 'Phone number must be at least 10 digits')
    .regex(/^\+?[1-9]\d{1,14}$/, 'Invalid phone number format (use +918151910856)'),
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
  const createPlot = useCreatePlot();
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
        // Still navigate to farmers list since farmer was created
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
                    error={errors.plot?.latitude?.message}
                  />
                )}
              />
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
                  disabled={createFarmer.isPending || createPlot.isPending}
                >
                  Cancel
                </Button>
                <Button
                  type="submit"
                  variant="contained"
                  disabled={createFarmer.isPending || createPlot.isPending}
                  startIcon={(createFarmer.isPending || createPlot.isPending) && <CircularProgress size={20} />}
                >
                  {(createFarmer.isPending || createPlot.isPending) ? 'Registering...' : 'Register Farmer'}
                </Button>
              </Box>
            </Grid>
          </Grid>
        </form>
      </Paper>
    </Box>
  );
};
