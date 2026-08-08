"""Asymmetric Conflict Resolution State Machine & 6 Override Rules."""
from typing import Tuple
from app.schemas.enums import HorizonMode, PrimaryAction, OverrideRule


def resolve_verdict(
    horizon_mode: HorizonMode,
    current_price: float,
    chandelier_stop: float,
    s_fund: float,
    s_tech: float,
    s_quant: float,
    s_composite: float,
    is_tier1_active: bool,
    has_bearish_divergence: bool,
    risk_reward_ratio: float,
) -> Tuple[PrimaryAction, OverrideRule, str, float]:
    """Evaluate deterministic 6-rule precedence hierarchy.
    
    Returns:
        (action, rule_applied, explanation, adjusted_composite_score)
    """
    # 1. Rule 6: Tier-1 Hard Governance Emergency Bypass
    if is_tier1_active:
        return (
            PrimaryAction.EXIT_FULLY,
            OverrideRule.TIER_1_HARD_GOVERNANCE_BYPASS,
            "EMERGENCY BYPASS: Severe governance red flag (Auditor Resignation / SEBI Probe / Default) triggered. Immediate capital preservation override.",
            0.0,
        )
        
    # 2. Rule 2: Stop Loss Breach Evaluation
    if current_price <= chandelier_stop:
        if horizon_mode == HorizonMode.COMPOUNDER and s_fund >= 70.0:
            return (
                PrimaryAction.TRIM_50,
                OverrideRule.RULE_2A_STOP_BREACH_COMPOUNDER,
                "Trailing stop breached on high-conviction compounder (S_fund >= 70). Trim 50% to lock gains while giving core holding a 1.0x ATR reset buffer.",
                s_composite,
            )
        else:
            return (
                PrimaryAction.EXIT_FULLY,
                OverrideRule.RULE_2B_STOP_BREACH_SWING,
                "Trailing stop breached. Downside protection rule commands full exit to preserve capital.",
                s_composite,
            )
            
    # 3. Rule 4: Double Structural Breakdown
    if s_fund < 45.0 and s_tech < 45.0:
        return (
            PrimaryAction.EXIT_FULLY,
            OverrideRule.RULE_4_DOUBLE_STRUCTURAL_BREAKDOWN,
            "Double structural breakdown detected (Fundamental < 45 & Technical < 45). Severe multi-pillar deterioration commands full exit.",
            s_composite,
        )
        
    # 4. Rule 3: Sell Into Technical Strength
    if s_fund < 45.0 and s_tech >= 70.0 and s_quant >= 60.0:
        return (
            PrimaryAction.TRIM_50,
            OverrideRule.RULE_3_SELL_INTO_STRENGTH,
            "Fundamental deterioration with temporary technical strength. Harvest speculative liquidity: Trim 50% into strength.",
            s_composite,
        )
        
    # 5. Rule 1: Compounder Volatility Buffer
    if (
        horizon_mode == HorizonMode.COMPOUNDER
        and s_fund >= 70.0
        and s_tech < 45.0
        and current_price > chandelier_stop
    ):
        return (
            PrimaryAction.TRIM_25,
            OverrideRule.RULE_1_COMPOUNDER_VOLATILITY_BUFFER,
            "Strong fundamental compounding thesis intact (S_fund >= 70), but short-term technicals weak. Trim 25% to lock partial profit; hold core position.",
            s_composite,
        )
        
    # 6. Rule 5: Momentum Exhaustion / Bearish RSI Peak Divergence
    if has_bearish_divergence and risk_reward_ratio < 1.0 and s_composite < 65.0:
        return (
            PrimaryAction.TRIM_25,
            OverrideRule.RULE_5_MOMENTUM_EXHAUSTION_DIVERGENCE,
            "Bearish RSI peak divergence detected with unfavorable Risk-Reward (< 1.0). Trim 25% into momentum exhaustion.",
            s_composite,
        )
        
    # 7. Layer 1: Continuous Baseline Scoring (No Overrides Fired)
    if s_composite >= 75.0:
        return (
            PrimaryAction.HOLD,
            OverrideRule.NONE,
            "Multi-pillar quantitative metrics are robust. Thesis is compounding as planned: HOLD position.",
            s_composite,
        )
    elif s_composite >= 60.0:
        return (
            PrimaryAction.TIGHTEN_STOP,
            OverrideRule.NONE,
            "Minor momentum or valuation deceleration detected. Maintain position but tighten trailing stop floor.",
            s_composite,
        )
    elif s_composite >= 45.0:
        return (
            PrimaryAction.TRIM_25,
            OverrideRule.NONE,
            "Moderate composite score degradation (45-60). Protect profits: Trim 25% of holding.",
            s_composite,
        )
    elif s_composite >= 30.0:
        return (
            PrimaryAction.TRIM_50,
            OverrideRule.NONE,
            "Significant composite score deterioration (30-45). High downside risk: Trim 50% of holding.",
            s_composite,
        )
    else:
        return (
            PrimaryAction.EXIT_FULLY,
            OverrideRule.NONE,
            "Severe composite score breakdown (< 30). Algorithmic downside protection commands complete exit.",
            s_composite,
        )
