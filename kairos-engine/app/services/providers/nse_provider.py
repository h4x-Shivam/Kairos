"""NSE India direct data provider adapter for live delivery percentage and market quotes."""
import logging
from typing import List, Dict, Any, Optional
import httpx
from app.schemas.enums import TimeFrame
from app.schemas.diagnostic import (
    OHLCVBar,
    FundamentalMetricsInput,
    SentimentDisclosureInput,
)
from app.services.providers.base import BaseDataProvider

logger = logging.getLogger(__name__)

NSE_BASE_URL = "https://www.nseindia.com"
NSE_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
    "Accept": "*/*",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://www.nseindia.com/get-quotes/equity?symbol=TCS",
}


def clean_nse_symbol(symbol: str) -> str:
    """Strip .NS / .BO exchange suffixes for NSE endpoints."""
    return symbol.strip().upper().replace(".NS", "").replace(".BO", "")


class NSEDirectProvider(BaseDataProvider):
    """Direct NSE India scraper provider for live delivery % and official bhavcopy data."""
    
    def __init__(self, timeout: float = 6.0):
        self.timeout = timeout
        self._session: Optional[httpx.Client] = None
        
    @property
    def provider_name(self) -> str:
        return "NSEDirectProvider"
        
    def _get_client(self) -> httpx.Client:
        """Create or return an active HTTP client with fresh NSE session cookies."""
        if self._session is None or self._session.is_closed:
            self._session = httpx.Client(
                headers=NSE_HEADERS,
                timeout=self.timeout,
                follow_redirects=True,
            )
            try:
                # Prime session cookies
                self._session.get(NSE_BASE_URL)
            except Exception as e:
                logger.warning("Failed to prime NSE cookies: %s", e)
        return self._session
        
    def is_healthy(self) -> bool:
        return True
        
    def get_delivery_metrics(self, symbol: str) -> Optional[float]:
        """Fetch official security-wise delivery percentage from NSE trade info."""
        sym = clean_nse_symbol(symbol)
        url = f"{NSE_BASE_URL}/api/quote-equity?symbol={sym}&section=trade_info"
        try:
            client = self._get_client()
            resp = client.get(url)
            if resp.status_code == 200:
                data = resp.json()
                sec_info = data.get("securityWiseDP", {})
                delivery_pct = sec_info.get("deliveryToTradedQuantity")
                if delivery_pct is not None:
                    return round(float(delivery_pct), 1)
        except Exception as e:
            logger.warning("Error fetching NSE delivery metrics for %s: %s", sym, e)
        return None
        
    def get_live_quote(self, symbol: str) -> Dict[str, Any]:
        """Fetch official NSE LTP, 52W High/Low, and company metadata."""
        sym = clean_nse_symbol(symbol)
        url = f"{NSE_BASE_URL}/api/quote-equity?symbol={sym}"
        try:
            client = self._get_client()
            resp = client.get(url)
            if resp.status_code == 200:
                data = resp.json()
                price_info = data.get("priceInfo", {})
                info = data.get("info", {})
                return {
                    "symbol": f"{sym}.NS",
                    "current_price": float(price_info.get("lastPrice") or 0.0),
                    "high_52w": float(price_info.get("weekHighLow", {}).get("max") or 0.0),
                    "company_name": info.get("companyName") or sym,
                    "beta": 1.0,
                }
        except Exception as e:
            logger.warning("Error fetching NSE live quote for %s: %s", sym, e)
        return {"symbol": f"{sym}.NS", "current_price": 0.0, "high_52w": 0.0, "beta": 1.0}
        
    def get_historical_ohlcv(
        self, symbol: str, timeframe: TimeFrame = TimeFrame.D1, limit: int = 100
    ) -> List[OHLCVBar]:
        """Historical series is delegated to Yahoo Finance / AngelOne for lower latency."""
        return []
        
    def get_fundamental_metrics(self, symbol: str) -> Optional[FundamentalMetricsInput]:
        return None
        
    def get_corporate_disclosures(
        self, symbol: str, days_back: int = 7
    ) -> List[SentimentDisclosureInput]:
        return []
        
    def close(self):
        """Close active HTTP client session."""
        if self._session and not self._session.is_closed:
            self._session.close()
