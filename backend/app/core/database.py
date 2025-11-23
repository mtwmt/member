from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

# 建立資料庫引擎
# SQLite 需要 check_same_thread=False，PostgreSQL 不需要
connect_args = {}
if settings.DATABASE_URL.startswith("sqlite"):
    connect_args["check_same_thread"] = False

engine = create_engine(settings.DATABASE_URL, connect_args=connect_args)

# 建立 Session 工廠
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 建立 Base class 供 models 繼承
Base = declarative_base()


def get_db():
    """
    Dependency: 取得資料庫 session
    使用 yield 確保 session 會被正確關閉
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """初始化資料庫 - 建立所有資料表"""
    # 匯入所有 models 確保它們被註冊
    from app.models import user  # noqa

    # 建立所有資料表
    Base.metadata.create_all(bind=engine)
