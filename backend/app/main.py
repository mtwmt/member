from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import auth
from app.core.config import settings
from app.core.database import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    """應用程式生命週期管理"""
    # Startup: 初始化資料庫
    print(" Initializing database...")
    init_db()
    print(" Database initialized successfully")
    yield
    # Shutdown: 清理資源 (如果需要)
    print(" Shutting down...")


# 建立 FastAPI 應用程式
app = FastAPI(
    title="Member System API",
    description="會員系統後端 API - 提供註冊、登入、登出等功能",
    version="1.0.0",
    lifespan=lifespan
)

# 設定 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 註冊路由
app.include_router(auth.router, prefix="/api")


@app.get("/")
async def root():
    """根路徑 - API 健康檢查"""
    return {
        "message": "Member System API is running",
        "docs": "/docs",
        "redoc": "/redoc"
    }


@app.get("/health")
async def health_check():
    """健康檢查端點"""
    return {"status": "healthy"}
