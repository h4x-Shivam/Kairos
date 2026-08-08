"""Unit tests for Pydantic Settings configuration."""
from app.core.config import Settings


def test_default_config_settings():
    """Verify default settings values and fallback flags."""
    cfg = Settings()
    assert cfg.ENVIRONMENT == "development"
    assert cfg.ENABLE_YFINANCE_FALLBACK is True
    assert cfg.ENABLE_NSE_SCRAPER_FALLBACK is True
    assert cfg.CACHE_TTL_QUOTE_SECONDS == 15
    assert cfg.CACHE_TTL_OHLCV_SECONDS == 300
    assert cfg.CACHE_TTL_FUNDAMENTALS_SECONDS == 86400
    assert cfg.CACHE_TTL_FILINGS_SECONDS == 1800
    assert cfg.HTTP_TIMEOUT_SECONDS == 10.0
