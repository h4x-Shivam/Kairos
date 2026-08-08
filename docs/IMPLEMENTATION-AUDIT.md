# Implementation Audit & Gap Analysis

**Project:** "When to Sell" Engine (Kairos Quant)  
**Date:** 2026-08-08  
**Audit Standard:** Strict PRD, TRD, UI_UX, APP_FLOW, BACKEND_SCHEMA, and API specification verification.

---

## Executive Summary

A comprehensive forensic audit of the previous codebase was conducted against the approved specification documents ([PRD.md](file:///d:/Kairos/PRD.md), [TRD.md](file:///d:/Kairos/TRD.md), [UI_UX.md](file:///d:/Kairos/UI_UX.md), [APP_FLOW.md](file:///d:/Kairos/APP_FLOW.md), [BACKEND_SCHEMA.md](file:///d:/Kairos/BACKEND_SCHEMA.md), [API.md](file:///d:/Kairos/API.md)). 

The audit revealed that while mathematical formulas for the core quant logic were verified via unit tests, the implementation suffered from **critical system-level gaps, missing asynchronous worker infrastructure, hardcoded single-stock seeding, absence of live exchange data providers, missing TradingView Lightweight Charts canvas, and mocked user authentication/billing subsystems.**

All previous code directories (`kairos-engine`, `kairos-web`) have been completely purged, preserving only the canonical `.md` architectural and specification documents.

---

## Detailed 16-Point Forensic Audit

### 1. What Was Actually Implemented
- **Pure Math Logic (Domain Layer):**
  - Wilder's Smoothing ATR formula ($\alpha = 1/14$) with $HH_{22}$ chandelier ratchet logic.
  - 4-Pillar modular score calculators: Fundamental ($S_{\text{fund}}$), Technical ($S_{\text{tech}}$), Quant/Risk ($S_{\text{quant}}$), and Sentiment aggregation ($S_{\text{news}}$).
  - 2D Precedence Grid matrix adjusting pillar weights and ATR multipliers across 3 Horizons (`COMPOUNDER`, `POSITIONAL`, `SWING_TRADER`) and 3 Market Caps (`LARGE_CAP`, `MID_CAP`, `SMALL_CAP`).
  - 6 Asymmetric Override Rules and Tier-1 Hard Governance Override logic.
  - Fractional Quarter-Kelly position trimming sizing.
  - Indian Capital Gains Tax Simulator (STCG 20% vs LTCG 12.5%).
  - Cryptographic SHA-256 SEBI Provenance Stamping.
- **REST & SSE Endpoints:**
  - Standard FastAPI routing structure for `/api/v1/diagnostic/evaluate`, `/api/v1/diagnostic/stream`, `/api/v1/simulator/trim`, `/api/v1/stocks/search`, `/api/v1/watchlist`, `/api/v1/audit/verify`.
- **UI Atomic Components:**
  - Next.js Tailwind design tokens adhering to Obsidian palette (`#07090E`), monospace typography hierarchy, and semantic verdict badges.

---

### 2. What Was Completely Missing
- **Abstract Data Provider Pipeline (`BaseDataProvider`):**
  - No implementation of `YFinanceDataProvider`, `ZerodhaKiteDataProvider`, `IndianAPIDataProvider`, or BSE/NSE official announcement scraper.
- **Celery & Celery Beat Worker Subsystem:**
  - No 15-minute intraday sweep worker.
  - No 5-minute Tier-1 hard governance emergency poller.
  - No nightly EOD fundamental & news batch worker.
- **Real ONNX / FinBERT Machine Learning Inference Engine:**
  - No ONNX Runtime or HuggingFace `ProsusAI/finbert` INT8 inference pipeline. Sentiment scores were merely static numbers read from database columns.
- **Dual-Granularity Backtesting Harness (PRD Section 7):**
  - Pass 1: 5-Year Weekly Macro Fundamental Backtester (100 NSE stocks) was missing.
  - Pass 2: 1-Year 15-Minute Intraday Trailing Stop & Whipsaw Backtester (30 stocks) was missing.
- **Real Financial Charting Canvas:**
  - TradingView Lightweight Charts (`lightweight-charts` v4.2.x) was not integrated; replaced with an ad-hoc static SVG mockup.
- **WhatsApp / SMS Stop-Loss Notification Pipeline (PRD Section 8/9):**
  - Completely absent.
- **Live Multi-Timeframe Series Switching (15m, 1D, 1W):**
  - The UI presented timeframe switcher buttons, but the backend lacked multi-timeframe OHLCV storage and aggregation.

---

### 3. What Was Implemented Incorrectly
- **Single-Stock Hardcoded Seeding:**
  - `seed.py` only populated historical OHLCV bars and financial ratios for `TATAMOTORS.NS`. Queries for `RELIANCE.NS`, `HDFCBANK.NS`, `SUZLON.NS`, `TCS.NS`, and `INFY.NS` crashed with `ValueError: Insufficient OHLCV price history`.
- **Database Engine Mismatch:**
  - Ran against a local SQLite file (`kairos_quant.db`) rather than the approved PostgreSQL 16 + TimescaleDB hypertable architecture.
- **Client Route Parameter Hydration in Next.js 15:**
  - Handled dynamic route parameters in client components via unmemoized promises, leading to Webpack dev cache invalidation.
- **Static Chart Mockup Instead of Canvas:**
  - [UI_UX.md](file:///d:/Kairos/UI_UX.md) and [TRD.md](file:///d:/Kairos/TRD.md) strictly mandate TradingView Lightweight Charts canvas with live candlestick rendering, 50/200 DMA overlays, and monotonic ascending Chandelier stop floors. The previous code used an SVG box.

---

### 4. Which Requirements Were Only Mocked
- **Market Data Feed:** No live connection to Yahoo Finance, NSE, or Zerodha; values were read from static seed arrays.
- **FinBERT NLP Analysis:** Sentiment score was hardcoded in seed data ($+0.84$), not derived from live text processing of regulatory filings.
- **Razorpay Pro Subscription Integration:** Razorpay checkout SDK and webhook HMAC verification was stubbed with client state flags.
- **User Authentication:** JWT token generation, password hashing (`bcrypt`), and user registration were stubbed without real session lifecycle management.

---

### 5. Which APIs / Data Sources Are Missing
- `YFinance` real-time/historical OHLCV downloader with caching.
- BSE/NSE corporate disclosure RSS/JSON scraper.
- `IndianAPI` / `DalalAI` fundamental balance sheet, P&L, and shareholding pattern data ingestion.
- `Zerodha KiteConnect` WebSocket streaming ticker adapter.

---

### 6. Which Backend Functionality Is Missing
- Dynamic data ingestion on unknown ticker search (auto-fetching and persisting new tickers on-demand).
- Asynchronous background task scheduler (Celery / Redis / APScheduler).
- Comprehensive error handling when external financial data sources fail, throttle, or return incomplete financial quarters.
- Real-time WebSocket feed for live price tick updates and trailing stop breach detection.

---

### 7. Which Database Functionality Is Missing
- TimescaleDB hypertable partitioning for `ohlcv_bars` (`timeframe`, `bar_time`).
- Alembic migration environment for schema evolution.
- User subscription tracking and payment webhook transaction logs.
- Automated TTL indexing for cached intermediate diagnostics in Redis.

---

### 8. Which AI / Analysis Functionality Is Missing
- `ProsusAI/finbert` INT8 ONNX Runtime model inference engine with tokenization and sentiment classification (`POSITIVE`, `NEUTRAL`, `NEGATIVE`).
- Time-decayed exponential weighting pipeline for multi-day disclosure aggregation ($w_i = e^{-\lambda \cdot \text{DaysAgo}}$).
- SEBI regulatory probe & auditor resignation keyword / zero-shot classification parser.

---

### 9. Which UI Screens Are Missing
- **TradingView Lightweight Charts Full Canvas Integration:** Dedicated chart canvas with timeframe switching, DMA overlays, and interactive Chandelier stop floor lines.
- **Pro Tier Checkout & Subscription Management Screen:** Real Razorpay modal flow and invoice/subscription status view.
- **Portfolio Health & Concentration Heatmap View (PRD Phase 3 / Pro Tier).**
- **Authentication Views:** Login, registration, and API key management modals.

---

### 10. Which User Flows Are Broken
- **Searching Non-Seeded Stocks:** Navigating to any stock other than `TATAMOTORS.NS` resulted in an unhandled 500 error due to missing database rows.
- **Timeframe Switching (15m vs 1D vs 1W):** Buttons in the chart component did not trigger data refetching or time-series aggregation.
- **Pro Tier Upgrade Flow:** Clicking "Upgrade to Pro" in the pricing section did not launch a functional checkout flow.

---

### 11. Which Buttons / Actions Currently Do Nothing
- `15m` / `1D` / `1W` timeframe toggles in Chandelier chart.
- "Upgrade to Pro" buttons in Pricing section (no payment gateway opened).
- "Sync Broker Portfolio" button in watchlist drawer.
- "Export Audit PDF" / "Copy Proof Hash" clipboard actions in certain sub-views.

---

### 12. What Must Be Deleted or Rewritten
- **All Previous Code:** Already deleted as per user instruction.
- **Data Ingestion Subsystem:** Must be built from scratch following the abstract `BaseDataProvider` pattern with real `yfinance` integration.
- **Charting Component:** Must be built using `@tradingview/lightweight-charts` with custom price line primitives for the Chandelier floor.
- **Database Layer:** Must be written with standard PostgreSQL/TimescaleDB models and standalone SQLite fallback for local testing without external services.

---

### 13. What Should Be Reused
- **Architectural Documentation:** [PRD.md](file:///d:/Kairos/PRD.md), [TRD.md](file:///d:/Kairos/TRD.md), [UI_UX.md](file:///d:/Kairos/UI_UX.md), [APP_FLOW.md](file:///d:/Kairos/APP_FLOW.md), [BACKEND_SCHEMA.md](file:///d:/Kairos/BACKEND_SCHEMA.md), [API.md](file:///d:/Kairos/API.md), and [AGENTS.md](file:///d:/Kairos/AGENTS.md).
- **Core Mathematical Formulations:**
  - Wilder ATR smoothed calculation.
  - 2D Precedence Grid weights & ATR delta offsets.
  - 6 Conflict Resolution Rules & Tier-1 Emergency Override state machine.
  - Quarter-Kelly sizing & Indian tax bracket formulas.
  - SHA-256 cryptographic audit hashing.
- **Terminal Design Tokens & Aesthetic Standard:**
  - Obsidian palette (`#07090E`, `#0D111A`, `#141A26`), monospace typography (`JetBrains Mono`, `Inter`), and high-contrast semantic verdict glow colors.

---

### 14. Critical Architectural Problems
- **Lack of On-Demand Ingestion:** The backend assumed all market data already lived in the database, breaking the app for any unseeded ticker.
- **Tight Coupling to Static Seeds:** The evaluator relied on pre-populated database rows rather than fetching from data providers dynamically.
- **Synchronous Bottlenecks:** Heavy computations were scheduled directly in the request handler without dedicated worker isolation.

---

### 15. Security Problems
- **Absence of Secrets Management:** Environment variables were not strictly enforced with validation schemas.
- **Stubbed Authentication:** Quota tracking relied solely on IP headers (`X-Forwarded-For`) which can be spoofed without secure Redis rate-limiting and JWT sessions.

---

### 16. Data / API Dependency Problems
- **No Resilient Upstream Fallback:** If Yahoo Finance or an exchange feed throttled or failed, the system lacked secondary fallbacks or cached stale-while-revalidate policies.
- **Hardcoded Indian Equity Symbol Formatting:** Inconsistent handling of `.NS` / `.BO` exchange suffixes between search queries and database lookups.

---

## Conclusion & Proposed Next Steps

The previous implementation provided a rapid conceptual proof-of-concept for the quant formulas, but did not satisfy the full production architectural standard.

With all non-markdown files purged, the next phase must follow a disciplined, clean-slate engineering roadmap:
1. Build a resilient, abstract data ingestion layer (`BaseDataProvider` + `YFinance` + Caching).
2. Implement pure quant math modules with 100% test coverage.
3. Build the FastAPI service with automated on-demand data fetching and TimescaleDB/PostgreSQL persistence.
4. Build the Next.js 15 frontend with real TradingView Lightweight Charts canvas and live terminal components.

**Status:** Awaiting User Approval. No code will be written until directed.
