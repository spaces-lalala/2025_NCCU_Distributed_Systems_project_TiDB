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
  },
  actions: {
    _saveCartToLocalStorage() {
      localStorage.setItem(CART_STORAGE_KEY, JSON.stringify(this.items));
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
    updateItemQuantity(productId: string, newQuantity: number) {
      if (newQuantity < 0) return;
      const itemIndex = this.items.findIndex(item => item.id === productId);

      if (itemIndex !== -1) {
        // Optionally, check newQuantity against this.items[itemIndex].stock
        if (newQuantity === 0) {
          this.items.splice(itemIndex, 1); // Remove item if quantity is 0
        } else {
          this.items[itemIndex].quantity = newQuantity;
        }
        this._saveCartToLocalStorage();
      }
    },
    removeItem(productId: string) {
      this.items = this.items.filter(item => item.id !== productId);
      this._saveCartToLocalStorage();
    },
    clearCart() {
      this.items = [];
      this._saveCartToLocalStorage();
    },
  },
}); 