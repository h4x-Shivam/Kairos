"""Pure NumPy and SciPy technical and volatility indicator algorithms."""
from typing import List, Tuple
import numpy as np
from scipy.signal import find_peaks
from app.schemas.diagnostic import OHLCVBar


def compute_true_range(highs: np.ndarray, lows: np.ndarray, closes: np.ndarray) -> np.ndarray:
    """Compute True Range (TR) array for a given OHLC series."""
    n = len(highs)
    if n == 0:
        return np.array([], dtype=np.float64)
    
    tr = np.zeros(n, dtype=np.float64)
    tr[0] = highs[0] - lows[0]
    
    for i in range(1, n):
        hl = highs[i] - lows[i]
        hc = abs(highs[i] - closes[i - 1])
        lc = abs(lows[i] - closes[i - 1])
        tr[i] = max(hl, hc, lc)
        
    return tr


def compute_wilder_atr(
    highs: np.ndarray, lows: np.ndarray, closes: np.ndarray, period: int = 14
) -> np.ndarray:
    """Compute Wilder's Exponentially Smoothed Average True Range (ATR).
    
    Formula:
        ATR[t] = (ATR[t-1] * 13 + TR[t]) / 14
    """
    n = len(highs)
    if n < period:
        raise ValueError(f"Insufficient bars ({n}) for ATR period ({period})")
        
    tr = compute_true_range(highs, lows, closes)
    atr = np.zeros(n, dtype=np.float64)
    
    # Initial SMA for the first 'period' elements
    atr[period - 1] = np.mean(tr[:period])
    
    # Wilder exponential smoothing
    for i in range(period, n):
        atr[i] = (atr[i - 1] * (period - 1) + tr[i]) / period
        
    return atr


def compute_chandelier_stop_series(
    bars: List[OHLCVBar], multiplier: float, lookback_hh: int = 22, atr_period: int = 14
) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Compute the ratcheting Chandelier trailing stop floor series.
    
    Returns:
        (chandelier_stops, atr_series, highest_high_series)
    """
    n = len(bars)
    if n < max(lookback_hh, atr_period):
        raise ValueError(f"Need at least {max(lookback_hh, atr_period)} bars to compute Chandelier Stop")
        
    highs = np.array([b.high for b in bars], dtype=np.float64)
    lows = np.array([b.low for b in bars], dtype=np.float64)
    closes = np.array([b.close for b in bars], dtype=np.float64)
    
    atr = compute_wilder_atr(highs, lows, closes, period=atr_period)
    highest_highs = np.zeros(n, dtype=np.float64)
    raw_stops = np.zeros(n, dtype=np.float64)
    ratcheted_stops = np.zeros(n, dtype=np.float64)
    
    start_idx = max(lookback_hh, atr_period) - 1
    
    for i in range(start_idx, n):
        window_highs = highs[i - lookback_hh + 1 : i + 1]
        hh = np.max(window_highs)
        highest_highs[i] = hh
        raw_stop = hh - (multiplier * atr[i])
        raw_stops[i] = raw_stop
        
        if i == start_idx:
            ratcheted_stops[i] = raw_stop
        else:
            # Monotonic ratchet: Trailing stop only moves up, never down.
            # However, if the previous bar closed below the previous stop (a breach),
            # a real user would have exited. Thus, we reset the ratchet to prevent 
            # locking in stale high-water marks over long stateless periods.
            if closes[i - 1] < ratcheted_stops[i - 1]:
                ratcheted_stops[i] = raw_stop
            else:
                ratcheted_stops[i] = max(ratcheted_stops[i - 1], raw_stop)
            
    return ratcheted_stops, atr, highest_highs


def compute_rsi_series(closes: np.ndarray, period: int = 14) -> np.ndarray:
    """Compute Wilder's 14-period Relative Strength Index (RSI)."""
    n = len(closes)
    if n <= period:
        raise ValueError(f"Insufficient bars ({n}) for RSI period ({period})")
        
    deltas = np.diff(closes)
    gains = np.where(deltas > 0, deltas, 0.0)
    losses = np.where(deltas < 0, -deltas, 0.0)
    
    rsi = np.zeros(n, dtype=np.float64)
    
    avg_gain = np.mean(gains[:period])
    avg_loss = np.mean(losses[:period])
    
    if avg_loss == 0:
        rsi[period] = 100.0
    else:
        rs = avg_gain / avg_loss
        rsi[period] = 100.0 - (100.0 / (1.0 + rs))
        
    for i in range(period + 1, n):
        gain = gains[i - 1]
        loss = losses[i - 1]
        
        avg_gain = (avg_gain * (period - 1) + gain) / period
        avg_loss = (avg_loss * (period - 1) + loss) / period
        
        if avg_loss == 0:
            rsi[i] = 100.0
        else:
            rs = avg_gain / avg_loss
            rsi[i] = 100.0 - (100.0 / (1.0 + rs))
            
    return rsi


def detect_bearish_rsi_divergence(
    closes: np.ndarray, rsi: np.ndarray, lookback: int = 30
) -> bool:
    """Detect Bearish RSI Peak Divergence over the lookback window.
    
    Criteria:
        - Price forms Higher High (Peak 2 > Peak 1)
        - RSI forms Lower High (RSI Peak 2 < RSI Peak 1)
        - Both peaks occur within the lookback window
        - Latest RSI >= 60.0 (Overbought / Distribution zone)
    """
    n = len(closes)
    if n < lookback:
        return False
        
    sub_closes = closes[-lookback:]
    sub_rsi = rsi[-lookback:]
    
    price_peaks, _ = find_peaks(sub_closes, distance=5)
    if len(price_peaks) < 2:
        return False
        
    # Analyze the last two prominent price peaks
    p1_idx, p2_idx = price_peaks[-2], price_peaks[-1]
    
    price_p1 = sub_closes[p1_idx]
    price_p2 = sub_closes[p2_idx]
    
    rsi_p1 = sub_rsi[p1_idx]
    rsi_p2 = sub_rsi[p2_idx]
    
    # Check Higher High in Price, Lower High in RSI, and current RSI elevated
    is_price_higher = price_p2 > (price_p1 * 1.005) # at least 0.5% higher
    is_rsi_lower = rsi_p2 < (rsi_p1 - 2.0)           # at least 2 RSI points lower
    is_current_overbought = sub_rsi[-1] >= 60.0
    
    return bool(is_price_higher and is_rsi_lower and is_current_overbought)
