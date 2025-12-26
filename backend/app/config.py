"""Configuration settings"""
from pydantic_settings import BaseSettings
from typing import List
import os

class Settings(BaseSettings):
    """Application settings"""
    
    ANTHROPIC_API_KEY: str
    ENVIRONMENT: str = "development"
    CLAUDE_MODEL: str = "claude-sonnet-4-20250514"
    CLAUDE_MAX_TOKENS: int = 1000
    
    # CORS origins - simpler handling
    @property
    def CORS_ORIGINS(self) -> List[str]:
        """Get CORS origins from env or use defaults"""
        cors_env = os.getenv("CORS_ORIGINS", "")
        if cors_env:
            # If it's a comma-separated string
            return [origin.strip() for origin in cors_env.split(",")]
        # Default origins
        return [
            "http://localhost:3000",
            "http://localhost:3001",
            "https://*.vercel.app"
        ]
    
    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "ignore"

settings = Settings()
