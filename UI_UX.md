# UI/UX Design Specification & Institutional Terminal Architecture — v3.0
# Project: "When to Sell" Engine (Kairos Quant)

**Document Status:** Approved Architecture & Frontend Design Specification  
**Parent Documents:** [PRD.md](file:///d:/Kairos/PRD.md) • [TRD.md](file:///d:/Kairos/TRD.md) • [APP_FLOW.md](file:///d:/Kairos/APP_FLOW.md) • [BACKEND_SCHEMA.md](file:///d:/Kairos/BACKEND_SCHEMA.md) • [API.md](file:///d:/Kairos/API.md)  
**Design Paradigm:** Brutalist Pure Monochrome Institutional Trading Terminal — "Linear Meets Bloomberg with Pitch-Black Grid Aesthetics"

---

## 0. Design Thesis & Anti-AI Philosophy

Kairos is an **institutional quant diagnostic terminal**, not a generic fintech dashboard or a cliché AI-generated web app.

### Strict Anti-AI Design Guardrails:
1. **Zero Generic AI Tropes:** No pastel purple gradients, no fuzzy rainbow drop-shadows, no rounded bubbly cards, no generic floating orbs, and no decorative stock illustrations.
2. **Brutalist Monochrome Precision:** Pitch black (`#000000`), chalk white (`#FFFFFF`), and razor-sharp 1px high-contrast borders (`#27272A`). Color is never used for mere decoration; it is strictly an informational state indicator.
3. **Institutional Data Density:** High information ratio per square inch. Layouts feature monospace numbers, tabular numeric alignment (`font-mono tabular-nums`), and explicit mathematical explainability.
4. **The Signature Kinetic Motif — Monotonic Chandelier Ratchet:** The core quantitative mechanism of Kairos is the **Chandelier Trailing-Stop floor**—a stop level that only ratchets upward, never down. Progress indicators, state changes, and evaluation steps permanently "lock in" with the same monotonic discipline.

---

## 1. Design Tokens & System Foundations

### 1.1 Pure Monochrome & High-Contrast System Palette

```css
:root {
  /* Pitch-Black & Brutalist Base */
  --bg-pitch: #000000;         /* Root terminal and page backdrop */
  --bg-panel: #09090B;         /* High-contrast panel / card surface */
  --bg-elevated: #18181B;      /* Active tabs, hover states, command popovers */
  --bg-input: #121215;         /* Search inputs and interactive fields */
  
  /* Razor Hairline Borders */
  --border-subtle: #27272A;    /* 1px structural container borders */
  --border-strong: #3F3F46;    /* Focused inputs, active tab indicators */
  --border-white: #FFFFFF;     /* Brutalist active focus outline */
  --grid-line: rgba(255, 255, 255, 0.05); /* Aceternity background grid lines */
  
  /* High-Contrast Typographic Hierarchy (WCAG 2.1 AAA Compliant) */
  --text-pure: #FFFFFF;        /* 100% Pure White (Hero headlines, action badges, prices) */
  --text-muted: #A1A1AA;       /* Zinc Gray (Labels, metric descriptors, timestamps) */
  --text-dark: #71717A;        /* Dark Muted Zinc (Keyboard shortcuts, footers) */
  --text-code: #E4E4E7;        /* Crisp Monospace text */
  
  /* Action & Semantic State Accents (Strictly for Verdicts & Alerts) */
  --state-hold: #10B981;       /* Emerald (HOLD) */
  --state-tighten: #06B6D4;    /* Cyan (TIGHTEN STOP) */
  --state-trim25: #F59E0B;     /* Amber (TRIM 25%) */
  --state-trim50: #F97316;     /* Orange (TRIM 50%) */
  --state-exit: #EF4444;       /* Crimson Red (EXIT FULLY) */
  --state-emergency: #DC2626;  /* Flashing Red (Tier-1 Hard Governance Bypass) */
}
```

---

### 1.2 Typography Hierarchy

| Role | Font Family | Weight | Size | Tracking | Usage |
|---|---|---|---|---|---|
| **Brutalist Brand Wordmark** | `Archivo Black` / `Cabinet Grotesk` | 900 (Black) | 22px | `-0.05em` | Minimalist `"svxm"` / `"KAIROS"` logo |
| **Hero Headline** | `Archivo Black` / `Space Grotesk` | 900 (Black) | 48px–60px | `-0.04em` | *"Kairos, want to know, when to sell your holding?"* |
| **Action Verdict Badge** | `Space Grotesk` / `Inter` | 900 (Black) | 40px–56px | `-0.03em` | Massive headline (`TRIM 25%`, `HOLD`, `EXIT FULLY`) |
| **Numeric Telemetry & Prices** | `JetBrains Mono` | 600 (Semi-Bold)| 16px–24px | `0.00em` | Tabular numbers: LTP (₹942.50), Stop (₹885.00), Kelly (25%) |
| **HUD Tab Labels** | `JetBrains Mono` | 700 (Bold) | 12px | `+0.08em` | `[ 01: CHARTS ]`, `[ 02: DIAGNOSTIC LEDGER ]` |
| **Data Metric Values** | `JetBrains Mono` | 500 (Medium) | 13px–15px | `0.00em` | PEG 1.12, ROCE 21.0%, RSI 41.2 |
| **Terminal Log Stream** | `JetBrains Mono` | 400 (Regular) | 12px–13px | `0.00em` | `> INGESTING NSE TICK SERIES [OK 42ms]` |
| **Explanatory Body Text** | `Inter` | 400 (Regular) | 14px | `-0.01em` | Mathematical reasons, rule descriptions, tooltips |

---

## 2. Navigation & Homepage Architecture

### 2.1 Minimalist High-Contrast Navbar (Image 1 Reference)
- **Visual Design:** Pure pitch-black (`#000000`) bar with a razor 1px bottom border (`#27272A`).
- **Left Anchor:** Brutalist lowercase/uppercase heavy wordmark `kairos` set in bold typography (`Archivo Black`).
- **Center Navigation:** Monospaced navigation links (`// RESEARCH`, `// METHODOLOGY`, `// SEBI PROOF`).
- **Right Anchor:** Brutalist tag badge `dev` / `v1.0` and live free-tier scan counter pill (`⚡ 3/3 SCANS`).

```
+-------------------------------------------------------------------------------------------------------------------+
| kairos                         // METHODOLOGY    // SEBI PROOF                        [⚡ 3/3 SCANS]   [dev]      |
+-------------------------------------------------------------------------------------------------------------------+
```

---

### 2.2 Aceternity Grid Hero Section (Image 2 Reference)
- **Background Engine:** Aceternity Dark Grid (`@aceternity/grid-background-demo`) rendered with sharp 1px grid lines (`rgba(255, 255, 255, 0.05)`) with an elliptical radial vignette fading into pitch black (`#000000`).
- **Hero Copy:**
  - Main Headline: **"Kairos, want to know, when to sell your holding?"** (Chalk White `#FFFFFF`, Heavy Brutalist tracking).
  - Subline: *"Algorithmic exit discipline & downside protection engine for Indian equities."*
- **Command Search Input:**
  - High-contrast centered command input box (`bg-[#09090B] border border-[#27272A] focus:border-white`).
  - Left icon: Terminal prompt `$` or search glass.
  - Keyboard hint badge: `⌘K` or `ENTER`.
  - Instant autocomplete popover with debounced search results (`TATAMOTORS.NS`, `RELIANCE.NS`, `HDFCBANK.NS`, `SUZLON.NS`).

---

### 2.3 Homepage Structure: 4 Core Slides / Sections

1. **Slide 1: Hero Command Center (Grid Background + Search):**
   - Direct stock entry point, instant scan execution, and quick-access watchlist pills.
2. **Slide 2: Mistake vs. Invariant Truth Matrix:**
   - Side-by-side comparative ledger contrasting retail emotional traps (The Disposition Effect, panic selling winners, holding decaying losers) against Kairos's quantitative invariants (Monotonic trailing floors, fractional Kelly trim, SEBI-stamped audit trails).
3. **Slide 3: 4-Pillar Algorithmic Architecture:**
   - Interactive breakdown of the 4 independent modules:
     - **Pillar A (Fundamental):** Balance sheet health, PEG, ROCE trend, Promoter pledge.
     - **Pillar B (Technical):** 50/200 DMA alignment, 14-period RSI, Delivery accumulation.
     - **Pillar C (Quant & Volatility):** 52-week drawdown, 1-year beta, annualized volatility.
     - **Pillar D (Regulatory NLP):** ONNX FinBERT corporate filing scanner & Tier-1 trigger.
4. **Slide 4: SEBI Cryptographic Proof & Pro Access:**
   - Live sample SHA-256 audit hash verification modal and Pro Tier subscription options (₹799/month).

---

## 3. Full-Screen HUD Radial Scanner Loading Transition

When a user selects or searches a ticker (e.g., `TATAMOTORS.NS`), the app smoothly transitions into a **Full-Screen HUD Radar Scanner**:

```
+-------------------------------------------------------------------------------------------------------------------+
|                                                                                                                   |
|                                            [ ◎ RADIAL TELEMETRY SCAN ]                                            |
|                                                   TATAMOTORS.NS                                                   |
|                                                                                                                   |
|                           ┌───────────────────────────────────────────────────────────┐                           |
|                           │  [✓] 01. INGESTING NSE TICK & MULTI-TIMEFRAME OHLCV BARS  │ [ 42ms ]                  |
|                           │  [✓] 02. RUNNING ONNX FINBERT REGULATORY FILING NLP SCAN  │ [ 68ms ]                  |
|                           │  [✓] 03. COMPUTING 4-PILLAR SCORES & SCIPY RSI DIVERGENCE │ [ 31ms ]                  |
|                           │  [◎] 04. RESOLVING 2D PRECEDENCE GRID & STAMPING SHA-256  │ [ RUNNING ]               |
|                           └───────────────────────────────────────────────────────────┘                           |
|                                                                                                                   |
|                                             [ TELEMETRY: 85% COMPLETE ]                                           |
+-------------------------------------------------------------------------------------------------------------------+
```

- **Visual Dynamics:**
  - Rotating concentric circular radar grid centered on screen.
  - Sequential telemetry checklist lines lighting up in monospace text with actual millisecond execution times.
  - Seamless, glitch-free cross-fade into the Multi-Tab Command Center Dashboard upon completion.

---

## 4. Multi-Tab Command Center Dashboard Architecture

The dashboard is structured into **Two Core Regions**:
1. **Persistent Top HUD & Typographic Verdict Banner** (Always visible).
2. **4 Dedicated High-Density Command Tabs** (Deep-dive workspaces).

```
+-------------------------------------------------------------------------------------------------------------------+
| TATAMOTORS.NS  •  Tata Motors Ltd  •  ₹942.50  [LARGE_CAP]           HORIZON: [ COMPOUNDER ● ]  SWING | ⚡ 2/3 SCANS|
+-------------------------------------------------------------------------------------------------------------------+
|                                                                                                                   |
|  [ PRIMARY ACTION VERDICT ]                                      [ VOLATILITY STOP FLOOR ]   [ RISK / REWARD ]    |
|  ██████████████████████████████████████████                      ₹885.00 (-6.10% Cushion)    1 : 2.39             |
|  TRIM 25%                                                        2.20x Wilder ATR            [KELLY: 25.0%]       |
|  Fundamental growth strong, but technical momentum waning.                                                        |
|  Lock partial profit (Trim 25%); maintain core position.         OVERRIDE: RULE_1_COMPOUNDER_VOLATILITY_BUFFER    |
|                                                                                                                   |
+-------------------------------------------------------------------------------------------------------------------+
| [ 01: CHARTS & STOP FLOOR ]   [ 02: DIAGNOSTIC LEDGER ]   [ 03: REGULATORY NLP ]   [ 04: TRIM SIMULATOR & TAX ]   |
+-------------------------------------------------------------------------------------------------------------------+
|                                                                                                                   |
|  [ ACTIVE TAB WORKSPACE CONTENT LOADED HERE ]                                                                     |
|                                                                                                                   |
+-------------------------------------------------------------------------------------------------------------------+
| SHA-256 AUDIT: a4f89d38c642bf1c94afbf4c8996fb92427ae41e4649b934ca495991b7852c91    [COPY AUDIT]  [INSPECT JSON]  |
+-------------------------------------------------------------------------------------------------------------------+
```

---

### 4.1 Tab 1: `[ 01: CHARTS & STOP FLOOR ]`
- **TradingView Lightweight Charts Integration:** Full HTML5 canvas rendering:
  - Multi-timeframe switcher: `[ 15M ]` `[ 1D ]` `[ 1W ]`.
  - Candlestick price series with 50 DMA (`#06B6D4`) and 200 DMA (`#A1A1AA`) overlays.
  - **Monotonic Stepped Chandelier Stop Floor Line (`#EF4444` / `#F59E0B`):** Step-line that ratchets strictly upward with price highs, visually proving the downside safety floor.
  - Upper Target Line (`#10B981` dashed line).
- **Interactive ATR Multiplier Slider:**
  - Fine-grained slider ($1.0\text{x}$ to $4.0\text{x}$ in $0.1\text{x}$ increments) allowing the user to dynamically test tighter or wider trailing stops with live risk-reward recalculation.

---

### 4.2 Tab 2: `[ 02: DIAGNOSTIC LEDGER ]`
- **4-Pillar Metric Grid:**
  - **Pillar 1: Fundamental Score ($S_{\text{fund}} = 84.0$):** PEG Ratio (1.12), ROCE Trend (+3.2% QoQ), Promoter Pledge (0.0%), FCF/Net Profit (0.88), Debt-to-Equity (0.42).
  - **Pillar 2: Technical Score ($S_{\text{tech}} = 38.0$):** Price vs 50 DMA, 200 DMA, 14-period RSI (41.2), Delivery Volume % (34.2%).
  - **Pillar 3: Quant & Risk Score ($S_{\text{quant}} = 65.0$):** 52-Week High Drawdown (-8.4%), 1-Year Realized Volatility (22.0%), Beta (1.12).
  - **Pillar 4: Regulatory & News ($S_{\text{news}} = 70.0$):** FinBERT time-decayed aggregate score, Tier-1 regulatory probe status (`CLEAR`).
- **2D Precedence Weights Applied:** Displays exact weights allocated (Fund: 45%, Tech: 15%, Quant: 25%, News: 15%).

---

### 4.3 Tab 3: `[ 03: REGULATORY NLP ]`
- **Chronological Regulatory Filing Feed:**
  - Listing of all corporate filings from BSE/NSE over the last 90 days.
  - FinBERT sentiment classification tag (`POSITIVE`, `NEUTRAL`, `NEGATIVE`) with raw confidence score (e.g. `+0.84`).
  - Tier-1 Hard Governance Override trigger status: Auditor resignation, credit rating downgrades, SEBI forensic audit alerts.

---

### 4.4 Tab 4: `[ 04: TRIM SIMULATOR & TAX ]`
- **Interactive Execution Calculator:**
  - Sliders for **Shares Held**, **Buy Price (₹)**, **Trim % (25%, 50%, 100%)**, and **Holding Period (Months)**.
  - Real-time output calculation:
    - Shares to Sell vs. Shares Retained.
    - Gross Cash Realized.
    - Indian Capital Gains Tax deduction (STCG 20% vs LTCG 12.5% on gains $>₹1.25\text{L}$).
    - Net Cash Added to Wallet.
    - **New Effective Breakeven Price** on retained shares and **Downside Cushion Expansion %**.

---

## 5. SEBI Audit Provenance Modal

Clicking `[INSPECT JSON]` or `[COPY AUDIT]` opens the **Cryptographic Verification Modal**:
- Displays raw immutable JSON input vector.
- Displays computed 64-character SHA-256 signature hash.
- Verified timestamp in IST and UTC.
- SEBI Algorithmic Diagnostic Sandbox compliance disclaimer.

---
*Maintained under Kairos Quant Engineering Standards.*
