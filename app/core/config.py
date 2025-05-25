from pydantic_settings import BaseSettings
from typing import Optional
import secrets


class Settings(BaseSettings):
    PROJECT_NAME: str = "Exemplar Prompt Hub"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    PROJECT_URL: str = "http://localhost:8000"  # Used for OpenRouter rankings
    
    # Security
    SECRET_KEY: str = "your-secret-key"  # Replace with a secure key
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 days
    OPENAI_API_KEY: str
    
    # Database
    DATABASE_URL: str = "sqlite:///./prompt_hub.db"
    
    # CORS
    BACKEND_CORS_ORIGINS: list = ["*"]
    
    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    DEBUG: bool = False
    
    # OpenRouter settings
    OPENROUTER_API_KEY: Optional[str] = None
    
    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings() 