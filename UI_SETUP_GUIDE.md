# KrishiMitra UI - Setup Guide

## Prerequisites

- Node.js 18+ installed
- npm or yarn package manager
- KrishiMitra backend running on http://localhost:8000

## Step 1: Create React + Vite Project

```bash
# Navigate to project root
cd C:\Users\Sowmya\OneDrive\projects\ai_crop_system

# Create frontend directory
npm create vite@latest frontend -- --template react-ts

# Navigate to frontend
cd frontend

# Install dependencies
npm install
```

## Step 2: Install Required Packages

```bash
# UI Framework
npm install @mui/material @emotion/react @emotion/styled

# Icons
npm install @mui/icons-material

# Routing
npm install react-router-dom

# API Client
npm install axios

# Data Fetching
npm install @tanstack/react-query

# Forms
npm install react-hook-form @hookform/resolvers zod

# Maps
npm install leaflet react-leaflet
npm install -D @types/leaflet

# Charts
npm install recharts

# Date Handling
npm install date-fns

# Notifications
npm install notistack

# Internationalization
npm install react-i18next i18next

# Development Tools
npm install -D @types/node
```

## Step 3: Project Structure

Create the following directory structure:

```bash
# Create directories
mkdir -p src/api
mkdir -p src/components/common
mkdir -p src/components/dashboard
mkdir -p src/components/farmer
mkdir -p src/components/advisory
mkdir -p src/pages
mkdir -p src/hooks
mkdir -p src/contexts
mkdir -p src/utils
mkdir -p src/types
mkdir -p public/assets
```

## Step 4: Configure Vite

Update `vite.config.ts`:

```typescript
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import path from 'path'

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
  server: {
    port: 3000,
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
    },
  },
})
```

## Step 5: Configure TypeScript

Update `tsconfig.json`:

```json
{
  "compilerOptions": {
    "target": "ES2020",
    "useDefineForClassFields": true,
    "lib": ["ES2020", "DOM", "DOM.Iterable"],
    "module": "ESNext",
    "skipLibCheck": true,
    "moduleResolution": "bundler",
    "allowImportingTsExtensions": true,
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true,
    "jsx": "react-jsx",
    "strict": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noFallthroughCasesInSwitch": true,
    "baseUrl": ".",
    "paths": {
      "@/*": ["./src/*"]
    }
  },
  "include": ["src"],
  "references": [{ "path": "./tsconfig.node.json" }]
}
```

## Step 6: Create Environment Configuration

Create `.env` file in frontend directory:

```env
VITE_API_BASE_URL=http://localhost:8000
VITE_APP_NAME=KrishiMitra
VITE_GOOGLE_MAPS_API_KEY=your_google_maps_key
```

Create `.env.example`:

```env
VITE_API_BASE_URL=http://localhost:8000
VITE_APP_NAME=KrishiMitra
VITE_GOOGLE_MAPS_API_KEY=
```

## Step 7: Create Theme Configuration

Create `src/theme.ts`:

```typescript
import { createTheme } from '@mui/material/styles';

export const theme = createTheme({
  palette: {
    primary: {
      main: '#2E7D32', // Green
      light: '#60AD5E',
      dark: '#005005',
    },
    secondary: {
      main: '#FF6F00', // Orange
      light: '#FFA040',
      dark: '#C43E00',
    },
    success: {
      main: '#4CAF50',
    },
    warning: {
      main: '#FFC107',
    },
    error: {
      main: '#F44336',
    },
    info: {
      main: '#2196F3',
    },
    background: {
      default: '#F5F5F5',
      paper: '#FFFFFF',
    },
  },
  typography: {
    fontFamily: '"Roboto", "Helvetica", "Arial", sans-serif',
    h1: {
      fontSize: '2.5rem',
      fontWeight: 600,
    },
    h2: {
      fontSize: '2rem',
      fontWeight: 600,
    },
    h3: {
      fontSize: '1.75rem',
      fontWeight: 600,
    },
    h4: {
      fontSize: '1.5rem',
      fontWeight: 600,
    },
    h5: {
      fontSize: '1.25rem',
      fontWeight: 600,
    },
    h6: {
      fontSize: '1rem',
      fontWeight: 600,
    },
  },
  components: {
    MuiButton: {
      styleOverrides: {
        root: {
          textTransform: 'none',
          borderRadius: 8,
        },
      },
    },
    MuiCard: {
      styleOverrides: {
        root: {
          borderRadius: 12,
          boxShadow: '0 2px 8px rgba(0,0,0,0.1)',
        },
      },
    },
  },
});
```

## Step 8: Create API Client

Create `src/api/client.ts`:

```typescript
import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

export const apiClient = axios.create({
  baseURL: `${API_BASE_URL}/api/v1`,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor for adding auth token
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor for handling errors
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Handle unauthorized - redirect to login
      localStorage.removeItem('access_token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);
```

## Step 9: Create Type Definitions

Create `src/types/farmer.ts`:

```typescript
export interface Farmer {
  farmer_id: string;
  phone_number: string;
  preferred_language: string;
  timezone: string;
  created_at: string;
  updated_at: string;
}

export interface Plot {
  plot_id: string;
  farmer_id: string;
  latitude: number;
  longitude: number;
  area_hectares: number;
  crop_types: string[];
  planting_date: string;
  created_at: string;
}
```

Create `src/types/advisory.ts`:

```typescript
export interface Advisory {
  advisory_id: string;
  farmer_id: string;
  plot_id: string;
  stress_type: string;
  risk_score: number;
  confidence: number;
  actions: Action[];
  total_cost: number;
  created_at: string;
  status: 'pending' | 'sent' | 'delivered' | 'failed';
}

export interface Action {
  action: string;
  priority: 'high' | 'medium' | 'low';
  cost: number;
  timeframe: string;
}
```

## Step 10: Update Main App

Update `src/App.tsx`:

```typescript
import { ThemeProvider } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { BrowserRouter } from 'react-router-dom';
import { SnackbarProvider } from 'notistack';
import { theme } from './theme';

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
            <div>
              <h1>KrishiMitra Dashboard</h1>
              <p>UI Coming Soon...</p>
            </div>
          </BrowserRouter>
        </SnackbarProvider>
      </ThemeProvider>
    </QueryClientProvider>
  );
}

export default App;
```

## Step 11: Update Package.json Scripts

Update `package.json`:

```json
{
  "scripts": {
    "dev": "vite",
    "build": "tsc && vite build",
    "preview": "vite preview",
    "lint": "eslint . --ext ts,tsx --report-unused-disable-directives --max-warnings 0",
    "type-check": "tsc --noEmit"
  }
}
```

## Step 12: Start Development Server

```bash
# Make sure backend is running first
# In backend terminal:
cd C:\Users\Sowmya\OneDrive\projects\ai_crop_system
.\venv\Scripts\activate
uvicorn src.main:app --reload

# In frontend terminal:
cd C:\Users\Sowmya\OneDrive\projects\ai_crop_system\frontend
npm run dev
```

Open browser to: http://localhost:3000

## Step 13: Verify Setup

You should see:
- ✅ Vite dev server running on port 3000
- ✅ Material-UI theme applied
- ✅ "KrishiMitra Dashboard" heading
- ✅ No console errors

## Project Structure After Setup

```
frontend/
├── node_modules/
├── public/
│   └── vite.svg
├── src/
│   ├── api/
│   │   └── client.ts
│   ├── components/
│   │   ├── common/
│   │   ├── dashboard/
│   │   ├── farmer/
│   │   └── advisory/
│   ├── pages/
│   ├── hooks/
│   ├── contexts/
│   ├── utils/
│   ├── types/
│   │   ├── farmer.ts
│   │   └── advisory.ts
│   ├── App.tsx
│   ├── main.tsx
│   ├── theme.ts
│   └── vite-env.d.ts
├── .env
├── .env.example
├── .gitignore
├── index.html
├── package.json
├── tsconfig.json
├── tsconfig.node.json
└── vite.config.ts
```

## Common Issues

### Port 3000 Already in Use
```bash
# Change port in vite.config.ts
server: {
  port: 3001,
}
```

### Module Not Found Errors
```bash
# Clear node_modules and reinstall
rm -rf node_modules package-lock.json
npm install
```

### TypeScript Errors
```bash
# Check TypeScript configuration
npm run type-check
```

### API Connection Issues
```bash
# Verify backend is running
curl http://localhost:8000/

# Check proxy configuration in vite.config.ts
```

## Next Steps

1. **Create Components**: Follow `UI_DEVELOPMENT_GUIDE.md`
2. **Implement Pages**: Build dashboard, farmers, advisories pages
3. **Add Authentication**: Implement login/logout
4. **Test**: Follow `UI_TESTING_GUIDE.md`

## Development Workflow

```bash
# Start backend (Terminal 1)
cd C:\Users\Sowmya\OneDrive\projects\ai_crop_system
.\venv\Scripts\activate
uvicorn src.main:app --reload

# Start frontend (Terminal 2)
cd C:\Users\Sowmya\OneDrive\projects\ai_crop_system\frontend
npm run dev

# Open browser
http://localhost:3000
```

---

**Setup complete!** Ready to build components? See `UI_DEVELOPMENT_GUIDE.md`
