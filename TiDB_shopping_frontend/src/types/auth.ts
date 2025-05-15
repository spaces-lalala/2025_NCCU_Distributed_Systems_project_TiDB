/**
 * Interface for user registration data to be sent to the API.
 */
export interface RegistrationData {
  name: string; // Member's name
  email: string;
  password: string;
}

/**
 * Interface for user login data to be sent to the API.
 */
export interface LoginCredentials {
  email: string;
  password: string;
}

/**
 * Interface for the expected user object in the authentication response.
 * Corresponds to backend's UserResponse model.
 */
export interface User {
  id: string; // User ID from the backend (should be string)
  name: string;
  email: string;
  // Add other user properties if your API returns them
}

/**
 * Interface for the expected response from authentication APIs (login/register).
 * Corresponds to backend's AuthSuccessResponse model.
 */
export interface AuthResponse {
  message: string; // Message from the API (e.g., "註冊成功！")
  token: string;   // JWT token
  user: User;      // User information
}

/**
 * For simple message responses like logout
 */
export interface SimpleMessageResponse {
  message: string;
} 