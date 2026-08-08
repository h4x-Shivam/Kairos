"""Domain Enums for Kairos Quant Engine."""
from enum import Enum


class HorizonMode(str, Enum):
    """Investor holding horizon profile."""
    COMPOUNDER = "COMPOUNDER"
    SWING = "SWING"


class MarketCapBucket(str, Enum):
    """Market capitalization tier for Indian equities."""
    LARGE_CAP = "LARGE_CAP"
    MID_CAP = "MID_CAP"
    SMALL_CAP = "SMALL_CAP"


class PrimaryAction(str, Enum):
    """Deterministic exit diagnostic actions."""
    HOLD = "HOLD"
    TIGHTEN_STOP = "TIGHTEN_STOP"
    TRIM_25 = "TRIM_25"
    TRIM_50 = "TRIM_50"
    EXIT_FULLY = "EXIT_FULLY"


class OverrideRule(str, Enum):
    """Named asymmetric conflict resolution and override rules."""
    NONE = "NONE"
    TIER_1_HARD_GOVERNANCE_BYPASS = "TIER_1_HARD_GOVERNANCE_BYPASS"
    RULE_2A_STOP_BREACH_COMPOUNDER = "RULE_2A_STOP_BREACH_COMPOUNDER"
    RULE_2B_STOP_BREACH_SWING = "RULE_2B_STOP_BREACH_SWING"
    RULE_1_COMPOUNDER_VOLATILITY_BUFFER = "RULE_1_COMPOUNDER_VOLATILITY_BUFFER"
    RULE_3_SELL_INTO_STRENGTH = "RULE_3_SELL_INTO_STRENGTH"
    RULE_4_DOUBLE_STRUCTURAL_BREAKDOWN = "RULE_4_DOUBLE_STRUCTURAL_BREAKDOWN"
    RULE_5_MOMENTUM_EXHAUSTION_DIVERGENCE = "RULE_5_MOMENTUM_EXHAUSTION_DIVERGENCE"


class SentimentLabel(str, Enum):
    """FinBERT sentiment classification labels."""
    POSITIVE = "POSITIVE"
    NEUTRAL = "NEUTRAL"
    NEGATIVE = "NEGATIVE"


class TimeFrame(str, Enum):
    """Supported candlestick timeframes."""
    M15 = "15m"
    D1 = "1d"
    W1 = "1w"
