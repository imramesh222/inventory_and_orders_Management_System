from typing import List
from pydantic_settings import BaseSettings
import os

class Settings(BaseSettings):
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./test.db")
    SECRET_KEY: str = os.getenv("SECRET_KEY", "supersecretkey")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60*24))
    SERVICE_PORT: int = int(os.getenv("SERVICE_PORT", 8000))

    # CORS
    ALLOW_ORIGINS: List[str] = ["*"]

    class Config:
        env_file = ".env"

settings = Settings()
