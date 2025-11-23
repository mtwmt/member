import { Component, inject, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { DatePipe } from '@angular/common';
import { AuthStore } from '../../core/store/auth-store';

@Component({
  selector: 'app-dashboard',
  imports: [DatePipe],
  templateUrl: './dashboard.html',
  styleUrl: './dashboard.css',
})
export class Dashboard implements OnInit {
  private readonly router = inject(Router);
  readonly authStore = inject(AuthStore);

  ngOnInit(): void {
    // 載入當前使用者資訊
    this.authStore.loadCurrentUser();
  }

  onLogout(): void {
    this.authStore.logout();
    this.router.navigate(['/auth/login']);
  }
}
