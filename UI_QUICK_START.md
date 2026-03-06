# KrishiMitra UI - Quick Start Guide

## 🚀 Fastest Way to Get Started

### Option 1: Automated Setup (Recommended)

```powershell
# Run the setup script
cd C:\Users\Sowmya\OneDrive\projects\ai_crop_system
.\setup_ui.ps1
```

This will:
- ✅ Create frontend project with Vite + React + TypeScript
- ✅ Install all dependencies
- ✅ Create directory structure
- ✅ Set up environment variables
- ✅ Optionally start dev server

### Option 2: Manual Setup

Follow the detailed guide: `UI_SETUP_GUIDE.md`

## 📋 Prerequisites

- ✅ Node.js 18+ installed
- ✅ npm or yarn
- ✅ Backend running on http://localhost:8000

Check Node.js:
```bash
node --version  # Should be v18 or higher
npm --version
```

## 🎯 What You'll Build

### Admin Dashboard
```
┌─────────────────────────────────────────┐
│  Header: KrishiMitra | 🔔 | 👤          │
├──────┬──────────────────────────────────┤
│ Menu │  Dashboard                       │
│      │  ┌────┬────┬────┬────┐          │
│ 🏠   │  │245 │ 12 │ 3  │98% │          │
│ 👥   │  │Farm│Adv │Alrt│Hlth│          │
│ 📋   │  └────┴────┴────┴────┘          │
│ 🛰️   │                                  │
│ 📊   │  Recent Advisories               │
│      │  ┌──────────────────────────┐   │
│      │  │ Ram Kumar - Water Stress │   │
│      │  │ ₹1750 | 2 hours ago     │   │
│      │  └──────────────────────────┘   │
│      │                                  │
│      │  Farmer Map                      │
│      │  ┌──────────────────────────┐   │
│      │  │     🗺️ Map View          │   │
│      │  └──────────────────────────┘   │
└──────┴──────────────────────────────────┘
```

### Key Features
- 📊 Real-time dashboard with stats
- 👥 Farmer management (CRUD)
- 📋 Advisory tracking
- 🗺️ Interactive maps
- 📈 Analytics and charts
- 🔔 Notifications
- 🌐 Multi-language support

## 🛠️ Technology Stack

- **Frontend**: React 18 + TypeScript
- **Build Tool**: Vite
- **UI Library**: Material-UI (MUI)
- **State**: React Query + Context
- **Routing**: React Router
- **Maps**: Leaflet
- **Charts**: Recharts
- **Forms**: React Hook Form + Zod

## 📁 Project Structure

```
frontend/
├── src/
│   ├── api/              # API client & endpoints
│   ├── components/       # Reusable components
│   │   ├── common/       # Header, Sidebar, etc.
│   │   ├── dashboard/    # Dashboard components
│   │   ├── farmer/       # Farmer components
│   │   └── advisory/     # Advisory components
│   ├── pages/            # Page components
│   ├── hooks/            # Custom React hooks
│   ├── types/            # TypeScript types
│   ├── utils/            # Utility functions
│   ├── App.tsx           # Main app component
│   └── theme.ts          # MUI theme config
├── public/               # Static assets
├── .env                  # Environment variables
└── package.json          # Dependencies
```

## 🚦 Development Workflow

### Step 1: Start Backend
```bash
# Terminal 1
cd C:\Users\Sowmya\OneDrive\projects\ai_crop_system
.\venv\Scripts\activate
uvicorn src.main:app --reload
```

### Step 2: Start Frontend
```bash
# Terminal 2
cd C:\Users\Sowmya\OneDrive\projects\ai_crop_system\frontend
npm run dev
```

### Step 3: Open Browser
```
http://localhost:3000
```

## 📝 Implementation Phases

### Phase 1: Setup (Day 1)
- ✅ Create project structure
- ✅ Install dependencies
- ✅ Configure theme
- ✅ Set up routing

### Phase 2: Core Components (Day 2)
- ✅ Header & Sidebar
- ✅ Layout component
- ✅ Stats cards
- ✅ Loading states

### Phase 3: Dashboard (Day 3)
- ✅ Overview stats
- ✅ Recent advisories
- ✅ Quick actions
- ✅ System health

### Phase 4: Farmers (Day 4)
- ✅ Farmer list table
- ✅ Search & filter
- ✅ Add/Edit forms
- ✅ Farmer details

### Phase 5: Advisories (Day 5)
- ✅ Advisory list
- ✅ Advisory details
- ✅ Status tracking
- ✅ Action items

### Phase 6: Maps & Charts (Day 6-7)
- ✅ Leaflet integration
- ✅ Farmer location map
- ✅ Plot visualization
- ✅ Analytics charts

### Phase 7: Polish (Day 8-9)
- ✅ Responsive design
- ✅ Error handling
- ✅ Loading states
- ✅ Notifications

### Phase 8: Testing (Day 10)
- ✅ Component tests
- ✅ Integration tests
- ✅ E2E tests

## 🎨 Design System

### Colors
```typescript
Primary:   #2E7D32  // Green (Agriculture)
Secondary: #FF6F00  // Orange (Alert)
Success:   #4CAF50  // Green
Warning:   #FFC107  // Yellow
Error:     #F44336  // Red
Info:      #2196F3  // Blue
```

### Typography
- **Headings**: Roboto, 600 weight
- **Body**: Roboto, 400 weight
- **Code**: Roboto Mono

### Spacing
- **Base unit**: 8px
- **Small**: 8px
- **Medium**: 16px
- **Large**: 24px
- **XLarge**: 32px

## 🔌 API Integration

### Example: Fetch Farmers
```typescript
// src/hooks/useFarmers.ts
import { useQuery } from '@tanstack/react-query';
import { apiClient } from '@/api/client';

export const useFarmers = () => {
  return useQuery({
    queryKey: ['farmers'],
    queryFn: async () => {
      const response = await apiClient.get('/farmers/');
      return response.data;
    },
  });
};

// Usage in component
const { data: farmers, isLoading } = useFarmers();
```

### Example: Create Farmer
```typescript
// src/hooks/useFarmers.ts
import { useMutation, useQueryClient } from '@tanstack/react-query';

export const useCreateFarmer = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (farmer) => {
      const response = await apiClient.post('/farmers/', farmer);
      return response.data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['farmers'] });
    },
  });
};

// Usage in component
const createFarmer = useCreateFarmer();
createFarmer.mutate({ phone_number: '+918151910856', ... });
```

## 🧪 Testing

```bash
# Run tests
npm test

# Run tests with coverage
npm run test:coverage

# Run E2E tests
npm run test:e2e
```

## 📦 Building for Production

```bash
# Build
npm run build

# Preview build
npm run preview
```

Output will be in `dist/` directory.

## 🚀 Deployment Options

### Option 1: Vercel (Recommended)
```bash
npm install -g vercel
vercel
```

### Option 2: Netlify
```bash
npm install -g netlify-cli
netlify deploy
```

### Option 3: AWS S3 + CloudFront
```bash
npm run build
aws s3 sync dist/ s3://your-bucket-name
```

### Option 4: Docker
```dockerfile
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build
EXPOSE 3000
CMD ["npm", "run", "preview"]
```

## 🔧 Configuration

### Environment Variables
```env
VITE_API_BASE_URL=http://localhost:8000
VITE_APP_NAME=KrishiMitra
VITE_GOOGLE_MAPS_API_KEY=your_key_here
```

### Proxy Configuration
In `vite.config.ts`:
```typescript
server: {
  proxy: {
    '/api': {
      target: 'http://localhost:8000',
      changeOrigin: true,
    },
  },
}
```

## 📚 Documentation

- **Setup**: `UI_SETUP_GUIDE.md`
- **Development**: `UI_DEVELOPMENT_GUIDE.md`
- **Implementation**: `UI_IMPLEMENTATION_GUIDE.md`
- **Testing**: `UI_TESTING_GUIDE.md` (to be created)
- **Deployment**: `UI_DEPLOYMENT_GUIDE.md` (to be created)

## 🆘 Troubleshooting

### Port 3000 Already in Use
```bash
# Change port in vite.config.ts
server: { port: 3001 }
```

### CORS Errors
Add to backend `src/main.py`:
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

### Module Not Found
```bash
rm -rf node_modules package-lock.json
npm install
```

### Build Errors
```bash
npm run type-check  # Check TypeScript errors
npm run lint        # Check linting errors
```

## 🎯 Next Steps

1. **Run setup script**: `.\setup_ui.ps1`
2. **Follow development guide**: `UI_DEVELOPMENT_GUIDE.md`
3. **Build components**: Start with Dashboard
4. **Add features**: Maps, charts, forms
5. **Test**: Write tests for components
6. **Deploy**: Choose deployment option

## 📞 Support

- **Documentation**: See `UI_IMPLEMENTATION_GUIDE.md`
- **Examples**: Check `UI_DEVELOPMENT_GUIDE.md`
- **Issues**: Review troubleshooting section

---

**Ready to build?** Run `.\setup_ui.ps1` to get started! 🚀
