import { useState } from 'react';
import {
  Box,
  Typography,
  Card,
  CardContent,
  Grid,
  TextField,
  Button,
  Divider,
  Alert,
  Tabs,
  Tab,
  Switch,
  FormControlLabel,
  MenuItem,
} from '@mui/material';
import { Save, Refresh } from '@mui/icons-material';

interface TabPanelProps {
  children?: React.ReactNode;
  index: number;
  value: number;
}

function TabPanel(props: TabPanelProps) {
  const { children, value, index, ...other } = props;
  return (
    <div hidden={value !== index} {...other}>
      {value === index && <Box sx={{ pt: 3 }}>{children}</Box>}
    </div>
  );
}

export const Settings = () => {
  const [activeTab, setActiveTab] = useState(0);
  const [message, setMessage] = useState<{ type: 'success' | 'error'; text: string } | null>(null);

  // API Keys
  const [twilioSid, setTwilioSid] = useState('AC675ef23df325351b1b8f8a7b6e67635c');
  const [twilioToken, setTwilioToken] = useState('••••••••••••••••');
  const [twilioPhone, setTwilioPhone] = useState('+17752270557');
  const [sentinelId, setSentinelId] = useState('5337ed74-d518-4795-b31a-3b5546d0cefd');
  const [sentinelSecret, setSentinelSecret] = useState('••••••••••••••••');
  const [weatherKey, setWeatherKey] = useState('9cb097bad8ee1c0e5e6e3f4a0b3ebc5b');

  // System Parameters
  const [refreshInterval, setRefreshInterval] = useState('300');
  const [ndviThreshold, setNdviThreshold] = useState('0.5');
  const [riskThreshold, setRiskThreshold] = useState('70');
  const [advisoryExpiry, setAdvisoryExpiry] = useState('7');

  // Notifications
  const [emailNotifications, setEmailNotifications] = useState(true);
  const [smsNotifications, setSmsNotifications] = useState(false);
  const [criticalAlerts, setCriticalAlerts] = useState(true);

  // Preferences
  const [defaultLanguage, setDefaultLanguage] = useState('hi');
  const [timezone, setTimezone] = useState('Asia/Kolkata');
  const [dateFormat, setDateFormat] = useState('DD/MM/YYYY');

  const handleSave = () => {
    setMessage({ type: 'success', text: 'Settings saved successfully!' });
    setTimeout(() => setMessage(null), 3000);
  };

  const handleReset = () => {
    setMessage({ type: 'success', text: 'Settings reset to defaults!' });
    setTimeout(() => setMessage(null), 3000);
  };

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        System Settings
      </Typography>
      <Typography color="textSecondary" paragraph>
        Configure system parameters, API keys, and preferences
      </Typography>

      {message && (
        <Alert severity={message.type} sx={{ mb: 3 }} onClose={() => setMessage(null)}>
          {message.text}
        </Alert>
      )}

      <Card>
        <Box sx={{ borderBottom: 1, borderColor: 'divider' }}>
          <Tabs value={activeTab} onChange={(_, newValue) => setActiveTab(newValue)}>
            <Tab label="API Keys" />
            <Tab label="System Parameters" />
            <Tab label="Notifications" />
            <Tab label="Preferences" />
          </Tabs>
        </Box>

        <CardContent>
          {/* API Keys Tab */}
          <TabPanel value={activeTab} index={0}>
            <Grid container spacing={3}>
              <Grid item xs={12}>
                <Typography variant="h6" gutterBottom>
                  Twilio Configuration
                </Typography>
                <Divider sx={{ mb: 2 }} />
              </Grid>
              <Grid item xs={12} md={6}>
                <TextField
                  fullWidth
                  label="Account SID"
                  value={twilioSid}
                  onChange={(e) => setTwilioSid(e.target.value)}
                  helperText="Your Twilio Account SID"
                />
              </Grid>
              <Grid item xs={12} md={6}>
                <TextField
                  fullWidth
                  label="Auth Token"
                  type="password"
                  value={twilioToken}
                  onChange={(e) => setTwilioToken(e.target.value)}
                  helperText="Your Twilio Auth Token"
                />
              </Grid>
              <Grid item xs={12} md={6}>
                <TextField
                  fullWidth
                  label="Phone Number"
                  value={twilioPhone}
                  onChange={(e) => setTwilioPhone(e.target.value)}
                  helperText="Twilio phone number with country code"
                />
              </Grid>

              <Grid item xs={12} sx={{ mt: 3 }}>
                <Typography variant="h6" gutterBottom>
                  Sentinel Hub Configuration
                </Typography>
                <Divider sx={{ mb: 2 }} />
              </Grid>
              <Grid item xs={12} md={6}>
                <TextField
                  fullWidth
                  label="Client ID"
                  value={sentinelId}
                  onChange={(e) => setSentinelId(e.target.value)}
                  helperText="Sentinel Hub Client ID"
                />
              </Grid>
              <Grid item xs={12} md={6}>
                <TextField
                  fullWidth
                  label="Client Secret"
                  type="password"
                  value={sentinelSecret}
                  onChange={(e) => setSentinelSecret(e.target.value)}
                  helperText="Sentinel Hub Client Secret"
                />
              </Grid>

              <Grid item xs={12} sx={{ mt: 3 }}>
                <Typography variant="h6" gutterBottom>
                  Weather API Configuration
                </Typography>
                <Divider sx={{ mb: 2 }} />
              </Grid>
              <Grid item xs={12} md={6}>
                <TextField
                  fullWidth
                  label="OpenWeatherMap API Key"
                  value={weatherKey}
                  onChange={(e) => setWeatherKey(e.target.value)}
                  helperText="Your OpenWeatherMap API key"
                />
              </Grid>
            </Grid>
          </TabPanel>

          {/* System Parameters Tab */}
          <TabPanel value={activeTab} index={1}>
            <Grid container spacing={3}>
              <Grid item xs={12}>
                <Typography variant="h6" gutterBottom>
                  Data Refresh Settings
                </Typography>
                <Divider sx={{ mb: 2 }} />
              </Grid>
              <Grid item xs={12} md={6}>
                <TextField
                  fullWidth
                  label="Refresh Interval (seconds)"
                  type="number"
                  value={refreshInterval}
                  onChange={(e) => setRefreshInterval(e.target.value)}
                  helperText="How often to refresh satellite/weather data"
                />
              </Grid>

              <Grid item xs={12} sx={{ mt: 3 }}>
                <Typography variant="h6" gutterBottom>
                  Threshold Settings
                </Typography>
                <Divider sx={{ mb: 2 }} />
              </Grid>
              <Grid item xs={12} md={4}>
                <TextField
                  fullWidth
                  label="NDVI Threshold"
                  type="number"
                  value={ndviThreshold}
                  onChange={(e) => setNdviThreshold(e.target.value)}
                  helperText="Minimum healthy NDVI value (0-1)"
                  inputProps={{ step: 0.1, min: 0, max: 1 }}
                />
              </Grid>
              <Grid item xs={12} md={4}>
                <TextField
                  fullWidth
                  label="Risk Threshold (%)"
                  type="number"
                  value={riskThreshold}
                  onChange={(e) => setRiskThreshold(e.target.value)}
                  helperText="Risk score for critical alerts"
                  inputProps={{ min: 0, max: 100 }}
                />
              </Grid>
              <Grid item xs={12} md={4}>
                <TextField
                  fullWidth
                  label="Advisory Expiry (days)"
                  type="number"
                  value={advisoryExpiry}
                  onChange={(e) => setAdvisoryExpiry(e.target.value)}
                  helperText="Days until advisory expires"
                  inputProps={{ min: 1, max: 30 }}
                />
              </Grid>
            </Grid>
          </TabPanel>

          {/* Notifications Tab */}
          <TabPanel value={activeTab} index={2}>
            <Grid container spacing={3}>
              <Grid item xs={12}>
                <Typography variant="h6" gutterBottom>
                  Notification Preferences
                </Typography>
                <Divider sx={{ mb: 2 }} />
              </Grid>
              <Grid item xs={12}>
                <FormControlLabel
                  control={
                    <Switch
                      checked={emailNotifications}
                      onChange={(e) => setEmailNotifications(e.target.checked)}
                    />
                  }
                  label="Email Notifications"
                />
                <Typography variant="body2" color="textSecondary" sx={{ ml: 4 }}>
                  Receive email notifications for new advisories
                </Typography>
              </Grid>
              <Grid item xs={12}>
                <FormControlLabel
                  control={
                    <Switch
                      checked={smsNotifications}
                      onChange={(e) => setSmsNotifications(e.target.checked)}
                    />
                  }
                  label="SMS Notifications"
                />
                <Typography variant="body2" color="textSecondary" sx={{ ml: 4 }}>
                  Receive SMS alerts for critical issues
                </Typography>
              </Grid>
              <Grid item xs={12}>
                <FormControlLabel
                  control={
                    <Switch
                      checked={criticalAlerts}
                      onChange={(e) => setCriticalAlerts(e.target.checked)}
                    />
                  }
                  label="Critical Alerts"
                />
                <Typography variant="body2" color="textSecondary" sx={{ ml: 4 }}>
                  Immediate alerts for critical crop stress
                </Typography>
              </Grid>
            </Grid>
          </TabPanel>

          {/* Preferences Tab */}
          <TabPanel value={activeTab} index={3}>
            <Grid container spacing={3}>
              <Grid item xs={12}>
                <Typography variant="h6" gutterBottom>
                  Regional Settings
                </Typography>
                <Divider sx={{ mb: 2 }} />
              </Grid>
              <Grid item xs={12} md={4}>
                <TextField
                  select
                  fullWidth
                  label="Default Language"
                  value={defaultLanguage}
                  onChange={(e) => setDefaultLanguage(e.target.value)}
                >
                  <MenuItem value="hi">Hindi</MenuItem>
                  <MenuItem value="en">English</MenuItem>
                  <MenuItem value="ta">Tamil</MenuItem>
                  <MenuItem value="te">Telugu</MenuItem>
                  <MenuItem value="mr">Marathi</MenuItem>
                </TextField>
              </Grid>
              <Grid item xs={12} md={4}>
                <TextField
                  select
                  fullWidth
                  label="Timezone"
                  value={timezone}
                  onChange={(e) => setTimezone(e.target.value)}
                >
                  <MenuItem value="Asia/Kolkata">Asia/Kolkata (IST)</MenuItem>
                  <MenuItem value="Asia/Dubai">Asia/Dubai (GST)</MenuItem>
                  <MenuItem value="UTC">UTC</MenuItem>
                </TextField>
              </Grid>
              <Grid item xs={12} md={4}>
                <TextField
                  select
                  fullWidth
                  label="Date Format"
                  value={dateFormat}
                  onChange={(e) => setDateFormat(e.target.value)}
                >
                  <MenuItem value="DD/MM/YYYY">DD/MM/YYYY</MenuItem>
                  <MenuItem value="MM/DD/YYYY">MM/DD/YYYY</MenuItem>
                  <MenuItem value="YYYY-MM-DD">YYYY-MM-DD</MenuItem>
                </TextField>
              </Grid>
            </Grid>
          </TabPanel>

          {/* Action Buttons */}
          <Box sx={{ mt: 4, display: 'flex', gap: 2, justifyContent: 'flex-end' }}>
            <Button
              variant="outlined"
              startIcon={<Refresh />}
              onClick={handleReset}
            >
              Reset to Defaults
            </Button>
            <Button
              variant="contained"
              startIcon={<Save />}
              onClick={handleSave}
            >
              Save Changes
            </Button>
          </Box>
        </CardContent>
      </Card>
    </Box>
  );
};
