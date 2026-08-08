"""Unit tests for SciPy RSI peak divergence detection."""
import numpy as np
from app.engine.indicators import detect_bearish_rsi_divergence


def test_bearish_rsi_divergence_detected():
    """Verify divergence is detected when price makes Higher High and RSI makes Lower High."""
    # Synthetic 40-bar series with two distinct peaks
    closes = np.array([
        100, 102, 105, 110, 115, 120, 125, 120, 115, 110, # Peak 1 at index 6 (price=125)
        108, 110, 115, 120, 128, 132, 135, 130, 128, 125, # Peak 2 at index 16 (price=135)
        122, 120, 118, 116, 115, 114, 113, 112, 111, 110,
        110, 112, 115, 120, 125, 130, 132, 134, 136, 138,
    ], dtype=np.float64)
    
    # Matching RSI where Peak 2 (index 16) is LOWER than Peak 1 (index 6)
    rsi = np.array([
        50, 55, 60, 68, 74, 79, 82, 75, 68, 60, # Peak 1 RSI = 82
        58, 62, 65, 68, 70, 72, 74, 69, 65, 63, # Peak 2 RSI = 74 (< 82)
        60, 58, 55, 52, 50, 48, 46, 45, 44, 43,
        45, 50, 55, 60, 64, 66, 68, 69, 70, 71, # Latest RSI = 71 (>= 60)
    ], dtype=np.float64)
    
    is_div = detect_bearish_rsi_divergence(closes, rsi, lookback=40)
    assert is_div is True


def test_bearish_rsi_divergence_not_detected_when_aligned():
    """Verify no divergence when price and RSI are both making Higher Highs."""
    closes = np.array([
        100, 105, 110, 115, 120, 125, 120, 115, 110, 105, # Peak 1 at 125
        110, 115, 120, 125, 130, 135, 130, 125, 120, 115, # Peak 2 at 135
        110, 112, 114, 116, 118, 120, 122, 124, 126, 128,
        125, 125, 125, 125, 125, 125, 125, 125, 125, 125,
    ], dtype=np.float64)
    
    rsi = np.array([
        50, 55, 60, 65, 70, 72, 68, 62, 55, 50, # Peak 1 RSI = 72
        55, 60, 65, 70, 75, 80, 74, 68, 62, 55, # Peak 2 RSI = 80 (> 72, Bullish alignment)
        52, 54, 56, 58, 60, 62, 64, 66, 68, 70,
        65, 65, 65, 65, 65, 65, 65, 65, 65, 65,
    ], dtype=np.float64)
    
    is_div = detect_bearish_rsi_divergence(closes, rsi, lookback=40)
    assert is_div is False
