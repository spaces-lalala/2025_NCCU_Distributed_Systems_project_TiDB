import { defineStore } from 'pinia';
import type { User, AuthResponse } from '@/types/auth'; // Import User and AuthResponse

interface AuthState {
  token: string | null;
  user: User | null; // Use specific User type
  isAuthenticated: boolean;
}

const initialUser = (): User | null => {
  const storedUser = localStorage.getItem('authUser');
  if (storedUser) {
    try {
      return JSON.parse(storedUser) as User;
    } catch (e) {
      console.error('Error parsing stored user:', e);
      localStorage.removeItem('authUser'); // Clear invalid user data
      return null;
    }
  }
  return null;
};

export const useAuthStore = defineStore('auth', {
  state: (): AuthState => ({
    token: localStorage.getItem('authToken') || null,
    user: initialUser(), // Initialize user from localStorage
    isAuthenticated: !!localStorage.getItem('authToken'),
  }),
  getters: {
    isLoggedIn: (state) => state.isAuthenticated, // Renamed for clarity
    currentUser: (state) => state.user, // Renamed for clarity
    authToken: (state) => state.token, // Getter for the token
  },
  actions: {
    // Action called after successful login or registration from backend
    setAuthState(authData: AuthResponse) {
      this.token = authData.token;
      this.user = authData.user;
      this.isAuthenticated = true;
      localStorage.setItem('authToken', authData.token);
      localStorage.setItem('authUser', JSON.stringify(authData.user));
    },
    logout() {
      this.token = null;
      this.user = null;
      this.isAuthenticated = false;
      localStorage.removeItem('authToken');
      localStorage.removeItem('authUser');
      // Potentially redirect to login page or clear other user-related stores
    },
    // Optional: Action to rehydrate user if only token exists (e.g., on app load)
    // This might involve calling a /api/me endpoint
    // async fetchCurrentUser() {
    //   if (this.token && !this.user) {
    //     try {
    //       // const userProfile = await someAuthService.fetchMe(this.token);
    //       // this.user = userProfile;
    //       // this.isAuthenticated = true;
    //       // localStorage.setItem('authUser', JSON.stringify(userProfile));
    //     } catch (error) {
    //       console.error('Failed to fetch current user:', error);
    //       this.logout(); // Important: Logout if token is invalid or fetching fails
    //     }
    //   }
    // },
  },
}); 