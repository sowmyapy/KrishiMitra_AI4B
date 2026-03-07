import { ThemeProvider } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { SnackbarProvider } from 'notistack';
import { theme } from './theme';
import { Layout } from './components/common/Layout';
import { Dashboard } from './pages/Dashboard';
import { Farmers } from './pages/Farmers';
import { FarmerRegistration } from './pages/FarmerRegistration';
import { FarmerDetail } from './pages/FarmerDetail';
import { Advisories } from './pages/Advisories';
import { Monitoring } from './pages/Monitoring';
import { AdvancedMonitoring } from './pages/AdvancedMonitoring';
import { Analytics } from './pages/Analytics';

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
                <Route path="/farmers/new" element={<FarmerRegistration />} />
                <Route path="/farmers/:farmerId" element={<FarmerDetail />} />
                <Route path="/advisories" element={<Advisories />} />
                <Route path="/monitoring" element={<Monitoring />} />
                <Route path="/monitoring/advanced" element={<AdvancedMonitoring />} />
                <Route path="/analytics" element={<Analytics />} />
              </Routes>
            </Layout>
          </BrowserRouter>
        </SnackbarProvider>
      </ThemeProvider>
    </QueryClientProvider>
  );
}

export default App;
