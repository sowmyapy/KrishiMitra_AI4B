import { useState } from 'react';
import {
  Box,
  Typography,
  Button,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  IconButton,
  TextField,
  InputAdornment,
  CircularProgress,
} from '@mui/material';
import { Add, Search, Edit, Visibility } from '@mui/icons-material';
import { useFarmers } from '@/hooks/useFarmers';
import { useNavigate } from 'react-router-dom';

export const Farmers = () => {
  const { data: farmers, isLoading } = useFarmers();
  const navigate = useNavigate();
  const [searchTerm, setSearchTerm] = useState('');

  const filteredFarmers = farmers?.filter((farmer) =>
    farmer.phone_number.includes(searchTerm)
  );

  if (isLoading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="400px">
        <CircularProgress />
      </Box>
    );
  }

  return (
    <Box>
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
        <Typography variant="h4">Farmers</Typography>
        <Button
          variant="contained"
          startIcon={<Add />}
          onClick={() => navigate('/farmers/new')}
        >
          Add Farmer
        </Button>
      </Box>

      <Box mb={3}>
        <TextField
          fullWidth
          placeholder="Search by phone number..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          InputProps={{
            startAdornment: (
              <InputAdornment position="start">
                <Search />
              </InputAdornment>
            ),
          }}
        />
      </Box>

      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Phone Number</TableCell>
              <TableCell>Language</TableCell>
              <TableCell>Timezone</TableCell>
              <TableCell>Registered</TableCell>
              <TableCell align="right">Actions</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {filteredFarmers && filteredFarmers.length > 0 ? (
              filteredFarmers.map((farmer) => (
                <TableRow key={farmer.farmer_id}>
                  <TableCell>{farmer.phone_number}</TableCell>
                  <TableCell>{farmer.preferred_language}</TableCell>
                  <TableCell>{farmer.timezone}</TableCell>
                  <TableCell>
                    {new Date(farmer.created_at).toLocaleDateString()}
                  </TableCell>
                  <TableCell align="right">
                    <IconButton
                      size="small"
                      onClick={() => navigate(`/farmers/${farmer.farmer_id}`)}
                    >
                      <Visibility />
                    </IconButton>
                    <IconButton
                      size="small"
                      onClick={() => navigate(`/farmers/${farmer.farmer_id}/edit`)}
                    >
                      <Edit />
                    </IconButton>
                  </TableCell>
                </TableRow>
              ))
            ) : (
              <TableRow>
                <TableCell colSpan={5} align="center">
                  <Typography color="textSecondary">
                    No farmers found. Click "Add Farmer" to register a new farmer.
                  </Typography>
                </TableCell>
              </TableRow>
            )}
          </TableBody>
        </Table>
      </TableContainer>
    </Box>
  );
};
