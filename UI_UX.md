# UI/UX Design Specification — v2.0
# Project: "When to Sell" Engine (Kairos)
**Document Status:** Consolidated — Supersedes all prior UI/UX drafts
**Parent Documents:** PRD.md • TRD.md • APP_FLOW.md • BACKEND_SCHEMA.md
**Design Paradigm:** Monochrome Editorial Minimalism — Heavy Typography, Two Reserved Signal Colors

---

## 1. Design Philosophy

### 1.1 What this is not
Kairos is not a Bloomberg-terminal pastiche and not a generic rounded-card SaaS dashboard. Both were explicitly tried and rejected during design iteration. No console/CLI styling (no `>` prompts, no blinking cursors, no line-by-line checkmark logs), no gradient stat cards, no icon badges per metric, no soft drop shadows, no hover-bounce/scale micro-interactions.

### 1.2 What this is
**Swiss/editorial minimalism.** Black, white, and grey, with exactly two reserved exception colors used nowhere except their named purpose (Section 3.2). Heavy typographic weight, size, and negative space carry the visual hierarchy and emotional register that color would normally carry. The product should feel closer to a well-designed print publication than a trading app.

### 1.3 Core UX principle: severity through weight, not hue
Because color is almost entirely unavailable, verdict severity escalates through **grayscale fill and font weight** — lighter/outlined for mild states, progressively darker fill and heavier weight for more serious states. The two reserved colors (yellow, red) each mark exactly one state; their rarity is what makes them legible. See Section 5 for the full severity ladder.

### 1.4 Explainability as a design requirement
Every verdict, score, and calculated figure must expose the reasoning behind it — this is a product requirement (SEBI non-advisory positioning depends on it), not just a nice-to-have. Composite scores, module weights, and the active rule that produced a verdict are never hidden behind a single number.

---

## 2. Design Tokens

### 2.1 Color System

```css
:root {
  /* Monochrome Base */
  --bg-primary: #0A0A0A;
  --bg-secondary: #141414;
  --bg-tertiary: #1F1F1F;

  --grey-100: #F5F5F5;
  --grey-300: #B3B3B3;
  --grey-500: #737373;
  --grey-700: #404040;
  --grey-900: #1A1A1A;

  --text-primary: #FFFFFF;
  --text-secondary: #A3A3A3;
  --text-tertiary: #6B6B6B;

  --border-subtle: rgba(255, 255, 255, 0.10);
  --border-active: rgba(255, 255, 255, 0.24);

  /* The only two reserved exception colors in the entire product */
  --signal-good: #EAB308;      /* Yellow — reserved exclusively for the HOLD verdict, nothing else */
  --signal-critical: #DC2626;  /* Red — reserved exclusively for Tier 1 governance/critical alerts, nothing else */
}
```

**Hard rule:** No color appears anywhere in the product other than these two, and each of those two never appears on anything except its named state. Module status labels, chart lines, buttons, links, tax/proceeds figures in the simulator — all grayscale. If a component seems to need a third color, solve it with grayscale weight/fill or spacing instead; that constraint is the point of this direction, not a limitation to design around.

### 2.2 Typography

| Role | Font Family | Weight | Notes |
|---|---|---|---|
| Wordmark / Display Headlines | Condensed grotesk (e.g. Archivo Black, Bebas Neue) | 800-900 | Used for "KAIROS" wordmark and hero headline only |
| Verdict Text | Same condensed display face | 800-900 | 72-96px at desktop width for the verdict label — dramatically larger than any other element on screen |
| Numeric & Prices | JetBrains Mono | 500-600 | All prices, scores, percentages, ratios — monospace is a legibility/tabular-alignment choice, not a terminal-aesthetic choice |
| Card Headers | Inter | 600 | Module titles, section headers |
| Body & Explanations | Inter | 300-400 | Deliberately light weight — the contrast between this and the heavy display weight is a primary hierarchy tool in a system without much color |
| Micro Labels | Inter | 500 | Uppercase badges, category tags, timestamps |

Generous negative space around the verdict box and section boundaries is required — minimalism needs real whitespace to read as intentional rather than sparse. Do not compress layout to fit more above the fold.

---

## 3. Navbar

- Wordmark far left, condensed display face, pure black background, 1px hairline border at the bottom only.
- Right side: horizon mode toggle (`SWING` / `COMPOUNDER`) as plain uppercase text with a small live indicator dot — not a rounded pill button.
- Free-tier quota indicator (e.g. `2/3 SCANS`) sits beside the mode toggle, same minimal text treatment.

---

## 4. Home Page

### 4.1 Hero Section
- Background: particle/grid background component, dimmed well below its demo default (~4-6% opacity) — the demo preset reads as an unfinished component-library showcase if left at full visibility.
- Headline: "Kairos. Know when to sell — before the market tells you." (or equivalent copy stating the actual product value, not just the brand name). Condensed display face, large, tight letter-spacing, white, centered.
- Subhead: one sentence, Inter light weight, muted grey, stating plainly what the diagnostic engine does — no marketing language.
- Search bar: monospace input, terminal-prompt-style placeholder (`Search NSE/BSE ticker...`), grayscale only.

### 4.2 Below the Fold (3-4 sections)
Show proof, not generic feature icons:
- **Proof 01:** Backtested drawdown reduction vs. buy-and-hold.
- **Proof 02:** A worked example of the conflict-resolution engine reconciling fundamentals vs. technicals.
- **Proof 03:** The SHA-256 deterministic-reproducibility mechanic, explained plainly.

Avoid generic "why choose us" icon-grid sections — every section should demonstrate something real about the engine, not describe it abstractly.

---

## 5. Verdict Severity System

Severity escalates through grayscale fill and weight. Exactly two reserved colors exist in the whole system, each mapped to exactly one state:

| Verdict | Treatment |
|---|---|
| `HOLD` | `--signal-good` yellow text/border, otherwise plain |
| `TIGHTEN_STOP` | White text, thin 1px `--grey-500` outline only, no fill — mildest concern, quietest treatment |
| `TRIM_25` | White text, `--grey-500` medium-grey fill block — visible step up from Tighten Stop |
| `TRIM_50` | White text, `--grey-900` near-black fill block, heavier font weight — clear step up from Trim 25% |
| `EXIT_FULLY` | White text on pure black fill, heaviest weight, widest letter-spacing — maximum grayscale severity |
| `TIER 1 CRITICAL` | White text on `--signal-critical` red fill — the **only** red in the entire product, deliberately breaking the pattern to register as a state outside normal severity |

This ordering is deliberate and must read as monotonically increasing severity through weight/fill alone. Never introduce a second color into this ladder.

Module status labels (`STRONG`/`WEAK`/`FAIR`/`POSITIVE`/`NEGATIVE`) stay grayscale only — `--signal-good` and `--signal-critical` are reserved exclusively for the top-level verdict, never extended down to module-level indicators.

---

## 6. Loading / Analysis State

On ticker submission, show a **single-stage-at-a-time editorial loading sequence** (not a console log):

Stages (frontend-timed for MVP; structure the component to swap to a real backend SSE stream later without rewriting — drive the UI off a `stage` state variable, not scattered timeouts):

```
[15%]  INITIALIZING           "Connecting to institutional telemetry feeds..."
[35%]  FETCHING_OHLCV         "Ingesting price series & computing Wilder ATR..."
[60%]  FETCHING_FUNDAMENTALS  "Analyzing balance sheet quality, ROCE & debt solvency..."
[80%]  SENTIMENT_ANALYSIS     "Scanning SEBI regulatory filings & NLP indicators..."
[92%]  RESOLVING_CONFLICTS    "Executing 2D Precedence Grid & asymmetric override rules..."
[100%] COMPLETE               → transitions to dashboard
```

- One stage shown at a time, large, centered, heavy weight — the current stage description is the only content on screen.
- Thin horizontal progress line (`--grey-700` track, white fill) beneath the text, advancing to match stage percentage.
- Crossfade transitions between stages — no typewriter/line-appearing effect.

**Backend note:** the real staged version requires a new `GET /api/v1/diagnostic/{symbol}/stream` (SSE or WebSocket) endpoint — the current TRD only defines a single-shot `GET /api/v1/diagnostic/{symbol}`. Track this as a Phase 2 backend addition; don't let frontend assume it already exists.

---

## 7. Dashboard Layout

### Zone 1 — Identity Strip (top, full width)
- Left: Ticker, company name, sector/industry pill, Beta, ISIN (small, muted).
- Right: LTP, live change %, day high/low.

### Zone 2 — Verdict Corner Box (top-right, large — roughly a quarter of viewport width, not a small badge)
Hard corners, 1px hairline border, no shadow. Contents top to bottom:
- Verdict label, per Section 5 treatment.
- Composite score (`63.4 / 100`), monospace, directly under the label — never omitted.
- Weights applied, one small monospace line (`FUND 45% · TECH 15% · QUANT 25% · NEWS 15%`).
- Active rule tag, small monospace pill (`RULE_1_COMPOUNDER_VOLATILITY_BUFFER`).
- Live monospace evaluation timestamp (`EVALUATED 15:45:02 IST`).
- Horizon toggle lives directly adjacent to this box, since it's the input driving everything inside it.
- Earnings-blackout badge (pre-earnings 48h window) and stale-data warning pill (`Cached Data — 15m delay`) attach here when active.

### Zone 3 — Stop-Loss Desk (left) + Risk/Reward & Sizing (right), side by side
- **Stop-Loss Desk:** calculated stop price, ATR(14) value, multiplier used (auto/manual indicator), distance-to-stop %, manual override control.
- **Risk/Reward:** target price with source badge (`ANALYST CONSENSUS` / `TECHNICAL FALLBACK` / `USER SET`), R:R ratio, Fractional Kelly trim %, custom target input.

### Zone 4 — Chandelier Chart
Full width. Candlesticks, 50/200 DMA, ratcheting Chandelier stop line, target line, timeframe switcher (`15m` / `1D` / `1W`). All lines grayscale except where a line directly represents the active verdict color (avoid this exception unless clearly justified — default to grayscale chart lines with labels).

### Zone 5 — 4-Module Diagnostic Grid (2x2, confirmed layout choice)
Hard corners, hairline borders, no icons, no drop shadows. Each box:
- Module label as small monospace header (`FUND`, `TECH`, `QUANT`, `NEWS`).
- Score as the dominant large monospace number — bigger than the label, this is where visual weight lives instead of card chrome.
- 3 driver metrics below in smaller monospace.
- Status word (`STRONG`/`WEAK`/`FAIR`/`POSITIVE`/`NEGATIVE`) per Section 5's grayscale-only rule.
- Expands inline on click into the deep-dive sub-metric table (5Y P/E median, FCF conversion, D/E ratio, etc., per the TRD's `explanation_trace` schema).

### Zone 6 — Execution Simulator ("What If I Trim Now?")
Buy price + quantity inputs, trim percentage slider/presets, instant tabular output (shares to sell/remaining, gross proceeds, realized profit, estimated tax, net cash, new breakeven, downside cushion expansion). All figures grayscale monospace — no amber/red accents on tax or proceeds lines; these are neutral information, not alerts, and must follow the same two-color-exception rule as everything else.

### Zone 7 — Regulatory Audit Footer (fixed, full width, bottom)
- SEBI non-advisory disclaimer text.
- SHA-256 audit hash, monospace, truncated with expand-on-click for the full hash.
- Must clear WCAG AA contrast (4.5:1) — use `--text-secondary`, not `--text-tertiary`, for this specific text.

### Conditional State — Tier 1 Governance Alert
When a hard-override trigger fires (auditor resignation, SEBI probe, promoter pledge >50%, circuit lock), this **replaces Zone 2 entirely** — the verdict box expands into the red critical state, forced `EXIT FULLY`, with a direct citation link to the triggering filing. Zones 3-6 remain visible but visually de-emphasized (reduced opacity) underneath it, since the override bypasses their scores entirely per the conflict-resolution engine. This is not a small banner added elsewhere on the page — the primary verdict area itself must communicate that normal scoring has been bypassed.

---

## 8. Responsive / Mobile Adaptation

- **Sticky verdict bar:** once the user scrolls past Zone 2, a fixed 48px bottom bar shows `TICKER • LTP • VERDICT (Stop: ₹X)`, following Section 5's grayscale/yellow/red treatment.
- **4-module grid → accordion:** the 2x2 grid collapses into swipeable single-column accordion rows on mobile, preserving the score-dominant typography.
- **Chart:** single-finger pan, pinch-to-zoom, long-press for crosshair inspection.
- **Loading sequence:** identical single-stage-at-a-time treatment, full width.

---

## 9. Accessibility (WCAG 2.1 AA)

- All body text must clear 4.5:1 contrast against `--bg-primary`. Verified: `--text-tertiary` (#6B6B6B) does **not** reliably clear this against pure black at small sizes — restrict `--text-tertiary` to large/bold text only, or promote disclaimer and other compliance-relevant text to `--text-secondary`.
- Every verdict state must be distinguishable without color — this is naturally satisfied by the weight/fill escalation system in Section 5, but confirm each state also carries a clear text label (never rely on fill/weight alone for a screen-reader user).
- Full keyboard navigation across search, horizon toggle, module accordions, and simulator inputs.

---

## 10. Open Items for Engineering
1. New SSE/WebSocket streaming endpoint for the loading sequence (Section 6) — needs to be added to TRD.md, not assumed to exist.
2. Confirm the `TargetSource` enum in the backend schema is corrected to match `ANALYST_CONSENSUS` / `TECHNICAL_FALLBACK` / `USER_CUSTOM` (a prior draft had a `HISTORICAL_PEG` value that doesn't correspond to any specified methodology).
3. Chart line coloring (Zone 4) defaults to grayscale — confirm with design whether any chart element should ever adopt the yellow/red verdict colors, or whether the chart stays fully monochrome regardless of verdict state.

---
*This document is the canonical UI/UX reference. Prior drafts (terminal/Bloomberg color scheme, green-signal variant, dual-red variant) are superseded.*