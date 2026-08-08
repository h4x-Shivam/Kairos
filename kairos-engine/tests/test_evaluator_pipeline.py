"""End-to-end integration tests for the Master Evaluator & SHA-256 Provenance Hashing."""
from app.schemas.enums import HorizonMode, MarketCapBucket, PrimaryAction, OverrideRule
from app.schemas.diagnostic import (
    DiagnosticInput,
    FundamentalMetricsInput,
    TechnicalMetricsInput,
    QuantMetricsInput,
    SentimentDisclosureInput,
)
from app.engine.evaluator import evaluate_diagnostic
from app.engine.audit_hash import verify_sebi_audit_hash
from tests.test_math_indicators import create_synthetic_bars


def test_evaluator_pipeline_tatamotors_simulation():
    """Verify complete end-to-end diagnostic evaluation on realistic Tata Motors input."""
    bars = create_synthetic_bars(50, base_price=900.0)
    current_price = bars[-1].close
    
    diag_input = DiagnosticInput(
        symbol="TATAMOTORS.NS",
        company_name="Tata Motors Ltd",
        current_price=current_price,
        horizon_mode=HorizonMode.COMPOUNDER,
        market_cap_bucket=MarketCapBucket.LARGE_CAP,
        bars=bars,
        fundamentals=FundamentalMetricsInput(
            peg_ratio=1.12,
            roce_current=21.4,
            roce_3q_avg=18.2,
            promoter_pledge_pct=0.0,
            fcf_to_net_profit=0.88,
            debt_to_equity=0.42,
        ),
        technicals=TechnicalMetricsInput(
            sma_50=current_price * 0.95,
            sma_200=current_price * 0.85,
            rsi_14=62.0,
            delivery_pct=48.5,
        ),
        quant=QuantMetricsInput(
            high_52w=current_price * 1.05,
            realized_volatility_1y=22.0,
            beta=1.12,
        ),
        disclosures=[
            SentimentDisclosureInput(
                headline="Tata Motors reports record JLR free cash flow",
                hours_ago=12.0,
                sentiment_score=0.85,
                is_tier1_trigger=False,
            )
        ],
        consensus_target_price=current_price * 1.25,
    )
    
    output = evaluate_diagnostic(diag_input)
    
    assert output.symbol == "TATAMOTORS.NS"
    assert output.horizon_mode == HorizonMode.COMPOUNDER
    assert output.market_cap_bucket == MarketCapBucket.LARGE_CAP
    assert output.scores.s_fund >= 80.0
    assert output.scores.s_tech >= 80.0
    assert output.scores.s_composite >= 75.0
    assert output.action == PrimaryAction.HOLD
    assert output.rule_applied == OverrideRule.NONE
    assert output.stop_telemetry.is_stop_breached is False
    assert len(output.audit_hash) == 64
    
    # Verify cryptographic audit hash matches payload
    reconstruct_payload = {
        "symbol": output.symbol,
        "horizon": output.horizon_mode.value,
        "market_cap": output.market_cap_bucket.value,
        "price": round(output.stop_telemetry.current_price, 2),
        "scores": output.scores.model_dump(),
        "action": output.action.value,
        "rule": output.rule_applied.value,
        "stop": round(output.stop_telemetry.chandelier_stop, 2),
        "evaluated_at": output.evaluated_at_epoch,
    }
    assert verify_sebi_audit_hash(reconstruct_payload, output.audit_hash) is True
