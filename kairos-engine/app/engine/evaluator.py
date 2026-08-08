"""Master Pure Quant Diagnostic Evaluator Orchestrator."""
import time
import numpy as np
from app.schemas.diagnostic import (
    DiagnosticInput,
    DiagnosticOutput,
    ScoreCard,
    StopLossTelemetry,
)
from app.engine.precedence_grid import resolve_precedence_grid
from app.engine.indicators import (
    compute_chandelier_stop_series,
    compute_rsi_series,
    detect_bearish_rsi_divergence,
)
from app.engine.module_a_fundamental import compute_fundamental_score
from app.engine.module_b_technical import compute_technical_score
from app.engine.module_c_quant import compute_quant_score
from app.engine.module_d_sentiment import (
    compute_sentiment_score,
    check_tier1_trigger_active,
)
from app.engine.conflict_resolution import resolve_verdict
from app.engine.risk_sizing import compute_risk_reward_and_kelly
from app.engine.audit_hash import generate_sebi_audit_hash


def evaluate_diagnostic(diag_input: DiagnosticInput) -> DiagnosticOutput:
    """Execute complete deterministic quant exit evaluation for a stock holding."""
    # 1. Resolve 2D Precedence Grid weights and dynamic ATR multiplier
    weights = resolve_precedence_grid(
        diag_input.horizon_mode,
        diag_input.market_cap_bucket,
        diag_input.manual_atr_mult,
    )
    
    # 2. Vectorized Technical Indicators & Chandelier Ratchet
    stops, atrs, highest_highs = compute_chandelier_stop_series(
        diag_input.bars,
        multiplier=weights.net_multiplier,
        lookback_hh=22,
        atr_period=14,
    )
    
    current_stop = float(stops[-1])
    current_atr = float(atrs[-1])
    current_hh = float(highest_highs[-1])
    
    # Stop cushion calculation (% distance from current price down to stop)
    if diag_input.current_price > 0:
        cushion_pct = ((current_stop - diag_input.current_price) / diag_input.current_price) * 100.0
    else:
        cushion_pct = 0.0
        
    is_breached = bool(diag_input.current_price <= current_stop)
    
    # RSI & Peak Divergence detection
    closes = np.array([b.close for b in diag_input.bars], dtype=np.float64)
    rsi_series = compute_rsi_series(closes, period=14)
    has_bearish_div = detect_bearish_rsi_divergence(closes, rsi_series, lookback=30)
    
    # 3. Calculate 4-Pillar Quantitative Scores
    s_fund = compute_fundamental_score(diag_input.fundamentals)
    s_tech = compute_technical_score(diag_input.current_price, diag_input.technicals)
    s_quant = compute_quant_score(diag_input.current_price, diag_input.quant)
    s_news = compute_sentiment_score(diag_input.disclosures)
    is_tier1_active = check_tier1_trigger_active(diag_input.disclosures)
    
    # 4. Continuous Weighted Composite Score
    raw_composite = (
        weights.w_fund * s_fund +
        weights.w_tech * s_tech +
        weights.w_quant * s_quant +
        weights.w_news * s_news
    )
    s_composite = round(float(raw_composite), 1)
    
    # 5. Risk-Reward Ratio and Quarter-Kelly Sizing
    risk_telemetry = compute_risk_reward_and_kelly(
        current_price=diag_input.current_price,
        chandelier_stop=current_stop,
        consensus_target_price=diag_input.consensus_target_price,
    )
    
    # 6. Asymmetric Conflict Resolution State Machine
    action, rule_applied, explanation, final_composite = resolve_verdict(
        horizon_mode=diag_input.horizon_mode,
        current_price=diag_input.current_price,
        chandelier_stop=current_stop,
        s_fund=s_fund,
        s_tech=s_tech,
        s_quant=s_quant,
        s_composite=s_composite,
        is_tier1_active=is_tier1_active,
        has_bearish_divergence=has_bearish_div,
        risk_reward_ratio=risk_telemetry.risk_reward_ratio,
    )
    
    scorecard = ScoreCard(
        s_fund=s_fund,
        s_tech=s_tech,
        s_quant=s_quant,
        s_news=s_news,
        s_composite=final_composite,
    )
    
    stop_telemetry = StopLossTelemetry(
        current_price=round(diag_input.current_price, 2),
        chandelier_stop=round(current_stop, 2),
        cushion_pct=round(cushion_pct, 2),
        atr_14=round(current_atr, 2),
        highest_high_22=round(current_hh, 2),
        is_stop_breached=is_breached,
    )
    
    # 7. Cryptographic SHA-256 Provenance Stamping
    epoch_now = int(time.time())
    audit_payload = {
        "symbol": diag_input.symbol,
        "horizon": diag_input.horizon_mode.value,
        "market_cap": diag_input.market_cap_bucket.value,
        "price": round(diag_input.current_price, 2),
        "scores": scorecard.model_dump(),
        "action": action.value,
        "rule": rule_applied.value,
        "stop": round(current_stop, 2),
        "evaluated_at": epoch_now,
    }
    audit_hash = generate_sebi_audit_hash(audit_payload)
    
    return DiagnosticOutput(
        symbol=diag_input.symbol,
        company_name=diag_input.company_name,
        horizon_mode=diag_input.horizon_mode,
        market_cap_bucket=diag_input.market_cap_bucket,
        action=action,
        rule_applied=rule_applied,
        explanation=explanation,
        scores=scorecard,
        weights=weights,
        stop_telemetry=stop_telemetry,
        risk_telemetry=risk_telemetry,
        audit_hash=audit_hash,
        evaluated_at_epoch=epoch_now,
    )
