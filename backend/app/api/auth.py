from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import decode_access_token
from app.schemas.user import (
    LogoutResponse,
    UserCreate,
    UserLogin,
    UserResponse,
    UserWithToken,
)
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["Authentication"])

# HTTP Bearer token scheme
security = HTTPBearer()


def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
    db: Session = Depends(get_db)
) -> UserResponse:
    """
    Dependency: 取得當前登入的使用者
    從 JWT token 解析使用者 ID 並從資料庫取得使用者資料
    """
    token = credentials.credentials
    payload = decode_access_token(token)

    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="無效的認證憑證",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user_id = payload.get("sub")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="無效的認證憑證",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = AuthService.get_user_by_id(db, int(user_id))
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="使用者不存在",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return UserResponse.model_validate(user)


@router.post("/register", response_model=UserWithToken, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """
    註冊新使用者

    - **username**: 使用者名稱 (3-50 字元，只能包含英文字母、數字和底線)
    - **email**: Email 地址
    - **password**: 密碼 (8-128 字元，需包含大小寫字母和數字)

    回傳使用者資料和 JWT token
    """
    # 建立使用者
    user = AuthService.register_user(db, user_data)

    # 產生 token
    access_token = AuthService.create_user_token(user.id)

    # 回傳使用者資料和 token
    return UserWithToken(
        user=UserResponse.model_validate(user),
        access_token=access_token
    )


@router.post("/login", response_model=UserWithToken)
async def login(login_data: UserLogin, db: Session = Depends(get_db)):
    """
    使用者登入

    - **email**: Email 地址
    - **password**: 密碼

    回傳使用者資料和 JWT token
    """
    # 驗證使用者
    user = AuthService.authenticate_user(db, login_data)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email 或密碼錯誤",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # 產生 token
    access_token = AuthService.create_user_token(user.id)

    # 回傳使用者資料和 token
    return UserWithToken(
        user=UserResponse.model_validate(user),
        access_token=access_token
    )


@router.post("/logout", response_model=LogoutResponse)
async def logout(current_user: UserResponse = Depends(get_current_user)):
    """
    使用者登出

    需要在 Header 中提供有效的 JWT token
    (前端需要自行清除 localStorage 中的 token)
    """
    return LogoutResponse()


@router.get("/user", response_model=UserResponse)
async def get_current_user_info(current_user: UserResponse = Depends(get_current_user)):
    """
    取得當前登入使用者的資料

    需要在 Header 中提供有效的 JWT token
    """
    return current_user
