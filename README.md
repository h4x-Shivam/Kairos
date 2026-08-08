# Kairos Quant — "When to Sell" Engine

> **Institutional-grade deterministic quantitative exit engine for retail investors in Indian equities (NSE/BSE).**

---

## 🏛️ System Architecture

Kairos Quant eliminates emotional decision-making when exiting stock positions using a 4-pillar multi-factor model and an asymmetric conflict resolution state machine.

### 4-Pillar Scoring Model
1. **Pillar A ($S_{\text{fund}}$):** Accounting quality, ROCE trend, FCF conversion, debt solvency, and promoter pledge.
2. **Pillar B ($S_{\text{tech}}$):** 50/200 DMA trend alignment, 14-period RSI momentum, and NSE delivery accumulation.
3. **Pillar C ($S_{\text{quant}}$):** 52-week high drawdown, 1-year realized volatility, and market beta.
4. **Pillar D ($S_{\text{news}}$):** Time-decayed FinBERT regulatory filing sentiment ($72\text{h}$ half-life) and Tier-1 emergency bypass triggers.

### Core Mathematical Features
- **Wilder's ATR(14) Smoothed Volatility:** $\alpha = 1/14$ true range exponential smoothing.
- **Monotonic Chandelier Ratchet:** $HH_{22} - m \cdot \text{ATR}_{14}$ trailing stop floor that strictly ratchets upward.
- **2D Precedence Grid:** Resolves dynamic factor weights and stop multipliers across Investor Horizon (`COMPOUNDER` vs `SWING`) and Market Cap (`LARGE`, `MID`, `SMALL`).
- **6 Asymmetric Conflict Overrides:** Priority-based rules resolving divergence between fundamentals, technicals, and governance red flags.
- **Fractional Quarter-Kelly Sizing & Indian Tax Simulator:** STCG (20%) vs LTCG (12.5%) net cash realization and breakeven cushion expansion.
- **SEBI SHA-256 Provenance:** Cryptographic timestamped audit hash on all diagnostic evaluations.

---

## 🚀 Quickstart

### Backend Math Engine (`kairos-engine`)

```bash
cd kairos-engine

# Install dependencies
pip install -r requirements.txt

# Run full test suite with coverage
python -m pytest tests/ -v --cov=app/engine
```

---

## 📄 Canonical Documentation

- [PRD.md](PRD.md) — Product Requirements Document
- [TRD.md](TRD.md) — Technical Requirements Document
- [UI_UX.md](UI_UX.md) — Institutional Terminal UI/UX Specification
- [APP_FLOW.md](APP_FLOW.md) — User Journey Architecture & State Transitions
- [BACKEND_SCHEMA.md](BACKEND_SCHEMA.md) — Database DDL & Schema Contracts
- [API.md](API.md) — RESTful & WebSocket API Contracts
- [AGENTS.md](AGENTS.md) — Engineering Standards & Architecture Governance
- [PROJECT_ANALYSIS.md](docs/PROJECT_ANALYSIS.md) — Comprehensive System Analysis
