"""Fractional Quarter-Kelly allocation and risk-reward calculation module."""
from typing import Optional
from app.schemas.diagnostic import RiskRewardTelemetry


def compute_risk_reward_and_kelly(
    current_price: float,
    chandelier_stop: float,
    atr: float,
    consensus_target_price: Optional[float] = None,
    win_rate: float = 0.55,
) -> RiskRewardTelemetry:
    """Compute Risk-Reward Ratio and Quarter-Kelly recommended portfolio allocation.
    
    Formulas:
        R = (Target - Current) / max(0.50, Current - Stop)
        f* = (W * R - (1 - W)) / R
        f_quarter = max(0, 0.25 * f*) * 100%
    """
    # 1. Resolve Target Price
    if consensus_target_price is not None and consensus_target_price > current_price:
        target_price = float(consensus_target_price)
    else:
        # Default baseline: 15% upside target
        target_price = round(current_price * 1.15, 2)
        
    reward_delta = max(0.0, target_price - current_price)
    # 1. Floor risk denominator using max(0.50, price - stop, 0.5 * atr)
    risk_delta = max(0.50, current_price - chandelier_stop, 0.5 * atr)
    
    # 2. Risk-Reward Ratio with Target Anomaly Guard
    if risk_delta <= 0.0:
        rr_ratio = 50.0
    else:
        raw_rr = reward_delta / risk_delta
        rr_ratio = max(0.0, min(50.0, raw_rr))
        
    # 3. Fractional Quarter-Kelly Allocation
    if rr_ratio <= 0.0:
        quarter_kelly = 0.0
    else:
        kelly_fraction = (win_rate * rr_ratio - (1.0 - win_rate)) / rr_ratio
        if kelly_fraction <= 0.0:
            quarter_kelly = 0.0
        else:
            # Quarter-Kelly clamped at 25% max portfolio cap
            quarter_kelly = min(25.0, 0.25 * kelly_fraction * 100.0)
            
    return RiskRewardTelemetry(
        target_price=round(target_price, 2),
        reward_delta=round(reward_delta, 2),
        risk_delta=round(risk_delta, 2),
        risk_reward_ratio=round(rr_ratio, 2),
        quarter_kelly_pct=round(quarter_kelly, 1),
    )
