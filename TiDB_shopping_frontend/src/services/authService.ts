import axios from 'axios';
import type { RegistrationData, AuthResponse, LoginCredentials, SimpleMessageResponse } from '@/types/auth';

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
export const registerUser = async (userData: RegistrationData): Promise<AuthResponse> => {
  const response = await fetch(`${API_BASE_URL}/auth/register`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(userData),
  });

  const responseData = await response.json(); // Always try to parse JSON

  if (!response.ok) {
    // Access detail from responseData, which should now be parsed
    throw new Error(responseData.detail || '註冊失敗');
  }
  return responseData as AuthResponse; // Expecting AuthResponse now
};

// --- Mock Login User Function ---
/**
 * Logs in a user (mock implementation).
 * @param credentials - The user login credentials (email, password).
 * @returns A promise that resolves with the authentication response.
 * @throws Will throw an error if login fails.
 */
export const loginUser = async (credentials: LoginCredentials): Promise<AuthResponse> => {
  const response = await fetch(`${API_BASE_URL}/auth/login`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(credentials),
  });

  const responseData = await response.json(); // Always try to parse JSON

  if (!response.ok) {
    // Access detail from responseData, which should now be parsed
    throw new Error(responseData.detail || '登入失敗');
  }
  return responseData as AuthResponse; // Return parsed data
};

export const logoutUser = async (): Promise<SimpleMessageResponse> => {
  // In a real app, this might call a backend endpoint to invalidate a session/token
  // For this mock, we just clear local storage in the store.
  console.log('Mock logoutUser called');
  // The actual store should handle clearing localStorage, but for safety we can also do it here if needed.
  // However, it's better for the Pinia store to manage its own state and side effects like localStorage.
  // localStorage.removeItem('authToken');
  // localStorage.removeItem('authUser');
  return { message: '登出成功 (模擬)' };
};

// Future authentication functions (login, logout, etc.) can be added here.
// For example:
// export const logoutUser = async (): Promise<void> => { ... }; 