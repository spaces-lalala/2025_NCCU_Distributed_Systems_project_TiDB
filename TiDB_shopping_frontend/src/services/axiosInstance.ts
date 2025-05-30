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
          console.error('Unauthorized access - 401', error.response);
          
          // 清除過期的認證資訊
          localStorage.removeItem('authToken');
          localStorage.removeItem('authUser');
          
          // 顯示友善的錯誤訊息
          if (window.location.pathname !== '/login') {
            // 避免在登入頁面重複重定向
            alert('您的登入已過期，請重新登入');
            window.location.href = '/login';
          }
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