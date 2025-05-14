export interface Product {
  id: string | number; // Or just string/number depending on your API
  name: string;
  description: string;
  price: number;
  stock: number;
  category?: string;
  images?: string[]; // Array of image URLs
  // Add any other product-specific fields
}

export interface CartItem extends Product {
  quantity: number;
}

export interface User {
  id: string;
  username: string;
  email: string;
  // Other user details, but avoid storing sensitive info like password here
}

export interface OrderItem {
  product_id: string | number;
  quantity: number;
  price_at_purchase: number; // Price at the time of order
  name?: string; // Optional: denormalized for easier display
  image_url?: string; // Optional: denormalized
}

export interface Order {
  id: string;
  user_id: string;
  items: OrderItem[];
  total_amount: number;
  status: 'pending' | 'processing' | 'shipped' | 'delivered' | 'cancelled';
  created_at: string; // ISO date string
  updated_at: string; // ISO date string
  shipping_address?: any; // Define a proper Address interface later
  // Add other order-specific fields
}

// Interface for Address (can be used in User Profile and Order)
export interface Address {
  street: string;
  city: string;
  state: string;
  zip_code: string;
  country: string;
  contact_name?: string;
  contact_phone?: string;
} 