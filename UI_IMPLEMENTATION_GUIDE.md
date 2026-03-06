# KrishiMitra UI Implementation Guide

## Overview

This guide will help you create a modern, responsive web UI for KrishiMitra with two main interfaces:
1. **Admin Dashboard** - For staff to manage farmers, view analytics, and monitor system
2. **Farmer Portal** - Simple interface for farmers to view their advisories

## Technology Stack Options

### Option 1: React + Vite (Recommended)
**Best for**: Modern, fast, component-based UI
- **Frontend**: React 18 + TypeScript
- **Build Tool**: Vite
- **UI Library**: Material-UI (MUI) or Tailwind CSS
- **State Management**: React Query + Context API
- **Maps**: Leaflet or Google Maps
- **Charts**: Recharts or Chart.js

### Option 2: Next.js
**Best for**: SEO-friendly, server-side rendering
- **Framework**: Next.js 14
- **UI Library**: Shadcn/ui + Tailwind CSS
- **State Management**: React Query
- **Maps**: Mapbox or Leaflet

### Option 3: Vue.js
**Best for**: Simpler learning curve
- **Framework**: Vue 3 + TypeScript
- **Build Tool**: Vite
- **UI Library**: Vuetify or Element Plus
- **State Management**: Pinia

## Recommended: React + Vite + Material-UI

This guide will focus on React + Vite + MUI as it's the most popular and well-supported option.

## Project Structure

```
frontend/
├── public/
│   ├── favicon.ico
│   └── logo.png
├── src/
│   ├── api/
│   │   ├── client.ts          # Axios instance
│   │   ├── farmers.ts         # Farmer API calls
│   │   ├── advisories.ts      # Advisory API calls
│   │   ├── monitoring.ts      # Monitoring API calls
│   │   └── auth.ts            # Authentication
│   ├── components/
│   │   ├── common/
│   │   │   ├── Header.tsx
│   │   │   ├── Sidebar.tsx
│   │   │   ├── LoadingSpinner.tsx
│   │   │   └── ErrorBoundary.tsx
│   │   ├── dashboard/
│   │   │   ├── StatsCard.tsx
│   │   │   ├── FarmerList.tsx
│   │   │   ├── AdvisoryList.tsx
│   │   │   └── MapView.tsx
│   │   ├── farmer/
│   │   │   ├── FarmerForm.tsx
│   │   │   ├── FarmerDetails.tsx
│   │   │   └── PlotMap.tsx
│   │   └── advisory/
│   │       ├── AdvisoryCard.tsx
│   │       ├── AdvisoryDetails.tsx
│   │       └── ActionList.tsx
│   ├── pages/
│   │   ├── Dashboard.tsx
│   │   ├── Farmers.tsx
│   │   ├── FarmerDetails.tsx
│   │   ├── Advisories.tsx
│   │   ├── Monitoring.tsx
│   │   ├── Analytics.tsx
│   │   └── Login.tsx
│   ├── hooks/
│   │   ├── useFarmers.ts
│   │   ├── useAdvisories.ts
│   │   └── useAuth.ts
│   ├── contexts/
│   │   └── AuthContext.tsx
│   ├── utils/
│   │   ├── formatters.ts
│   │   └── validators.ts
│   ├── types/
│   │   ├── farmer.ts
│   │   ├── advisory.ts
│   │   └── monitoring.ts
│   ├── App.tsx
│   ├── main.tsx
│   └── theme.ts
├── package.json
├── tsconfig.json
├── vite.config.ts
└── README.md
```

## Key Features to Implement

### 1. Admin Dashboard
- **Overview Stats**: Total farmers, active advisories, system health
- **Recent Advisories**: List of latest advisories sent
- **Farmer Map**: Interactive map showing all farmer locations
- **System Monitoring**: API health, data ingestion status

### 2. Farmer Management
- **Farmer List**: Searchable, filterable table
- **Add/Edit Farmer**: Form with validation
- **Farmer Details**: Profile, plots, advisory history
- **Plot Management**: Add/edit plots with map picker

### 3. Advisory Management
- **Advisory List**: Filter by status, date, farmer
- **Advisory Details**: Full advisory with actions, costs
- **Manual Advisory**: Create and send custom advisory
- **Advisory History**: Timeline view

### 4. Monitoring Dashboard
- **Satellite Data**: NDVI visualization, historical trends
- **Weather Data**: Current conditions, forecast
- **Crop Health**: Health scores, stress indicators
- **Alerts**: Active alerts and warnings

### 5. Analytics
- **Advisory Effectiveness**: Success rates, farmer feedback
- **Cost Analysis**: Total costs, cost per farmer
- **Usage Stats**: API calls, data usage
- **Trends**: Seasonal patterns, crop health trends

## UI Components Breakdown

### Dashboard Page
```
┌─────────────────────────────────────────────────────────┐
│  Header: KrishiMitra | Notifications | Profile          │
├─────────────────────────────────────────────────────────┤
│ Sidebar │  Main Content                                 │
│         │  ┌──────────┬──────────┬──────────┐          │
│ • Home  │  │ Farmers  │Advisories│  Alerts  │          │
│ • Farm  │  │   245    │    12    │    3     │          │
│ • Advis │  └──────────┴──────────┴──────────┘          │
│ • Monit │                                               │
│ • Analy │  Recent Advisories                            │
│         │  ┌─────────────────────────────────────────┐ │
│         │  │ Farmer: Ram Kumar                       │ │
│         │  │ Issue: Water Stress                     │ │
│         │  │ Actions: 2 | Cost: ₹1750               │ │
│         │  │ Status: Sent | 2 hours ago             │ │
│         │  └─────────────────────────────────────────┘ │
│         │                                               │
│         │  Farmer Locations Map                         │
│         │  ┌─────────────────────────────────────────┐ │
│         │  │         🗺️ Interactive Map              │ │
│         │  │         📍 Farmer markers               │ │
│         │  └─────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────┘
```

### Farmer Details Page
```
┌─────────────────────────────────────────────────────────┐
│  ← Back to Farmers                                       │
├─────────────────────────────────────────────────────────┤
│  Farmer Profile                                          │
│  ┌──────────────────────────────────────────────────┐  │
│  │ Name: Ram Kumar                                   │  │
│  │ Phone: +918151910856                             │  │
│  │ Language: Hindi                                   │  │
│  │ Location: Pune, Maharashtra                       │  │
│  │ Registered: Jan 15, 2025                         │  │
│  └──────────────────────────────────────────────────┘  │
│                                                          │
│  Plots                                                   │
│  ┌──────────────────────────────────────────────────┐  │
│  │ Plot 1: 2.5 hectares                             │  │
│  │ Crops: Ragi, Mango                               │  │
│  │ Location: 13.2443, 77.7122                       │  │
│  │ Health: 🟡 Moderate (NDVI: 0.55)                │  │
│  │ [View on Map] [Edit]                             │  │
│  └──────────────────────────────────────────────────┘  │
│                                                          │
│  Advisory History                                        │
│  ┌──────────────────────────────────────────────────┐  │
│  │ Mar 1, 2025 - Water Stress                       │  │
│  │ Feb 15, 2025 - Heat Stress                       │  │
│  │ Jan 30, 2025 - Pest Alert                        │  │
│  └──────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
```

### Advisory Details Page
```
┌─────────────────────────────────────────────────────────┐
│  Advisory Details                                        │
├─────────────────────────────────────────────────────────┤
│  Farmer: Ram Kumar (+918151910856)                      │
│  Date: March 1, 2025, 10:30 AM                          │
│  Status: ✅ Delivered                                    │
│                                                          │
│  Issue Detected                                          │
│  ┌──────────────────────────────────────────────────┐  │
│  │ 💧 Water Stress                                  │  │
│  │ Risk Score: 75/100 (High)                        │  │
│  │ Confidence: 85%                                   │  │
│  └──────────────────────────────────────────────────┘  │
│                                                          │
│  Data Analysis                                           │
│  ┌──────────────────────────────────────────────────┐  │
│  │ NDVI: 0.45 (Below normal)                        │  │
│  │ Temperature: 38.5°C (High)                       │  │
│  │ Humidity: 25% (Low)                              │  │
│  │ Soil Moisture: 15% (Critical)                    │  │
│  └──────────────────────────────────────────────────┘  │
│                                                          │
│  Recommended Actions                                     │
│  ┌──────────────────────────────────────────────────┐  │
│  │ 1. ⚠️ Immediate irrigation                       │  │
│  │    Priority: High                                 │  │
│  │    Timeframe: 24 hours                           │  │
│  │    Cost: ₹500                                    │  │
│  │                                                   │  │
│  │ 2. 🌾 Apply mulch to retain moisture            │  │
│  │    Priority: Medium                               │  │
│  │    Timeframe: 3 days                             │  │
│  │    Cost: ₹1250                                   │  │
│  └──────────────────────────────────────────────────┘  │
│                                                          │
│  Total Estimated Cost: ₹1750                            │
│                                                          │
│  Voice Call Status                                       │
│  ┌──────────────────────────────────────────────────┐  │
│  │ Call SID: CA1234567890                           │  │
│  │ Duration: 45 seconds                              │  │
│  │ Status: Completed                                 │  │
│  │ [🔊 Play Recording]                              │  │
│  └──────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
```

## Color Scheme

### Primary Colors
- **Primary**: #2E7D32 (Green - Agriculture)
- **Secondary**: #FF6F00 (Orange - Alert)
- **Success**: #4CAF50 (Green)
- **Warning**: #FFC107 (Yellow)
- **Error**: #F44336 (Red)
- **Info**: #2196F3 (Blue)

### Status Colors
- **Healthy**: #4CAF50 (Green)
- **Moderate**: #FFC107 (Yellow)
- **Stressed**: #FF9800 (Orange)
- **Critical**: #F44336 (Red)

## Icons

Use Material Icons or Heroicons:
- 🌾 Farmer
- 📋 Advisory
- 🛰️ Satellite
- 🌤️ Weather
- 📞 Phone Call
- 🗺️ Map
- 📊 Analytics
- ⚙️ Settings

## Responsive Design

### Breakpoints
- **Mobile**: < 768px
- **Tablet**: 768px - 1024px
- **Desktop**: > 1024px

### Mobile-First Approach
- Stack components vertically on mobile
- Collapsible sidebar
- Touch-friendly buttons (min 44px)
- Simplified navigation

## Accessibility

- **WCAG 2.1 AA Compliance**
- Keyboard navigation
- Screen reader support
- High contrast mode
- Focus indicators
- Alt text for images
- ARIA labels

## Internationalization (i18n)

Support multiple languages:
- English (en)
- Hindi (hi)
- Bengali (bn)
- Telugu (te)
- Marathi (mr)
- Tamil (ta)

Use `react-i18next` for translations.

## Next Steps

1. **Setup**: Follow `UI_SETUP_GUIDE.md` to create the project
2. **Development**: Follow `UI_DEVELOPMENT_GUIDE.md` for implementation
3. **Testing**: Follow `UI_TESTING_GUIDE.md` for testing
4. **Deployment**: Follow `UI_DEPLOYMENT_GUIDE.md` for deployment

## Estimated Timeline

- **Setup & Basic Structure**: 1-2 days
- **Core Components**: 3-5 days
- **API Integration**: 2-3 days
- **Styling & Polish**: 2-3 days
- **Testing**: 2-3 days
- **Deployment**: 1 day

**Total**: 11-17 days for MVP

## Resources

- React Docs: https://react.dev
- Material-UI: https://mui.com
- Vite: https://vitejs.dev
- React Query: https://tanstack.com/query
- Leaflet: https://leafletjs.com

---

Ready to start? See `UI_SETUP_GUIDE.md` for step-by-step setup instructions!
