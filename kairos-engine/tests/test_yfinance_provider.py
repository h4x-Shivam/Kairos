"""Unit tests for YahooFinanceProvider adapter."""
import pandas as pd
import pytest
from app.services.providers.yfinance_provider import (
    YahooFinanceProvider,
    normalize_symbol_for_yf,
)
from app.schemas.enums import TimeFrame


def test_symbol_normalization():
    """Verify Indian ticker normalization to .NS default."""
    assert normalize_symbol_for_yf("RELIANCE") == "RELIANCE.NS"
    assert normalize_symbol_for_yf("TCS.NS") == "TCS.NS"
    assert normalize_symbol_for_yf("INFY.BO") == "INFY.BO"


def test_yfinance_historical_ohlcv_mock(mocker):
    """Verify OHLCV extraction and conversion to OHLCVBar objects."""
    provider = YahooFinanceProvider()
    
    # Mock yfinance Ticker.history DataFrame
    mock_df = pd.DataFrame({
        "Open": [100.0, 102.0, 105.0],
        "High": [105.0, 108.0, 110.0],
        "Low": [98.0, 101.0, 104.0],
        "Close": [102.0, 106.0, 108.0],
        "Volume": [1000.0, 1500.0, 2000.0],
    }, index=pd.date_range("2024-01-01", periods=3, freq="D"))
    
    mock_ticker = mocker.MagicMock()
    mock_ticker.history.return_value = mock_df
    mocker.patch("yfinance.Ticker", return_value=mock_ticker)
    
    bars = provider.get_historical_ohlcv("TATAMOTORS", timeframe=TimeFrame.D1, limit=3)
    assert len(bars) == 3
    assert bars[0].open == 100.0
    assert bars[-1].close == 108.0


def test_yfinance_fundamentals_mock(mocker):
    """Verify extraction of accounting ratios from Ticker.info."""
    provider = YahooFinanceProvider()
    
    mock_ticker = mocker.MagicMock()
    mock_ticker.info = {
        "pegRatio": 1.25,
        "returnOnEquity": 0.22,
        "debtToEquity": 35.0, # 35%
        "freeCashflow": 50000000.0,
        "netIncomeToCommon": 60000000.0,
    }
    mocker.patch("yfinance.Ticker", return_value=mock_ticker)
    
    fund = provider.get_fundamental_metrics("INFY")
    assert fund is not None
    assert fund.peg_ratio == 1.25
    assert fund.roce_current == 22.0
    assert fund.debt_to_equity == 0.35
    assert fund.fcf_to_net_profit == 0.83
