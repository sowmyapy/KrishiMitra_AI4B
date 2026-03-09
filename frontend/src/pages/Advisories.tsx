import { useState, useEffect } from 'react';
import { getApiUrl } from '@/api/client';
import { useNavigate } from 'react-router-dom';
import {
  Box,
  Typography,
  Card,
  CardContent,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  TablePagination,
  Chip,
  TextField,
  MenuItem,
  CircularProgress,
  Alert,
  IconButton,
  Tooltip,
  Grid,
} from '@mui/material';
import { Visibility, Refresh } from '@mui/icons-material';

interface Advisory {
  advisory_id: string;
  farmer_id: string;
  farm_plot_id: string;
  stress_type: string;
  urgency_level: string;
  advisory_text?: string;
  actions: any[];
  created_at: string;
  expires_at: string;
}

export const Advisories = () => {
  const navigate = useNavigate();
  const [advisories, setAdvisories] = useState<Advisory[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [page, setPage] = useState(0);
  const [rowsPerPage, setRowsPerPage] = useState(10);
  const [filterStressType, setFilterStressType] = useState('all');
  const [filterUrgency, setFilterUrgency] = useState('all');

  const fetchAdvisories = async () => {
    setLoading(true);
    setError(null);
    try {
      // Fetch all farmers first
      const farmersResponse = await fetch(getApiUrl('/api/v1/farmers/'));
      const farmers = await farmersResponse.json();

      // Fetch advisories for each farmer
      const allAdvisories: Advisory[] = [];
      for (const farmer of farmers) {
        try {
          const advisoriesResponse = await fetch(
            getApiUrl(`/api/v1/advisories/farmer/${farmer.farmer_id}`)
          );
          if (advisoriesResponse.ok) {
            const farmerAdvisories = await advisoriesResponse.json();
            allAdvisories.push(...farmerAdvisories);
          }
        } catch (err) {
          console.error(`Failed to fetch advisories for farmer ${farmer.farmer_id}`, err);
        }
      }

      // Sort by created_at descending
      allAdvisories.sort((a, b) => 
        new Date(b.created_at).getTime() - new Date(a.created_at).getTime()
      );

      setAdvisories(allAdvisories);
    } catch (err) {
      setError('Failed to fetch advisories');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchAdvisories();
  }, []);

  const handleChangePage = (_event: unknown, newPage: number) => {
    setPage(newPage);
  };

  const handleChangeRowsPerPage = (event: React.ChangeEvent<HTMLInputElement>) => {
    setRowsPerPage(parseInt(event.target.value, 10));
    setPage(0);
  };

  const getUrgencyColor = (urgency: string) => {
    switch (urgency) {
      case 'critical': return 'error';
      case 'high': return 'warning';
      case 'medium': return 'info';
      case 'low': return 'success';
      default: return 'default';
    }
  };

  const getStressColor = (stress: string) => {
    switch (stress) {
      case 'severe_stress': return 'error';
      case 'water_stress': return 'primary';
      case 'heat_stress': return 'error';
      case 'moderate_stress': return 'warning';
      case 'general_stress': return 'default';
      case 'healthy': return 'success';
      default: return 'default';
    }
  };

  // Filter advisories
  const filteredAdvisories = advisories.filter(advisory => {
    if (filterStressType !== 'all' && advisory.stress_type !== filterStressType) {
      return false;
    }
    if (filterUrgency !== 'all' && advisory.urgency_level !== filterUrgency) {
      return false;
    }
    return true;
  });

  // Paginate
  const paginatedAdvisories = filteredAdvisories.slice(
    page * rowsPerPage,
    page * rowsPerPage + rowsPerPage
  );

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="400px">
        <CircularProgress />
      </Box>
    );
  }

  return (
    <Box>
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
        <Typography variant="h4">All Advisories</Typography>
        <Tooltip title="Refresh">
          <IconButton onClick={fetchAdvisories} color="primary">
            <Refresh />
          </IconButton>
        </Tooltip>
      </Box>

      {error && (
        <Alert severity="error" sx={{ mb: 3 }}>
          {error}
        </Alert>
      )}

      <Card sx={{ mb: 3 }}>
        <CardContent>
          <Grid container spacing={2}>
            <Grid size={{ xs: 12, sm: 6, md: 3 }}>
              <TextField
                select
                fullWidth
                label="Stress Type"
                value={filterStressType}
                onChange={(e) => setFilterStressType(e.target.value)}
              >
                <MenuItem value="all">All Types</MenuItem>
                <MenuItem value="severe_stress">Severe Stress</MenuItem>
                <MenuItem value="water_stress">Water Stress</MenuItem>
                <MenuItem value="heat_stress">Heat Stress</MenuItem>
                <MenuItem value="moderate_stress">Moderate Stress</MenuItem>
                <MenuItem value="general_stress">General Stress</MenuItem>
                <MenuItem value="healthy">Healthy</MenuItem>
              </TextField>
            </Grid>
            <Grid size={{ xs: 12, sm: 6, md: 3 }}>
              <TextField
                select
                fullWidth
                label="Urgency Level"
                value={filterUrgency}
                onChange={(e) => setFilterUrgency(e.target.value)}
              >
                <MenuItem value="all">All Levels</MenuItem>
                <MenuItem value="critical">Critical</MenuItem>
                <MenuItem value="high">High</MenuItem>
                <MenuItem value="medium">Medium</MenuItem>
                <MenuItem value="low">Low</MenuItem>
              </TextField>
            </Grid>
            <Grid size={{ xs: 12, sm: 6, md: 3 }}>
              <Box display="flex" alignItems="center" height="100%">
                <Typography variant="body2" color="textSecondary">
                  Total: {filteredAdvisories.length} advisories
                </Typography>
              </Box>
            </Grid>
          </Grid>
        </CardContent>
      </Card>

      <Card>
        <TableContainer>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell>Date</TableCell>
                <TableCell>Stress Type</TableCell>
                <TableCell>Urgency</TableCell>
                <TableCell>Advisory Message</TableCell>
                <TableCell>Expires</TableCell>
                <TableCell align="center">View</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {paginatedAdvisories.length === 0 ? (
                <TableRow>
                  <TableCell colSpan={6} align="center">
                    <Typography color="textSecondary">
                      No advisories found
                    </Typography>
                  </TableCell>
                </TableRow>
              ) : (
                paginatedAdvisories.map((advisory) => (
                  <TableRow key={advisory.advisory_id} hover>
                    <TableCell>
                      {new Date(advisory.created_at).toLocaleString()}
                    </TableCell>
                    <TableCell>
                      <Chip
                        label={advisory.stress_type.replace('_', ' ').toUpperCase()}
                        size="small"
                        color={getStressColor(advisory.stress_type) as any}
                      />
                    </TableCell>
                    <TableCell>
                      <Chip
                        label={advisory.urgency_level.toUpperCase()}
                        size="small"
                        color={getUrgencyColor(advisory.urgency_level) as any}
                      />
                    </TableCell>
                    <TableCell>
                      {advisory.advisory_text ? (
                        <Typography 
                          variant="body2" 
                          sx={{ 
                            whiteSpace: 'pre-wrap',
                            maxWidth: '400px',
                            overflow: 'hidden',
                            textOverflow: 'ellipsis',
                            display: '-webkit-box',
                            WebkitLineClamp: 3,
                            WebkitBoxOrient: 'vertical',
                          }}
                        >
                          {advisory.advisory_text}
                        </Typography>
                      ) : (
                        <Typography variant="body2" color="textSecondary">
                          {advisory.actions?.length || 0} actions
                        </Typography>
                      )}
                    </TableCell>
                    <TableCell>
                      {new Date(advisory.expires_at).toLocaleDateString()}
                    </TableCell>
                    <TableCell align="center">
                      <Tooltip title="View Farmer">
                        <IconButton
                          size="small"
                          onClick={() => navigate(`/farmers/${advisory.farmer_id}`)}
                        >
                          <Visibility />
                        </IconButton>
                      </Tooltip>
                    </TableCell>
                  </TableRow>
                ))
              )}
            </TableBody>
          </Table>
        </TableContainer>
        <TablePagination
          rowsPerPageOptions={[5, 10, 25, 50]}
          component="div"
          count={filteredAdvisories.length}
          rowsPerPage={rowsPerPage}
          page={page}
          onPageChange={handleChangePage}
          onRowsPerPageChange={handleChangeRowsPerPage}
        />
      </Card>
    </Box>
  );
};
