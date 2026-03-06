import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useSnackbar } from 'notistack';
import {
  Box,
  Typography,
  Grid,
  Card,
  CardContent,
  CircularProgress,
  Alert,
  Chip,
  Divider,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Button,
  Switch,
  FormControlLabel,
} from '@mui/material';
import {
  WbSunny,
  Opacity,
  Thermostat,
  Air,
  Grass,
  Map,
  PlayArrow,
  Stop,
  Refresh,
} from '@mui/icons-material';

interface FarmerMonitoring {
  farmer_id: string;
  phone_number: string;
  plot_count: number;
  latest_advisory: any;
  health_status: string;
}

interface MonitoringStatus {
  is_running: boolean;
  check_interval_seconds: number;
  risk_threshold: number;
  call_threshold: number;
  stats: {
    started_at: string;
    last_check: string | null;
    total_checks: number;
    farmers_monitored: number;
    advisories_generated: number;
    calls_made: number;
    errors: number;
  };
}

export const Monitoring = () => {
  const navigate = useNavigate();
  const { enqueueSnackbar } = useSnackbar();
  const [monitoring, setMonitoring] = useState<FarmerMonitoring[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [weatherData, setWeatherData] = useState<any>(null);
  const [monitoringStatus, setMonitoringStatus] = useState<MonitoringStatus | null>(null);
  const [statusLoading, setStatusLoading] = useState(false);

  useEffect(() => {
    fetchMonitoringData();
    fetchWeatherData();
    fetchMonitoringStatus();
  }, []);

  const fetchMonitoringStatus = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/v1/monitoring/status');
      if (response.ok) {
        const data = await response.json();
        setMonitoringStatus(data);
      }
    } catch (err) {
      console.error('Failed to fetch monitoring status', err);
    }
  };

  const handleStartMonitoring = async () => {
    setStatusLoading(true);
    try {
      const response = await fetch('http://localhost:8000/api/v1/monitoring/start', {
        method: 'POST',
      });
      if (response.ok) {
        await fetchMonitoringStatus();
        enqueueSnackbar('Automated monitoring started', { variant: 'success' });
      } else {
        enqueueSnackbar('Failed to start monitoring', { variant: 'error' });
      }
    } catch (err) {
      console.error('Failed to start monitoring', err);
      enqueueSnackbar('Failed to start monitoring', { variant: 'error' });
    } finally {
      setStatusLoading(false);
    }
  };

  const handleStopMonitoring = async () => {
    setStatusLoading(true);
    try {
      const response = await fetch('http://localhost:8000/api/v1/monitoring/stop', {
        method: 'POST',
      });
      if (response.ok) {
        await fetchMonitoringStatus();
        enqueueSnackbar('Automated monitoring stopped', { variant: 'info' });
      } else {
        enqueueSnackbar('Failed to stop monitoring', { variant: 'error' });
      }
    } catch (err) {
      console.error('Failed to stop monitoring', err);
      enqueueSnackbar('Failed to stop monitoring', { variant: 'error' });
    } finally {
      setStatusLoading(false);
    }
  };

  const handleCheckNow = async () => {
    setStatusLoading(true);
    enqueueSnackbar('Running immediate check...', { variant: 'info' });
    try {
      const response = await fetch('http://localhost:8000/api/v1/monitoring/check-now', {
        method: 'POST',
      });
      if (response.ok) {
        const result = await response.json();
        await fetchMonitoringStatus();
        await fetchMonitoringData();
        enqueueSnackbar(
          `Check complete! Monitored: ${result.monitoring_status.stats.farmers_monitored}, Advisories: ${result.monitoring_status.stats.advisories_generated}`,
          { variant: 'success' }
        );
      } else {
        enqueueSnackbar('Failed to trigger check', { variant: 'error' });
      }
    } catch (err) {
      console.error('Failed to trigger check', err);
      enqueueSnackbar('Failed to trigger check', { variant: 'error' });
    } finally {
      setStatusLoading(false);
    }
  };

  const fetchMonitoringData = async () => {
    setLoading(true);
    setError(null);

    try {
      // Fetch all farmers
      const farmersResponse = await fetch('http://localhost:8000/api/v1/farmers/');
      const farmers = await farmersResponse.json();

      // Fetch latest advisory for each farmer
      const monitoringData: FarmerMonitoring[] = [];
      
      for (const farmer of farmers) {
        try {
          const advisoriesResponse = await fetch(
            `http://localhost:8000/api/v1/advisories/farmer/${farmer.farmer_id}`
          );
          
          let latestAdvisory = null;
          let healthStatus = 'unknown';
          
          if (advisoriesResponse.ok) {
            const advisories = await advisoriesResponse.json();
            if (advisories.length > 0) {
              // Sort by created_at and get latest
              advisories.sort((a: any, b: any) => 
                new Date(b.created_at).getTime() - new Date(a.created_at).getTime()
              );
              latestAdvisory = advisories[0];
              healthStatus = latestAdvisory.stress_type;
            }
          }

          monitoringData.push({
            farmer_id: farmer.farmer_id,
            phone_number: farmer.phone_number,
            plot_count: 1, // Simplified
            latest_advisory: latestAdvisory,
            health_status: healthStatus,
          });
        } catch (err) {
          console.error(`Failed to fetch data for farmer ${farmer.farmer_id}`);
        }
      }

      setMonitoring(monitoringData);
    } catch (err) {
      setError('Failed to fetch monitoring data');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const fetchWeatherData = async () => {
    try {
      // Fetch weather for Bangalore (default location)
      const response = await fetch(
        'https://api.openweathermap.org/data/2.5/weather?lat=12.9716&lon=77.5946&appid=9cb097bad8ee1c0e5e6e3f4a0b3ebc5b&units=metric'
      );
      if (response.ok) {
        const data = await response.json();
        setWeatherData(data);
      }
    } catch (err) {
      console.error('Failed to fetch weather data', err);
    }
  };

  const getHealthColor = (status: string) => {
    switch (status) {
      case 'healthy': return 'success';
      case 'general_stress': return 'default';
      case 'moderate_stress': return 'warning';
      case 'water_stress': return 'primary';
      case 'heat_stress': return 'error';
      case 'severe_stress': return 'error';
      default: return 'default';
    }
  };

  const getHealthIcon = (status: string) => {
    switch (status) {
      case 'healthy': return '✓';
      case 'general_stress': return '○';
      case 'moderate_stress': return '⚠';
      case 'water_stress': return '💧';
      case 'heat_stress': return '🔥';
      case 'severe_stress': return '⚠';
      default: return '?';
    }
  };

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="400px">
        <CircularProgress />
      </Box>
    );
  }

  if (error) {
    return <Alert severity="error">{error}</Alert>;
  }

  // Calculate summary stats
  const healthyCrops = monitoring.filter(m => m.health_status === 'healthy').length;
  const stressedCrops = monitoring.filter(m => 
    m.health_status.includes('stress') && m.health_status !== 'healthy'
  ).length;
  const criticalCrops = monitoring.filter(m => 
    m.health_status === 'severe_stress' || m.health_status === 'heat_stress'
  ).length;

  return (
    <Box>
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={2}>
        <Box>
          <Typography variant="h4" gutterBottom>
            Crop Monitoring Dashboard
          </Typography>
          <Typography color="textSecondary">
            Real-time crop health monitoring and environmental conditions
          </Typography>
        </Box>
        <Button
          variant="contained"
          color="primary"
          startIcon={<Map />}
          onClick={() => navigate('/monitoring/advanced')}
        >
          View Map
        </Button>
      </Box>

      {/* Automated Monitoring Controls */}
      <Card sx={{ mb: 3, bgcolor: 'primary.light', color: 'primary.contrastText' }}>
        <CardContent>
          <Box display="flex" justifyContent="space-between" alignItems="center">
            <Box>
              <Typography variant="h6" gutterBottom>
                Automated Monitoring System
              </Typography>
              <Typography variant="body2">
                {monitoringStatus?.is_running
                  ? 'System is actively monitoring all farmers'
                  : 'System is currently stopped'}
              </Typography>
              {monitoringStatus?.stats?.last_check && (
                <Typography variant="caption" display="block" sx={{ mt: 1 }}>
                  Last check: {new Date(monitoringStatus.stats.last_check).toLocaleString()}
                </Typography>
              )}
            </Box>
            <Box display="flex" gap={2} alignItems="center">
              <Box textAlign="center">
                <Typography variant="h4">{monitoringStatus?.stats?.total_checks || 0}</Typography>
                <Typography variant="caption">Checks</Typography>
              </Box>
              <Box textAlign="center">
                <Typography variant="h4">{monitoringStatus?.stats?.farmers_monitored || 0}</Typography>
                <Typography variant="caption">Farmers</Typography>
              </Box>
              <Box textAlign="center">
                <Typography variant="h4">{monitoringStatus?.stats?.advisories_generated || 0}</Typography>
                <Typography variant="caption">Advisories</Typography>
              </Box>
              <Box textAlign="center">
                <Typography variant="h4">{monitoringStatus?.stats?.calls_made || 0}</Typography>
                <Typography variant="caption">Calls</Typography>
              </Box>
              <Divider orientation="vertical" flexItem sx={{ mx: 2 }} />
              <Box display="flex" gap={1}>
                {monitoringStatus?.is_running ? (
                  <Button
                    variant="contained"
                    color="error"
                    startIcon={<Stop />}
                    onClick={handleStopMonitoring}
                    disabled={statusLoading}
                  >
                    Stop
                  </Button>
                ) : (
                  <Button
                    variant="contained"
                    color="success"
                    startIcon={<PlayArrow />}
                    onClick={handleStartMonitoring}
                    disabled={statusLoading}
                  >
                    Start
                  </Button>
                )}
                <Button
                  variant="outlined"
                  startIcon={<Refresh />}
                  onClick={handleCheckNow}
                  disabled={statusLoading}
                  sx={{ color: 'white', borderColor: 'white' }}
                >
                  Check Now
                </Button>
              </Box>
            </Box>
          </Box>
        </CardContent>
      </Card>

      {/* Weather Overview */}
      {weatherData && (
        <Card sx={{ mb: 3 }}>
          <CardContent>
            <Typography variant="h6" gutterBottom>
              Current Weather Conditions (Bangalore)
            </Typography>
            <Divider sx={{ mb: 2 }} />
            <Grid container spacing={3}>
              <Grid item xs={6} sm={3}>
                <Box display="flex" alignItems="center" gap={1}>
                  <Thermostat color="error" />
                  <Box>
                    <Typography variant="h5">
                      {weatherData.main.temp.toFixed(1)}°C
                    </Typography>
                    <Typography variant="body2" color="textSecondary">
                      Temperature
                    </Typography>
                  </Box>
                </Box>
              </Grid>
              <Grid item xs={6} sm={3}>
                <Box display="flex" alignItems="center" gap={1}>
                  <Opacity color="primary" />
                  <Box>
                    <Typography variant="h5">
                      {weatherData.main.humidity}%
                    </Typography>
                    <Typography variant="body2" color="textSecondary">
                      Humidity
                    </Typography>
                  </Box>
                </Box>
              </Grid>
              <Grid item xs={6} sm={3}>
                <Box display="flex" alignItems="center" gap={1}>
                  <Air color="info" />
                  <Box>
                    <Typography variant="h5">
                      {weatherData.wind.speed.toFixed(1)} m/s
                    </Typography>
                    <Typography variant="body2" color="textSecondary">
                      Wind Speed
                    </Typography>
                  </Box>
                </Box>
              </Grid>
              <Grid item xs={6} sm={3}>
                <Box display="flex" alignItems="center" gap={1}>
                  <WbSunny color="warning" />
                  <Box>
                    <Typography variant="h5">
                      {weatherData.weather[0].main}
                    </Typography>
                    <Typography variant="body2" color="textSecondary">
                      Conditions
                    </Typography>
                  </Box>
                </Box>
              </Grid>
            </Grid>
          </CardContent>
        </Card>
      )}

      {/* Health Summary */}
      <Grid container spacing={3} sx={{ mb: 3 }}>
        <Grid item xs={12} sm={4}>
          <Card>
            <CardContent>
              <Box display="flex" alignItems="center" gap={2}>
                <Grass sx={{ fontSize: 48, color: 'success.main' }} />
                <Box>
                  <Typography variant="h4">{healthyCrops}</Typography>
                  <Typography color="textSecondary">Healthy Crops</Typography>
                </Box>
              </Box>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} sm={4}>
          <Card>
            <CardContent>
              <Box display="flex" alignItems="center" gap={2}>
                <Grass sx={{ fontSize: 48, color: 'warning.main' }} />
                <Box>
                  <Typography variant="h4">{stressedCrops}</Typography>
                  <Typography color="textSecondary">Under Stress</Typography>
                </Box>
              </Box>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} sm={4}>
          <Card>
            <CardContent>
              <Box display="flex" alignItems="center" gap={2}>
                <Grass sx={{ fontSize: 48, color: 'error.main' }} />
                <Box>
                  <Typography variant="h4">{criticalCrops}</Typography>
                  <Typography color="textSecondary">Critical</Typography>
                </Box>
              </Box>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Farmer Monitoring Table */}
      <Card>
        <CardContent>
          <Typography variant="h6" gutterBottom>
            Farmer Crop Health Status
          </Typography>
          <Divider sx={{ mb: 2 }} />
          <TableContainer>
            <Table>
              <TableHead>
                <TableRow>
                  <TableCell>Farmer</TableCell>
                  <TableCell>Health Status</TableCell>
                  <TableCell>Latest Advisory</TableCell>
                  <TableCell>Urgency</TableCell>
                  <TableCell>Actions Required</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {monitoring.length === 0 ? (
                  <TableRow>
                    <TableCell colSpan={5} align="center">
                      <Typography color="textSecondary">
                        No monitoring data available
                      </Typography>
                    </TableCell>
                  </TableRow>
                ) : (
                  monitoring.map((item) => (
                    <TableRow key={item.farmer_id} hover>
                      <TableCell>{item.phone_number}</TableCell>
                      <TableCell>
                        <Chip
                          label={`${getHealthIcon(item.health_status)} ${item.health_status.replace('_', ' ').toUpperCase()}`}
                          size="small"
                          color={getHealthColor(item.health_status) as any}
                        />
                      </TableCell>
                      <TableCell>
                        {item.latest_advisory
                          ? new Date(item.latest_advisory.created_at).toLocaleDateString()
                          : 'No advisory'}
                      </TableCell>
                      <TableCell>
                        {item.latest_advisory ? (
                          <Chip
                            label={item.latest_advisory.urgency_level.toUpperCase()}
                            size="small"
                            color={
                              item.latest_advisory.urgency_level === 'critical'
                                ? 'error'
                                : item.latest_advisory.urgency_level === 'high'
                                ? 'warning'
                                : item.latest_advisory.urgency_level === 'medium'
                                ? 'info'
                                : 'success'
                            }
                          />
                        ) : (
                          '-'
                        )}
                      </TableCell>
                      <TableCell>
                        {item.latest_advisory?.actions?.length || 0} actions
                      </TableCell>
                    </TableRow>
                  ))
                )}
              </TableBody>
            </Table>
          </TableContainer>
        </CardContent>
      </Card>
    </Box>
  );
};
