"""Unit tests for Wilder ATR, Chandelier Ratchet, and Technical Indicators."""
import numpy as np
import pytest
from app.schemas.diagnostic import OHLCVBar
from app.engine.indicators import (
    compute_true_range,
    compute_wilder_atr,
    compute_chandelier_stop_series,
    compute_rsi_series,
)


def create_synthetic_bars(n: int = 30, base_price: float = 1000.0) -> list[OHLCVBar]:
    """Generate n synthetic OHLCV bars with steady upward trend."""
    bars = []
    for i in range(n):
        p = base_price + (i * 10.0)
        bars.append(
            OHLCVBar(
                time=1700000000 + (i * 86400),
                open=p - 2.0,
                high=p + 8.0,
                low=p - 5.0,
                close=p + 4.0,
                volume=100000.0 + (i * 1000),
            )
        )
    return bars


def test_true_range_calculation():
    """Verify true range handles gap ups and gap downs correctly."""
    highs = np.array([100.0, 110.0, 105.0])
    lows = np.array([90.0, 95.0, 85.0])
    closes = np.array([95.0, 105.0, 90.0])
    
    tr = compute_true_range(highs, lows, closes)
    assert len(tr) == 3
    assert tr[0] == 10.0 # 100 - 90
    assert tr[1] == 15.0 # max(110-95, |110-95|, |95-95|) = 15
    assert tr[2] == 20.0 # max(105-85, |105-105|, |85-105|) = 20


def test_wilder_atr_smoothing():
    """Verify Wilder's 14-period exponential smoothing formula."""
    # Create constant true range bars where High - Low = 10.0 and Close = Low + 5
    # Since previous Close is within current High/Low range, TR is exactly 10.0 for every bar.
    highs = np.full(30, 105.0)
    lows = np.full(30, 95.0)
    closes = np.full(30, 100.0)
    
    atr = compute_wilder_atr(highs, lows, closes, period=14)
    assert len(atr) == 30
    assert atr[13] == 10.0 # First 14 bars SMA is 10.0
    
    # Every subsequent Wilder smoothed value must remain exactly 10.0
    for i in range(13, 30):
        assert abs(atr[i] - 10.0) < 1e-6


def test_chandelier_stop_monotonic_ratchet():
    """Verify Chandelier stop floor NEVER decreases (ratchets strictly upward)."""
    bars = create_synthetic_bars(40, 1000.0)
    # Add a sudden dip in the last 5 bars
    for i in range(35, 40):
        bars[i] = OHLCVBar(
            time=bars[i].time,
            open=1200.0,
            high=1220.0, # High is lower than peak at bar 34 (1348.0)
            low=1100.0,
            close=1150.0,
            volume=50000.0,
        )
        
    stops, atrs, highest_highs = compute_chandelier_stop_series(bars, multiplier=2.2, lookback_hh=22)
    
    assert len(stops) == 40
    # From index 21 to 39, every stop must be >= previous stop
    for i in range(22, 40):
        assert stops[i] >= stops[i - 1], f"Chandelier stop decreased at index {i}: {stops[i]} < {stops[i-1]}"


def test_rsi_series_bounds():
    """Verify RSI calculation stays strictly in [0, 100]."""
    bars = create_synthetic_bars(50, 100.0)
    closes = np.array([b.close for b in bars])
    rsi = compute_rsi_series(closes, period=14)
    
    assert len(rsi) == 50
    valid_rsi = rsi[14:]
    assert np.all(valid_rsi >= 0.0)
    assert np.all(valid_rsi <= 100.0)
    # Consistent uptrend should yield RSI > 70
    assert valid_rsi[-1] > 70.0


def test_insufficient_bars_error():
    """Verify exception raised when bar count is less than lookback."""
    bars = create_synthetic_bars(10, 100.0)
    with pytest.raises(ValueError):
        compute_chandelier_stop_series(bars, multiplier=2.0, lookback_hh=22)
