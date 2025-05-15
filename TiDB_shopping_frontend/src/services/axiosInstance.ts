import axios from 'axios';

const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || '/api', // Ensure VITE_API_BASE_URL is in your .env
  headers: {
    'Content-Type': 'application/json',
    // You can add other common headers here
  },
});

// Request Interceptor
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('authToken'); // Or get from Pinia store
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response Interceptor (optional, for handling global errors or data transformation)
apiClient.interceptors.response.use(
  (response) => {
    // You can transform response data here if needed
    return response;
  },
  (error) => {
    // Handle global errors (e.g., 401 Unauthorized, 403 Forbidden)
    if (error.response) {
      switch (error.response.status) {
        case 401:
          // Handle unauthorized access, e.g., redirect to login
          // useAuthStore().logout(); // If using Pinia and auth store is accessible here
          // window.location.href = '/login';
          console.error('Unauthorized access - 401', error.response);
          break;
        case 403:
          console.error('Forbidden - 403', error.response);
          // Handle forbidden access
          break;
        // Add other global error handling as needed
        default:
          // console.error('API Error:', error.response);
          break;
      }
    }
    return Promise.reject(error);
  }
);

export default apiClient; 