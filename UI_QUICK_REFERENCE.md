# KrishiMitra UI - Quick Reference

## 🚀 Access the UI

**URL**: http://localhost:3000

## 📍 Pages Available

| Page | URL | Description |
|------|-----|-------------|
| **Dashboard** | `/` | Stats, recent farmers, quick actions |
| **Farmers List** | `/farmers` | Table of all farmers with search |
| **Register Farmer** | `/farmers/new` | Form with interactive map |
| **Advisories** | `/advisories` | Coming soon |
| **Monitoring** | `/monitoring` | Coming soon |
| **Analytics** | `/analytics` | Coming soon |
| **Settings** | `/settings` | Coming soon |

## 🎯 Quick Actions

### Register a Farmer
1. Go to: http://localhost:3000/farmers/new
2. Phone: `+918151910856`
3. Language: `Hindi (हिंदी)`
4. Click map or use GPS
5. Area: `2.5` hectares
6. Crops: Select from dropdown
7. Date: Choose planting date
8. Click "Register Farmer"

### View Farmers
1. Go to: http://localhost:3000/farmers
2. Search by phone number
3. Click View/Edit icons

### Navigate
- Click sidebar menu items
- Or use URLs directly

## 🎨 Features

✅ Interactive map with GPS
✅ 11 language options
✅ 25+ crop types
✅ Form validation
✅ Responsive design
✅ Search functionality
✅ Stats dashboard

## 🔧 Development

### Make Changes
1. Edit files in `frontend/src/`
2. Save - auto-reloads instantly
3. Check browser

### Add New Page
1. Create `frontend/src/pages/MyPage.tsx`
2. Add route in `frontend/src/App.tsx`
3. Add to sidebar in `Sidebar.tsx`

### Add New Component
1. Create in `frontend/src/components/`
2. Import where needed
3. Use Material-UI components

## 📝 Code Snippets

### API Call
```typescript
import { useFarmers } from '@/hooks/useFarmers';

const { data, isLoading } = useFarmers();
```

### Navigation
```typescript
import { useNavigate } from 'react-router-dom';

const navigate = useNavigate();
navigate('/farmers');
```

### Form
```typescript
import { useForm } from 'react-hook-form';

const { register, handleSubmit } = useForm();
```

## 🆘 Troubleshooting

### UI not loading?
- Check: http://localhost:3000
- Restart: Stop and run `npm run dev` in frontend/

### API errors?
- Check backend running on port 8000
- Check CORS configured (already done ✅)

### Map not showing?
- Check internet connection (needs OpenStreetMap tiles)
- Check browser console for errors

### Changes not appearing?
- Save the file
- Check terminal for errors
- Hard refresh browser (Ctrl+F5)

## 📚 Files Structure

```
frontend/src/
├── components/
│   ├── common/
│   │   ├── Header.tsx       ✅
│   │   ├── Sidebar.tsx      ✅
│   │   └── Layout.tsx       ✅
│   ├── dashboard/
│   │   └── StatsCard.tsx    ✅
│   └── farmer/
│       └── MapPicker.tsx    ✅
├── pages/
│   ├── Dashboard.tsx        ✅
│   ├── Farmers.tsx          ✅
│   └── FarmerRegistration.tsx ✅
├── hooks/
│   └── useFarmers.ts        ✅
├── types/
│   └── farmer.ts            ✅
├── api/
│   └── client.ts            ✅
├── App.tsx                  ✅
└── theme.ts                 ✅
```

## 🎯 What's Next?

1. **Test** the registration form
2. **Register** a few farmers
3. **View** the dashboard populate
4. **Deploy** to AWS (see `AWS_UI_DEPLOYMENT.md`)

## 💡 Tips

- Use sidebar for navigation
- Dashboard shows recent farmers
- Map picker supports GPS
- Form validates all fields
- Search works on phone numbers
- Mobile-friendly design

---

**Ready!** Open http://localhost:3000 and start using KrishiMitra! 🌾
