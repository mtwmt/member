import { Injectable, inject } from '@angular/core';
import { signalStore, withState, withMethods, patchState } from '@ngrx/signals';
import { rxMethod } from '@ngrx/signals/rxjs-interop';
import { pipe, switchMap, tap, catchError, of } from 'rxjs';
import { AuthService } from '../services/auth';
import { User, LoginRequest, RegisterRequest } from '../../shared/models/user.model';

/**
 * 認證狀態介面
 */
interface AuthState {
  user: User | null;
  isLoading: boolean;
  error: string | null;
}

/**
 * 初始狀態
 */
const initialState: AuthState = {
  user: null,
  isLoading: false,
  error: null,
};

/**
 * 認證 Signal Store - 使用 NgRx Signal Store 管理認證狀態
 */
export const AuthStore = signalStore(
  { providedIn: 'root' },
  withState(initialState),
  withMethods((store) => {
    const authService = inject(AuthService);

    return {
      /**
       * 使用者登入
       */
      login: rxMethod<LoginRequest>(
        pipe(
          tap(() => patchState(store, { isLoading: true, error: null })),
          switchMap((request) =>
            authService.login(request).pipe(
              tap((response) => {
                patchState(store, {
                  user: response.user,
                  isLoading: false,
                  error: null,
                });
              }),
              catchError((error) => {
                patchState(store, {
                  user: null,
                  isLoading: false,
                  error: error.error?.detail || '登入失敗',
                });
                return of(null);
              })
            )
          )
        )
      ),

      /**
       * 使用者註冊
       */
      register: rxMethod<RegisterRequest>(
        pipe(
          tap(() => patchState(store, { isLoading: true, error: null })),
          switchMap((request) =>
            authService.register(request).pipe(
              tap((response) => {
                patchState(store, {
                  user: response.user,
                  isLoading: false,
                  error: null,
                });
              }),
              catchError((error) => {
                patchState(store, {
                  user: null,
                  isLoading: false,
                  error: error.error?.detail || '註冊失敗',
                });
                return of(null);
              })
            )
          )
        )
      ),

      /**
       * 取得當前使用者
       */
      loadCurrentUser: rxMethod<void>(
        pipe(
          tap(() => patchState(store, { isLoading: true, error: null })),
          switchMap(() =>
            authService.getCurrentUser().pipe(
              tap((user) => {
                patchState(store, {
                  user,
                  isLoading: false,
                  error: null,
                });
              }),
              catchError((error) => {
                patchState(store, {
                  user: null,
                  isLoading: false,
                  error: error.error?.detail || '取得使用者資訊失敗',
                });
                return of(null);
              })
            )
          )
        )
      ),

      /**
       * 使用者登出
       */
      logout: () => {
        authService.logout();
        patchState(store, initialState);
      },

      /**
       * 清除錯誤訊息
       */
      clearError: () => {
        patchState(store, { error: null });
      },
    };
  })
);
