export interface User {
  id: number;
  username: string;
  email: string;
  isLogin: boolean;
  createdTime: string;
}

export interface LoginRequest {
  email: string;
  password: string;
}

export interface RegisterRequest {
  username: string;
  email: string;
  password: string;
}

export interface AuthResponse {
  user: User;
  accessToken: string;
  tokenType: string;
}
