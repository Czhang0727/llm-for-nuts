"""
Configuration management for bot chat API
"""
import os
from typing import Literal
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings"""
    
    # API Configuration
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 5000
    
    # LLM Provider Configuration
    LLM_PROVIDER: Literal["openai", "dashscope"] = "openai"
    
    # API Keys
    OPENAI_API_KEY: str = ""
    DASHSCOPE_API_KEY: str = ""
    
    # LLM Model Configuration
    OPENAI_MODEL: str = "gpt-3.5-turbo"
    DASHSCOPE_MODEL: str = "qwen-turbo"
    
    # Chat Configuration
    MAX_HISTORY_LENGTH: int = 20  # Maximum number of messages to keep in context
    
    # Database Configuration
    DATABASE_PATH: str = "data/chat.db"  # SQLite database file path
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


# Global settings instance
settings = Settings()

# Validate API keys based on provider
if settings.LLM_PROVIDER == "openai" and not settings.OPENAI_API_KEY:
    print("Warning: OPENAI_API_KEY not set. OpenAI provider will not work.")
elif settings.LLM_PROVIDER == "dashscope" and not settings.DASHSCOPE_API_KEY:
    print("Warning: DASHSCOPE_API_KEY not set. Dashscope provider will not work.")

