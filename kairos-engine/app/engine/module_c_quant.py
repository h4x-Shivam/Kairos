"""Pillar C: Volatility, drawdown, and market risk scoring module ($S_{quant}$)."""
from app.schemas.diagnostic import QuantMetricsInput


def score_52w_drawdown(current_price: float, high_52w: float) -> float:
    """Score drawdown from 52-week peak."""
    if high_52w <= 0:
        return 50.0
    dd_pct = ((current_price - high_52w) / high_52w) * 100.0
    if dd_pct >= -5.0:
        return 100.0
    if dd_pct >= -10.0:
        return 85.0
    if dd_pct >= -18.0:
        return 65.0
    if dd_pct >= -28.0:
        return 40.0
    return 15.0


def score_realized_volatility(vol_1y: float) -> float:
    """Score 1-year annualized realized volatility."""
    if vol_1y <= 18.0:
        return 100.0
    if vol_1y <= 28.0:
        return 80.0
    if vol_1y <= 40.0:
        return 55.0
    if vol_1y <= 55.0:
        return 30.0
    return 10.0


def score_beta(beta: float) -> float:
    """Score 1-year market beta."""
    if 0.60 <= beta <= 1.10:
        return 100.0
    if 1.10 < beta <= 1.40:
        return 75.0
    if 0.30 <= beta < 0.60:
        return 70.0
    if 1.40 < beta <= 1.80:
        return 40.0
    return 20.0


def compute_quant_score(current_price: float, quant: QuantMetricsInput) -> float:
    r"""Compute normalized composite Volatility & Risk Score ($S_{quant} \in [0, 100]$)."""
    s_dd = score_52w_drawdown(current_price, quant.high_52w)
    s_vol = score_realized_volatility(quant.realized_volatility_1y)
    s_beta = score_beta(quant.beta)
    
    score = 0.50 * s_dd + 0.30 * s_vol + 0.20 * s_beta
    return round(float(score), 1)
