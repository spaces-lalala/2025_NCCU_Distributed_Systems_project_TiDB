/**
 * Interface for user registration data to be sent to the API.
 */
export interface UserRegistrationData {
  name: string; // Member's name
  email: string;
  password: string;
}

/**
 * Interface for user login data to be sent to the API.
 */
export interface UserLoginData {
  email: string;
  password: string;
}

/**
 * Interface for the expected user object in the authentication response.
 */
export interface User {
  id: string | number; // User ID from the backend
  name: string;
  email: string;
  // Add other user properties if your API returns them
}

/**
 * Interface for the expected response from authentication APIs (login/register).
 */
export interface AuthResponse {
  token?: string; // JWT token
  user?: User;    // User information
  message?: string; // Optional success or error message from the API
} 