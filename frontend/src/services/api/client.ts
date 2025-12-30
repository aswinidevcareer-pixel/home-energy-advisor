import axios from 'axios';

export const apiClient = axios.create({
  baseURL: '/api/v1',
  headers: {
    'Content-Type': 'application/json'
  },
  timeout: 120000  // 2 minutes for LLM operations
});

// Request interceptor - log outgoing requests (dev only)
apiClient.interceptors.request.use(
  (config) => {
    if (import.meta.env.DEV) {
      console.log(`📤 API Request: ${config.method?.toUpperCase()} ${config.url}`);
    }
    return config;
  },
  (error) => {
    console.error('❌ Request Error:', error);
    return Promise.reject(error);
  }
);

// Response interceptor - handle errors centrally
apiClient.interceptors.response.use(
  (response) => {
    if (import.meta.env.DEV) {
      console.log(`✅ API Response: ${response.config.method?.toUpperCase()} ${response.config.url}`, response.status);
    }
    return response;
  },
  (error) => {
    // Log technical details for developers (only in console)
    if (import.meta.env.DEV) {
      console.group('❌ API Error');
      console.error('URL:', error.config?.url);
      console.error('Method:', error.config?.method);
      console.error('Status:', error.response?.status);
      console.error('Data:', error.response?.data);
      console.groupEnd();
    }
    
    // Don't modify the error, let the calling code handle it
    return Promise.reject(error);
  }
);
