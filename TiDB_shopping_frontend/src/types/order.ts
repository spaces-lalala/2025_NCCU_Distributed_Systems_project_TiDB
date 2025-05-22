/**
 * Represents an item when creating an order.
 * Backend's OrderItemBase for creation requires productId, productName, quantity, and price.
 */
export interface OrderItemForCreation {
  productId: string;
  productName: string;
  quantity: number;
  price: number; // Price per unit at the time of purchase
}

/**
 * Payload for creating a new order.
 * This should match the fields expected by the POST /api/orders endpoint.
 */
export interface OrderCreationPayload {
  items: OrderItemForCreation[];
  totalAmount: number;
}

/**
 * Represents an item within a retrieved order.
 * Corresponds to backend's OrderItemBase as returned in an Order.
 */
export interface OrderItem {
  productId: string;
  productName: string;
  quantity: number;
  price: number; // Price per unit at the time of purchase
}

/**
 * Represents a customer's order as retrieved from the backend.
 * Corresponds to backend's OrderBase.
 */
export interface Order {
  id: string;
  orderNumber: string;
  userId: string;
  orderDate: string; // Typically ISO string from backend
  totalAmount: number;
  status: 'PENDING' | 'PROCESSING' | 'SHIPPED' | 'DELIVERED' | 'CANCELLED' | string; // Allow string for future statuses
  items: OrderItem[];
}

// Response from creating an order is the newly created Order itself
export type OrderCreationResponse = Order;
