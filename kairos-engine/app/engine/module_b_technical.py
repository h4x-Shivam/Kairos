"""Pillar B: Technical trend and momentum scoring module ($S_{tech}$)."""
from app.schemas.diagnostic import TechnicalMetricsInput


def score_dma_alignment(price: float, sma_50: float, sma_200: float) -> float:
    """Score moving average trend structure."""
    if price >= sma_50 and sma_50 >= sma_200:
        return 100.0
    if price >= sma_200 and price < sma_50:
        return 75.0
    if price < sma_200 and price >= sma_50:
        return 45.0
    return 15.0


def score_rsi(rsi_14: float) -> float:
    """Score RSI momentum band."""
    if 50.0 <= rsi_14 <= 65.0:
        return 100.0
    if 40.0 <= rsi_14 < 50.0:
        return 75.0
    if 65.0 < rsi_14 <= 75.0:
        return 65.0
    if 30.0 <= rsi_14 < 40.0:
        return 40.0
    if rsi_14 > 75.0:
        return 30.0
    return 15.0


def score_delivery(delivery_pct: float) -> float:
    """Score NSE security delivery percentage."""
    if delivery_pct >= 50.0:
        return 100.0
    if delivery_pct >= 40.0:
        return 80.0
    if delivery_pct >= 30.0:
        return 60.0
    if delivery_pct >= 20.0:
        return 40.0
    return 20.0


def compute_technical_score(current_price: float, tech: TechnicalMetricsInput) -> float:
    r"""Compute normalized composite Technical Score ($S_{tech} \in [0, 100]$)."""
    s_dma = score_dma_alignment(current_price, tech.sma_50, tech.sma_200)
    s_rsi = score_rsi(tech.rsi_14)
    s_del = score_delivery(tech.delivery_pct)
    
    score = 0.40 * s_dma + 0.35 * s_rsi + 0.25 * s_del
    return round(float(score), 1)
