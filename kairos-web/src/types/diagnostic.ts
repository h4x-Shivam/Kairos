/**
 * Strict TypeScript Data Contracts for Kairos Quant Engine.
 */

export type HorizonMode = "COMPOUNDER" | "SWING";
export type MarketCapBucket = "LARGE_CAP" | "MID_CAP" | "SMALL_CAP";
export type PrimaryAction = "HOLD" | "TIGHTEN_STOP" | "TRIM_25" | "TRIM_50" | "EXIT_FULLY";

export type OverrideRule =
  | "NONE"
  | "TIER_1_HARD_GOVERNANCE_BYPASS"
  | "RULE_2A_STOP_BREACH_COMPOUNDER"
  | "RULE_2B_STOP_BREACH_SWING"
  | "RULE_1_COMPOUNDER_VOLATILITY_BUFFER"
  | "RULE_3_SELL_INTO_STRENGTH"
  | "RULE_4_DOUBLE_STRUCTURAL_BREAKDOWN"
  | "RULE_5_MOMENTUM_EXHAUSTION_DIVERGENCE";

export interface PlainLanguageExplanations {
  summary: string;
  pillar_fund: string;
  pillar_tech: string;
  pillar_quant: string;
  pillar_news: string;
}

export interface ScoreCard {
  s_fund: number;
  s_tech: number;
  s_quant: number;
  s_news: number;
  s_composite: number;
}

export interface PrecedenceWeights {
  w_fund: number;
  w_tech: number;
  w_quant: number;
  w_news: number;
  base_multiplier: number;
  net_multiplier: number;
}

export interface StopLossTelemetry {
  current_price: number;
  chandelier_stop: number;
  cushion_pct: number;
  atr_14: number;
  highest_high_22: number;
  is_stop_breached: boolean;
}

export interface RiskRewardTelemetry {
  target_price: number;
  reward_delta: number;
  risk_delta: number;
  risk_reward_ratio: number;
  quarter_kelly_pct: number;
}

export interface ChartDataPoint {
  time: number;
  open: number;
  high: number;
  low: number;
  close: number;
  stop: number;
}

export interface FundamentalMetrics {
  peg_ratio: number | null;
  roce_current: number;
  roce_3q_avg: number;
  promoter_pledge_pct: number;
  fcf_to_net_profit: number;
  debt_to_equity: number;
}

export interface TechnicalMetrics {
  sma_50: number;
  sma_200: number;
  rsi_14: number;
  delivery_pct: number;
}

export interface QuantMetrics {
  high_52w: number;
  realized_volatility_1y: number;
  beta: number;
}

export interface SentimentDisclosureInput {
  headline: string;
  hours_ago: number;
  sentiment_score: number;
  is_tier1_trigger: boolean;
}

export interface TaxImpactResult {
  shares_held: number;
  shares_to_sell: number;
  shares_retained: number;
  buy_price: number;
  current_price: number;
  gross_proceeds: number;
  capital_gain: number;
  tax_type: "STCG" | "LTCG";
  tax_rate_pct: number;
  tax_liability: number;
  net_cash_realized: number;
  new_breakeven_price: number;
  new_downside_cushion_pct: number;
}

export interface DiagnosticOutput {
  symbol: string;
  company_name: string;
  horizon_mode: HorizonMode;
  market_cap_bucket: MarketCapBucket;
  action: PrimaryAction;
  rule_applied: OverrideRule;
  explanation: string;
  scores: ScoreCard;
  weights: PrecedenceWeights;
  stop_telemetry: StopLossTelemetry;
  risk_telemetry: RiskRewardTelemetry;
  fundamentals: FundamentalMetrics;
  technicals: TechnicalMetrics;
  quant: QuantMetrics;
  disclosures: SentimentDisclosureInput[];
  chart_data: ChartDataPoint[];
  plain_language: PlainLanguageExplanations;
  audit_hash: string;
  evaluated_at_epoch: number;
  tax_impact?: TaxImpactResult | null;
}

export interface StockSearchResult {
  symbol: string;
  company_name: string;
  exchange: string;
  market_cap_bucket: MarketCapBucket;
  sector: string;
}

export type StageType =
  | "INITIALIZING"
  | "FETCHING_OHLCV"
  | "FETCHING_FUNDAMENTALS"
  | "SENTIMENT_ANALYSIS"
  | "RESOLVING_CONFLICTS"
  | "COMPLETE"
  | "ERROR";

export interface TelemetryEvent {
  stage: StageType;
  progress: number;
  message: string;
  data?: DiagnosticOutput | null;
}
