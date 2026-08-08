"""Abstract BaseDataProvider interface defining the contract for all market data sources."""
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from app.schemas.enums import TimeFrame
from app.schemas.diagnostic import (
    OHLCVBar,
    FundamentalMetricsInput,
    TechnicalMetricsInput,
    QuantMetricsInput,
    SentimentDisclosureInput,
)


class BaseDataProvider(ABC):
    """Abstract provider interface for market data ingestion."""
    
    @property
    @abstractmethod
    def provider_name(self) -> str:
        """Unique identifier name for this data provider."""
        pass
        
    @abstractmethod
    def is_healthy(self) -> bool:
        """Check if provider connection / API credentials are valid and active."""
        pass
        
    @abstractmethod
    def get_historical_ohlcv(
        self, symbol: str, timeframe: TimeFrame = TimeFrame.D1, limit: int = 100
    ) -> List[OHLCVBar]:
        """Fetch historical OHLCV candlestick series."""
        pass
        
    @abstractmethod
    def get_live_quote(self, symbol: str) -> Dict[str, Any]:
        """Fetch real-time LTP, 52W high, and volume quote."""
        pass
        
    @abstractmethod
    def get_fundamental_metrics(self, symbol: str) -> Optional[FundamentalMetricsInput]:
        """Fetch financial ratios and accounting metrics."""
        pass
        
    @abstractmethod
    def get_delivery_metrics(self, symbol: str) -> Optional[float]:
        """Fetch security delivery accumulation percentage."""
        pass
        
    @abstractmethod
    def get_corporate_disclosures(
        self, symbol: str, days_back: int = 7
    ) -> List[SentimentDisclosureInput]:
        """Fetch corporate announcements and regulatory filings."""
        pass
