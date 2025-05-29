import apiClient from './axiosInstance'; // 使用統一的 axios 實例
import type { RegistrationData, AuthResponse, LoginCredentials, SimpleMessageResponse } from '@/types/auth';

/**
 * Registers a new user.
 * @param userData - The user registration data (name, email, password).
 * @returns A promise that resolves with the authentication response.
 * @throws Will throw an error if registration fails.
 */
export const registerUser = async (userData: RegistrationData): Promise<AuthResponse> => {
  try {
    const response = await apiClient.post<AuthResponse>('/auth/register', userData);
    console.log('註冊成功 API 回應:', response.data);
    return response.data;
  } catch (error: any) {
    console.error('註冊失敗:', error);
    const errorMessage = error.response?.data?.detail || error.message || '註冊失敗';
    throw new Error(errorMessage);
  }
};

/**
 * Logs in a user.
 * @param credentials - The user login credentials (email, password).
 * @returns A promise that resolves with the authentication response.
 * @throws Will throw an error if login fails.
 */
export const loginUser = async (credentials: LoginCredentials): Promise<AuthResponse> => {
  try {
    const response = await apiClient.post<AuthResponse>('/auth/login', credentials);
    console.log('登入成功 API 回應:', response.data);
    return response.data;
  } catch (error: any) {
    console.error('登入失敗:', error);
    const errorMessage = error.response?.data?.detail || error.message || '登入失敗';
    throw new Error(errorMessage);
  }
};

export const logoutUser = async (): Promise<SimpleMessageResponse> => {
  try {
    const response = await apiClient.post<SimpleMessageResponse>('/auth/logout');
    return response.data;
  } catch (error: any) {
    console.error('登出失敗:', error);
    // 即使後端登出失敗，我們仍然清除本地存儲
    return { message: '登出成功' };
  }
};