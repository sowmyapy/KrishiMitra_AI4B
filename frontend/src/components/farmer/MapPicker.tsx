import { useEffect, useState } from 'react';
import { Box, Typography, TextField, Button, Alert } from '@mui/material';
import { MapContainer, TileLayer, Marker, useMapEvents } from 'react-leaflet';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';

// Fix Leaflet default marker icon
import icon from 'leaflet/dist/images/marker-icon.png';
import iconShadow from 'leaflet/dist/images/marker-shadow.png';

const DefaultIcon = L.icon({
  iconUrl: icon,
  shadowUrl: iconShadow,
  iconSize: [25, 41],
  iconAnchor: [12, 41],
});

L.Marker.prototype.options.icon = DefaultIcon;

interface MapPickerProps {
  value: { lat: number; lng: number } | null;
  onChange: (location: { lat: number; lng: number }) => void;
  error?: string;
}

function LocationMarker({ position, setPosition }: any) {
  useMapEvents({
    click(e) {
      setPosition(e.latlng);
    },
  });

  return position === null ? null : <Marker position={position} />;
}

export const MapPicker: React.FC<MapPickerProps> = ({ value, onChange, error }) => {
  const [position, setPosition] = useState<L.LatLng | null>(
    value ? L.latLng(value.lat, value.lng) : null
  );
  const [manualLat, setManualLat] = useState(value?.lat.toString() || '');
  const [manualLng, setManualLng] = useState(value?.lng.toString() || '');

  useEffect(() => {
    if (position) {
      onChange({ lat: position.lat, lng: position.lng });
      setManualLat(position.lat.toFixed(6));
      setManualLng(position.lng.toFixed(6));
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
        },
        (error) => {
          console.error('Error getting location:', error);
          alert('Could not get your location. Please enter coordinates manually.');
        }
      );
    } else {
      alert('Geolocation is not supported by your browser.');
    }
  };

  return (
    <Box>
      <Typography variant="subtitle2" gutterBottom>
        Farm Location *
      </Typography>

      <Box display="flex" gap={2} mb={2}>
        <TextField
          label="Latitude"
          value={manualLat}
          onChange={(e) => setManualLat(e.target.value)}
          size="small"
          fullWidth
          error={!!error}
        />
        <TextField
          label="Longitude"
          value={manualLng}
          onChange={(e) => setManualLng(e.target.value)}
          size="small"
          fullWidth
          error={!!error}
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

      <Box sx={{ height: 400, border: '1px solid #ccc', borderRadius: 1, mb: 1 }}>
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
        <Typography variant="caption" color="textSecondary">
          Selected: {position.lat.toFixed(6)}, {position.lng.toFixed(6)}
        </Typography>
      )}

      {error && (
        <Alert severity="error" sx={{ mt: 1 }}>
          {error}
        </Alert>
      )}
    </Box>
  );
};
