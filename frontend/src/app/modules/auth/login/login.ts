import { Component, inject, effect } from '@angular/core';
import { FormBuilder, FormGroup, Validators, ReactiveFormsModule } from '@angular/forms';
import { Router, RouterLink, ActivatedRoute } from '@angular/router';
import { AuthStore } from '../../../core/store/auth-store';

@Component({
  selector: 'app-login',
  imports: [ReactiveFormsModule, RouterLink],
  templateUrl: './login.html',
  styleUrl: './login.css',
})
export class Login {
  private readonly fb = inject(FormBuilder);
  private readonly router = inject(Router);
  private readonly route = inject(ActivatedRoute);
  readonly authStore = inject(AuthStore);

  loginForm: FormGroup;
  returnUrl: string = '/dashboard';

  constructor() {
    this.loginForm = this.fb.group({
      email: ['', [Validators.required, Validators.email]],
      password: ['', [Validators.required, Validators.minLength(6)]],
    });

    // 取得登入後要返回的 URL
    this.returnUrl = this.route.snapshot.queryParams['returnUrl'] || '/dashboard';

    // 使用 effect 監聽登入狀態變化
    effect(() => {
      const user = this.authStore.user();
      if (user && !this.authStore.isLoading()) {
        this.router.navigate([this.returnUrl]);
      }
    });
  }

  onSubmit(): void {
    if (this.loginForm.valid) {
      const { email, password } = this.loginForm.value;
      this.authStore.login({ email, password });
    } else {
      this.loginForm.markAllAsTouched();
    }
  }

  get email() {
    return this.loginForm.get('email');
  }

  get password() {
    return this.loginForm.get('password');
  }
}
