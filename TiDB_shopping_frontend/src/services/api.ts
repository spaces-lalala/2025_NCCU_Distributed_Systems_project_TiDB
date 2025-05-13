import axios from 'axios';

const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || '/api', // Use environment variable or default
  headers: {
    'Content-Type': 'application/json',
    // You can add other common headers here
  },
});

// You can also add interceptors here if needed
// For example, to automatically add an auth token to requests
// apiClient.interceptors.request.use(config => {
//   const token = localStorage.getItem('authToken');
//   if (token) {
//     config.headers.Authorization = `Bearer ${token}`;
//   }
//   return config;
// });

export default apiClient; 