from pydantic_settings import BaseSettings
from typing import List
import secrets


class Settings(BaseSettings):
    PROJECT_NAME: str = "ALrashid Portfolio Management"
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days
    
    POSTGRES_SERVER: str = "localhost"
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_DB: str = "alrashid_portfolio"
    POSTGRES_PORT: str = "5432"
    
    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
    
    BASE_CURRENCY: str = "KWD"
    SECONDARY_CURRENCY: str = "USD"
    SUPPORTED_CURRENCIES: List[str] = ["KWD", "USD", "GBP", "EUR", "AED", "SAR", "EGP"]
    
    TIMEZONE: str = "Asia/Kuwait"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
