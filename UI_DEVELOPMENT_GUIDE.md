# KrishiMitra UI - Development Guide

## Phase 1: Core Components (Day 1-2)

### 1.1 Create Layout Components

#### Header Component

Create `src/components/common/Header.tsx`:

```typescript
import { AppBar, Toolbar, Typography, IconButton, Badge, Box } from '@mui/material';
import { Notifications, AccountCircle, Menu as MenuIcon } from '@mui/icons-material';

interface HeaderProps {
  onMenuClick: () => void;
}

export const Header: React.FC<HeaderProps> = ({ onMenuClick }) => {
  return (
    <AppBar position="fixed" sx={{ zIndex: (theme) => theme.zIndex.drawer + 1 }}>
      <Toolbar>
        <IconButton
          color="inherit"
          edge="start"
          onClick={onMenuClick}
          sx={{ mr: 2, display: { sm: 'none' } }}
        >
          <MenuIcon />
        </IconButton>
        
        <Typography variant="h6" noWrap component="div" sx={{ flexGrow: 1 }}>
          🌾 KrishiMitra
        </Typography>

        <IconButton color="inherit">
          <Badge badgeContent={3} color="error">
            <Notifications />
          </Badge>
        </IconButton>

        <IconButton color="inherit">
          <AccountCircle />
        </IconButton>
      </Toolbar>
    </AppBar>
  );
};
```

#### Sidebar Component

Create `src/components/common/Sidebar.tsx`:

```typescript
import {
  Drawer,
  List,
  ListItem,
  ListItemButton,
  ListItemIcon,
  ListItemText,
  Toolbar,
  Box,
} from '@mui/material';
import {
  Dashboard,
  People,
  Assignment,
  Satellite,
  Analytics,
  Settings,
} from '@mui/icons-material';
import { useNavigate, useLocation } from 'react-router-dom';

const DRAWER_WIDTH = 240;

const menuItems = [
  { text: 'Dashboard', icon: <Dashboard />, path: '/' },
  { text: 'Farmers', icon: <People />, path: '/farmers' },
  { text: 'Advisories', icon: <Assignment />, path: '/advisories' },
  { text: 'Monitoring', icon: <Satellite />, path: '/monitoring' },
  { text: 'Analytics', icon: <Analytics />, path: '/analytics' },
  { text: 'Settings', icon: <Settings />, path: '/settings' },
];

interface SidebarProps {
  mobileOpen: boolean;
  onClose: () => void;
}

export const Sidebar: React.FC<SidebarProps> = ({ mobileOpen, onClose }) => {
  const navigate = useNavigate();
  const location = useLocation();

  const drawer = (
    <Box>
      <Toolbar />
      <List>
        {menuItems.map((item) => (
          <ListItem key={item.text} disablePadding>
            <ListItemButton
              selected={location.pathname === item.path}
              onClick={() => {
                navigate(item.path);
                onClose();
              }}
            >
              <ListItemIcon>{item.icon}</ListItemIcon>
              <ListItemText primary={item.text} />
            </ListItemButton>
          </ListItem>
        ))}
      </List>
    </Box>
  );

  return (
    <Box
      component="nav"
      sx={{ width: { sm: DRAWER_WIDTH }, flexShrink: { sm: 0 } }}
    >
      {/* Mobile drawer */}
      <Drawer
        variant="temporary"
        open={mobileOpen}
        onClose={onClose}
        ModalProps={{ keepMounted: true }}
        sx={{
          display: { xs: 'block', sm: 'none' },
          '& .MuiDrawer-paper': { boxSizing: 'border-box', width: DRAWER_WIDTH },
        }}
      >
        {drawer}
      </Drawer>

      {/* Desktop drawer */}
      <Drawer
        variant="permanent"
        sx={{
          display: { xs: 'none', sm: 'block' },
          '& .MuiDrawer-paper': { boxSizing: 'border-box', width: DRAWER_WIDTH },
        }}
        open
      >
        {drawer}
      </Drawer>
    </Box>
  );
};
```

#### Main Layout

Create `src/components/common/Layout.tsx`:

```typescript
import { useState } from 'react';
import { Box, Toolbar } from '@mui/material';
import { Header } from './Header';
import { Sidebar } from './Sidebar';

interface LayoutProps {
  children: React.ReactNode;
}

export const Layout: React.FC<LayoutProps> = ({ children }) => {
  const [mobileOpen, setMobileOpen] = useState(false);

  const handleDrawerToggle = () => {
    setMobileOpen(!mobileOpen);
  };

  return (
    <Box sx={{ display: 'flex' }}>
      <Header onMenuClick={handleDrawerToggle} />
      <Sidebar mobileOpen={mobileOpen} onClose={handleDrawerToggle} />
      
      <Box
        component="main"
        sx={{
          flexGrow: 1,
          p: 3,
          width: { sm: `calc(100% - 240px)` },
          minHeight: '100vh',
          backgroundColor: 'background.default',
        }}
      >
        <Toolbar />
        {children}
      </Box>
    </Box>
  );
};
```

### 1.2 Create Dashboard Components

#### Stats Card

Create `src/components/dashboard/StatsCard.tsx`:

```typescript
import { Card, CardContent, Typography, Box } from '@mui/material';
import { SvgIconComponent } from '@mui/icons-material';

interface StatsCardProps {
  title: string;
  value: string | number;
  icon: React.ReactElement<SvgIconComponent>;
  color: string;
  subtitle?: string;
}

export const StatsCard: React.FC<StatsCardProps> = ({
  title,
  value,
  icon,
  color,
  subtitle,
}) => {
  return (
    <Card>
      <CardContent>
        <Box display="flex" justifyContent="space-between" alignItems="center">
          <Box>
            <Typography color="textSecondary" gutterBottom variant="body2">
              {title}
            </Typography>
            <Typography variant="h4" component="div">
              {value}
            </Typography>
            {subtitle && (
              <Typography variant="body2" color="textSecondary">
                {subtitle}
              </Typography>
            )}
          </Box>
          <Box
            sx={{
              backgroundColor: color,
              borderRadius: 2,
              p: 2,
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
};
```

### 1.3 Create API Hooks

#### Farmers Hook

Create `src/hooks/useFarmers.ts`:

```typescript
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { apiClient } from '@/api/client';
import { Farmer } from '@/types/farmer';

export const useFarmers = () => {
  return useQuery({
    queryKey: ['farmers'],
    queryFn: async () => {
      const response = await apiClient.get<Farmer[]>('/farmers/');
      return response.data;
    },
  });
};

export const useFarmer = (farmerId: string) => {
  return useQuery({
    queryKey: ['farmer', farmerId],
    queryFn: async () => {
      const response = await apiClient.get<Farmer>(`/farmers/${farmerId}`);
      return response.data;
    },
    enabled: !!farmerId,
  });
};

export const useCreateFarmer = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (farmer: Partial<Farmer>) => {
      const response = await apiClient.post<Farmer>('/farmers/', farmer);
      return response.data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['farmers'] });
    },
  });
};
```

#### Advisories Hook

Create `src/hooks/useAdvisories.ts`:

```typescript
import { useQuery } from '@tanstack/react-query';
import { apiClient } from '@/api/client';
import { Advisory } from '@/types/advisory';

export const useAdvisories = (filters?: {
  farmerId?: string;
  status?: string;
  limit?: number;
}) => {
  return useQuery({
    queryKey: ['advisories', filters],
    queryFn: async () => {
      const response = await apiClient.get<Advisory[]>('/advisories/', {
        params: filters,
      });
      return response.data;
    },
  });
};

export const useAdvisory = (advisoryId: string) => {
  return useQuery({
    queryKey: ['advisory', advisoryId],
    queryFn: async () => {
      const response = await apiClient.get<Advisory>(`/advisories/${advisoryId}`);
      return response.data;
    },
    enabled: !!advisoryId,
  });
};
```

## Phase 2: Dashboard Page (Day 3)

Create `src/pages/Dashboard.tsx`:

```typescript
import { Grid, Typography, Box, Card, CardContent } from '@mui/material';
import { People, Assignment, Warning, CheckCircle } from '@mui/icons-material';
import { StatsCard } from '@/components/dashboard/StatsCard';
import { useFarmers } from '@/hooks/useFarmers';
import { useAdvisories } from '@/hooks/useAdvisories';

export const Dashboard = () => {
  const { data: farmers, isLoading: farmersLoading } = useFarmers();
  const { data: advisories, isLoading: advisoriesLoading } = useAdvisories({ limit: 10 });

  if (farmersLoading || advisoriesLoading) {
    return <Typography>Loading...</Typography>;
  }

  const activeAdvisories = advisories?.filter(a => a.status === 'sent').length || 0;
  const criticalAlerts = advisories?.filter(a => a.risk_score > 70).length || 0;

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
            icon={<People sx={{ color: 'white' }} />}
            color="#2E7D32"
            subtitle="+12 this month"
          />
        </Grid>

        <Grid item xs={12} sm={6} md={3}>
          <StatsCard
            title="Active Advisories"
            value={activeAdvisories}
            icon={<Assignment sx={{ color: 'white' }} />}
            color="#2196F3"
            subtitle="Last 7 days"
          />
        </Grid>

        <Grid item xs={12} sm={6} md={3}>
          <StatsCard
            title="Critical Alerts"
            value={criticalAlerts}
            icon={<Warning sx={{ color: 'white' }} />}
            color="#F44336"
            subtitle="Requires attention"
          />
        </Grid>

        <Grid item xs={12} sm={6} md={3}>
          <StatsCard
            title="System Health"
            value="98%"
            icon={<CheckCircle sx={{ color: 'white' }} />}
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
                Recent Advisories
              </Typography>
              {advisories?.slice(0, 5).map((advisory) => (
                <Box
                  key={advisory.advisory_id}
                  sx={{
                    p: 2,
                    mb: 1,
                    border: '1px solid #e0e0e0',
                    borderRadius: 1,
                  }}
                >
                  <Typography variant="subtitle1">
                    {advisory.stress_type}
                  </Typography>
                  <Typography variant="body2" color="textSecondary">
                    Risk: {advisory.risk_score}/100 | Cost: ₹{advisory.total_cost}
                  </Typography>
                </Box>
              ))}
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={4}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Quick Actions
              </Typography>
              {/* Add quick action buttons here */}
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Box>
  );
};
```

## Phase 3: Farmers Page (Day 4)

Create `src/pages/Farmers.tsx`:

```typescript
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
    return <Typography>Loading...</Typography>;
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
            {filteredFarmers?.map((farmer) => (
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
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    </Box>
  );
};
```

## Phase 4: Routing Setup

Update `src/App.tsx`:

```typescript
import { ThemeProvider } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { SnackbarProvider } from 'notistack';
import { theme } from './theme';
import { Layout } from './components/common/Layout';
import { Dashboard } from './pages/Dashboard';
import { Farmers } from './pages/Farmers';

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      refetchOnWindowFocus: false,
      retry: 1,
    },
  },
});

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <ThemeProvider theme={theme}>
        <CssBaseline />
        <SnackbarProvider maxSnack={3}>
          <BrowserRouter>
            <Layout>
              <Routes>
                <Route path="/" element={<Dashboard />} />
                <Route path="/farmers" element={<Farmers />} />
                {/* Add more routes as you build pages */}
              </Routes>
            </Layout>
          </BrowserRouter>
        </SnackbarProvider>
      </ThemeProvider>
    </QueryClientProvider>
  );
}

export default App;
```

## Development Workflow

```bash
# Terminal 1: Backend
cd C:\Users\Sowmya\OneDrive\projects\ai_crop_system
.\venv\Scripts\activate
uvicorn src.main:app --reload

# Terminal 2: Frontend
cd C:\Users\Sowmya\OneDrive\projects\ai_crop_system\frontend
npm run dev
```

## Testing Your Progress

1. **Dashboard**: http://localhost:3000/
   - Should show stats cards
   - Should display recent advisories

2. **Farmers**: http://localhost:3000/farmers
   - Should show farmers table
   - Should have search functionality

## Next Steps

1. **Add more pages**: Advisories, Monitoring, Analytics
2. **Add forms**: Create/Edit farmer, Create advisory
3. **Add maps**: Leaflet integration for plot visualization
4. **Add charts**: Recharts for analytics
5. **Add authentication**: Login/logout functionality

## Common Issues

### CORS Errors
Add CORS middleware to backend `src/main.py`:
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### API Connection Issues
Check proxy in `vite.config.ts` and ensure backend is running.

---

**Ready to continue?** Build more pages and components following this pattern!
