"""AngelOne SmartAPI data provider adapter with automated TOTP headless authentication."""
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import pyotp
try:
    from SmartApi import SmartConnect
except ImportError:
    SmartConnect = None  # type: ignore
from app.core.config import settings
from app.schemas.enums import TimeFrame
from app.schemas.diagnostic import (
    OHLCVBar,
    FundamentalMetricsInput,
    SentimentDisclosureInput,
)
from app.services.providers.base import BaseDataProvider

logger = logging.getLogger(__name__)


class AngelOneSmartApiProvider(BaseDataProvider):
    """Production broker feed provider leveraging AngelOne SmartAPI."""
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        client_code: Optional[str] = None,
        pin: Optional[str] = None,
        totp_key: Optional[str] = None,
    ):
        self.api_key = api_key or settings.ANGELONE_API_KEY
        self.client_code = client_code or settings.ANGELONE_CLIENT_CODE
        self.pin = pin or settings.ANGELONE_PIN
        self.totp_key = totp_key or settings.ANGELONE_TOTP_KEY
        
        self.smart_api: Optional[SmartConnect] = None
        self.auth_token: Optional[str] = None
        self.feed_token: Optional[str] = None
        
    @property
    def provider_name(self) -> str:
        return "AngelOneSmartApiProvider"
        
    def is_healthy(self) -> bool:
        """Check if all required credentials are configured."""
        return bool(self.api_key and self.client_code and self.pin and self.totp_key)
        
    def authenticate(self) -> bool:
        """Perform automated headless 2FA login via TOTP generator."""
        if not self.is_healthy():
            logger.info("AngelOne credentials not configured. Operating in fallback mode.")
            return False
            
        try:
            self.smart_api = SmartConnect(api_key=self.api_key)
            totp_code = pyotp.TOTP(self.totp_key).now()
            session_data = self.smart_api.generateSession(
                clientCode=self.client_code,
                password=self.pin,
                totp=totp_code,
            )
            
            if session_data and session_data.get("status") and session_data.get("data"):
                self.auth_token = session_data["data"].get("jwtToken")
                self.feed_token = self.smart_api.getfeedToken()
                logger.info("AngelOne SmartAPI authenticated successfully.")
                return True
            else:
                logger.warning("AngelOne authentication failed: %s", session_data)
                return False
        except Exception as e:
            logger.error("Exception during AngelOne TOTP authentication: %s", e)
            return False
            
    def get_historical_ohlcv(
        self, symbol: str, timeframe: TimeFrame = TimeFrame.D1, limit: int = 100
    ) -> List[OHLCVBar]:
        """Fetch historical candlestick series from AngelOne."""
        if not self.auth_token:
            if not self.authenticate():
                return []
                
        interval_map = {
            TimeFrame.M15: "FIFTEEN_MINUTE",
            TimeFrame.D1: "ONE_DAY",
            TimeFrame.W1: "ONE_DAY", # Aggregate to 1w if needed
        }
        interval = interval_map.get(timeframe, "ONE_DAY")
        
        now = datetime.now()
        from_date = (now - timedelta(days=limit * 2)).strftime("%Y-%m-%d 09:15")
        to_date = now.strftime("%Y-%m-%d 15:30")
        
        # Clean symbol token resolution (or symbol mapping)
        sym = symbol.strip().upper().replace(".NS", "").replace(".BO", "")
        
        try:
            # We must map 'sym' to an AngelOne numerical token (e.g., from OpenAPIScripMaster.json).
            # Returning empty list to force Yahoo Finance fallback until mapping is implemented.
            logger.warning("AngelOne OHLCV mapping not implemented for %s, falling back to YFinance", sym)
            return []
            
            candle_params = {
                "exchange": "NSE",
                "symboltoken": "3045", # Placeholder token or mapped token
                "interval": interval,
                "fromdate": from_date,
                "todate": to_date,
            }
            if self.smart_api:
                data = self.smart_api.getCandleData(candle_params)
                if data and data.get("status") and data.get("data"):
                    bars: List[OHLCVBar] = []
                    for row in data["data"][-limit:]:
                        # Format: [datetime_str, open, high, low, close, volume]
                        dt = datetime.fromisoformat(row[0])
                        bars.append(
                            OHLCVBar(
                                time=int(dt.timestamp()),
                                open=float(row[1]),
                                high=float(row[2]),
                                low=float(row[3]),
                                close=float(row[4]),
                                volume=float(row[5]),
                            )
                        )
                    return bars
        except Exception as e:
            logger.warning("Error fetching AngelOne OHLCV for %s: %s", sym, e)
        return []
        
    def get_live_quote(self, symbol: str) -> Dict[str, Any]:
        """Fetch live LTP and tick quote via AngelOne SmartAPI."""
        if not self.auth_token:
            if not self.authenticate():
                return {}
        return {}
        
    def get_fundamental_metrics(self, symbol: str) -> Optional[FundamentalMetricsInput]:
        """AngelOne does not provide accounting fundamentals; returns None."""
        return None
        
    def get_delivery_metrics(self, symbol: str) -> Optional[float]:
        return None
        
    def get_corporate_disclosures(
        self, symbol: str, days_back: int = 7
    ) -> List[SentimentDisclosureInput]:
        return []
