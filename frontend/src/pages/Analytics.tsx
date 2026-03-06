import { useState, useEffect } from 'react';
import {
  Box,
  Typography,
  Grid,
  Card,
  CardContent,
  CircularProgress,
  Alert,
  Divider,
  Chip,
} from '@mui/material';
import {
  People,
  Assessment,
  Phone,
  TrendingUp,
  Warning,
  CheckCircle,
} from '@mui/icons-material';

interface Stats {
  totalFarmers: number;
  totalAdvisories: number;
  totalPlots: number;
  advisoriesByStress: Record<string, number>;
  advisoriesByUrgency: Record<string, number>;
  recentAdvisories: number;
  expiredAdvisories: number;
}

export const Analytics = () => {
  const [stats, setStats] = useState<Stats | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchStats();
  }, []);

  const fetchStats = async () => {
    setLoading(true);
    setError(null);
    
    try {
      // Fetch farmers
      const farmersResponse = await fetch('http://localhost:8000/api/v1/farmers/');
      const farmers = await farmersResponse.json();

      // Fetch all advisories
      const allAdvisories: any[] = [];
      for (const farmer of farmers) {
        try {
          const advisoriesResponse = await fetch(
            `http://localhost:8000/api/v1/advisories/farmer/${farmer.farmer_id}`
          );
          if (advisoriesResponse.ok) {
            const farmerAdvisories = await advisoriesResponse.json();
            allAdvisories.push(...farmerAdvisories);
          }
        } catch (err) {
          console.error(`Failed to fetch advisories for farmer ${farmer.farmer_id}`);
        }
      }

      // Calculate stats
      const now = new Date();
      const sevenDaysAgo = new Date(now.getTime() - 7 * 24 * 60 * 60 * 1000);

      const advisoriesByStress: Record<string, number> = {};
      const advisoriesByUrgency: Record<string, number> = {};
      let recentAdvisories = 0;
      let expiredAdvisories = 0;

      allAdvisories.forEach(advisory => {
        // Count by stress type
        advisoriesByStress[advisory.stress_type] = 
          (advisoriesByStress[advisory.stress_type] || 0) + 1;

        // Count by urgency
        advisoriesByUrgency[advisory.urgency_level] = 
          (advisoriesByUrgency[advisory.urgency_level] || 0) + 1;

        // Count recent (last 7 days)
        if (new Date(advisory.created_at) >= sevenDaysAgo) {
          recentAdvisories++;
        }

        // Count expired
        if (new Date(advisory.expires_at) < now) {
          expiredAdvisories++;
        }
      });

      setStats({
        totalFarmers: farmers.length,
        totalAdvisories: allAdvisories.length,
        totalPlots: farmers.length, // Simplified - assuming 1 plot per farmer
        advisoriesByStress,
        advisoriesByUrgency,
        recentAdvisories,
        expiredAdvisories,
      });
    } catch (err) {
      setError('Failed to fetch analytics data');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="400px">
        <CircularProgress />
      </Box>
    );
  }

  if (error || !stats) {
    return (
      <Alert severity="error">{error || 'Failed to load analytics'}</Alert>
    );
  }

  const StatCard = ({ title, value, icon, color }: any) => (
    <Card>
      <CardContent>
        <Box display="flex" justifyContent="space-between" alignItems="center">
          <Box>
            <Typography color="textSecondary" gutterBottom variant="body2">
              {title}
            </Typography>
            <Typography variant="h4">{value}</Typography>
          </Box>
          <Box
            sx={{
              backgroundColor: `${color}.light`,
              borderRadius: 2,
              p: 1.5,
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
            }}
          >
            {icon}
          </Box>
        </Box>
      </CardContent>
    </Card>
  );

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Analytics Dashboard
      </Typography>
      <Typography color="textSecondary" paragraph>
        Overview of system performance and advisory statistics
      </Typography>

      {/* Key Metrics */}
      <Grid container spacing={3} sx={{ mb: 4 }}>
        <Grid item xs={12} sm={6} md={3}>
          <StatCard
            title="Total Farmers"
            value={stats.totalFarmers}
            icon={<People sx={{ color: 'primary.main', fontSize: 40 }} />}
            color="primary"
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <StatCard
            title="Total Advisories"
            value={stats.totalAdvisories}
            icon={<Assessment sx={{ color: 'success.main', fontSize: 40 }} />}
            color="success"
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <StatCard
            title="Recent (7 days)"
            value={stats.recentAdvisories}
            icon={<TrendingUp sx={{ color: 'info.main', fontSize: 40 }} />}
            color="info"
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <StatCard
            title="Expired"
            value={stats.expiredAdvisories}
            icon={<Warning sx={{ color: 'warning.main', fontSize: 40 }} />}
            color="warning"
          />
        </Grid>
      </Grid>

      {/* Advisories by Stress Type */}
      <Grid container spacing={3}>
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Advisories by Stress Type
              </Typography>
              <Divider sx={{ mb: 2 }} />
              {Object.keys(stats.advisoriesByStress).length === 0 ? (
                <Typography color="textSecondary">No data available</Typography>
              ) : (
                <Box>
                  {Object.entries(stats.advisoriesByStress)
                    .sort(([, a], [, b]) => b - a)
                    .map(([type, count]) => (
                      <Box
                        key={type}
                        display="flex"
                        justifyContent="space-between"
                        alignItems="center"
                        py={1}
                      >
                        <Box display="flex" alignItems="center" gap={1}>
                          <Chip
                            label={type.replace('_', ' ').toUpperCase()}
                            size="small"
                            color={
                              type.includes('severe') || type.includes('heat')
                                ? 'error'
                                : type.includes('water')
                                ? 'primary'
                                : type.includes('moderate')
                                ? 'warning'
                                : type === 'healthy'
                                ? 'success'
                                : 'default'
                            }
                          />
                        </Box>
                        <Typography variant="h6">{count}</Typography>
                      </Box>
                    ))}
                </Box>
              )}
            </CardContent>
          </Card>
        </Grid>

        {/* Advisories by Urgency */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Advisories by Urgency Level
              </Typography>
              <Divider sx={{ mb: 2 }} />
              {Object.keys(stats.advisoriesByUrgency).length === 0 ? (
                <Typography color="textSecondary">No data available</Typography>
              ) : (
                <Box>
                  {Object.entries(stats.advisoriesByUrgency)
                    .sort(([, a], [, b]) => b - a)
                    .map(([urgency, count]) => (
                      <Box
                        key={urgency}
                        display="flex"
                        justifyContent="space-between"
                        alignItems="center"
                        py={1}
                      >
                        <Box display="flex" alignItems="center" gap={1}>
                          <Chip
                            label={urgency.toUpperCase()}
                            size="small"
                            color={
                              urgency === 'critical'
                                ? 'error'
                                : urgency === 'high'
                                ? 'warning'
                                : urgency === 'medium'
                                ? 'info'
                                : 'success'
                            }
                          />
                        </Box>
                        <Typography variant="h6">{count}</Typography>
                      </Box>
                    ))}
                </Box>
              )}
            </CardContent>
          </Card>
        </Grid>

        {/* Summary Stats */}
        <Grid item xs={12}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                System Summary
              </Typography>
              <Divider sx={{ mb: 2 }} />
              <Grid container spacing={2}>
                <Grid item xs={12} sm={6} md={3}>
                  <Box textAlign="center" py={2}>
                    <Typography variant="h3" color="primary">
                      {stats.totalFarmers}
                    </Typography>
                    <Typography color="textSecondary">Registered Farmers</Typography>
                  </Box>
                </Grid>
                <Grid item xs={12} sm={6} md={3}>
                  <Box textAlign="center" py={2}>
                    <Typography variant="h3" color="success.main">
                      {stats.totalAdvisories}
                    </Typography>
                    <Typography color="textSecondary">Total Advisories</Typography>
                  </Box>
                </Grid>
                <Grid item xs={12} sm={6} md={3}>
                  <Box textAlign="center" py={2}>
                    <Typography variant="h3" color="info.main">
                      {stats.totalAdvisories > 0
                        ? (stats.recentAdvisories / stats.totalAdvisories * 100).toFixed(0)
                        : 0}%
                    </Typography>
                    <Typography color="textSecondary">Recent Activity</Typography>
                  </Box>
                </Grid>
                <Grid item xs={12} sm={6} md={3}>
                  <Box textAlign="center" py={2}>
                    <Typography variant="h3" color="warning.main">
                      {stats.totalAdvisories > 0
                        ? ((stats.totalAdvisories - stats.expiredAdvisories) / stats.totalAdvisories * 100).toFixed(0)
                        : 0}%
                    </Typography>
                    <Typography color="textSecondary">Active Advisories</Typography>
                  </Box>
                </Grid>
              </Grid>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Box>
  );
};
