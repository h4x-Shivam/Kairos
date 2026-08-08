"""2D Precedence Grid matrix resolver for dynamic weights and ATR multipliers."""
from typing import Dict, Tuple, Optional
from app.schemas.enums import HorizonMode, MarketCapBucket
from app.schemas.diagnostic import PrecedenceWeights

# Matrix configuration: (w_fund, w_tech, w_quant, w_news, base_k, cap_delta)
_GRID_CONFIG: Dict[Tuple[HorizonMode, MarketCapBucket], Tuple[float, float, float, float, float, float]] = {
    # COMPOUNDER Permutations
    (HorizonMode.COMPOUNDER, MarketCapBucket.LARGE_CAP): (0.45, 0.15, 0.25, 0.15, 2.5, -0.3),
    (HorizonMode.COMPOUNDER, MarketCapBucket.MID_CAP):   (0.35, 0.25, 0.25, 0.15, 2.5,  0.0),
    (HorizonMode.COMPOUNDER, MarketCapBucket.SMALL_CAP): (0.25, 0.35, 0.25, 0.15, 2.5,  0.5),
    
    # SWING Permutations
    (HorizonMode.SWING, MarketCapBucket.LARGE_CAP):      (0.20, 0.40, 0.30, 0.10, 1.8, -0.3),
    (HorizonMode.SWING, MarketCapBucket.MID_CAP):        (0.15, 0.45, 0.30, 0.10, 1.8,  0.0),
    (HorizonMode.SWING, MarketCapBucket.SMALL_CAP):      (0.10, 0.50, 0.30, 0.10, 1.8,  0.5),
}


def resolve_precedence_grid(
    horizon: HorizonMode,
    market_cap: MarketCapBucket,
    manual_multiplier_override: Optional[float] = None,
) -> PrecedenceWeights:
    """Resolve the 2D Precedence Grid weights and net ATR multiplier.
    
    Args:
        horizon: COMPOUNDER or SWING
        market_cap: LARGE_CAP, MID_CAP, or SMALL_CAP
        manual_multiplier_override: Optional user manual override for multiplier
        
    Returns:
        PrecedenceWeights schema object
    """
    key = (horizon, market_cap)
    if key not in _GRID_CONFIG:
        raise ValueError(f"Unmapped 2D grid permutation: {key}")
        
    w_fund, w_tech, w_quant, w_news, base_k, cap_delta = _GRID_CONFIG[key]
    
    if manual_multiplier_override is not None and manual_multiplier_override > 0:
        net_m = float(manual_multiplier_override)
    else:
        net_m = round(base_k + cap_delta, 2)
        
    # Verify weights sum to 1.0
    total_w = round(w_fund + w_tech + w_quant + w_news, 4)
    if total_w != 1.0:
        raise ValueError(f"Precedence weights for {key} do not sum to 1.0 (sum={total_w})")
        
    return PrecedenceWeights(
        w_fund=w_fund,
        w_tech=w_tech,
        w_quant=w_quant,
        w_news=w_news,
        base_multiplier=base_k,
        net_multiplier=net_m,
    )
