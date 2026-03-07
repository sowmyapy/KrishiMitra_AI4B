import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

// Export for use in components that need direct fetch calls
export const getApiUrl = (path: string) => `${API_BASE_URL}${path}`;

export const apiClient = axios.create({
  baseURL: `${API_BASE_URL}/api/v1`,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor for adding auth token (optional for now)
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
    // Don't redirect on 401 for now - authentication is optional
    // if (error.response?.status === 401) {
    //   localStorage.removeItem('access_token');
    //   window.location.href = '/login';
    // }
    return Promise.reject(error);
  }
);
