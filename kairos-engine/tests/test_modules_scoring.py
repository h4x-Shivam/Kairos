"""Exhaustive boundary and bucket tests for 4-Pillar scoring modules."""
from app.schemas.diagnostic import (
    FundamentalMetricsInput,
    TechnicalMetricsInput,
    QuantMetricsInput,
    SentimentDisclosureInput,
)
from app.engine.module_a_fundamental import (
    score_peg,
    score_roce_trend,
    score_promoter_pledge,
    score_fcf_conversion,
    score_debt_to_equity,
    compute_fundamental_score,
)
from app.engine.module_b_technical import (
    score_dma_alignment,
    score_rsi,
    score_delivery,
    compute_technical_score,
)
from app.engine.module_c_quant import (
    score_52w_drawdown,
    score_realized_volatility,
    score_beta,
    compute_quant_score,
)
from app.engine.module_d_sentiment import (
    compute_sentiment_score,
    check_tier1_trigger_active,
)


def test_fundamental_scoring_branches():
    """Verify all conditional branches for Module A."""
    # PEG
    assert score_peg(None) == 50.0
    assert score_peg(-1.0) == 10.0
    assert score_peg(0.8) == 100.0
    assert score_peg(1.3) == 80.0
    assert score_peg(1.8) == 60.0
    assert score_peg(2.3) == 40.0
    assert score_peg(3.5) == 20.0
    
    # ROCE Trend
    assert score_roce_trend(20.0, 17.0) == 100.0 # +3.0
    assert score_roce_trend(20.0, 19.0) == 85.0  # +1.0
    assert score_roce_trend(20.0, 20.0) == 70.0  # 0.0
    assert score_roce_trend(18.5, 20.0) == 45.0  # -1.5
    assert score_roce_trend(15.0, 20.0) == 20.0  # -5.0
    
    # Promoter Pledge
    assert score_promoter_pledge(0.0) == 100.0
    assert score_promoter_pledge(3.0) == 85.0
    assert score_promoter_pledge(10.0) == 60.0
    assert score_promoter_pledge(18.0) == 30.0
    assert score_promoter_pledge(25.0) == 0.0
    
    # FCF Conversion
    assert score_fcf_conversion(0.9) == 100.0
    assert score_fcf_conversion(0.6) == 75.0
    assert score_fcf_conversion(0.2) == 50.0
    assert score_fcf_conversion(-0.2) == 20.0
    
    # Debt / Equity
    assert score_debt_to_equity(0.15) == 100.0
    assert score_debt_to_equity(0.50) == 80.0
    assert score_debt_to_equity(1.00) == 60.0
    assert score_debt_to_equity(1.50) == 35.0
    assert score_debt_to_equity(2.50) == 10.0
    
    fund_input = FundamentalMetricsInput(
        peg_ratio=0.9,
        roce_current=22.0,
        roce_3q_avg=19.0,
        promoter_pledge_pct=0.0,
        fcf_to_net_profit=0.95,
        debt_to_equity=0.1,
    )
    score = compute_fundamental_score(fund_input)
    assert score == 100.0


def test_technical_scoring_branches():
    """Verify all conditional branches for Module B."""
    # DMA alignment
    assert score_dma_alignment(100, 90, 80) == 100.0  # Golden
    assert score_dma_alignment(85, 90, 80) == 75.0   # Healthy pullback
    assert score_dma_alignment(85, 80, 90) == 45.0   # Recovery
    assert score_dma_alignment(70, 80, 90) == 15.0   # Death alignment
    
    # RSI bands
    assert score_rsi(58.0) == 100.0
    assert score_rsi(45.0) == 75.0
    assert score_rsi(70.0) == 65.0
    assert score_rsi(35.0) == 40.0
    assert score_rsi(82.0) == 30.0
    assert score_rsi(22.0) == 15.0
    
    # Delivery %
    assert score_delivery(55.0) == 100.0
    assert score_delivery(45.0) == 80.0
    assert score_delivery(35.0) == 60.0
    assert score_delivery(25.0) == 40.0
    assert score_delivery(15.0) == 20.0
    
    tech_input = TechnicalMetricsInput(
        sma_50=90.0,
        sma_200=80.0,
        rsi_14=58.0,
        delivery_pct=55.0,
    )
    score = compute_technical_score(100.0, tech_input)
    assert score == 100.0


def test_quant_scoring_branches():
    """Verify all conditional branches for Module C."""
    # Drawdown
    assert score_52w_drawdown(98.0, 100.0) == 100.0 # -2%
    assert score_52w_drawdown(92.0, 100.0) == 85.0  # -8%
    assert score_52w_drawdown(85.0, 100.0) == 65.0  # -15%
    assert score_52w_drawdown(75.0, 100.0) == 40.0  # -25%
    assert score_52w_drawdown(60.0, 100.0) == 15.0  # -40%
    assert score_52w_drawdown(100.0, 0.0) == 50.0   # Zero guard
    
    # Realized Volatility
    assert score_realized_volatility(15.0) == 100.0
    assert score_realized_volatility(22.0) == 80.0
    assert score_realized_volatility(32.0) == 55.0
    assert score_realized_volatility(48.0) == 30.0
    assert score_realized_volatility(62.0) == 10.0
    
    # Beta
    assert score_beta(0.95) == 100.0
    assert score_beta(1.25) == 75.0
    assert score_beta(0.45) == 70.0
    assert score_beta(1.60) == 40.0
    assert score_beta(2.20) == 20.0
    assert score_beta(0.10) == 20.0
    
    quant_input = QuantMetricsInput(
        high_52w=100.0,
        realized_volatility_1y=15.0,
        beta=0.95,
    )
    score = compute_quant_score(98.0, quant_input)
    assert score == 100.0


def test_sentiment_scoring_empty_and_decay():
    """Verify Module D with empty disclosures and time-decay."""
    assert compute_sentiment_score([]) == 50.0
    assert check_tier1_trigger_active([]) is False
    
    # Negative disclosure 10 days ago (>168 hrs) should NOT trigger active tier-1 bypass
    stale_tier1 = [
        SentimentDisclosureInput(
            headline="Past investigation closed",
            hours_ago=250.0,
            sentiment_score=-0.8,
            is_tier1_trigger=True,
        )
    ]
    assert check_tier1_trigger_active(stale_tier1) is False
    
    # Active tier-1 trigger 24 hrs ago
    active_tier1 = [
        SentimentDisclosureInput(
            headline="Statutory auditor resigns abruptly",
            hours_ago=24.0,
            sentiment_score=-1.0,
            is_tier1_trigger=True,
        )
    ]
    assert check_tier1_trigger_active(active_tier1) is True
    assert compute_sentiment_score(active_tier1) < 20.0
