import type { OrderPayload, OrderResponse } from '@/types/order';

/**
 * Simulates submitting an order to a backend API.
 * In a real application, this would make an HTTP request.
 *
 * @param {OrderPayload} payload - The order data to submit.
 * @returns {Promise<OrderResponse>} A promise that resolves with the order submission response.
 */
export const submitOrder = async (payload: OrderPayload): Promise<OrderResponse> => {
  console.log('[Mock API] Submitting order with payload:', payload);

  // Simulate API call delay
  await new Promise(resolve => setTimeout(resolve, 1000));

  // Simulate a successful response
  if (payload.items && payload.items.length > 0) {
    const mockOrderId = `mock_order_${new Date().getTime()}`;
    return {
      success: true,
      message: '訂單已成功提交！',
      order_id: mockOrderId,
    };
  } else {
    // Simulate an error if no items in cart (though this should be caught earlier)
    return {
      success: false,
      message: '訂單提交失敗：購物車中沒有商品。',
      order_id: ''
    };
  }
  // To simulate a server error, you could randomly throw an error:
  // if (Math.random() < 0.1) { // 10% chance of error
  //   throw new Error('模擬伺服器錯誤，請稍後再試！');
  // }
}; 