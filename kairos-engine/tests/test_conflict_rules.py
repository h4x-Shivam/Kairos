"""Unit tests for the 6 Named Asymmetric Conflict Rules & State Machine."""
from app.schemas.enums import HorizonMode, PrimaryAction, OverrideRule
from app.engine.conflict_resolution import resolve_verdict


def test_rule_6_tier1_governance_bypass():
    """Verify active Tier-1 trigger forces EXIT_FULLY regardless of scores."""
    action, rule, expl, composite = resolve_verdict(
        horizon_mode=HorizonMode.COMPOUNDER,
        current_price=1000.0,
        chandelier_stop=800.0,
        s_fund=95.0, # High fundamentals
        s_tech=90.0, # High technicals
        s_quant=90.0,
        s_composite=92.5,
        is_tier1_active=True, # Auditor resignation / SEBI probe
        has_bearish_divergence=False,
        risk_reward_ratio=5.0,
    )
    assert action == PrimaryAction.EXIT_FULLY
    assert rule == OverrideRule.TIER_1_HARD_GOVERNANCE_BYPASS
    assert composite == 0.0


def test_rule_2a_stop_breach_compounder():
    """Verify stop breach on high-conviction compounder triggers TRIM_50%."""
    action, rule, expl, _ = resolve_verdict(
        horizon_mode=HorizonMode.COMPOUNDER,
        current_price=790.0,
        chandelier_stop=800.0, # Price is below stop
        s_fund=85.0,           # S_fund >= 70
        s_tech=50.0,
        s_quant=60.0,
        s_composite=68.0,
        is_tier1_active=False,
        has_bearish_divergence=False,
        risk_reward_ratio=2.0,
    )
    assert action == PrimaryAction.TRIM_50
    assert rule == OverrideRule.RULE_2A_STOP_BREACH_COMPOUNDER


def test_rule_2b_stop_breach_swing():
    """Verify stop breach on swing trade triggers immediate EXIT_FULLY."""
    action, rule, expl, _ = resolve_verdict(
        horizon_mode=HorizonMode.SWING,
        current_price=790.0,
        chandelier_stop=800.0,
        s_fund=85.0,
        s_tech=50.0,
        s_quant=60.0,
        s_composite=68.0,
        is_tier1_active=False,
        has_bearish_divergence=False,
        risk_reward_ratio=2.0,
    )
    assert action == PrimaryAction.EXIT_FULLY
    assert rule == OverrideRule.RULE_2B_STOP_BREACH_SWING


def test_rule_4_double_structural_breakdown():
    """Verify S_fund < 45 and S_tech < 45 triggers EXIT_FULLY even above stop."""
    action, rule, expl, _ = resolve_verdict(
        horizon_mode=HorizonMode.COMPOUNDER,
        current_price=1000.0,
        chandelier_stop=800.0,
        s_fund=35.0, # Bad fundamentals
        s_tech=40.0, # Bad technicals
        s_quant=60.0,
        s_composite=42.0,
        is_tier1_active=False,
        has_bearish_divergence=False,
        risk_reward_ratio=2.0,
    )
    assert action == PrimaryAction.EXIT_FULLY
    assert rule == OverrideRule.RULE_4_DOUBLE_STRUCTURAL_BREAKDOWN


def test_rule_3_sell_into_technical_strength():
    """Verify S_fund < 45 with S_tech >= 70 triggers TRIM_50%."""
    action, rule, expl, _ = resolve_verdict(
        horizon_mode=HorizonMode.COMPOUNDER,
        current_price=1000.0,
        chandelier_stop=800.0,
        s_fund=38.0, # Bad fundamentals
        s_tech=75.0, # Strong speculative rally
        s_quant=65.0,
        s_composite=55.0,
        is_tier1_active=False,
        has_bearish_divergence=False,
        risk_reward_ratio=2.0,
    )
    assert action == PrimaryAction.TRIM_50
    assert rule == OverrideRule.RULE_3_SELL_INTO_STRENGTH


def test_rule_1_compounder_volatility_buffer():
    """Verify S_fund >= 70 with S_tech < 45 on Compounder triggers TRIM_25%."""
    action, rule, expl, _ = resolve_verdict(
        horizon_mode=HorizonMode.COMPOUNDER,
        current_price=1000.0,
        chandelier_stop=800.0,
        s_fund=88.0, # Strong business
        s_tech=42.0, # Temporary dip
        s_quant=70.0,
        s_composite=68.0,
        is_tier1_active=False,
        has_bearish_divergence=False,
        risk_reward_ratio=2.0,
    )
    assert action == PrimaryAction.TRIM_25
    assert rule == OverrideRule.RULE_1_COMPOUNDER_VOLATILITY_BUFFER


def test_rule_5_momentum_exhaustion_divergence():
    """Verify Rule 5 fires when bearish divergence detected, R:R < 1.0, and S_composite < 65."""
    action, rule, expl, _ = resolve_verdict(
        horizon_mode=HorizonMode.SWING,
        current_price=1000.0,
        chandelier_stop=800.0,
        s_fund=55.0,
        s_tech=60.0,
        s_quant=60.0,
        s_composite=62.0,
        is_tier1_active=False,
        has_bearish_divergence=True,
        risk_reward_ratio=0.8,
    )
    assert action == PrimaryAction.TRIM_25
    assert rule == OverrideRule.RULE_5_MOMENTUM_EXHAUSTION_DIVERGENCE


def test_layer_1_continuous_tighten_stop():
    """Verify S_composite between 60 and 74 yields TIGHTEN_STOP."""
    action, rule, expl, _ = resolve_verdict(
        horizon_mode=HorizonMode.COMPOUNDER,
        current_price=1000.0,
        chandelier_stop=800.0,
        s_fund=68.0,
        s_tech=65.0,
        s_quant=65.0,
        s_composite=66.0,
        is_tier1_active=False,
        has_bearish_divergence=False,
        risk_reward_ratio=2.0,
    )
    assert action == PrimaryAction.TIGHTEN_STOP
    assert rule == OverrideRule.NONE


def test_layer_1_continuous_trim_25():
    """Verify S_composite between 45 and 59 yields TRIM_25."""
    action, rule, expl, _ = resolve_verdict(
        horizon_mode=HorizonMode.SWING,
        current_price=1000.0,
        chandelier_stop=800.0,
        s_fund=50.0,
        s_tech=52.0,
        s_quant=55.0,
        s_composite=52.0,
        is_tier1_active=False,
        has_bearish_divergence=False,
        risk_reward_ratio=2.0,
    )
    assert action == PrimaryAction.TRIM_25
    assert rule == OverrideRule.NONE


def test_layer_1_continuous_trim_50():
    """Verify S_composite between 30 and 44 yields TRIM_50."""
    action, rule, expl, _ = resolve_verdict(
        horizon_mode=HorizonMode.SWING,
        current_price=1000.0,
        chandelier_stop=800.0,
        s_fund=46.0, # Not below 45 to avoid double breakdown
        s_tech=46.0,
        s_quant=35.0,
        s_composite=38.0,
        is_tier1_active=False,
        has_bearish_divergence=False,
        risk_reward_ratio=2.0,
    )
    assert action == PrimaryAction.TRIM_50
    assert rule == OverrideRule.NONE


def test_layer_1_continuous_exit_fully():
    """Verify S_composite < 30 yields EXIT_FULLY."""
    action, rule, expl, _ = resolve_verdict(
        horizon_mode=HorizonMode.SWING,
        current_price=1000.0,
        chandelier_stop=800.0,
        s_fund=46.0,
        s_tech=46.0,
        s_quant=20.0,
        s_composite=25.0,
        is_tier1_active=False,
        has_bearish_divergence=False,
        risk_reward_ratio=2.0,
    )
    assert action == PrimaryAction.EXIT_FULLY
    assert rule == OverrideRule.NONE
