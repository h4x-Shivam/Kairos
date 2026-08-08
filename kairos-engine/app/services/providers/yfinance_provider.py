"""Yahoo Finance data provider adapter for OHLCV bars, financial ratios, and fallback quotes."""
import logging
from typing import List, Dict, Any, Optional
import numpy as np
import pandas as pd
import yfinance as yf
from app.schemas.enums import TimeFrame
from app.schemas.diagnostic import (
    OHLCVBar,
    FundamentalMetricsInput,
    SentimentDisclosureInput,
)
from app.services.providers.base import BaseDataProvider

logger = logging.getLogger(__name__)


def normalize_symbol_for_yf(symbol: str) -> str:
    """Ensure Indian equity symbol has .NS (default) or .BO suffix."""
    sym = symbol.strip().upper()
    if sym.endswith(".NS") or sym.endswith(".BO"):
        return sym
    return f"{sym}.NS"


class YahooFinanceProvider(BaseDataProvider):
    """Zero-cost Yahoo Finance provider implementation."""
    
    @property
    def provider_name(self) -> str:
        return "YahooFinanceProvider"
        
    def is_healthy(self) -> bool:
        return True
        
    def get_historical_ohlcv(
        self, symbol: str, timeframe: TimeFrame = TimeFrame.D1, limit: int = 100
    ) -> List[OHLCVBar]:
        """Fetch historical candlestick series via yfinance."""
        yf_symbol = normalize_symbol_for_yf(symbol)
        interval_map = {
            TimeFrame.M15: "15m",
            TimeFrame.D1: "1d",
            TimeFrame.W1: "1wk",
        }
        interval = interval_map.get(timeframe, "1d")
        
        # Determine period based on limit
        if timeframe == TimeFrame.M15:
            period = "30d"
        elif limit <= 100:
            period = "6mo"
        elif limit <= 250:
            period = "1y"
        else:
            period = "2y"
            
        ticker = yf.Ticker(yf_symbol)
        df = ticker.history(period=period, interval=interval)
        
        if df.empty or len(df) == 0:
            raise ValueError(f"No historical price data returned for {yf_symbol}")
            
        bars: List[OHLCVBar] = []
        for index, row in df.tail(limit).iterrows():
            # Convert timestamp index to epoch integer
            if isinstance(index, pd.Timestamp):
                epoch = int(index.timestamp())
            else:
                epoch = int(pd.to_datetime(index).timestamp())
                
            bars.append(
                OHLCVBar(
                    time=epoch,
                    open=float(row["Open"]),
                    high=float(row["High"]),
                    low=float(row["Low"]),
                    close=float(row["Close"]),
                    volume=float(row["Volume"]),
                )
            )
        return bars
        
    def get_live_quote(self, symbol: str) -> Dict[str, Any]:
        """Fetch latest price, 52W high/low, and market beta via yfinance."""
        yf_symbol = normalize_symbol_for_yf(symbol)
        ticker = yf.Ticker(yf_symbol)
        info = ticker.info or {}
        
        fast_info = getattr(ticker, "fast_info", None)
        last_price = (
            getattr(fast_info, "last_price", None)
            or info.get("currentPrice")
            or info.get("regularMarketPrice")
            or 0.0
        )
        high_52w = (
            getattr(fast_info, "year_high", None)
            or info.get("fiftyTwoWeekHigh")
            or (last_price * 1.1)
        )
        beta = float(info.get("beta") or 1.0)
        
        return {
            "symbol": yf_symbol,
            "current_price": float(last_price),
            "high_52w": float(high_52w),
            "beta": beta,
            "company_name": info.get("shortName") or info.get("longName") or yf_symbol,
        }
        
    def get_fundamental_metrics(self, symbol: str) -> Optional[FundamentalMetricsInput]:
        """Extract fundamentals from yfinance ticker info."""
        yf_symbol = normalize_symbol_for_yf(symbol)
        ticker = yf.Ticker(yf_symbol)
        info = ticker.info or {}
        
        peg_ratio = info.get("pegRatio")
        if peg_ratio is not None:
            peg_ratio = float(peg_ratio)
            
        roe = float(info.get("returnOnEquity") or 0.15) * 100.0
        roce_proxy = max(5.0, roe)
        
        # Debt to Equity
        de = info.get("debtToEquity")
        if de is not None:
            debt_to_equity = float(de) / 100.0 if float(de) > 10.0 else float(de)
        else:
            debt_to_equity = 0.3
            
        # Free Cash Flow to Net Profit
        fcf = info.get("freeCashflow")
        net_income = info.get("netIncomeToCommon")
        if fcf is not None and net_income is not None and net_income > 0:
            fcf_to_pat = float(fcf) / float(net_income)
        else:
            fcf_to_pat = 0.75
            
        return FundamentalMetricsInput(
            peg_ratio=peg_ratio,
            roce_current=round(roce_proxy, 1),
            roce_3q_avg=round(roce_proxy * 0.95, 1),
            promoter_pledge_pct=0.0,
            fcf_to_net_profit=round(fcf_to_pat, 2),
            debt_to_equity=round(debt_to_equity, 2),
        )
        
    def get_delivery_metrics(self, symbol: str) -> Optional[float]:
        """Yahoo Finance does not supply delivery percentages; returns None for NSE fallback."""
        return None
        
    def get_corporate_disclosures(
        self, symbol: str, days_back: int = 7
    ) -> List[SentimentDisclosureInput]:
        """Fetch recent news headlines from Yahoo Finance."""
        yf_symbol = normalize_symbol_for_yf(symbol)
        ticker = yf.Ticker(yf_symbol)
        news_items = ticker.news or []
        
        disclosures: List[SentimentDisclosureInput] = []
        for item in news_items:
            title = item.get("title", "")
            if not title:
                continue
            disclosures.append(
                SentimentDisclosureInput(
                    headline=title,
                    hours_ago=12.0, # Default recent window
                    sentiment_score=0.0, # Will be scored by SentimentService
                    is_tier1_trigger=False,
                )
            )
        return disclosures
