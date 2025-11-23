# Member System Backend (FastAPI)

會員系統後端 API，使用 FastAPI + SQLAlchemy + SQLite 開發。

## 功能特色

- ✅ 使用者註冊 (含密碼強度驗證)
- ✅ 使用者登入 (JWT 認證)
- ✅ 使用者登出
- ✅ 取得當前使用者資料
- ✅ 自動生成 API 文檔 (Swagger UI)
- ✅ 密碼 bcrypt 加密
- ✅ CORS 跨域支援

## 技術棧

- **FastAPI**: 現代化的 Python Web 框架
- **SQLAlchemy**: ORM 資料庫工具
- **SQLite**: 輕量級資料庫
- **Pydantic**: 資料驗證
- **JWT**: 認證機制
- **bcrypt**: 密碼加密

## 安裝與執行

### 1. 建立虛擬環境 (建議)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 2. 安裝依賴

```bash
pip install -r requirements.txt
```

### 3. 設定環境變數

複製 `.env.example` 為 `.env` 並修改設定:

```bash
cp .env.example .env
```

**重要**: 請修改 `.env` 中的 `SECRET_KEY` 為至少 32 字元的隨機字串。

### 4. 啟動伺服器

```bash
# 開發模式 (自動重載)
uvicorn app.main:app --reload --port 8000

# 生產模式
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### 5. 查看 API 文檔

啟動後訪問以下網址:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## API 端點

### 認證相關

| Method | Endpoint | 描述 | 需要認證 |
|--------|----------|------|----------|
| POST | `/api/auth/register` | 註冊新使用者 | ❌ |
| POST | `/api/auth/login` | 使用者登入 | ❌ |
| POST | `/api/auth/logout` | 使用者登出 | ✅ |
| GET | `/api/auth/me` | 取得當前使用者資料 | ✅ |

### 範例請求

#### 註冊

```bash
curl -X POST "http://localhost:8000/api/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "Test1234"
  }'
```

#### 登入

```bash
curl -X POST "http://localhost:8000/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "Test1234"
  }'
```

#### 取得當前使用者 (需要 token)

```bash
curl -X GET "http://localhost:8000/api/auth/me" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

## 專案結構

```
backend/
├── app/
│   ├── api/              # API 路由
│   │   └── auth.py
│   ├── core/             # 核心配置
│   │   ├── config.py
│   │   ├── database.py
│   │   └── security.py
│   ├── models/           # 資料庫模型
│   │   └── user.py
│   ├── schemas/          # Pydantic 驗證模型
│   │   └── user.py
│   ├── services/         # 業務邏輯
│   │   └── auth_service.py
│   └── main.py           # 應用入口
├── .env                  # 環境變數
├── .gitignore
├── requirements.txt      # Python 依賴
└── README.md
```

## 密碼規則

- 最少 8 個字元
- 至少 1 個大寫字母
- 至少 1 個小寫字母
- 至少 1 個數字

## 開發建議

1. 使用虛擬環境隔離依賴
2. 修改 `.env` 中的 `SECRET_KEY`
3. 生產環境建議使用 PostgreSQL 取代 SQLite
4. 啟用 HTTPS
5. 設定適當的 CORS 來源

## 測試

```bash
# 安裝測試依賴
pip install pytest pytest-asyncio httpx

# 執行測試
pytest
```

## License

MIT
