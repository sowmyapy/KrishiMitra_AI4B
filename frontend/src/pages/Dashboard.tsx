import { Grid, Typography, Box, Card, CardContent, CircularProgress, Button } from '@mui/material';
import { People, Assignment, Warning, CheckCircle, Add } from '@mui/icons-material';
import { StatsCard } from '@/components/dashboard/StatsCard';
import { useFarmers } from '@/hooks/useFarmers';
import { useNavigate } from 'react-router-dom';

export const Dashboard = () => {
  const { data: farmers, isLoading: farmersLoading } = useFarmers();
  const navigate = useNavigate();

  if (farmersLoading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="400px">
        <CircularProgress />
      </Box>
    );
  }

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Dashboard
      </Typography>

      <Grid container spacing={3} sx={{ mb: 3 }}>
        <Grid item xs={12} sm={6} md={3}>
          <StatsCard
            title="Total Farmers"
            value={farmers?.length || 0}
            icon={<People sx={{ fontSize: 40 }} />}
            color="#2E7D32"
            subtitle="+12 this month"
          />
        </Grid>

        <Grid item xs={12} sm={6} md={3}>
          <StatsCard
            title="Active Advisories"
            value={0}
            icon={<Assignment sx={{ fontSize: 40 }} />}
            color="#2196F3"
            subtitle="Last 7 days"
          />
        </Grid>

        <Grid item xs={12} sm={6} md={3}>
          <StatsCard
            title="Critical Alerts"
            value={0}
            icon={<Warning sx={{ fontSize: 40 }} />}
            color="#F44336"
            subtitle="Requires attention"
          />
        </Grid>

        <Grid item xs={12} sm={6} md={3}>
          <StatsCard
            title="System Health"
            value="98%"
            icon={<CheckCircle sx={{ fontSize: 40 }} />}
            color="#4CAF50"
            subtitle="All systems operational"
          />
        </Grid>
      </Grid>

      <Grid container spacing={3}>
        <Grid item xs={12} md={8}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Recent Farmers
              </Typography>
              {farmers && farmers.length > 0 ? (
                farmers.slice(0, 5).map((farmer) => (
                  <Box
                    key={farmer.farmer_id}
                    sx={{
                      p: 2,
                      mb: 1,
                      border: '1px solid #e0e0e0',
                      borderRadius: 1,
                      cursor: 'pointer',
                      '&:hover': {
                        backgroundColor: '#f5f5f5',
                      },
                    }}
                    onClick={() => navigate(`/farmers/${farmer.farmer_id}`)}
                  >
                    <Typography variant="subtitle1">
                      {farmer.phone_number}
                    </Typography>
                    <Typography variant="body2" color="textSecondary">
                      Language: {farmer.preferred_language} | Registered: {new Date(farmer.created_at).toLocaleDateString()}
                    </Typography>
                  </Box>
                ))
              ) : (
                <Box textAlign="center" py={4}>
                  <Typography color="textSecondary" gutterBottom>
                    No farmers registered yet
                  </Typography>
                  <Button
                    variant="contained"
                    startIcon={<Add />}
                    onClick={() => navigate('/farmers/new')}
                    sx={{ mt: 2 }}
                  >
                    Register First Farmer
                  </Button>
                </Box>
              )}
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={4}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Quick Actions
              </Typography>
              <Box display="flex" flexDirection="column" gap={2}>
                <Button
                  variant="outlined"
                  fullWidth
                  startIcon={<Add />}
                  onClick={() => navigate('/farmers/new')}
                >
                  Register Farmer
                </Button>
                <Button
                  variant="outlined"
                  fullWidth
                  startIcon={<People />}
                  onClick={() => navigate('/farmers')}
                >
                  View All Farmers
                </Button>
                <Button
                  variant="outlined"
                  fullWidth
                  startIcon={<Assignment />}
                  onClick={() => navigate('/advisories')}
                >
                  View Advisories
                </Button>
              </Box>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Box>
  );
};
