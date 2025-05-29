/**
 * Represents an item when creating an order.
 * Backend's OrderItemBase for creation requires product_id and quantity.
 */
export interface OrderItemForCreation {
  product_id: number;  // Changed to match backend expectation
  quantity: number;
}

/**
 * Payload for creating a new order.
 * This should match the fields expected by the POST /api/orders endpoint.
 */
export interface OrderCreationPayload {
  items: OrderItemForCreation[];
}

/**
 * Represents an item within a retrieved order.
 * Corresponds to backend's OrderItemOut with snake_case field names.
 */
export interface OrderItem {
  id: string;
  product_id: number;
  product_name: string;
  quantity: number;
  price: number; // Price per unit at the time of purchase
}

/**
 * Represents a customer's order as retrieved from the backend.
 * Corresponds to backend's OrderOut with snake_case field names.
 */
export interface Order {
  id: string;
  order_number: string;
  user_id: string;
  order_date: string; // Typically ISO string from backend
  total_amount: number;
  status: 'PENDING' | 'PROCESSING' | 'SHIPPED' | 'DELIVERED' | 'CANCELLED' | string; // Allow string for future statuses
  items: OrderItem[];
}

// Response from creating an order is the newly created Order itself
export type OrderCreationResponse = Order;
