"""Kairos Pure Quant Math Engine Package."""
from app.engine.indicators import (
    compute_true_range,
    compute_wilder_atr,
    compute_chandelier_stop_series,
    compute_rsi_series,
    detect_bearish_rsi_divergence,
)
from app.engine.precedence_grid import resolve_precedence_grid
from app.engine.module_a_fundamental import compute_fundamental_score
from app.engine.module_b_technical import compute_technical_score
from app.engine.module_c_quant import compute_quant_score
from app.engine.module_d_sentiment import compute_sentiment_score, check_tier1_trigger_active
from app.engine.conflict_resolution import resolve_verdict
from app.engine.risk_sizing import compute_risk_reward_and_kelly
from app.engine.tax_simulator import simulate_trim_execution
from app.engine.audit_hash import generate_sebi_audit_hash, verify_sebi_audit_hash
from app.engine.evaluator import evaluate_diagnostic

__all__ = [
    "compute_true_range",
    "compute_wilder_atr",
    "compute_chandelier_stop_series",
    "compute_rsi_series",
    "detect_bearish_rsi_divergence",
    "resolve_precedence_grid",
    "compute_fundamental_score",
    "compute_technical_score",
    "compute_quant_score",
    "compute_sentiment_score",
    "check_tier1_trigger_active",
    "resolve_verdict",
    "compute_risk_reward_and_kelly",
    "simulate_trim_execution",
    "generate_sebi_audit_hash",
    "verify_sebi_audit_hash",
    "evaluate_diagnostic",
]
