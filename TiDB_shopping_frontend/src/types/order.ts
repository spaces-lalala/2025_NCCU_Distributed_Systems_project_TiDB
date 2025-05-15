/**
 * @interface OrderItemPayload
 * @description Represents a single item within an order payload.
 */
export interface OrderItemPayload {
  product_id: string | number; // Assuming product_id can be string or number
  quantity: number;
  price_at_purchase: number; // Price of the item at the time of purchase
}

/**
 * @interface CustomerDetailsPayload
 * @description Represents customer details in the order payload.
 */
export interface CustomerDetailsPayload {
  name: string;
  phone: string;
  address: string;
  email: string;
}

/**
 * @interface OrderPayload
 * @description Defines the structure for submitting a new order.
 */
export interface OrderPayload {
  customer_details: CustomerDetailsPayload;
  items: OrderItemPayload[];
  total_amount: number;
  shipping_method: 'standard' | 'express';
  payment_method: 'cod' | 'credit_card_mock';
  notes?: string;
  status: 'pending' | 'processing' | 'shipped' | 'delivered' | 'cancelled'; // Example statuses
}

/**
 * @interface OrderResponse
 * @description Defines the expected structure of the response after submitting an order.
 */
export interface OrderResponse {
  success: boolean;
  message: string;
  order_id: string; // Unique identifier for the created order
  // Optionally, you can include the full order details as well
  // order_details?: OrderPayload & { created_at: string; updated_at: string };
} 