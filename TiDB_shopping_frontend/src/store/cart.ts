import { defineStore } from 'pinia';
import type { Product } from '@/types/product'; // Correctly import Product type

// Define CartItem interface, extending Product
export interface CartItem extends Product {
  quantity: number;
}

interface CartState {
  items: CartItem[];
}

const CART_STORAGE_KEY = 'shoppingCart';

const loadCartFromLocalStorage = (): CartItem[] => {
  const storedCart = localStorage.getItem(CART_STORAGE_KEY);
  if (storedCart) {
    try {
      // A simple validation could be added here to check if parsed data conforms to CartItem[]
      return JSON.parse(storedCart) as CartItem[];
    } catch (e) {
      console.error('Error parsing cart from localStorage:', e);
      localStorage.removeItem(CART_STORAGE_KEY);
      return [];
    }
  }
  return [];
};

export const useCartStore = defineStore('cart', {
  state: (): CartState => ({
    items: loadCartFromLocalStorage(),
  }),
  getters: {
    // Getter to access all cart items
    getCartItems: (state): CartItem[] => state.items,
    // Getter for the total number of unique items in the cart
    // cartUniqueItemCount: (state) => state.items.length,
    // Getter for the total quantity of all items in the cart
    totalItemQuantity: (state): number => {
      return state.items.reduce((total, item) => total + item.quantity, 0);
    },
    // Getter for the total price of all items in the cart
    totalPrice: (state): number => {
      return state.items.reduce((total, item) => total + (item.price * item.quantity), 0);
    },
    isEmpty: (state): boolean => state.items.length === 0,
  },  actions: {
    _saveCartToLocalStorage() {
      localStorage.setItem(CART_STORAGE_KEY, JSON.stringify(this.items));
    },
      // 新增：檢查單個商品的庫存
    async checkProductStock(productId: string | number): Promise<number | null> {
      try {
        const response = await fetch(`/api/products/${productId}`);
        if (!response.ok) throw new Error('庫存檢查失敗');
        const data = await response.json();
        return data.stock;
      } catch (error) {
        console.error('庫存檢查失敗：', error);
        return null;
      }
    },

    // 新增：驗證整個購物車的庫存
    async validateCartStock(): Promise<{ valid: boolean; issues: string[] }> {
      const issues: string[] = [];
      
      for (const item of this.items) {
        const currentStock = await this.checkProductStock(item.id);
        if (currentStock === null) {
          issues.push(`無法驗證商品 "${item.name}" 的庫存`);
          continue;
        }
        
        if (currentStock <= 0) {
          issues.push(`商品 "${item.name}" 已售完`);
        } else if (item.quantity > currentStock) {
          issues.push(`商品 "${item.name}" 庫存不足，目前僅剩 ${currentStock} 件`);
        }
      }
      
      return { valid: issues.length === 0, issues };
    },

    addItem(product: Product, quantityToAdd: number = 1) {
      if (quantityToAdd <= 0) return;

      const existingItem = this.items.find(item => item.id === product.id);
      if (existingItem) {
        // Optionally, check against product.stock before adding
        existingItem.quantity += quantityToAdd;
      } else {
        // Optionally, check if quantityToAdd > product.stock
        this.items.push({ ...product, quantity: quantityToAdd });
      }
      this._saveCartToLocalStorage();
    },
      async updateItemQuantity(productId: string | number, newQuantity: number): Promise<boolean> {
      if (newQuantity < 0) return false;
      
      const itemIndex = this.items.findIndex(item => item.id == productId); // 使用 == 來比較不同類型
      if (itemIndex === -1) return false;

      // 檢查庫存
      const currentStock = await this.checkProductStock(productId);
      if (currentStock === null) return false;
      
      if (newQuantity > currentStock) {
        // 庫存不足，不更新數量
        return false;
      }

      if (newQuantity === 0) {
        this.items.splice(itemIndex, 1); // Remove item if quantity is 0
      } else {
        this.items[itemIndex].quantity = newQuantity;
      }
      this._saveCartToLocalStorage();
      return true;
    },
    
    removeItem(productId: string | number) {
      this.items = this.items.filter(item => item.id != productId); // 使用 != 來比較不同類型
      this._saveCartToLocalStorage();
    },
    clearCart() {
      this.items = [];
      this._saveCartToLocalStorage();
    },
  },
}); 