"""Unit tests for Quarter-Kelly Sizing and Indian Capital Gains Tax Simulator."""
from app.engine.risk_sizing import compute_risk_reward_and_kelly
from app.engine.tax_simulator import simulate_trim_execution


def test_quarter_kelly_calculation():
    """Verify Quarter-Kelly caps at 25% and handles favorable R:R."""
    # Current: 1000, Stop: 900 (Risk: 100), Target: 1300 (Reward: 300) -> R:R = 3.0
    # Kelly = (0.55 * 3 - 0.45) / 3 = (1.65 - 0.45) / 3 = 1.20 / 3 = 0.40 (40%)
    # Quarter Kelly = 0.25 * 40% = 10.0%
    telemetry = compute_risk_reward_and_kelly(
        current_price=1000.0,
        chandelier_stop=900.0,
        consensus_target_price=1300.0,
        atr=40.0,
        win_rate=0.55,
    )
    assert telemetry.reward_delta == 300.0
    assert telemetry.risk_delta == 100.0
    assert telemetry.risk_reward_ratio == 3.0
    assert telemetry.quarter_kelly_pct == 10.0


def test_quarter_kelly_negative_expectation():
    """Verify Quarter-Kelly returns 0% when R:R is unfavorable."""
    telemetry = compute_risk_reward_and_kelly(
        current_price=1000.0,
        chandelier_stop=700.0, # Risk = 300
        atr=40.0,
        consensus_target_price=1050.0, # Reward = 50 -> R:R = 0.17
    )
    assert telemetry.quarter_kelly_pct == 0.0


def test_indian_tax_stcg_trim_25():
    """Verify STCG (holding <= 12m) charges flat 20% on realized capital gain."""
    # 100 shares bought at 500 (Cost = 50k), current price = 1000 (Val = 100k)
    # Trim 25% -> Sell 25 shares.
    # Gross proceeds = 25 * 1000 = 25,000.
    # Cost basis = 25 * 500 = 12,500.
    # Gain = 12,500. STCG Tax (20%) = 2,500.
    # Net cash = 22,500.
    # Retained 75 shares. Remaining capital = 50,000 - 22,500 = 27,500.
    # New breakeven = 27,500 / 75 = ₹366.67.
    result = simulate_trim_execution(
        shares_held=100,
        buy_price=500.0,
        current_price=1000.0,
        trim_percentage=25.0,
        holding_period_months=6, # STCG
    )
    assert result["shares_to_sell"] == 25
    assert result["shares_retained"] == 75
    assert result["gross_proceeds"] == 25000.0
    assert result["capital_gain"] == 12500.0
    assert result["tax_type"] == "STCG"
    assert result["tax_rate_pct"] == 20.0
    assert result["tax_liability"] == 2500.0
    assert result["net_cash_realized"] == 22500.0
    assert result["new_breakeven_price"] == 366.67
    assert result["new_downside_cushion_pct"] == 63.33


def test_indian_tax_ltcg_with_exemption():
    """Verify LTCG (>12m) applies 12.5% only to gains exceeding ₹1.25L."""
    # 1000 shares bought at 500, current price = 1000.
    # Trim 50% -> Sell 500 shares.
    # Gross proceeds = 500 * 1000 = 5,00,000. Cost = 500 * 500 = 2,50,000.
    # Gain = 2,50,000.
    # Taxable gain = 2,50,000 - 1,25,000 = 1,25,000.
    # LTCG Tax (12.5%) = 1,25,000 * 0.125 = 15,625.
    result = simulate_trim_execution(
        shares_held=1000,
        buy_price=500.0,
        current_price=1000.0,
        trim_percentage=50.0,
        holding_period_months=18, # LTCG
    )
    assert result["shares_to_sell"] == 500
    assert result["tax_type"] == "LTCG"
    assert result["tax_rate_pct"] == 12.5
    assert result["tax_liability"] == 15625.0
    assert result["net_cash_realized"] == 484375.0

def test_indian_tax_stcg_boundary_12_months():
    """Verify holding exactly 12 months is treated as STCG under Indian tax law."""
    result = simulate_trim_execution(
        shares_held=100,
        buy_price=500.0,
        current_price=1000.0,
        trim_percentage=25.0,
        holding_period_months=12, # Exactly 12 -> STCG
    )
    assert result["tax_type"] == "STCG"
    assert result["tax_rate_pct"] == 20.0
