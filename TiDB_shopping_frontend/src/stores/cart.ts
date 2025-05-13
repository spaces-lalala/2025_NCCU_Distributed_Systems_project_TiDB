import { defineStore } from 'pinia';

export const useCartStore = defineStore('cart', {
  state: () => ({
    // items: [] as CartItem[], // We'll define CartItem type later
    // total: 0,
  }),
  actions: {
    // addToCart(product: Product) {}, // We'll define Product type later
    // removeFromCart(productId: string) {},
    // updateQuantity(productId: string, quantity: number) {},
    // clearCart() {},
  },
  getters: {
    // cartItemCount: (state) => state.items.length,
    // cartTotalAmount: (state) => state.total,
  },
}); 