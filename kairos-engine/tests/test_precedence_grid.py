"""Unit tests for the 2D Precedence Grid Matrix."""
from app.schemas.enums import HorizonMode, MarketCapBucket
from app.engine.precedence_grid import resolve_precedence_grid


def test_compounder_large_cap_weights():
    """Verify Compounder + Large Cap yields 45% Fund and 2.2x ATR multiplier."""
    weights = resolve_precedence_grid(HorizonMode.COMPOUNDER, MarketCapBucket.LARGE_CAP)
    assert weights.w_fund == 0.45
    assert weights.w_tech == 0.15
    assert weights.w_quant == 0.25
    assert weights.w_news == 0.15
    assert weights.net_multiplier == 2.20
    assert round(weights.w_fund + weights.w_tech + weights.w_quant + weights.w_news, 4) == 1.0


def test_swing_small_cap_weights():
    """Verify Swing + Small Cap yields 50% Tech and 2.3x ATR multiplier."""
    weights = resolve_precedence_grid(HorizonMode.SWING, MarketCapBucket.SMALL_CAP)
    assert weights.w_fund == 0.10
    assert weights.w_tech == 0.50
    assert weights.w_quant == 0.30
    assert weights.w_news == 0.10
    assert weights.net_multiplier == 2.30
    assert round(weights.w_fund + weights.w_tech + weights.w_quant + weights.w_news, 4) == 1.0


def test_all_six_permutations_sum_to_one():
    """Verify all 6 permutations in the 2D matrix sum exactly to 1.0."""
    for horizon in HorizonMode:
        for mcap in MarketCapBucket:
            weights = resolve_precedence_grid(horizon, mcap)
            total = weights.w_fund + weights.w_tech + weights.w_quant + weights.w_news
            assert round(total, 4) == 1.0
            assert weights.net_multiplier > 0.0


def test_manual_multiplier_override():
    """Verify manual override replaces calculated net multiplier."""
    weights = resolve_precedence_grid(
        HorizonMode.COMPOUNDER, MarketCapBucket.LARGE_CAP, manual_multiplier_override=3.5
    )
    assert weights.net_multiplier == 3.50
    assert weights.base_multiplier == 2.50
