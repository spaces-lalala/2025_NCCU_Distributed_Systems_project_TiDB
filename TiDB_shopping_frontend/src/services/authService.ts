import axios from 'axios';
import type { UserRegistrationData, AuthResponse } from '@/types/auth';

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
};

// Future authentication functions (login, logout, etc.) can be added here.
// For example:
// export const loginUser = async (credentials: UserLoginData): Promise<AuthResponse> => { ... };
// export const logoutUser = async (): Promise<void> => { ... }; 