# 🌾 KrishiMitra UI - Complete Guide

## 📖 Overview

This is the web-based user interface for KrishiMitra, providing an intuitive dashboard for managing farmers, monitoring crop health, and tracking advisories.

## 🚀 Quick Start

### Automated Setup (Easiest)
```powershell
.\setup_ui.ps1
```

### Manual Setup
```bash
cd frontend
npm install
npm run dev
```

Open: http://localhost:3000

## 📚 Documentation

| Document | Purpose | Time |
|----------|---------|------|
| **`UI_QUICK_START.md`** | Fastest way to get started | 5 min |
| **`UI_SETUP_GUIDE.md`** | Detailed setup instructions | 15 min |
| **`UI_DEVELOPMENT_GUIDE.md`** | Component development guide | 30 min |
| **`UI_IMPLEMENTATION_GUIDE.md`** | Complete implementation plan | 1 hour |

## 🎯 What You'll Build

### Admin Dashboard
- 📊 Real-time statistics
- 👥 Farmer management
- 📋 Advisory tracking
- 🗺️ Interactive maps
- 📈 Analytics & charts
- 🔔 Notifications

### Features
- ✅ Responsive design (mobile, tablet, desktop)
- ✅ Multi-language support (Hindi, English, etc.)
- ✅ Real-time data updates
- ✅ Interactive maps with Leaflet
- ✅ Charts and analytics
- ✅ Form validation
- ✅ Error handling
- ✅ Loading states

## 🛠️ Tech Stack

- **Framework**: React 18 + TypeScript
- **Build Tool**: Vite
- **UI Library**: Material-UI (MUI)
- **State Management**: React Query + Context API
- **Routing**: React Router v6
- **Maps**: Leaflet
- **Charts**: Recharts
- **Forms**: React Hook Form + Zod
- **HTTP Client**: Axios
- **Notifications**: Notistack
- **i18n**: react-i18next

## 📁 Project Structure

```
frontend/
├── src/
│   ├── api/              # API client & endpoints
│   │   ├── client.ts
│   │   ├── farmers.ts
│   │   ├── advisories.ts
│   │   └── monitoring.ts
│   ├── components/       # Reusable components
│   │   ├── common/       # Header, Sidebar, Layout
│   │   ├── dashboard/    # Dashboard components
│   │   ├── farmer/       # Farmer components
│   │   └── advisory/     # Advisory components
│   ├── pages/            # Page components
│   │   ├── Dashboard.tsx
│   │   ├── Farmers.tsx
│   │   ├── Advisories.tsx
│   │   └── Monitoring.tsx
│   ├── hooks/            # Custom React hooks
│   │   ├── useFarmers.ts
│   │   ├── useAdvisories.ts
│   │   └── useAuth.ts
│   ├── contexts/         # React contexts
│   │   └── AuthContext.tsx
│   ├── types/            # TypeScript types
│   │   ├── farmer.ts
│   │   ├── advisory.ts
│   │   └── monitoring.ts
│   ├── utils/            # Utility functions
│   ├── App.tsx           # Main app component
│   ├── main.tsx          # Entry point
│   └── theme.ts          # MUI theme config
├── public/               # Static assets
├── .env                  # Environment variables
├── package.json          # Dependencies
├── vite.config.ts        # Vite configuration
└── tsconfig.json         # TypeScript config
```

## 🎨 UI Preview

### Dashboard
```
┌─────────────────────────────────────────────────────────┐
│  🌾 KrishiMitra              🔔 (3)    👤 Admin        │
├──────┬──────────────────────────────────────────────────┤
│      │  Dashboard                                       │
│ 🏠   │  ┌──────────┬──────────┬──────────┬──────────┐ │
│ 👥   │  │ Farmers  │Advisories│  Alerts  │  Health  │ │
│ 📋   │  │   245    │    12    │    3     │   98%    │ │
│ 🛰️   │  └──────────┴──────────┴──────────┴──────────┘ │
│ 📊   │                                                  │
│ ⚙️   │  Recent Advisories                              │
│      │  ┌────────────────────────────────────────────┐ │
│      │  │ Ram Kumar - Water Stress                   │ │
│      │  │ Risk: 75/100 | Cost: ₹1750                │ │
│      │  │ Status: Sent | 2 hours ago                │ │
│      │  └────────────────────────────────────────────┘ │
│      │                                                  │
│      │  Farmer Locations                               │
│      │  ┌────────────────────────────────────────────┐ │
│      │  │         🗺️ Interactive Map                 │ │
│      │  │         📍 Farmer markers                  │ │
│      │  │         🟢 Healthy  🟡 Moderate  🔴 Risk  │ │
│      │  └────────────────────────────────────────────┘ │
└──────┴──────────────────────────────────────────────────┘
```

### Farmers Page
```
┌─────────────────────────────────────────────────────────┐
│  Farmers                              [+ Add Farmer]    │
├─────────────────────────────────────────────────────────┤
│  🔍 Search by phone number...                           │
├─────────────────────────────────────────────────────────┤
│  Phone          │ Language │ Location  │ Actions        │
├─────────────────┼──────────┼───────────┼────────────────┤
│  +918151910856  │ Hindi    │ Pune      │ 👁️ ✏️         │
│  +919876543210  │ Bengali  │ Kolkata   │ 👁️ ✏️         │
│  +917654321098  │ Telugu   │ Hyderabad │ 👁️ ✏️         │
└─────────────────────────────────────────────────────────┘
```

## 🚦 Development Workflow

### 1. Start Backend
```bash
# Terminal 1
cd C:\Users\Sowmya\OneDrive\projects\ai_crop_system
.\venv\Scripts\activate
uvicorn src.main:app --reload
```

### 2. Start Frontend
```bash
# Terminal 2
cd C:\Users\Sowmya\OneDrive\projects\ai_crop_system\frontend
npm run dev
```

### 3. Open Browser
```
http://localhost:3000
```

## 📝 Implementation Timeline

| Phase | Tasks | Duration |
|-------|-------|----------|
| **Setup** | Project creation, dependencies | 1-2 days |
| **Core** | Layout, routing, theme | 1-2 days |
| **Dashboard** | Stats, charts, recent items | 2-3 days |
| **Farmers** | List, CRUD, details | 2-3 days |
| **Advisories** | List, details, tracking | 2-3 days |
| **Maps** | Leaflet integration, markers | 1-2 days |
| **Polish** | Responsive, errors, loading | 2-3 days |
| **Testing** | Unit, integration, E2E | 2-3 days |

**Total**: 13-21 days for complete MVP

## 🎨 Design System

### Colors
- **Primary**: #2E7D32 (Green - Agriculture)
- **Secondary**: #FF6F00 (Orange - Alert)
- **Success**: #4CAF50
- **Warning**: #FFC107
- **Error**: #F44336
- **Info**: #2196F3

### Status Colors
- **Healthy**: 🟢 #4CAF50
- **Moderate**: 🟡 #FFC107
- **Stressed**: 🟠 #FF9800
- **Critical**: 🔴 #F44336

### Typography
- **Font**: Roboto
- **Headings**: 600 weight
- **Body**: 400 weight

## 🔌 API Integration

### Example: Fetch Data
```typescript
// Hook
const { data, isLoading, error } = useFarmers();

// Component
if (isLoading) return <LoadingSpinner />;
if (error) return <ErrorMessage error={error} />;
return <FarmerList farmers={data} />;
```

### Example: Mutate Data
```typescript
// Hook
const createFarmer = useCreateFarmer();

// Component
const handleSubmit = (data) => {
  createFarmer.mutate(data, {
    onSuccess: () => {
      showNotification('Farmer created successfully');
      navigate('/farmers');
    },
  });
};
```

## 🧪 Testing

```bash
# Run tests
npm test

# Coverage
npm run test:coverage

# E2E tests
npm run test:e2e
```

## 📦 Building

```bash
# Development build
npm run build

# Preview production build
npm run preview
```

## 🚀 Deployment

### Vercel (Recommended)
```bash
npm install -g vercel
vercel
```

### Netlify
```bash
npm install -g netlify-cli
netlify deploy
```

### Docker
```bash
docker build -t krishimitra-ui .
docker run -p 3000:3000 krishimitra-ui
```

## 🔧 Configuration

### Environment Variables
```env
VITE_API_BASE_URL=http://localhost:8000
VITE_APP_NAME=KrishiMitra
VITE_GOOGLE_MAPS_API_KEY=your_key
```

### CORS Setup
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

## 🆘 Troubleshooting

### Port Already in Use
```typescript
// vite.config.ts
server: { port: 3001 }
```

### CORS Errors
- Check backend CORS middleware
- Verify API_BASE_URL in .env

### Module Not Found
```bash
rm -rf node_modules package-lock.json
npm install
```

### Build Errors
```bash
npm run type-check
npm run lint
```

## 📚 Resources

- **React**: https://react.dev
- **Material-UI**: https://mui.com
- **Vite**: https://vitejs.dev
- **React Query**: https://tanstack.com/query
- **React Router**: https://reactrouter.com
- **Leaflet**: https://leafletjs.com
- **Recharts**: https://recharts.org

## 🎯 Next Steps

1. **Setup**: Run `.\setup_ui.ps1`
2. **Learn**: Read `UI_DEVELOPMENT_GUIDE.md`
3. **Build**: Follow component examples
4. **Test**: Write tests for components
5. **Deploy**: Choose deployment option

## 📞 Support

- **Quick Start**: `UI_QUICK_START.md`
- **Setup**: `UI_SETUP_GUIDE.md`
- **Development**: `UI_DEVELOPMENT_GUIDE.md`
- **Implementation**: `UI_IMPLEMENTATION_GUIDE.md`

---

**Ready to build the UI?** Start with `UI_QUICK_START.md`! 🚀
