from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """應用程式配置"""

    # Database
    DATABASE_URL: str = "sqlite:///./member.db"

    # Security
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440  # 24 hours

    # CORS
    CORS_ORIGINS: str = "http://localhost:4200,http://localhost:4201,http://127.0.0.1:4200,http://127.0.0.1:4201"

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True
    )

    @property
    def cors_origins_list(self) -> list[str]:
        """將 CORS_ORIGINS 字串轉換為列表"""
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]


# 建立全域設定實例
settings = Settings()
