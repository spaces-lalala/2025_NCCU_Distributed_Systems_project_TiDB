import { defineStore } from 'pinia';
// import type { Product, CartItem } from '@/types/domain'; // Assuming types are defined

// Placeholder types, replace with actual types from @/types/domain
interface Product {
  id: string | number;
  name: string;
  price: number;
  // ... other product properties
}

interface CartItem extends Product {
  quantity: number;
}

interface CartState {
  items: CartItem[];
}

const CART_STORAGE_KEY = 'shoppingCart';

// Helper function to load cart from localStorage
const loadCartFromLocalStorage = (): CartItem[] => {
  const storedCart = localStorage.getItem(CART_STORAGE_KEY);
  if (storedCart) {
    try {
      return JSON.parse(storedCart);
    } catch (e) {
      console.error('Error parsing cart from localStorage', e);
      localStorage.removeItem(CART_STORAGE_KEY); // Clear corrupted cart data
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
    cartItemCount: (state) => {
      return state.items.reduce((total, item) => total + item.quantity, 0);
    },
    cartTotalPrice: (state) => {
      return state.items.reduce((total, item) => total + item.price * item.quantity, 0);
    },
    isEmpty: (state) => state.items.length === 0,
  },
  actions: {
    _saveCartToLocalStorage() {
      localStorage.setItem(CART_STORAGE_KEY, JSON.stringify(this.items));
    },
    addItem(product: Product, quantity: number = 1) {
      if (quantity <= 0) return;

      const existingItem = this.items.find(item => item.id === product.id);
      if (existingItem) {
        existingItem.quantity += quantity;
      } else {
        this.items.push({ ...product, quantity });
      }
      this._saveCartToLocalStorage();
    },
    updateItemQuantity(productId: string | number, quantity: number) {
      if (quantity < 0) return;
      const itemIndex = this.items.findIndex(item => item.id === productId);
      if (itemIndex !== -1) {
        if (quantity === 0) {
          this.items.splice(itemIndex, 1);
        } else {
          this.items[itemIndex].quantity = quantity;
        }
        this._saveCartToLocalStorage();
      }
    },
    removeItem(productId: string | number) {
      this.items = this.items.filter(item => item.id !== productId);
      this._saveCartToLocalStorage();
    },
    clearCart() {
      this.items = [];
      this._saveCartToLocalStorage();
    },
  },
}); 