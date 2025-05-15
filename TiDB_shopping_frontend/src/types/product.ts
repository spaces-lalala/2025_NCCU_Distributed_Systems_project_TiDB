export interface Product {
  id: string;
  name: string;
  description: string;
  price: number;
  stock: number;
  image_url: string; // Or a more complex type if you have multiple images
  category: string;
  // Add any other product-specific fields here
} 