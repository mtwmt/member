# 會員系統架構設計文檔

## 技術棧

### 前端
- **框架**: Angular 17+ (Standalone Components)
- **狀態管理**: @ngrx/signals (Signal Store)
- **UI 框架**: TailwindCSS + DaisyUI
- **HTTP Client**: Angular HttpClient with Interceptors
- **認證**: JWT (存於 localStorage)

### 後端
- **框架**: FastAPI (Python 3.10+)
- **ORM**: SQLAlchemy 2.0
- **資料庫**: SQLite
- **認證**: JWT (python-jose)
- **密碼加密**: bcrypt (passlib)
- **資料驗證**: Pydantic v2
- **API 文檔**: 自動生成 OpenAPI (Swagger)

---

## 系統架構圖

```
┌──────────────────────────────────────────────────────────┐
│                     Frontend Layer                        │
│  ┌────────────────────────────────────────────────────┐  │
│  │  Presentation Layer (Components)                   │  │
│  │  ├─ Smart Components (Container)                   │  │
│  │  │  ├─ LoginComponent                              │  │
│  │  │  ├─ RegisterComponent                           │  │
│  │  │  └─ DashboardComponent                          │  │
│  │  └─ Presentational Components (UI)                 │  │
│  └────────────────────────────────────────────────────┘  │
│  ┌────────────────────────────────────────────────────┐  │
│  │  Business Logic Layer (Services & Store)           │  │
│  │  ├─ AuthService (API 呼叫)                         │  │
│  │  ├─ AuthStore (Signal Store - 狀態管理)           │  │
│  │  ├─ AuthGuard (路由守衛)                           │  │
│  │  └─ AuthInterceptor (自動附加 JWT)                 │  │
│  └────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────┘
                          ↕ HTTP/REST API (JSON)
┌──────────────────────────────────────────────────────────┐
│                     Backend Layer                         │
│  ┌────────────────────────────────────────────────────┐  │
│  │  API Layer (FastAPI Routes)                        │  │
│  │  ├─ POST /api/auth/register                        │  │
│  │  ├─ POST /api/auth/login                           │  │
│  │  ├─ POST /api/auth/logout                          │  │
│  │  └─ GET  /api/auth/user (需要 JWT)                   │  │
│  └────────────────────────────────────────────────────┘  │
│  ┌────────────────────────────────────────────────────┐  │
│  │  Business Logic Layer (Services)                   │  │
│  │  ├─ AuthService                                    │  │
│  │  │  ├─ register_user()                             │  │
│  │  │  ├─ authenticate_user()                         │  │
│  │  │  └─ get_current_user()                          │  │
│  │  └─ Security Module                                │  │
│  │     ├─ hash_password()                             │  │
│  │     ├─ verify_password()                           │  │
│  │     ├─ create_access_token()                       │  │
│  │     └─ verify_token()                              │  │
│  └────────────────────────────────────────────────────┘  │
│  ┌────────────────────────────────────────────────────┐  │
│  │  Data Access Layer (SQLAlchemy)                    │  │
│  │  ├─ User Model (ORM)                               │  │
│  │  └─ Database Session Management                    │  │
│  └────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────┘
                          ↕ ORM
┌──────────────────────────────────────────────────────────┐
│                  Database Layer (SQLite)                  │
│  ├─ users (id, username, email, password_hash, ...)      │
└──────────────────────────────────────────────────────────┘
```

---

## 資料庫設計

### Users Table Schema

```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    is_login BOOLEAN DEFAULT TRUE,
    created_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_username ON users(username);
```

---

## API 規格

### 1. 註冊 API

**Endpoint**: `POST /api/auth/register`

**Request Body**:
```json
{
  "username": "string (3-50 chars)",
  "email": "string (valid email)",
  "password": "string (8-128 chars, 需包含大小寫字母+數字)"
}
```

**Response (Success - 201)**:
```json
{
  "user": {
    "id": 1,
    "username": "testuser",
    "email": "test@example.com",
    "created_time": "2025-01-23T12:00:00"
  },
  "access_token": "eyJhbGc...",
  "token_type": "bearer"
}
```

**Response (Error - 400)**:
```json
{
  "detail": "Email already registered"
}
```

---

### 2. 登入 API

**Endpoint**: `POST /api/auth/login`

**Request Body**:
```json
{
  "email": "string",
  "password": "string"
}
```

**Response (Success - 200)**:
```json
{
  "user": {
    "id": 1,
    "username": "testuser",
    "email": "test@example.com"
  },
  "access_token": "eyJhbGc...",
  "token_type": "bearer"
}
```

**Response (Error - 401)**:
```json
{
  "detail": "Incorrect email or password"
}
```

---

### 3. 登出 API

**Endpoint**: `POST /api/auth/logout`

**Headers**: `Authorization: Bearer {token}`

**Response (Success - 200)**:
```json
{
  "message": "Successfully logged out"
}
```

---

### 4. 取得當前用戶 API

**Endpoint**: `GET /api/auth/user`

**Headers**: `Authorization: Bearer {token}`

**Response (Success - 200)**:
```json
{
  "id": 1,
  "username": "testuser",
  "email": "test@example.com",
  "is_login": true,
  "created_time": "2025-01-23T12:00:00"
}
```

**Response (Error - 401)**:
```json
{
  "detail": "Could not validate credentials"
}
```

---

## 後端目錄結構

```
backend/
├── app/
│   ├── api/
│   │   ├── __init__.py
│   │   └── auth.py              # 認證相關路由
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py            # 環境變數配置
│   │   ├── database.py          # 資料庫連接
│   │   └── security.py          # JWT & 密碼處理
│   ├── models/
│   │   ├── __init__.py
│   │   └── user.py              # SQLAlchemy User Model
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── user.py              # Pydantic 驗證模型
│   ├── services/
│   │   ├── __init__.py
│   │   └── auth_service.py      # 認證業務邏輯
│   ├── __init__.py
│   └── main.py                  # FastAPI 應用入口
├── tests/
│   └── test_auth.py
├── .env
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

---

## 前端目錄結構

```
frontend/
├── src/
│   ├── app/
│   │   ├── core/
│   │   │   ├── guards/
│   │   │   │   └── auth.guard.ts
│   │   │   ├── interceptors/
│   │   │   │   └── auth.interceptor.ts
│   │   │   └── services/
│   │   │       └── auth.service.ts
│   │   ├── shared/
│   │   │   ├── components/
│   │   │   └── models/
│   │   │       └── user.model.ts
│   │   ├── modules/
│   │   │   ├── auth/
│   │   │   │   ├── login/
│   │   │   │   │   ├── login.component.ts
│   │   │   │   │   ├── login.component.html
│   │   │   │   │   └── login.component.css
│   │   │   │   ├── register/
│   │   │   │   │   ├── register.component.ts
│   │   │   │   │   ├── register.component.html
│   │   │   │   │   └── register.component.css
│   │   │   │   └── auth.routes.ts
│   │   │   └── dashboard/
│   │   │       ├── dashboard.component.ts
│   │   │       ├── dashboard.component.html
│   │   │       ├── dashboard.component.css
│   │   │       └── dashboard.routes.ts
│   │   ├── store/
│   │   │   └── auth.store.ts     # Signal Store
│   │   ├── app.component.ts
│   │   ├── app.config.ts
│   │   └── app.routes.ts
│   ├── environments/
│   │   ├── environment.ts
│   │   └── environment.prod.ts
│   ├── assets/
│   ├── styles.css
│   └── index.html
├── tailwind.config.js
├── angular.json
├── tsconfig.json
└── package.json
```

---

## 安全性設計

### 1. 密碼強度規則 (中強度)
- 最少 8 個字元
- 至少包含 1 個大寫字母
- 至少包含 1 個小寫字母
- 至少包含 1 個數字
- 可選:特殊字元

### 2. JWT 配置
- **演算法**: HS256
- **過期時間**: 24 小時
- **儲存位置**: localStorage (前端)
- **傳輸方式**: Authorization Header (Bearer token)

### 3. CORS 設定
```python
origins = [
    "http://localhost:4200",  # Angular dev server
    "http://localhost:8080",
]
```

### 4. 密碼加密
- **演算法**: bcrypt
- **Rounds**: 12

---

## 開發流程

### Phase 1: 後端開發
1. 設置 FastAPI 專案
2. 建立資料庫模型
3. 實作認證邏輯
4. 實作 API endpoints
5. 測試 API (Swagger UI)

### Phase 2: 前端開發
1. 設置 Angular 專案
2. 配置 TailwindCSS + DaisyUI
3. 建立 Signal Store
4. 實作登入/註冊組件
5. 實作 Auth Guard & Interceptor
6. 整合後端 API

### Phase 3: 整合測試
1. 前後端聯調
2. 測試完整流程
3. 錯誤處理優化

---

## 環境變數

### Backend (.env)
```env
DATABASE_URL=sqlite:///./member.db
SECRET_KEY=your-secret-key-min-32-chars
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440
CORS_ORIGINS=http://localhost:4200
```

### Frontend (environment.ts)
```typescript
export const environment = {
  production: false,
  apiUrl: 'http://localhost:8000/api'
};
```

---

## 部署考量

### 開發環境
- Backend: `uvicorn app.main:app --reload --port 8000`
- Frontend: `ng serve --port 4200`

### 生產環境
- Backend: Uvicorn + Gunicorn
- Frontend: `ng build --configuration production`
- 資料庫: 考慮升級至 PostgreSQL

---

## 未來擴展方向

1. **會員功能**
   - 忘記密碼 (Email 驗證)
   - Email 驗證機制
   - 會員資料編輯
   - 頭像上傳

2. **權限管理**
   - 角色系統 (RBAC)
   - 權限控管

3. **社交登入**
   - Google OAuth
   - Facebook Login

4. **安全性增強**
   - Refresh Token 機制
   - 多因素認證 (2FA)
   - 登入日誌

5. **效能優化**
   - Redis 快取
   - API Rate Limiting
   - 資料庫索引優化
