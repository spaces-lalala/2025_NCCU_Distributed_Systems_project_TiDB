import apiClient from './axiosInstance'; // 使用配置好的 axios 實例
import type { Order, OrderCreationPayload, OrderCreationResponse } from '@/types/order';

/**
 * Fetches the order history for the authenticated user.
 * @returns {Promise<Order[]>} A promise that resolves with an array of orders.
 * @throws Will throw an error if the request fails or if authentication fails.
 */
export const getOrders = async (): Promise<Order[]> => {
  try {
    const response = await apiClient.get<Order[]>('/orders');
    return response.data;
  } catch (error: any) {
    const detail = error.response?.data?.detail || error.response?.data?.message || error.message || '伺服器錯誤';
    console.error('獲取訂單歷史失敗:', detail);
    throw new Error(`獲取訂單歷史時發生錯誤: ${detail}`);
  }
};

/**
 * Creates a new order.
 * @param {OrderCreationPayload} orderData - The payload for creating the order.
 * @returns {Promise<OrderCreationResponse>} A promise that resolves with the newly created order.
 * @throws Will throw an error if the request fails or if authentication fails.
 */
export const createOrder = async (orderData: OrderCreationPayload): Promise<OrderCreationResponse> => {
  try {
    const response = await apiClient.post<OrderCreationResponse>('/orders', orderData);
    return response.data;
  } catch (error: any) {
    let errorMessage = '建立訂單時發生未知錯誤';
    if (error.response) {
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