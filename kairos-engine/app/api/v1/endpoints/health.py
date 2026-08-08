"""Health and readiness probe endpoints."""
import time
from typing import Dict, Any
from fastapi import APIRouter
from app.services.providers.angelone_provider import AngelOneSmartApiProvider
from app.services.providers.yfinance_provider import YahooFinanceProvider
from app.services.providers.nse_provider import NSEDirectProvider

router = APIRouter(tags=["Health"])


@router.get("/health")
def get_health() -> Dict[str, Any]:
    """Basic liveness probe."""
    return {
        "status": "healthy",
        "service": "kairos-quant-engine",
        "timestamp": int(time.time()),
        "version": "1.0.0",
    }


@router.get("/ready")
def get_readiness() -> Dict[str, Any]:
    """Readiness probe checking upstream provider configurations."""
    angel = AngelOneSmartApiProvider()
    yf = YahooFinanceProvider()
    nse = NSEDirectProvider()
    
    return {
        "status": "ready",
        "timestamp": int(time.time()),
        "providers": {
            "angelone_smartapi": angel.is_healthy(),
            "yfinance_fallback": yf.is_healthy(),
            "nse_direct_scraper": nse.is_healthy(),
        },
    }
