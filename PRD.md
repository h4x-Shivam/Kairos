# Product Requirements Document (PRD) — v1.1
# Project: "When to Sell" Engine (Kairos Quant)
**Document Status:** Approved Architecture Draft  
**Target Market:** India (NSE & BSE Equities)  
**Primary Output:** Rule-Based Quantitative Diagnostic & Exit Engine

---

## 1. Executive Summary & Philosophy

### 1.1 Problem Statement
Retail investors in Indian equities suffer from a systemic behavioral flaw: **they focus entirely on stock entry (when to buy), but have no disciplined, unemotional framework for when, how much, and why to exit.**
This leads to:
1. **The Disposition Effect:** Selling winning compounders at +10% to "lock in profits" while holding fundamentally broken companies down -60% to zero.
2. **Panic Selling on Normal Volatility:** Getting shaken out by standard intraday noise because static stops (e.g., flat 10%) do not account for volatility.
3. **Black-Box Distrust:** Reluctance to trust "AI prediction" tools that offer unsubstantiated price targets without mathematical transparency, backtests, or risk-adjusted sizing.

### 1.2 Product Vision & Value Proposition
Kairos is an institutional-grade, transparent quantitative diagnostic decision-support system designed for Indian retail and prosumer equity investors.

Instead of predicting future prices, Kairos delivers:
- **A Clear Verdict:** `HOLD` | `TIGHTEN STOP` | `TRIM 25%` | `TRIM 50%` | `EXIT FULLY`
- **A Composite Diagnostic Score ($S_{\text{composite}} \in [0, 100]$):** Broken down across 4 modular pillars.
- **Dynamic Volatility-Adjusted Trailing Stops (Chandelier Exit):** Powered by ATR, calibrated for stock beta and holding horizon.
- **Risk-Reward & Fractional Kelly Position Trimming Sizing:** Mathematical position reduction guidelines.
- **Zero Black-Box Explainability:** Complete diagnostic trace displaying exact inputs, formulas, and driver indicators.

### 1.3 Defensive Regulatory Architecture (SEBI RA/IA Compliance)
Kairos is architected strictly as an **Algorithmic Diagnostic Sandbox**—not a discretionary financial advisor:
- **Language & Tone:** Diagnostic metrics (e.g., *"Calculated Stop: ₹920"*, *"Composite Score: 41/100"*) rather than advisory directives (*"SELL NOW"*).
- **User-Driven Inputs:** Users select their horizon, risk tolerance, and price targets.
- **Full Reproducibility:** Every diagnostic verdict is deterministically reproducible from public exchange filings, market ticks, and documented mathematical rules with a persistent audit log.

---

## 2. User Personas & The 2D Precedence Matrix

### 2.1 Persona Definitions

| Dimension | Persona 1: Positional Swing Trader | Persona 2: Core Equity Compounder |
|---|---|---|
| **Holding Horizon** | 2 weeks to 3 months | 6 months to 3+ years |
| **Primary Risk Concern** | Momentum breakdown, trend reversal, trailing profit protection | Fundamental deterioration, solvency risks, governance red flags |
| **System Mode** | **`Positional Swing`** | **`Core Compounder`** |
| **Default ATR Multiplier Base** | Tight Base ($1.8\times$) | Wide Chandelier Base ($2.5\times$) |
| **Scoring Bias** | Higher Technical ($S_{\text{tech}}$) & Quant ($S_{\text{quant}}$) | Higher Fundamental ($S_{\text{fund}}$) & Filings ($S_{\text{news}}$) |
| **Primary Execution Cadence** | 15–30 min Intraday Sweeps + Real-Time Trailing Stop Check | EOD Batch + Real-Time Tier 1 Governance Overrides |

---

### 2.2 Precedence Hierarchy: Horizon Mode vs. Market-Cap/Beta Bucket

To eliminate ambiguity, system parameters are determined via a **2-Factor Deterministic Grid (Horizon Mode $\times$ Market-Cap/Beta Bucket)**.

#### 1. Dynamic Weight Allocation Grid ($w_{\text{fund}}, w_{\text{tech}}, w_{\text{quant}}, w_{\text{news}}$)

$$\sum w_i = 100\%$$

| Horizon Mode | Stock Category Bucket | Classification Criteria | Fund ($w_{\text{fund}}$) | Tech ($w_{\text{tech}}$) | Quant ($w_{\text{quant}}$) | News ($w_{\text{news}}$) |
|---|---|---|---|---|---|---|
| **Core Compounder** | **Large-Cap / Low Beta** | Nifty 100, $\beta < 0.9$ | **45%** | **15%** | **25%** | **15%** |
| **Core Compounder** | **Mid-Cap / Moderate Beta** | Nifty Midcap 150, $0.9 \le \beta \le 1.3$ | **35%** | **25%** | **25%** | **15%** |
| **Core Compounder** | **Small-Cap / High Beta** | Smallcap 250 / Microcap, $\beta > 1.3$ | **25%** | **35%** | **25%** | **15%** |
| **Positional Swing** | **Large-Cap / Low Beta** | Nifty 100, $\beta < 0.9$ | **20%** | **40%** | **30%** | **10%** |
| **Positional Swing** | **Mid-Cap / Moderate Beta** | Nifty Midcap 150, $0.9 \le \beta \le 1.3$ | **15%** | **45%** | **30%** | **10%** |
| **Positional Swing** | **Small-Cap / High Beta** | Smallcap 250 / Microcap, $\beta > 1.3$ | **10%** | **50%** | **30%** | **10%** |

---

#### 2. ATR Multiplier Deterministic Precedence Formula

To avoid noise-whipsaws on high-beta smallcaps while preserving tight stops for low-beta swing positions, the ATR Multiplier ($k$) is calculated as:

$$k_{\text{default}} = \text{clamp}\Big(k_{\text{base}}(\text{Horizon Mode}) + \Delta k(\text{Beta Bucket}), \, 1.5, \, 3.5\Big)$$

Where:
- $k_{\text{base}}(\text{Positional Swing}) = 1.8$
- $k_{\text{base}}(\text{Core Compounder}) = 2.5$
- $\Delta k(\text{Large-Cap, } \beta < 0.9) = -0.3$ *(calm stocks move in tighter bands; tight stop captures trend shifts without giveback)*
- $\Delta k(\text{Mid-Cap, } 0.9 \le \beta \le 1.3) = 0.0$
- $\Delta k(\text{Small-Cap, } \beta > 1.3) = +0.5$ *(volatile stocks require wider cushion to avoid being stopped out by standard daily high-variance noise)*

**Resulting Default ATR Multiplier Grid:**

| Horizon Mode | Large-Cap ($\beta < 0.9$) | Mid-Cap ($0.9 \le \beta \le 1.3$) | Small-Cap ($\beta > 1.3$) |
|---|---|---|---|
| **Positional Swing** | **$1.5\times$** | **$1.8\times$** | **$2.3\times$** |
| **Core Compounder** | **$2.2\times$** | **$2.5\times$** | **$3.0\times$** |

> **Power User Override:** If the user toggles *"Manual ATR Stop Override"*, the auto-calculated $k_{\text{default}}$ is replaced with the user's manual slider value ($1.0\times \le k \le 4.0\times$).

---

## 3. Modular Scoring Specifications

### 3.1 Module A: Fundamental Score ($S_{\text{fund}} \in [0, 100]$)
Evaluates business solvency, cash conversion, operating trajectory, and valuation stretch.

$$\mathbf{S_{\text{fund}}} = 0.25 \cdot S_{\text{PEG}} + 0.20 \cdot S_{\text{Val}} + 0.20 \cdot S_{\text{ROCE}} + 0.15 \cdot S_{\text{FCF}} + 0.20 \cdot S_{\text{Solvency}}$$

| Metric | Formula | Scoring Normalization | Signal Tier |
|---|---|---|---|
| **PEG Ratio** ($S_{\text{PEG}}$) | $\text{P/E} \div (\text{EPS Growth Rate}_{\text{TTM}})$ | $\le 1.0 \rightarrow 100$; $1.0\text{--}2.0 \rightarrow 60$; $>2.0 \rightarrow 20$; Negative Growth $\rightarrow 0$ | High |
| **Valuation vs History** ($S_{\text{Val}}$) | $\text{Current P/E} \div \text{5-Year Median P/E}$ | $\le 1.0 \rightarrow 100$; $1.0\text{--}1.3 \rightarrow 60$; $>1.3 \rightarrow 20$; $>1.8 \rightarrow 0$ | Medium |
| **ROCE Trend** ($S_{\text{ROCE}}$) | $\text{ROCE}_{\text{Current}} - \text{ROCE}_{\text{3Q MA}}$ | Expanding $>+1\% \rightarrow 100$; Stable ($\pm 1\%$) $\rightarrow 60$; Declining $>2\% \rightarrow 15$ | High |
| **FCF Conversion** ($S_{\text{FCF}}$) | $\text{TTM FCF} \div \text{TTM Net Profit}$ | Ratio $>0.8 \rightarrow 100$; $0.3\text{--}0.8 \rightarrow 60$; Negative FCF with positive PAT $\rightarrow 10$ | Medium |
| **Solvency & Pledge** ($S_{\text{Solvency}}$) | Debt/Equity + % Promoter Pledged | $\text{D/E} < 0.5$ & Pledge $0\% \rightarrow 100$; Pledge $20\text{--}50\% \rightarrow 30$; Pledge $>50\% \rightarrow$ **Tier 1 Red Flag** | Critical |

---

### 3.2 Module B: Technical Score ($S_{\text{tech}} \in [0, 100]$)
Evaluates multi-timeframe moving average structure, momentum exhaustion, and institutional distribution.

$$\mathbf{S_{\text{tech}}} = 0.35 \cdot S_{\text{Trend}} + 0.30 \cdot S_{\text{RSI}} + 0.20 \cdot S_{\text{Delivery}} + 0.15 \cdot S_{\text{Drawdown}}$$

| Metric | Formula / Condition | Scoring Normalization |
|---|---|---|
| **Trend Alignment** ($S_{\text{Trend}}$) | Price vs 50 DMA vs 200 DMA | $\text{Price} > 50\text{DMA} > 200\text{DMA} \rightarrow 100$; $\text{Price} < 50\text{DMA}$ but $> 200\text{DMA} \rightarrow 50$; $\text{Price} < 50\text{DMA}$ & $< 200\text{DMA} \rightarrow 10$; Death Cross ($50 < 200$) $\rightarrow 0$ |
| **RSI & Divergence** ($S_{\text{RSI}}$) | 14-period RSI + 30-day Peak Divergence | Bullish Range ($45\text{--}65$) $\rightarrow 90$; Overbought ($>75$) no divergence $\rightarrow 60$; **Bearish Divergence** (Price New High + RSI Lower High) $\rightarrow 15$; Severe Breakdown ($<30$) $\rightarrow 5$ |
| **Delivery % Volume Filter** ($S_{\text{Delivery}}$) | $\frac{\text{Current Delivery Vol}}{\text{20-Day Avg Delivery Vol}}$ on Down vs Up days | Down Day with Delivery Vol $>1.5\times$ Avg $\rightarrow 10$ (Institutional Distribution); Up Day with High Delivery $\rightarrow 95$ (Institutional Accumulation); High Vol with Low Delivery $\rightarrow 50$ (Intraday Speculative) |
| **Peak Drawdown Envelope** ($S_{\text{Drawdown}}$) | $(\text{Recent 52w High} - \text{Price}) \div \text{52w High}$ | Normalized against stock's 2-year median drawdown band |

---

### 3.3 Module C: Quant & Risk Management Score ($S_{\text{quant}} \in [0, 100]$)

$$\mathbf{S_{\text{quant}}} = 0.40 \cdot S_{\text{StopBuffer}} + 0.35 \cdot S_{\text{RR}} + 0.25 \cdot S_{\text{Kelly}}$$

#### 1. Dynamic ATR Chandelier Trailing Stop Calculation
$$\text{TR}_t = \max\Big(H_t - L_t, \, |H_t - C_{t-1}|, \, |L_t - C_{t-1}|\Big), \quad \text{ATR}_{14} = \frac{1}{14}\sum_{i=1}^{14} \text{TR}_{t-i}$$
$$\text{Calculated Stop-Loss} = \max_{i \in [0, N]} (H_{t-i}) - (k_{\text{default}} \cdot \text{ATR}_{14})$$
- $S_{\text{StopBuffer}}$ evaluates distance from price to stop-loss:
  - $\text{Price} > \text{Stop-Loss} + 2\text{ATR} \rightarrow 100$
  - $\text{Price} \in [\text{Stop-Loss}, \, \text{Stop-Loss} + 1\text{ATR}] \rightarrow 40$
  - $\text{Price} \le \text{Stop-Loss} \rightarrow 0$ (Triggers Tier 2 Soft Override)

#### 2. Layered Fallback Risk-Reward Ratio ($S_{\text{RR}}$)
$$\text{R:R Ratio} = \frac{\text{Target Price} - \text{Current Price}}{\text{Current Price} - \text{Calculated Stop-Loss}}$$
**Target Price Derivation Hierarchy:**
1. **Tier 1 (User Defined):** If user inputs target $\rightarrow$ Use explicitly ($100\%$ conviction priority).
2. **Tier 2 (Analyst Consensus):** If institutional consensus target exists ($\ge 3$ analysts) $\rightarrow$ Use with badge `Analyst Consensus`.
3. **Tier 3 (Technical Fallback):** 52-Week High or nearest Fibonacci Extension level ($1.272\times$ / $1.618\times$ swing high).

*Scoring: $\text{R:R} \ge 2.5:1 \rightarrow 100$; $1.5\text{--}2.5 \rightarrow 65$; $1.0\text{--}1.5 \rightarrow 40$; $<1.0:1 \rightarrow 10$.*

#### 3. Fractional Kelly Position-Trimming Sizing & Score ($S_{\text{Kelly}}$)
$$\text{Kelly \%} = W - \frac{1 - W}{R}$$
*where $W = \text{Estimated Win Probability (category backtested baseline)}$, $R = \text{Reward-to-Risk Ratio}$.*  
To avoid drawdown risk, the engine uses **Quarter-Kelly ($\frac{1}{4}$ Kelly)** to calculate recommended trim amounts:

$$\text{Kelly Sizing Table:}$$

| Quantitative Condition | $S_{\text{quant}}$ Condition | Recommended Mechanical Sizing |
|---|---|---|
| Kelly Output healthy & R:R $\ge 2.0$ | $S_{\text{quant}} \ge 65$ | **No Trim (0%)** — Let runner compound |
| Kelly Output contracts $\ge 30\%$ from entry baseline | $45 \le S_{\text{quant}} < 65$ | **Trim 25%** — Harvest partial gain |
| Kelly Output contracts $>50\%$ or R:R $< 1.0$ | $30 \le S_{\text{quant}} < 45$ | **Trim 50%** — Capital protection |
| Stop-Loss breached or Tier 1 Hard Override | $S_{\text{quant}} < 30$ or Tier 1 | **Exit Fully (100%)** |

---

### 3.4 Module D: News & Primary Filings FinBERT ($S_{\text{news}} \in [0, 100]$)

#### Pipeline:
1. **Primary Feed:** BSE/NSE Regulatory Disclosure Feed (Corporate Filings, Board Meeting Announcements, Auditor Changes, Credit Rating Actions).
2. **Secondary Feed:** Tier-1 Indian Financial News Feeds (LiveMint, Moneycontrol, Economic Times).
3. **NLP Engine:** HuggingFace `ProsusAI/finbert` (classes: *Positive*, *Neutral*, *Negative*).
4. **Time-Decayed Exponential Aggregation:**
   $$S_{\text{news}} = \sum_{i=1}^{M} w_i \cdot \text{FinBERT\_Score}_i, \quad w_i = e^{-\lambda \cdot (\text{Days Ago}_i)}$$
   *News from the last 72 hours carries $4\times$ the weight of news from 10 days ago.*

---

## 4. Conflict-Resolution Engine & 2-Tier Override Hierarchy

### 4.1 Tier 1: Hard Governance Overrides (Immediate Exit Bypass)

```
       [Incoming Stock Evaluation]
                  │
                  ▼
   ┌────────────────────────────────────────────────┐
   │ TIER 1 HARD GOVERNANCE INTEGRITY CHECK         │
   │ 1. Auditor Resignation during non-audit cycle  │
   │ 2. SEBI Forensic Audit / Serious Inquiry Notice│
   │ 3. Credit Rating Downgrade to Default/Junk     │
   │ 4. Promoter Pledging > 50% of total shares     │
   │ 5. Lower Circuit Lock (Zero Bid Liquidity)     │
   └──────────────────────┬─────────────────────────┘
                          │
             ┌────────────┴────────────┐
        [TRIGGERED]               [CLEARED]
             │                         │
             ▼                         ▼
   ┌───────────────────┐    ┌───────────────────────────────────┐
   │ IMMEDIATE VERDICT:│    │ TIER 2 & CONTINUOUS SCORING CHECK │
   │   "EXIT FULLY     │    │ (Stop-loss & Matrix Rules)        │
   │ (CRITICAL ALERT)" │    └───────────────────────────────────┘
   │ Bypasses Scoring  │
   └───────────────────┘
```

**Tier 1 Execution:** If any trigger is active, the engine **completely bypasses all scoring modules** and locks the output:
- **Verdict:** `EXIT FULLY`
- **Badge:** `CRITICAL GOVERNANCE ALERT`
- **Explanation:** Displays the exact regulatory filing / alert text with source timestamp.

---

### 4.2 Tier 2: Soft Overrides & Modifiers

1. **Mechanical Stop-Loss Breach ($P < \text{Calculated Stop-Loss}$):**
   - Forces $S_{\text{StopBuffer}} = 0$, heavily depressing $S_{\text{quant}}$.
   - **Elite Fundamental Buffer ($S_{\text{fund}} \ge 70$):** If the company has exceptional fundamentals, the engine does *not* panic-exit; it outputs **`TRIM 50%`** and tightens the stop to $1.0\times\text{ATR}$ (Emergency Floor).
   - **Standard/Weak Stock ($S_{\text{fund}} < 70$):** Output locks to **`EXIT FULLY`**.
2. **Earnings Uncertainty State (Pre-Earnings 48h Window):**
   - Displays `Earnings Uncertainty` badge.
   - Suppresses Technical Module weight by 50% (reallocating weight to Fundamental & News) to prevent whipsaws from pre-results volatility.
   - Triggers an automated EOD rescore within 24 hours post-results announcement.

---

### 4.3 Complete Conflict-Resolution Architecture: Continuous Baseline + Discrete Rule Overrides

#### Layer 1: Continuous Baseline Score ($S_{\text{composite}}$)
$$S_{\text{composite}} = w_{\text{fund}} S_{\text{fund}} + w_{\text{tech}} S_{\text{tech}} + w_{\text{quant}} S_{\text{quant}} + w_{\text{news}} S_{\text{news}}$$

**Default Continuous Verdict Mapping (Full State-Space Fallback):**

| Composite Score Range ($S_{\text{composite}}$) | Default Base Verdict | Recommended Action |
|---|---|---|
| **$75 \le S_{\text{composite}} \le 100$** | **`HOLD`** | Trend strong, fundamentals intact. Maintain trailing stop. |
| **$60 \le S_{\text{composite}} < 75$** | **`TIGHTEN STOP`** | Momentum slowing or valuation stretched. Tighten ATR to $1.5\times$. |
| **$45 \le S_{\text{composite}} < 60$** | **`TRIM 25%`** | Partial deterioration. Harvest 25% profit, raise stop. |
| **$30 \le S_{\text{composite}} < 45$** | **`TRIM 50%`** | Substantial breakdown in 2+ pillars. Sell half into remaining liquidity. |
| **$0 \le S_{\text{composite}} < 30$** | **`EXIT FULLY`** | Full structural decay or unhedged downside. Preserve capital. |

---

#### Layer 2: Named Asymmetric Override Rules (Top Priority over Layer 1)

When specific structural divergence patterns occur, they override the continuous default mapping:

| Rule Name | Trigger Condition | System Output Verdict | Mathematical Justification & Action |
|---|---|---|---|
| **Rule 1: Compounder Volatility Buffer** | $S_{\text{fund}} \ge 70$, $S_{\text{tech}} < 45$, Price $>$ Stop | **`TRIM 25%`** | Strong fundamental compounder facing temporary technical pullback. Trim 25% to lock gains, tighten stop; do not panic-exit. |
| **Rule 2: Stop-Loss Breach on Compounder** | $S_{\text{fund}} \ge 70$, Price $\le$ Stop | **`TRIM 50%`** | High-conviction compounder breached primary ATR stop. Trim 50% to protect principal; tighten stop to $1.0\times\text{ATR}$ emergency line. |
| **Rule 3: Sell Into Technical Strength** | $S_{\text{fund}} < 45$, $S_{\text{tech}} \ge 70$, $S_{\text{quant}} \ge 60$ | **`TRIM 50%`** | Price momentum is surging, but underlying business fundamentals are deteriorating. Harvest 50% into market liquidity before price catches down. |
| **Rule 4: Double Structural Breakdown** | $S_{\text{fund}} < 45$, $S_{\text{tech}} < 45$ | **`EXIT FULLY`** | Both technical trend and fundamental quality have failed. Full exit regardless of sentiment. |
| **Rule 5: Momentum Exhaustion / Overbought Divergence** | $S_{\text{RSI}} \le 15$ (Bearish Div), R:R $< 1.0$, $S_{\text{composite}} < 65$ | **`TRIM 35%`** | Severe bearish RSI divergence at 52-week high with unfavorable R:R. Trim 35% to lock cycle top. |
| **Rule 6: Tier 1 Governance Bypass** | Any Tier 1 Trigger Active | **`EXIT FULLY`** | Solvency / regulatory emergency. Complete bypass of all scores. |

---

## 5. Data Architecture & Ingestion Strategy

### 5.1 Decoupled Data Provider Interface (`BaseDataProvider`)

The data layer is strictly decoupled to ensure zero vendor lock-in and seamless transition from local prototyping to production:

```python
class BaseDataProvider(ABC):
    @abstractmethod
    async def get_ohlcv(self, symbol: str, timeframe: str, lookback_bars: int) -> pd.DataFrame:
        """Fetch Open, High, Low, Close, Volume, Delivery Volume."""
        pass

    @abstractmethod
    async def get_financials(self, symbol: str) -> dict:
        """Fetch Quarterly Income Statement, Balance Sheet, Cash Flow, Ratios."""
        pass

    @abstractmethod
    async def get_corporate_filings_and_news(self, symbol: str, lookback_days: int) -> list[dict]:
        """Fetch BSE/NSE official disclosures and financial news headlines."""
        pass

    @abstractmethod
    async def get_governance_and_shareholding(self, symbol: str) -> dict:
        """Fetch promoter pledge %, auditor changes, and credit rating actions."""
        pass
```

- **Phase 1 Implementation:** `YFinanceDataProvider` (`.NS` / `.BO` tickers) + BSE public announcement scraper + local cached fundamentals.
- **Phase 2 Implementation:** `AngelOneSmartApiProvider` (Real-time SmartStream ticks/OHLCV with TOTP auth) + `IndianAPIDataProvider` (Structured fundamentals & shareholding) + direct BSE/NSE disclosure websockets.

---

### 5.2 Multi-Tier Ingestion Cadence

| Tier / Module | Execution Cadence | Trigger Mechanism | Cache TTL |
|---|---|---|---|
| **Tier 1 Hard Overrides** | **5-Minute Polling** during market hours (9:15–15:30 IST) | Celery Async Beat Worker | None (Immediate Alert on detection) |
| **Technicals & Trailing Stops (Modules B & C)** | **15–30 Minute Sweeps** + On-Demand User Request | Async FastAPI background task / WebSocket tick cache | 5 Minutes (Redis) |
| **Fundamentals (Module A)** | **Daily EOD** (Post 6:00 PM IST) | Nightly batch job | 24 Hours (Redis + Postgres) |
| **News & FinBERT Sentiment (Module D)** | **Hourly Poll** + EOD Batch | FinBERT Batch Inference Worker | 1 Hour (Postgres) |

---

## 6. UI/UX Design Specifications & Information Architecture

### 6.1 Visual Design Philosophy: "Linear Meets Robinhood"
- **Theme:** Deep Obsidian Slate (`#0B0F17`, `#121824`, `#1A2234`) with glassmorphic cards and 1px borders (`rgba(255, 255, 255, 0.08)`).
- **Typography:** JetBrains Mono for all numeric tables, prices, and tickers; Inter for UI copy and explanations.
- **High-Contrast Verdict Badges:**
  - `HOLD`: Precision Emerald (`#10B981`, glow: `rgba(16, 185, 129, 0.2)`)
  - `TIGHTEN STOP`: Sky Cyan (`#0EA5E9`)
  - `TRIM 25%`: Warm Amber (`#F59E0B`)
  - `TRIM 50%`: Vivid Tangerine (`#F97316`)
  - `EXIT FULLY`: Crimson Red (`#EF4444`, glow: `rgba(239, 68, 68, 0.25)`)

---

### 6.2 Primary Diagnostic Dashboard Layout

```
+-------------------------------------------------------------------------------------------------------+
|  [Logo: KAIROS QUANT]         [Search: HDFCBANK.NS]          [Mode: (x) Positional Swing  ( ) Compounder]
+-------------------------------------------------------------------------------------------------------+
|                                                                                                       |
|  HDFC BANK LTD (NSE: HDFCBANK) • Banking / Large-Cap • Beta: 0.84              LTP: ₹1,642.00 (+0.4%) |
|                                                                                                       |
|  +-------------------------------------------------------------------------------------------------+  |
|  |  VERDICT: HOLD                                          COMPOSITE SCORE: 78 / 100               |  |
|  |  Action: Long-term compounder trend intact. Maintain trailing stop at ₹1,548.00 (ATR 2.2x).    |  |
|  +-------------------------------------------------------------------------------------------------+  |
|                                                                                                       |
|  +-----------------------------------+  +----------------------------------------------------------+  |
|  | CALCULATED STOP-LOSS              |  | RISK-REWARD & POSITION SIZING                            |  |
|  | ₹1,548.00 (ATR 2.2x: ₹42.70)      |  | Target: ₹1,880.00 (Analyst Consensus - 34 Analysts)     |  |
|  | Distance to Stop: -5.7%           |  | R:R Ratio: 2.53 : 1  •  Kelly Action: 0% Trim (Hold All) |  |
|  +-----------------------------------+  +----------------------------------------------------------+  |
|                                                                                                       |
|  +-------------------------------------------------------------------------------------------------+  |
|  | [DIAGNOSTIC CARD: ZERO BLACK-BOX 4-MODULE BREAKDOWN]                                            |  |
|  |                                                                                                 |  |
|  | [A: FUNDAMENTAL 84/100]  [B: TECHNICAL 72/100]    [C: QUANT 78/100]     [D: NEWS & FILINGS 70] |  |
|  | • PEG: 1.2 (Fair)        • 50 > 200 DMA (Bullish) • ATR Stop: ₹1,548    • FinBERT: +0.62 Pos    |  |
|  | • ROCE: +1.8% QoQ        • RSI: 58.4 (Neutral)    • R:R: 2.53:1 (Good)  • 0 Governance Red Flags|  |
|  | • D/E: 0.0% Pledge       • Delivery %: 64% (High) • Stop Dist: 5.7%     • Recent Q3 PAT: +18%   |  |
|  +-------------------------------------------------------------------------------------------------+  |
|                                                                                                       |
|  +-------------------------------------------------------------------------------------------------+  |
|  | [DYNAMIC CHANDELIER TRAILING STOP CHART]                                                        |  |
|  | [ Interactive Multi-Timeframe Candlestick View with Overlay: 50DMA, 200DMA, Chandelier Stop Line]|  |
|  +-------------------------------------------------------------------------------------------------+  |
|                                                                                                       |
|  +-------------------------------------------------------------------------------------------------+  |
|  | [EXECUTION SIMULATOR: "WHAT IF I TRIM NOW?"]                                                    |  |
|  | [User Inputs: 100 Shares @ ₹1,420 Buy Price] -> [Slider: 25% Trim]                              |  |
|  | Realized Profit: ₹5,550.00  •  Est STCG Tax: ₹832.50  •  Effective Break-Even on 75 Shares: ₹1,377|  |
|  +-------------------------------------------------------------------------------------------------+  |
+-------------------------------------------------------------------------------------------------------+
```

---

## 7. Dual-Granularity Backtesting Validation Framework

To ensure statistical credibility before launch, Kairos uses a **2-Tier Dual-Granularity Backtesting Harness**:

```
                               ┌────────────────────────────────────────┐
                               │     DUAL-GRANULARITY BACKTESTING       │
                               └───────────────────┬────────────────────┘
                                                   │
                ┌──────────────────────────────────┴──────────────────────────────────┐
                ▼                                                                     ▼
┌───────────────────────────────────────────────┐     ┌───────────────────────────────────────────────┐
│ PASS 1: MACRO FUNDAMENTAL & REGIME BACKTEST   │     │ PASS 2: MICRO INTRADAY STOP & MOMENTUM        │
│ • Universe: 100 NSE Stocks across 5 Years     │     │ • Universe: 30 Liquid / High-Beta Stocks      │
│ • Resolution: Weekly EOD Runs                 │     │ • Resolution: 15-Minute Intraday Bars (1 Year)│
│ • Tests: Fundamental Decay, Compounder Holds, │     │ • Tests: Trailing Stop Whipsaw Rate, Delivery │
│   Quarterly Result Rescores, Kelly Trimming   │     │   Spike Filters, Intraday Circuit Triggers    │
└───────────────────────────────────────────────┘     └───────────────────────────────────────────────┘
```

### 7.1 Validation Benchmarks
The engine verdicts will be evaluated against:
1. **Strategy A (Kairos Quant Engine):** Dynamic rule-based trims, stops, and compounder holds.
2. **Strategy B (Naive Buy & Hold):** Holding without exiting.
3. **Strategy C (Static 10% Trailing Stop):** Standard retail fixed stop.

### 7.2 Published Statistical Target Metrics:
- **Drawdown Mitigation:** Portfolio max drawdown reduction $\ge 35\%$ vs. Buy & Hold during correction phases (e.g., 2020 crash, 2022 midcap selloff).
- **False Exit Rate on Compounders:** $<15\%$ premature exits on multi-bagger compounders.
- **Sharpe & Sortino Ratio:** Minimum $+0.40$ improvement in annualized Sharpe ratio over benchmark Nifty 500 TRI.

---

## 8. Monetization & Business Tiering

| Tier | Price | Diagnostic Limits | Key Features |
|---|---|---|---|
| **Free Explorer** | ₹0 / month | 3 stock diagnostics / day | Basic Verdict, Stop-loss price, 4-module summary, Fixed ATR |
| **Pro Trader / Investor** | ₹799 / month (or ₹6,999 / year) | Unlimited Diagnostics | Full Chandelier customizer, Execution Simulator, WhatsApp / SMS Stop-Loss Alerts, FinBERT disclosure trace |
| **Portfolio Pro** *(Phase 3)* | ₹1,499 / month | 1-Click Broker Portfolio Sync | Full Portfolio Risk Heatmap, Concentration Alerts, Multi-Stock Rebalance Simulator |

---

## 9. Phased Implementation Milestones

- **Phase 1: Quant Core & Prototype Engine (Current Focus)**
  - Swappable `BaseDataProvider` with `YFinanceDataProvider` implementation.
  - Complete implementation of Modules A, B, C (ATR & Kelly math) + 2-Factor Precedence Engine + Asymmetric Override Rules.
  - Linear/Robinhood-inspired Desktop web interface with dynamic charts and Execution Simulator.
  - Initial 20-stock validation backtest.
- **Phase 2: Live Indian Data & FinBERT Intelligence**
  - Integrate AngelOne SmartAPI (SmartConnect + TOTP) + IndianAPI/DalalAI.
  - Deploy FinBERT inference worker for BSE/NSE corporate disclosures.
  - Live 15-minute intraday sweep engine.
- **Phase 3: Real-Time Alerts, Broker Sync & Launch**
  - Broker portfolio sync (AngelOne / Zerodha / Groww).
  - WhatsApp / Email stop-loss breach notification system.
  - Production deployment & public backtest report publication.

---

## 10. Acceptance Criteria Checklist (PRD Approval)

- [x] **ATR Multiplier Contradiction Resolved:** Higher beta smallcaps receive wider multipliers ($2.3\times\text{--}3.0\times$) to absorb volatility; low-beta largecaps receive tighter multipliers ($1.5\times\text{--}2.2\times$).
- [x] **Trim Percentage Harmonized:** Normal technical weakness = `Trim 25%`; Actual stop-loss breach on elite stock = `Trim 50%`; Stop-loss breach on regular stock = `Exit Fully`.
- [x] **Precedence Logic Formalized:** Complete 2D Grid (Horizon Mode $\times$ Market-Cap/Beta) governs default weights and ATR multipliers.
- [x] **Full State Space Covered:** Continuous composite baseline formula ($S_{\text{composite}}$) covers all intermediate scores, with 6 priority named override rules.
- [x] **Dual-Granularity Backtesting Defined:** Weekly 5-year Macro Backtest + 15-minute 1-year Intraday Execution Backtest.
- [x] **Variable Names Unambiguous:** All mathematical symbols ($S_{\text{fund}}, S_{\text{tech}}, S_{\text{quant}}, S_{\text{news}}, S_{\text{composite}}, S_{\text{StopBuffer}}, S_{\text{RR}}, S_{\text{Kelly}}$) strictly defined.
