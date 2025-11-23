import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, tap } from 'rxjs';
import { environment } from '../../../environments/environment';
import {
  User,
  LoginRequest,
  RegisterRequest,
  AuthResponse,
} from '../../shared/models/user.model';

@Injectable({
  providedIn: 'root',
})
export class AuthService {
  private readonly http = inject(HttpClient);
  private readonly apiUrl = `${environment.apiUrl}/auth`;
  private readonly TOKEN_KEY = 'access_token';

  /**
   * 使用者註冊
   */
  register(request: RegisterRequest): Observable<AuthResponse> {
    return this.http.post<AuthResponse>(`${this.apiUrl}/register`, request).pipe(
      tap((response) => {
        this.setToken(response.accessToken);
      })
    );
  }

  /**
   * 使用者登入
   */
  login(request: LoginRequest): Observable<AuthResponse> {
    return this.http.post<AuthResponse>(`${this.apiUrl}/login`, request).pipe(
      tap((response) => {
        this.setToken(response.accessToken);
      })
    );
  }

  /**
   * 使用者登出
   */
  logout(): void {
    this.removeToken();
  }

  /**
   * 取得當前使用者資訊
   */
  getCurrentUser(): Observable<User> {
    return this.http.get<User>(`${this.apiUrl}/user`);
  }

  /**
   * 儲存 JWT Token
   */
  private setToken(token: string): void {
    localStorage.setItem(this.TOKEN_KEY, token);
  }

  /**
   * 取得 JWT Token
   */
  getToken(): string | null {
    return localStorage.getItem(this.TOKEN_KEY);
  }

  /**
   * 移除 JWT Token
   */
  private removeToken(): void {
    localStorage.removeItem(this.TOKEN_KEY);
  }

  /**
   * 檢查是否已登入
   */
  isAuthenticated(): boolean {
    return this.getToken() !== null;
  }
}
