import axios from 'axios';
import type { Order, OrderCreationPayload, OrderCreationResponse } from '@/types/order';
import { useAuthStore } from '@/store/auth';

const API_BASE_URL = '/api';

// Helper to get the auth token and set headers
const getAuthHeaders = () => {
  const authStore = useAuthStore(); // Correct way to get Pinia store instance
  const token = authStore.token;
  if (!token) {
    console.error('Auth token is not available for order service.');
    throw new Error('AUTH_TOKEN_MISSING'); 
  }
  return {
    'Authorization': `Bearer ${token}`,
    'Content-Type': 'application/json',
  };
};

/**
 * Fetches the order history for the authenticated user.
 * @returns {Promise<Order[]>} A promise that resolves with an array of orders.
 * @throws Will throw an error if the request fails or if the auth token is missing.
 */
export const getOrders = async (): Promise<Order[]> => {
  try {
    const headers = getAuthHeaders();
    const response = await axios.get<Order[]>(`${API_BASE_URL}/orders`, { headers });
    return response.data;
  } catch (error: any) {
    if (error.message === 'AUTH_TOKEN_MISSING') {
      console.error('Get orders failed: Authentication token is missing.');
      throw new Error('使用者未登入或 Token 無效，無法獲取訂單。');
    }
    const detail = error.response?.data?.detail || error.response?.data?.message || error.message || '伺服器錯誤';
    console.error('獲取訂單歷史失敗:', detail);
    throw new Error(`獲取訂單歷史時發生錯誤: ${detail}`);
  }
};

/**
 * Creates a new order.
 * @param {OrderCreationPayload} orderData - The payload for creating the order.
 * @returns {Promise<OrderCreationResponse>} A promise that resolves with the newly created order.
 * @throws Will throw an error if the request fails or if the auth token is missing.
 */
export const createOrder = async (orderData: OrderCreationPayload): Promise<OrderCreationResponse> => {
  try {
    const headers = getAuthHeaders();
    const response = await axios.post<OrderCreationResponse>(`${API_BASE_URL}/orders`, orderData, { headers });
    return response.data;
  } catch (error: any) {
    if (error.message === 'AUTH_TOKEN_MISSING') {
      console.error('Create order failed: Authentication token is missing.');
      throw new Error('使用者未登入或 Token 無效，無法建立訂單。');
    }

    let errorMessage = '建立訂單時發生未知錯誤';
    if (axios.isAxiosError(error) && error.response) {
      console.error('建立訂單 API 錯誤:', error.response.status, error.response.data);
      if (error.response.status === 422 && error.response.data && error.response.data.detail) {
        // Format Pydantic validation errors
        try {
          const details = error.response.data.detail;
          if (Array.isArray(details)) {
            errorMessage = details.map(d => {
              const field = d.loc && d.loc.length > 1 ? d.loc.slice(1).join(' -> ') : 'Unknown field'; // Extract field path
              return `${field}: ${d.msg}`;
            }).join('; ');
            errorMessage = `輸入資料有誤: ${errorMessage}`;
          } else if (typeof details === 'string') {
            errorMessage = details; // Raw string error
          } else {
            errorMessage = '後端驗證錯誤，但格式無法解析。';
          }
        } catch (e) {
          // Fallback if parsing detail fails
          errorMessage = error.response.data.detail || '輸入資料驗證失敗。'; 
        }
      } else if (error.response.data && error.response.data.detail) {
        errorMessage = error.response.data.detail;
      } else if (typeof error.response.data === 'string') {
        errorMessage = error.response.data;
      } else {
        errorMessage = error.message || '建立訂單失敗，請稍後再試。';
      }
    } else {
      console.error('建立訂單時發生非 Axios 錯誤:', error);
      errorMessage = error.message || '建立訂單時發生客戶端錯誤。';
    }
    throw new Error(errorMessage);
  }
}; 