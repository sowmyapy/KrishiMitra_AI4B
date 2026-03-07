import { useState, useEffect } from 'react';
import { getApiUrl } from '@/api/client';
import {
  Box,
  Typography,
  Card,
  CardContent,
  Grid,
  CircularProgress,
  Alert,
  Chip,
  List,
  ListItem,
  ListItemText,
  Divider,
} from '@mui/material';
import { LocationOn, Satellite } from '@mui/icons-material';

interface PlotData {
  farmer_id: string;
  phone_number: string;
  latitude: number;
  longitude: number;
  health_status: string;
  ndvi: number;
}

export const AdvancedMonitoring = () => {
  const [plots, setPlots] = useState<PlotData[]>([]);
  const [loading, setLoading] = useState(true);
  const [selectedPlot, setSelectedPlot] = useState<PlotData | null>(null);

  useEffect(() => {
    fetchPlotData();
  }, []);

  const fetchPlotData = async () => {
    setLoading(true);
    try {
      const farmersResponse = await fetch(getApiUrl('/api/v1/farmers/'));
      const farmers = await farmersResponse.json();

      const plotData: PlotData[] = [];
      
      for (const farmer of farmers) {
        // Simulated plot locations (in real app, fetch from backend)
        const advisoriesResponse = await fetch(
            getApiUrl(`/api/v1/advisories/farmer/${farmer.farmer_id}`)
        );
        
        let healthStatus = 'unknown';
        let ndvi = 0.5;
        
        if (advisoriesResponse.ok) {
          const advisories = await advisoriesResponse.json();
          if (advisories.length > 0) {
            const latest = advisories[0];
            healthStatus = latest.stress_type;
            // Simulate NDVI based on health
            ndvi = healthStatus === 'healthy' ? 0.7 : 
                   healthStatus.includes('severe') ? 0.3 : 0.5;
          }
        }

        // Use simulated coordinates (Bangalore area)
        plotData.push({
          farmer_id: farmer.farmer_id,
          phone_number: farmer.phone_number,
          latitude: 12.9716 + (Math.random() - 0.5) * 0.1,
          longitude: 77.5946 + (Math.random() - 0.5) * 0.1,
          health_status: healthStatus,
          ndvi: ndvi,
        });
      }

      setPlots(plotData);
      if (plotData.length > 0) {
        setSelectedPlot(plotData[0]);
      }
    } catch (err) {
      console.error('Failed to fetch plot data', err);
    } finally {
      setLoading(false);
    }
  };

  const getHealthColor = (status: string) => {
    if (status === 'healthy') return '#4caf50';
    if (status.includes('severe') || status.includes('heat')) return '#f44336';
    if (status.includes('water')) return '#2196f3';
    if (status.includes('moderate')) return '#ff9800';
    return '#9e9e9e';
  };

  const getNDVIColor = (ndvi: number) => {
    if (ndvi > 0.6) return '#4caf50';
    if (ndvi > 0.4) return '#ff9800';
    return '#f44336';
  };

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="400px">
        <CircularProgress />
      </Box>
    );
  }

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Advanced Monitoring - Plot Locations
      </Typography>
      <Typography color="textSecondary" paragraph>
        Interactive view of farm plots with satellite data
      </Typography>

      <Grid container spacing={3}>
        {/* Map View (Simplified) */}
        <Grid item xs={12} md={8}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Plot Locations Map
              </Typography>
              <Divider sx={{ mb: 2 }} />
              
              {/* Simplified map representation */}
              <Box
                sx={{
                  height: 500,
                  backgroundColor: '#e8f5e9',
                  position: 'relative',
                  borderRadius: 1,
                  overflow: 'hidden',
                }}
              >
                {/* Grid lines */}
                <Box
                  sx={{
                    position: 'absolute',
                    top: 0,
                    left: 0,
                    right: 0,
                    bottom: 0,
                    backgroundImage: 'linear-gradient(#ccc 1px, transparent 1px), linear-gradient(90deg, #ccc 1px, transparent 1px)',
                    backgroundSize: '50px 50px',
                    opacity: 0.3,
                  }}
                />
                
                {/* Plot markers */}
                {plots.map((plot, index) => {
                  const x = ((plot.longitude - 77.54) / 0.11) * 100;
                  const y = ((12.97 - plot.latitude + 0.05) / 0.1) * 100;
                  
                  return (
                    <Box
                      key={plot.farmer_id}
                      onClick={() => setSelectedPlot(plot)}
                      sx={{
                        position: 'absolute',
                        left: `${x}%`,
                        top: `${y}%`,
                        transform: 'translate(-50%, -50%)',
                        cursor: 'pointer',
                        transition: 'all 0.3s',
                        '&:hover': {
                          transform: 'translate(-50%, -50%) scale(1.2)',
                        },
                      }}
                    >
                      <LocationOn
                        sx={{
                          fontSize: 40,
                          color: getHealthColor(plot.health_status),
                          filter: selectedPlot?.farmer_id === plot.farmer_id 
                            ? 'drop-shadow(0 0 8px rgba(0,0,0,0.5))' 
                            : 'none',
                        }}
                      />
                      <Typography
                        variant="caption"
                        sx={{
                          position: 'absolute',
                          top: -20,
                          left: '50%',
                          transform: 'translateX(-50%)',
                          backgroundColor: 'white',
                          padding: '2px 6px',
                          borderRadius: 1,
                          whiteSpace: 'nowrap',
                          fontSize: '10px',
                        }}
                      >
                        Plot {index + 1}
                      </Typography>
                    </Box>
                  );
                })}
                
                {/* Legend */}
                <Box
                  sx={{
                    position: 'absolute',
                    bottom: 16,
                    right: 16,
                    backgroundColor: 'white',
                    padding: 2,
                    borderRadius: 1,
                    boxShadow: 2,
                  }}
                >
                  <Typography variant="caption" fontWeight="bold" display="block" mb={1}>
                    Health Status
                  </Typography>
                  <Box display="flex" flexDirection="column" gap={0.5}>
                    <Box display="flex" alignItems="center" gap={1}>
                      <Box sx={{ width: 12, height: 12, backgroundColor: '#4caf50', borderRadius: '50%' }} />
                      <Typography variant="caption">Healthy</Typography>
                    </Box>
                    <Box display="flex" alignItems="center" gap={1}>
                      <Box sx={{ width: 12, height: 12, backgroundColor: '#ff9800', borderRadius: '50%' }} />
                      <Typography variant="caption">Moderate</Typography>
                    </Box>
                    <Box display="flex" alignItems="center" gap={1}>
                      <Box sx={{ width: 12, height: 12, backgroundColor: '#f44336', borderRadius: '50%' }} />
                      <Typography variant="caption">Critical</Typography>
                    </Box>
                  </Box>
                </Box>
              </Box>
            </CardContent>
          </Card>
        </Grid>

        {/* Plot Details */}
        <Grid item xs={12} md={4}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Selected Plot Details
              </Typography>
              <Divider sx={{ mb: 2 }} />
              
              {selectedPlot ? (
                <Box>
                  <Box mb={2}>
                    <Typography variant="body2" color="textSecondary">
                      Farmer
                    </Typography>
                    <Typography variant="body1">{selectedPlot.phone_number}</Typography>
                  </Box>

                  <Box mb={2}>
                    <Typography variant="body2" color="textSecondary">
                      Location
                    </Typography>
                    <Typography variant="body1">
                      {selectedPlot.latitude.toFixed(4)}, {selectedPlot.longitude.toFixed(4)}
                    </Typography>
                  </Box>

                  <Box mb={2}>
                    <Typography variant="body2" color="textSecondary">
                      Health Status
                    </Typography>
                    <Chip
                      label={selectedPlot.health_status.replace('_', ' ').toUpperCase()}
                      size="small"
                      sx={{ backgroundColor: getHealthColor(selectedPlot.health_status), color: 'white' }}
                    />
                  </Box>

                  <Box mb={2}>
                    <Typography variant="body2" color="textSecondary">
                      NDVI (Vegetation Index)
                    </Typography>
                    <Box display="flex" alignItems="center" gap={1}>
                      <Typography variant="h6">{selectedPlot.ndvi.toFixed(2)}</Typography>
                      <Chip
                        label={selectedPlot.ndvi > 0.6 ? 'Good' : selectedPlot.ndvi > 0.4 ? 'Fair' : 'Poor'}
                        size="small"
                        sx={{ backgroundColor: getNDVIColor(selectedPlot.ndvi), color: 'white' }}
                      />
                    </Box>
                  </Box>

                  <Box mb={2}>
                    <Typography variant="body2" color="textSecondary" gutterBottom>
                      Satellite Data
                    </Typography>
                    <Box display="flex" alignItems="center" gap={1}>
                      <Satellite fontSize="small" color="primary" />
                      <Typography variant="caption">
                        Last updated: {new Date().toLocaleDateString()}
                      </Typography>
                    </Box>
                  </Box>
                </Box>
              ) : (
                <Typography color="textSecondary">
                  Select a plot on the map to view details
                </Typography>
              )}
            </CardContent>
          </Card>

          {/* All Plots List */}
          <Card sx={{ mt: 2 }}>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                All Plots
              </Typography>
              <Divider sx={{ mb: 1 }} />
              <List dense>
                {plots.map((plot, index) => (
                  <ListItem
                    key={plot.farmer_id}
                    button
                    selected={selectedPlot?.farmer_id === plot.farmer_id}
                    onClick={() => setSelectedPlot(plot)}
                  >
                    <LocationOn
                      sx={{
                        mr: 1,
                        color: getHealthColor(plot.health_status),
                        fontSize: 20,
                      }}
                    />
                    <ListItemText
                      primary={`Plot ${index + 1}`}
                      secondary={plot.phone_number}
                    />
                    <Chip
                      label={plot.ndvi.toFixed(2)}
                      size="small"
                      sx={{ backgroundColor: getNDVIColor(plot.ndvi), color: 'white' }}
                    />
                  </ListItem>
                ))}
              </List>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Box>
  );
};
