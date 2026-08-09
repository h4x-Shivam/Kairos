"""Application configuration and environment variables via Pydantic Settings."""
from typing import Optional
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Central configuration parameters for Kairos Engine."""
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )
    
    # Environment
    ENVIRONMENT: str = Field("development", description="development | staging | production")
    LOG_LEVEL: str = Field("INFO")
    
    # Databases
    DATABASE_URL: str = Field(..., description="PostgreSQL database URL")
    REDIS_URL: str = Field(..., description="Redis connection URL")
    
    # AngelOne SmartAPI Credentials
    ANGELONE_API_KEY: Optional[str] = Field(None)
    ANGELONE_CLIENT_CODE: Optional[str] = Field(None)
    ANGELONE_PIN: Optional[str] = Field(None)
    ANGELONE_TOTP_KEY: Optional[str] = Field(None)
    
    # Fallback Toggles
    ENABLE_YFINANCE_FALLBACK: bool = Field(True)
    ENABLE_NSE_SCRAPER_FALLBACK: bool = Field(True)
    
    # Cache TTLs (Seconds)
    CACHE_TTL_QUOTE_SECONDS: int = Field(15)
    CACHE_TTL_OHLCV_SECONDS: int = Field(300)
    CACHE_TTL_FUNDAMENTALS_SECONDS: int = Field(86400)
    CACHE_TTL_FILINGS_SECONDS: int = Field(1800)
    
    # Network Timeouts
    HTTP_TIMEOUT_SECONDS: float = Field(10.0)


settings = Settings()
