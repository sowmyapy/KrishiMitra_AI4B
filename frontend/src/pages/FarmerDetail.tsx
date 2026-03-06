import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import {
  Box,
  Typography,
  Button,
  Grid,
  Card,
  CardContent,
  Chip,
  CircularProgress,
  Alert,
  Divider,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  MenuItem,
} from '@mui/material';
import { ArrowBack, Phone, Assessment, Edit } from '@mui/icons-material';
import { useFarmer } from '@/hooks/useFarmers';

export const FarmerDetail = () => {
  const { farmerId } = useParams<{ farmerId: string }>();
  const navigate = useNavigate();
  const { data: farmer, isLoading } = useFarmer(farmerId!);
  const [generatingAdvisory, setGeneratingAdvisory] = useState(false);
  const [makingCall, setMakingCall] = useState(false);
  const [message, setMessage] = useState<{ type: 'success' | 'error'; text: string } | null>(null);
  const [advisories, setAdvisories] = useState<any[]>([]);
  const [loadingAdvisories, setLoadingAdvisories] = useState(false);
  const [editDialogOpen, setEditDialogOpen] = useState(false);
  const [editLanguage, setEditLanguage] = useState('');
  const [editTimezone, setEditTimezone] = useState('');
  const [updating, setUpdating] = useState(false);

  // Fetch advisories when component mounts or after generating new advisory
  useEffect(() => {
    if (farmerId) {
      fetchAdvisories();
    }
  }, [farmerId]);

  // Initialize edit form when farmer data loads
  useEffect(() => {
    if (farmer) {
      setEditLanguage(farmer.preferred_language);
      setEditTimezone(farmer.timezone);
    }
  }, [farmer]);

  const fetchAdvisories = async () => {
    setLoadingAdvisories(true);
    try {
      const response = await fetch(`http://localhost:8000/api/v1/advisories/farmer/${farmerId}`);
      if (response.ok) {
        const data = await response.json();
        setAdvisories(data);
      }
    } catch (error) {
      console.error('Error fetching advisories:', error);
    } finally {
      setLoadingAdvisories(false);
    }
  };

  const handleGenerateAdvisory = async () => {
    setGeneratingAdvisory(true);
    setMessage(null);
    
    try {
      // Call the backend to generate advisory
      const response = await fetch(`http://localhost:8000/api/v1/advisories/generate/${farmerId}`, {
        method: 'POST',
      });
      
      if (response.ok) {
        setMessage({ type: 'success', text: 'Advisory generated successfully!' });
        // Refresh advisories list
        await fetchAdvisories();
      } else {
        const errorData = await response.json();
        setMessage({ type: 'error', text: errorData.detail || 'Failed to generate advisory' });
      }
    } catch (error) {
      setMessage({ type: 'error', text: 'Error generating advisory' });
    } finally {
      setGeneratingAdvisory(false);
    }
  };

  const handleMakeCall = async () => {
    setMakingCall(true);
    setMessage(null);
    
    try {
      // Call the backend to initiate voice call
      const response = await fetch(`http://localhost:8000/api/v1/voice/call/${farmerId}`, {
        method: 'POST',
      });
      
      if (response.ok) {
        const data = await response.json();
        setMessage({ 
          type: 'success', 
          text: `Voice call initiated! Call SID: ${data.call_sid}. The farmer will receive a call shortly.` 
        });
      } else {
        const errorData = await response.json();
        setMessage({ 
          type: 'error', 
          text: errorData.detail || 'Failed to initiate call' 
        });
      }
    } catch (error) {
      setMessage({ type: 'error', text: 'Error initiating call' });
    } finally {
      setMakingCall(false);
    }
  };

  const handleOpenEditDialog = () => {
    setEditDialogOpen(true);
  };

  const handleCloseEditDialog = () => {
    setEditDialogOpen(false);
    // Reset to current values
    if (farmer) {
      setEditLanguage(farmer.preferred_language);
      setEditTimezone(farmer.timezone);
    }
  };

  const handleUpdateFarmer = async () => {
    setUpdating(true);
    setMessage(null);
    
    try {
      const response = await fetch(`http://localhost:8000/api/v1/farmers/${farmerId}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          phone_number: farmer?.phone_number,
          preferred_language: editLanguage,
          timezone: editTimezone,
        }),
      });
      
      if (response.ok) {
        setMessage({ type: 'success', text: 'Farmer information updated successfully!' });
        setEditDialogOpen(false);
        // Refresh farmer data
        window.location.reload();
      } else {
        const errorData = await response.json();
        setMessage({ type: 'error', text: errorData.detail || 'Failed to update farmer' });
      }
    } catch (error) {
      setMessage({ type: 'error', text: 'Error updating farmer' });
    } finally {
      setUpdating(false);
    }
  };

  if (isLoading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="400px">
        <CircularProgress />
      </Box>
    );
  }

  if (!farmer) {
    return (
      <Box>
        <Alert severity="error">Farmer not found</Alert>
        <Button onClick={() => navigate('/farmers')} sx={{ mt: 2 }}>
          Back to Farmers
        </Button>
      </Box>
    );
  }

  return (
    <Box>
      <Box display="flex" alignItems="center" mb={3}>
        <Button
          startIcon={<ArrowBack />}
          onClick={() => navigate('/farmers')}
          sx={{ mr: 2 }}
        >
          Back
        </Button>
        <Typography variant="h4">Farmer Details</Typography>
      </Box>

      {message && (
        <Alert severity={message.type} sx={{ mb: 3 }} onClose={() => setMessage(null)}>
          {message.text}
        </Alert>
      )}

      <Grid container spacing={3}>
        {/* Farmer Information */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Box display="flex" justifyContent="space-between" alignItems="center" mb={2}>
                <Typography variant="h6">
                  Farmer Information
                </Typography>
                <Button
                  size="small"
                  startIcon={<Edit />}
                  onClick={handleOpenEditDialog}
                >
                  Edit
                </Button>
              </Box>
              <Divider sx={{ mb: 2 }} />
              
              <Box mb={2}>
                <Typography variant="body2" color="textSecondary">
                  Phone Number
                </Typography>
                <Typography variant="body1">{farmer.phone_number}</Typography>
              </Box>

              <Box mb={2}>
                <Typography variant="body2" color="textSecondary">
                  Preferred Language
                </Typography>
                <Chip label={farmer.preferred_language.toUpperCase()} size="small" />
              </Box>

              <Box mb={2}>
                <Typography variant="body2" color="textSecondary">
                  Timezone
                </Typography>
                <Typography variant="body1">{farmer.timezone}</Typography>
              </Box>

              <Box>
                <Typography variant="body2" color="textSecondary">
                  Registered
                </Typography>
                <Typography variant="body1">
                  {new Date(farmer.created_at).toLocaleString()}
                </Typography>
              </Box>
            </CardContent>
          </Card>
        </Grid>

        {/* Actions */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Actions
              </Typography>
              <Divider sx={{ mb: 2 }} />

              <Box display="flex" flexDirection="column" gap={2}>
                <Button
                  variant="contained"
                  color="primary"
                  startIcon={generatingAdvisory ? <CircularProgress size={20} /> : <Assessment />}
                  onClick={handleGenerateAdvisory}
                  disabled={generatingAdvisory}
                  fullWidth
                >
                  {generatingAdvisory ? 'Generating...' : 'Generate Advisory'}
                </Button>

                <Button
                  variant="contained"
                  color="success"
                  startIcon={makingCall ? <CircularProgress size={20} /> : <Phone />}
                  onClick={handleMakeCall}
                  disabled={makingCall}
                  fullWidth
                >
                  {makingCall ? 'Calling...' : 'Make Voice Call'}
                </Button>
              </Box>

              <Box mt={3}>
                <Typography variant="body2" color="textSecondary">
                  <strong>Generate Advisory:</strong> Analyzes satellite and weather data to create a personalized advisory for this farmer.
                </Typography>
                <Typography variant="body2" color="textSecondary" sx={{ mt: 1 }}>
                  <strong>Make Voice Call:</strong> Initiates a voice call to deliver the advisory in the farmer's preferred language.
                </Typography>
              </Box>
            </CardContent>
          </Card>
        </Grid>

        {/* Farm Plot Information - Placeholder */}
        <Grid item xs={12}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Farm Plots
              </Typography>
              <Divider sx={{ mb: 2 }} />
              <Typography variant="body2" color="textSecondary">
                Plot information will be displayed here once the backend API is connected.
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        {/* Advisories Section */}
        <Grid item xs={12}>
          <Card>
            <CardContent>
              <Box display="flex" justifyContent="space-between" alignItems="center" mb={2}>
                <Typography variant="h6">
                  Recent Advisories
                </Typography>
                {loadingAdvisories && <CircularProgress size={20} />}
              </Box>
              <Divider sx={{ mb: 2 }} />
              
              {advisories.length === 0 ? (
                <Typography variant="body2" color="textSecondary">
                  No advisories yet. Click "Generate Advisory" to create one.
                </Typography>
              ) : (
                <TableContainer>
                  <Table>
                    <TableHead>
                      <TableRow>
                        <TableCell>Date</TableCell>
                        <TableCell>Stress Type</TableCell>
                        <TableCell>Urgency</TableCell>
                        <TableCell>Actions</TableCell>
                        <TableCell>Expires</TableCell>
                      </TableRow>
                    </TableHead>
                    <TableBody>
                      {advisories.map((advisory) => (
                        <TableRow key={advisory.advisory_id}>
                          <TableCell>
                            {new Date(advisory.created_at).toLocaleString()}
                          </TableCell>
                          <TableCell>
                            <Chip 
                              label={advisory.stress_type.replace('_', ' ').toUpperCase()} 
                              size="small"
                              color={
                                advisory.stress_type === 'water_stress' ? 'primary' :
                                advisory.stress_type === 'heat_stress' ? 'error' :
                                'default'
                              }
                            />
                          </TableCell>
                          <TableCell>
                            <Chip 
                              label={advisory.urgency_level.toUpperCase()} 
                              size="small"
                              color={
                                advisory.urgency_level === 'critical' ? 'error' :
                                advisory.urgency_level === 'high' ? 'warning' :
                                advisory.urgency_level === 'medium' ? 'info' :
                                'default'
                              }
                            />
                          </TableCell>
                          <TableCell>
                            {advisory.actions && advisory.actions.length > 0 ? (
                              <Box>
                                {advisory.actions.map((action: any, idx: number) => (
                                  <Typography key={idx} variant="body2" sx={{ mb: 0.5 }}>
                                    {idx + 1}. {action.description} ({action.timing})
                                  </Typography>
                                ))}
                              </Box>
                            ) : (
                              <Typography variant="body2" color="textSecondary">
                                No actions
                              </Typography>
                            )}
                          </TableCell>
                          <TableCell>
                            {new Date(advisory.expires_at).toLocaleDateString()}
                          </TableCell>
                        </TableRow>
                      ))}
                    </TableBody>
                  </Table>
                </TableContainer>
              )}
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Edit Farmer Dialog */}
      <Dialog open={editDialogOpen} onClose={handleCloseEditDialog} maxWidth="sm" fullWidth>
        <DialogTitle>Edit Farmer Information</DialogTitle>
        <DialogContent>
          <Box sx={{ pt: 2 }}>
            <TextField
              select
              fullWidth
              label="Preferred Language"
              value={editLanguage}
              onChange={(e) => setEditLanguage(e.target.value)}
              sx={{ mb: 2 }}
            >
              <MenuItem value="hi">Hindi (हिन्दी)</MenuItem>
              <MenuItem value="en">English</MenuItem>
              <MenuItem value="te">Telugu (తెలుగు)</MenuItem>
              <MenuItem value="ta">Tamil (தமிழ்)</MenuItem>
              <MenuItem value="mr">Marathi (मराठी)</MenuItem>
            </TextField>

            <TextField
              select
              fullWidth
              label="Timezone"
              value={editTimezone}
              onChange={(e) => setEditTimezone(e.target.value)}
            >
              <MenuItem value="Asia/Kolkata">Asia/Kolkata (IST)</MenuItem>
              <MenuItem value="Asia/Dubai">Asia/Dubai (GST)</MenuItem>
              <MenuItem value="UTC">UTC</MenuItem>
            </TextField>
          </Box>
        </DialogContent>
        <DialogActions>
          <Button onClick={handleCloseEditDialog} disabled={updating}>
            Cancel
          </Button>
          <Button 
            onClick={handleUpdateFarmer} 
            variant="contained" 
            disabled={updating}
            startIcon={updating ? <CircularProgress size={20} /> : null}
          >
            {updating ? 'Updating...' : 'Update'}
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};
