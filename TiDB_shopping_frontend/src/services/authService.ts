import axios from 'axios';
import type { UserRegistrationData, AuthResponse, UserLoginData } from '@/types/auth';

// API Base URL is set to /api as per user's choice.
// This requires a proxy setup in vite.config.ts for development.
const API_BASE_URL = '/api';

/**
 * Registers a new user.
 * @param userData - The user registration data (name, email, password).
 * @returns A promise that resolves with the authentication response.
 * @throws Will throw an error if registration fails.
 */
export const registerUser = async (userData: UserRegistrationData): Promise<AuthResponse> => {
  console.log('[AuthService - MOCK] Registering user:', userData);
  // Simulate API call delay
  await new Promise(resolve => setTimeout(resolve, 1000));

  // Simulate a successful registration
  if (userData.email === "test@example.com") { // Simulate existing user for testing
    console.log('[AuthService - MOCK] Simulating registration failure (email exists).');
    throw new Error('此 Email 地址已被註冊。');
  }

  console.log('[AuthService - MOCK] Simulating registration success.');
  return {
    message: '使用者註冊成功 (模擬)!',
    // Normally, a real API might return a token and user object upon registration,
    // but for a simple registration flow, a message might be sufficient,
    // and the user would then proceed to login.
    // token: 'mock-jwt-token-on-register',
    // user: {
    //   id: 'mock-user-id',
    //   name: userData.name,
    //   email: userData.email
    // }
  };

  /* Original Axios call - commented out for mock implementation
  try {
    // The actual API endpoint for registration is /api/auth/register
    const response = await axios.post<AuthResponse>(`${API_BASE_URL}/auth/register`, userData);
    return response.data;
  } catch (error: unknown) {
    if (axios.isAxiosError(error) && error.response) {
      // Try to use the error message from the backend response
      const backendMessage = error.response.data?.message;
      throw new Error(backendMessage || '使用者註冊失敗，請檢查您的輸入或稍後再試。');
    } else if (error instanceof Error) {
      // For other types of errors (e.g., network errors)
      throw new Error(`註冊過程中發生錯誤: ${error.message}`);
    }
    // Fallback for unknown errors
    throw new Error('註冊過程中發生未知錯誤，請稍後再試。');
  }
  */
};

// --- Mock Login User Function ---
/**
 * Logs in a user (mock implementation).
 * @param credentials - The user login credentials (email, password).
 * @returns A promise that resolves with the authentication response.
 * @throws Will throw an error if login fails.
 */
export const loginUser = async (credentials: UserLoginData): Promise<AuthResponse> => {
  console.log('[AuthService - MOCK] Logging in user with credentials:', credentials);
  // Simulate API call delay
  await new Promise(resolve => setTimeout(resolve, 1000));

  // Mocked user data - use details from企劃書 4.2. 預設使用者帳號
  const mockUser = {
    id: 'user-001',
    name: '普通用戶A',
    email: 'user@example.com'
  };

  if (credentials.email === mockUser.email && credentials.password === 'password123') {
    console.log('[AuthService - MOCK] Simulating login success.');
    return {
      token: 'mock-jwt-token-for-user001',
      user: mockUser,
      message: '登入成功 (模擬)!',
    };
  } else {
    console.log('[AuthService - MOCK] Simulating login failure (invalid credentials).');
    throw new Error('Email 或密碼錯誤 (模擬)。');
  }
};

// Future authentication functions (login, logout, etc.) can be added here.
// For example:
// export const loginUser = async (credentials: UserLoginData): Promise<AuthResponse> => { ... };
// export const logoutUser = async (): Promise<void> => { ... }; 