from typing import Optional

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.security import create_access_token, hash_password, verify_password
from app.models.user import User
from app.schemas.user import UserCreate, UserLogin


class AuthService:
    """認證服務 - 處理所有認證相關的業務邏輯"""

    @staticmethod
    def register_user(db: Session, user_data: UserCreate) -> User:
        """
        註冊新使用者

        Args:
            db: 資料庫 session
            user_data: 使用者註冊資料

        Returns:
            建立的使用者物件

        Raises:
            HTTPException: 當 email 或 username 已存在時
        """
        # 檢查 email 是否已存在
        existing_user = db.query(User).filter(User.email == user_data.email).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email 已被註冊"
            )

        # 檢查 username 是否已存在
        existing_user = db.query(User).filter(
            User.username == user_data.username
        ).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="使用者名稱已被使用"
            )

        # 建立新使用者
        hashed_pw = hash_password(user_data.password)
        new_user = User(
            username=user_data.username,
            email=user_data.email,
            password_hash=hashed_pw
        )

        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return new_user

    @staticmethod
    def authenticate_user(db: Session, login_data: UserLogin) -> Optional[User]:
        """
        驗證使用者登入

        Args:
            db: 資料庫 session
            login_data: 登入資料

        Returns:
            使用者物件，若驗證失敗則回傳 None
        """
        # 查詢使用者
        user = db.query(User).filter(User.email == login_data.email).first()

        # 驗證使用者是否存在及密碼是否正確
        if not user or not verify_password(login_data.password, user.password_hash):
            return None

        # 檢查帳號是否啟用
        if not user.is_login:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="帳號已被停用"
            )

        return user

    @staticmethod
    def create_user_token(user_id: int) -> str:
        """
        為使用者建立 JWT token

        Args:
            user_id: 使用者 ID

        Returns:
            JWT token 字串
        """
        token_data = {"sub": str(user_id)}
        return create_access_token(token_data)

    @staticmethod
    def get_user_by_id(db: Session, user_id: int) -> Optional[User]:
        """
        根據 ID 取得使用者

        Args:
            db: 資料庫 session
            user_id: 使用者 ID

        Returns:
            使用者物件，若不存在則回傳 None
        """
        return db.query(User).filter(User.id == user_id).first()
