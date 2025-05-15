import { defineStore } from 'pinia';

interface AuthState {
  token: string | null;
  user: Record<string, any> | null; // Replace with a more specific User type later
  isAuthenticated: boolean;
}

export const useAuthStore = defineStore('auth', {
  state: (): AuthState => ({
    token: localStorage.getItem('authToken') || null,
    user: null, // Fetch user details on app load if token exists
    isAuthenticated: !!localStorage.getItem('authToken'),
  }),
  getters: {
    // Example getter
    // isLoggedIn: (state) => state.isAuthenticated,
    // getUser: (state) => state.user,
  },
  actions: {
    login(token: string, userData?: Record<string, any>) {
      this.token = token;
      this.user = userData || null;
      this.isAuthenticated = true;
      localStorage.setItem('authToken', token);
      // Potentially redirect or perform other actions
    },
    logout() {
      this.token = null;
      this.user = null;
      this.isAuthenticated = false;
      localStorage.removeItem('authToken');
      // Potentially redirect to login page
    },
    // async fetchUser() { // Example action to fetch user data
    //   if (this.token && !this.user) {
    //     try {
    //       // const userData = await authService.getProfile(); // Assuming authService
    //       // this.user = userData;
    //     } catch (error) {
    //       console.error('Failed to fetch user profile:', error);
    //       this.logout(); // Logout if fetching profile fails
    //     }
    //   }
    // },
  },
}); 