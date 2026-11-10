"""Configuration settings for ERPNext Headless Portal."""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "ERPNext Headless Portal"
    VERSION: str = "1.0.0"
    API_PREFIX: str = "/api/v1"
    SECRET_KEY: str = "super-secret-jwt-key-replace-in-production-2026"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 1 day

    # ERPNext backend connection
    ERPNEXT_URL: str = "http://localhost:8000"
    ERPNEXT_API_KEY: str = "frappe_admin_key"
    ERPNEXT_API_SECRET: str = "frappe_admin_secret"

    class Config:
        env_file = ".env"
        extra = "allow"


settings = Settings()
