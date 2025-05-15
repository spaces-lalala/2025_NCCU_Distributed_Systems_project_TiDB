import axios from 'axios';
import type { UserRegistrationData, AuthResponse, UserLoginData } from '@/types/auth';

// API Base URL is set to /api as per user's choice.
// This requires a proxy setup in vite.config.ts for development.
const API_BASE_URL = '/api';

// --- Mock User Storage ---
// In a real backend, this would be a database.
// For mocking, we'll use a Map to store registered users: { email: password }
// And another Map for user details: { email: { id: string, name: string, email: string } }
const mockRegisteredUsersCredentials = new Map<string, string>();
const mockRegisteredUsersDetails = new Map<string, { id: string; name: string; email: string }>();

// Pre-populate with the default user from the plan, so it's always available for login
const defaultUserEmail = 'user@example.com';
const defaultUserPassword = 'password123'; // As per plan
const defaultUserName = '普通用戶A'; // As per plan
mockRegisteredUsersCredentials.set(defaultUserEmail, defaultUserPassword);
mockRegisteredUsersDetails.set(defaultUserEmail, {
  id: `mock-id-${defaultUserEmail}`,
  name: defaultUserName,
  email: defaultUserEmail
});
// Add the 'existeduser@example.com' to simulate it being pre-registered for testing duplicate registration
const preExistingEmail = 'existeduser@example.com';
mockRegisteredUsersCredentials.set(preExistingEmail, 'password123'); // Give it a dummy password
mockRegisteredUsersDetails.set(preExistingEmail, {
    id: `mock-id-${preExistingEmail}`,
    name: 'Already Exists',
    email: preExistingEmail
});

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

  if (mockRegisteredUsersCredentials.has(userData.email)) {
    console.log('[AuthService - MOCK] Simulating registration failure (email exists).');
    throw new Error('此 Email 地址已被註冊。');
  }

  // Store the new user with their actual password for login simulation
  mockRegisteredUsersCredentials.set(userData.email, userData.password);
  mockRegisteredUsersDetails.set(userData.email, {
    id: `mock-id-${userData.email}-${Date.now()}`, // Simple unique ID
    name: userData.name,
    email: userData.email
  });

  console.log('[AuthService - MOCK] Simulating registration success for:', userData.email);
  console.log('[AuthService - MOCK] Current registered users:', Array.from(mockRegisteredUsersCredentials.keys()));
  return {
    message: '使用者註冊成功 (模擬)! 請使用您註冊的密碼登入。',
    // No token/user returned on register, user must login
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
  console.log('[AuthService] Logging in user with backend:', credentials);
  try {
    const response = await axios.post<AuthResponse>(`${API_BASE_URL}/auth/login`, credentials);
    console.log('[AuthService] Login response from backend:', response.data);
    return response.data; // Backend should return { message, token, user }
  } catch (error: unknown) {
    console.error('[AuthService] Error during login with backend:', error);
    if (axios.isAxiosError(error) && error.response) {
      const backendMessage = error.response.data?.message || error.response.data?.detail;
      throw new Error(backendMessage || 'Email 或密碼錯誤，請檢查您的輸入或稍後再試。');
    } else if (error instanceof Error) {
      throw new Error(`登入過程中發生錯誤: ${error.message}`);
    }
    throw new Error('登入過程中發生未知錯誤，請稍後再試。');
  }
};

// Future authentication functions (login, logout, etc.) can be added here.
// For example:
// export const logoutUser = async (): Promise<void> => { ... }; 