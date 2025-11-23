import re
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator


def to_camel(string: str) -> str:
    """將 snake_case 轉換為 camelCase"""
    components = string.split('_')
    return components[0] + ''.join(x.title() for x in components[1:])


class UserCreate(BaseModel):
    """使用者註冊 Schema"""

    username: str = Field(
        ...,
        min_length=3,
        max_length=50,
        description="使用者名稱 (3-50 字元)"
    )
    email: EmailStr = Field(..., description="Email 地址")
    password: str = Field(
        ...,
        min_length=6,
        max_length=128,
        description="密碼 (6-128 字元)"
    )

    @field_validator("username")
    @classmethod
    def validate_username(cls, v: str) -> str:
        """驗證使用者名稱格式"""
        if not re.match(r"^[a-zA-Z0-9_]+$", v):
            raise ValueError("使用者名稱只能包含英文字母、數字和底線")
        return v


class UserLogin(BaseModel):
    """使用者登入 Schema"""

    email: EmailStr = Field(..., description="Email 地址")
    password: str = Field(..., description="密碼")


class UserResponse(BaseModel):
    """使用者回傳資料 Schema"""

    id: int
    username: str
    email: str
    is_login: bool
    created_time: datetime

    model_config = ConfigDict(
        from_attributes=True,
        alias_generator=to_camel,
        populate_by_name=True,
        serialize_by_alias=True,
    )


class Token(BaseModel):
    """JWT Token Schema"""

    access_token: str
    token_type: str = "bearer"

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        serialize_by_alias=True,
    )


class UserWithToken(BaseModel):
    """使用者資料 + Token Schema"""

    user: UserResponse
    access_token: str
    token_type: str = "bearer"

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        serialize_by_alias=True,
    )


class LogoutResponse(BaseModel):
    """登出回應 Schema"""

    message: str = "Successfully logged out"
