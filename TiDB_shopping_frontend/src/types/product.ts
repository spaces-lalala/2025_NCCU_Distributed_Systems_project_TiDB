export interface Product {
  id: number;
  name: string;
  description?: string;
  price: number;
  stock: number;
  image_url?: string;   // 後端用
  imageUrl?: string;    // 前端顯示用
  sold?: number;
  category_name?: string;
}
