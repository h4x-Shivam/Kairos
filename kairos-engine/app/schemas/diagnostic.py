"""Diagnostic schemas and Pydantic data contracts for Kairos Quant."""
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, ConfigDict
from app.schemas.enums import (
    HorizonMode,
    MarketCapBucket,
    PrimaryAction,
    OverrideRule,
)


class PlainLanguageExplanations(BaseModel):
    """Contextual plain-language text representations for verdicts and pillars."""
    model_config = ConfigDict(frozen=True)
    
    summary: str
    pillar_fund: str
    pillar_tech: str
    pillar_quant: str
    pillar_news: str


class OHLCVBar(BaseModel):
    """Single OHLCV candlestick bar."""
    model_config = ConfigDict(frozen=True)
    
    time: int = Field(..., description="Unix epoch timestamp in seconds")
    open: float = Field(..., ge=0.0)
    high: float = Field(..., ge=0.0)
    low: float = Field(..., ge=0.0)
    close: float = Field(..., ge=0.0)
    volume: float = Field(..., ge=0.0)


class FundamentalMetricsInput(BaseModel):
    """Pillar A: Fundamental accounting and valuation inputs."""
    model_config = ConfigDict(frozen=True)
    
    peg_ratio: Optional[float] = Field(None, description="Price/Earnings to Growth ratio")
    roce_current: float = Field(..., description="Current Return on Capital Employed in %")
    roce_3q_avg: float = Field(..., description="Trailing 3-quarter average ROCE in %")
    promoter_pledge_pct: float = Field(0.0, ge=0.0, le=100.0, description="Promoter shares pledged in %")
    fcf_to_net_profit: float = Field(..., description="Free Cash Flow / Net Profit ratio")
    debt_to_equity: float = Field(0.0, ge=0.0, description="Total Debt / Total Equity ratio")


class TechnicalMetricsInput(BaseModel):
    """Pillar B: Technical moving averages and momentum inputs."""
    model_config = ConfigDict(frozen=True)
    
    sma_50: float = Field(..., ge=0.0)
    sma_200: float = Field(..., ge=0.0)
    rsi_14: float = Field(..., ge=0.0, le=100.0)
    delivery_pct: float = Field(..., ge=0.0, le=100.0, description="NSE Security Delivery %")


class QuantMetricsInput(BaseModel):
    """Pillar C: Volatility, drawdown, and beta inputs."""
    model_config = ConfigDict(frozen=True)
    
    high_52w: float = Field(..., ge=0.0)
    realized_volatility_1y: float = Field(..., ge=0.0, description="1-year annualized volatility in %")
    beta: float = Field(1.0, description="1-year Beta vs Nifty 50")


class SentimentDisclosureInput(BaseModel):
    """Pillar D: Structured corporate announcement input."""
    model_config = ConfigDict(frozen=True)
    
    headline: str
    hours_ago: float = Field(..., ge=0.0)
    sentiment_score: float = Field(..., ge=-1.0, le=1.0, description="FinBERT score: -1 to +1")
    is_tier1_trigger: bool = Field(False, description="Auditor resignation, SEBI probe, or debt default")


class ScoreCard(BaseModel):
    """Individual pillar scores and continuous composite score [0, 100]."""
    model_config = ConfigDict(frozen=True)
    
    s_fund: float = Field(..., ge=0.0, le=100.0)
    s_tech: float = Field(..., ge=0.0, le=100.0)
    s_quant: float = Field(..., ge=0.0, le=100.0)
    s_news: float = Field(..., ge=0.0, le=100.0)
    s_composite: float = Field(..., ge=0.0, le=100.0)


class PrecedenceWeights(BaseModel):
    """Resolved 2D Precedence Grid weights and multipliers."""
    model_config = ConfigDict(frozen=True)
    
    w_fund: float
    w_tech: float
    w_quant: float
    w_news: float
    base_multiplier: float
    net_multiplier: float


class StopLossTelemetry(BaseModel):
    """Chandelier ratcheting stop floor telemetry."""
    model_config = ConfigDict(frozen=True)
    
    current_price: float
    chandelier_stop: float
    cushion_pct: float
    atr_14: float
    highest_high_22: float
    is_stop_breached: bool


class RiskRewardTelemetry(BaseModel):
    """Fractional Kelly allocation and asymmetric risk-reward telemetry."""
    model_config = ConfigDict(frozen=True)
    
    target_price: float
    reward_delta: float
    risk_delta: float
    risk_reward_ratio: float
    quarter_kelly_pct: float


class ChartDataPoint(BaseModel):
    """Single point in time containing actual price and calculated stop-loss."""
    model_config = ConfigDict(frozen=True)
    
    time: int
    open: float
    high: float
    low: float
    close: float
    stop: float


class DiagnosticInput(BaseModel):
    """Canonical input payload required for full diagnostic evaluation."""
    model_config = ConfigDict(frozen=True)
    
    symbol: str
    company_name: str
    current_price: float = Field(..., ge=0.0)
    horizon_mode: HorizonMode
    market_cap_bucket: MarketCapBucket
    bars: List[OHLCVBar] = Field(..., min_length=22, description="At least 22 historical OHLCV bars")
    fundamentals: FundamentalMetricsInput
    technicals: TechnicalMetricsInput
    quant: QuantMetricsInput
    disclosures: List[SentimentDisclosureInput] = Field(default_factory=list)
    consensus_target_price: Optional[float] = None
    manual_atr_mult: Optional[float] = None


class DiagnosticOutput(BaseModel):
    """Canonical output contract produced by the Quant Math Engine."""
    model_config = ConfigDict(frozen=True)
    
    symbol: str
    company_name: str
    horizon_mode: HorizonMode
    market_cap_bucket: MarketCapBucket
    action: PrimaryAction
    rule_applied: OverrideRule
    explanation: str
    scores: ScoreCard
    weights: PrecedenceWeights
    stop_telemetry: StopLossTelemetry
    risk_telemetry: RiskRewardTelemetry
    fundamentals: FundamentalMetricsInput
    technicals: TechnicalMetricsInput
    quant: QuantMetricsInput
    disclosures: List[SentimentDisclosureInput]
    chart_data: List[ChartDataPoint]
    plain_language: PlainLanguageExplanations
    audit_hash: str
    evaluated_at_epoch: int
    tax_impact: Optional[Dict[str, Any]] = None

