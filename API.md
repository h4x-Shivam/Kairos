# RESTful API & WebSocket Data Contracts — v1.0
# Project: "When to Sell" Engine (Kairos Quant)
**Document Status:** Approved Implementation Specification  
**Parent Documents:** [PRD.md](file:///d:/Kairos/PRD.md) • [TRD.md](file:///d:/Kairos/TRD.md) • [UI_UX.md](file:///d:/Kairos/UI_UX.md) • [APP_FLOW.md](file:///d:/Kairos/APP_FLOW.md) • [BACKEND_SCHEMA.md](file:///d:/Kairos/BACKEND_SCHEMA.md)  
**Protocol:** HTTPS / WSS • JSON API 1.0 • OpenAPI 3.1.0 Compliant

---

## 1. Global API Standards & Protocols

### 1.1 Base URLs
- **Production:** `https://api.kairosquant.com/api/v1`
- **Staging:** `https://staging-api.kairosquant.com/api/v1`
- **Local Development:** `http://localhost:8000/api/v1`

### 1.2 Authentication & Authorization
- **Anonymous / Free Tier:** No auth token required. Rate-limited and quota-gated by client IP and `X-Client-Fingerprint`.
- **Pro / Admin Tier:** Bearer JWT in the standard authorization header:
  `Authorization: Bearer <jwt_token>`

### 1.3 Standard Response Headers
All API responses include rate-limiting, daily quota, and audit headers:

```http
X-RateLimit-Limit: 10
X-RateLimit-Remaining: 9
X-RateLimit-Reset: 1723114800
X-Daily-Quota-Limit: 3
X-Daily-Quota-Remaining: 2
X-Daily-Quota-Reset: 2026-08-09T00:00:00+05:30
X-Audit-Hash: a4f89d38c642bf1c94afbf4c8996fb92427ae41e4649b934ca495991b7852c91
```

### 1.4 Unified Error Response Contract
All error responses adhere to a consistent error schema:

```json
{
  "status": "error",
  "error": {
    "code": "DAILY_QUOTA_EXCEEDED",
    "message": "Daily scan quota reached (3/3). Upgrade to Pro for unlimited diagnostics.",
    "details": {
      "quota_limit": 3,
      "quota_used": 3,
      "reset_at": "2026-08-09T00:00:00+05:30"
    }
  }
}
```

### 1.5 Standard HTTP Status Codes

| HTTP Status Code | Meaning & Trigger Scenario |
|---|---|
| `200 OK` | Request processed successfully; payload attached. |
| `400 Bad Request` | Malformed parameters (e.g. invalid timeframe, negative buy price). |
| `401 Unauthorized` | Missing or expired JWT on a protected endpoint. |
| `402 Payment Required` | Free-tier daily quota exhausted (3 scans/24h). Mounts Pro Upgrade modal. |
| `404 Not Found` | Symbol not found on NSE/BSE registry or delisted. |
| `422 Unprocessable Entity` | Pydantic validation failure on request body. |
| `429 Too Many Requests` | Burst rate limiter triggered ($> 10\text{ req/min}$). |
| `500 Internal Server Error` | Unexpected backend or database exception. |
| `503 Service Unavailable` | Upstream data provider timeout (Yahoo Finance / NSE feed). |

---

## 2. Stock Universe & Autocomplete Endpoints

### 2.1 Search & Autocomplete
`GET /stocks/search`

Provides low-latency ($< 30\text{ms}$) debounced search across NSE/BSE listed equities.

#### Query Parameters:
- `q` (string, required, min length: 1): Ticker prefix or company name (e.g., `TATA`, `RELI`).
- `limit` (integer, optional, default: `10`, max: `25`): Max records returned.

#### Response: `200 OK`
```json
{
  "status": "success",
  "data": {
    "query": "TATA",
    "results_count": 2,
    "items": [
      {
        "symbol": "TATAMOTORS.NS",
        "company_name": "Tata Motors Ltd",
        "isin": "INE155A01022",
        "exchange": "NSE",
        "sector": "Automobile",
        "industry": "Commercial & Passenger Vehicles",
        "market_cap_bucket": "LARGE_CAP",
        "market_cap_cr": 345000.00,
        "beta_1y": 1.12,
        "last_price": 942.50
      },
      {
        "symbol": "TATASTEEL.NS",
        "company_name": "Tata Steel Ltd",
        "isin": "INE081A01020",
        "exchange": "NSE",
        "sector": "Metals & Mining",
        "industry": "Steel Products",
        "market_cap_bucket": "LARGE_CAP",
        "market_cap_cr": 192000.00,
        "beta_1y": 1.34,
        "last_price": 154.20
      }
    ]
  }
}
```

---

## 3. Quant Diagnostic & Engine Endpoints

### 3.1 Evaluate Stock Diagnostic (Primary Engine)
`GET /diagnostic/{symbol}`

Calculates the complete 4-module diagnostic score, evaluates the 2D Precedence Grid and Conflict-Resolution state machine, and generates the deterministic SHA-256 audit fingerprint.

#### Path Parameters:
- `symbol` (string, required): NSE/BSE ticker symbol (e.g., `TATAMOTORS.NS`).

#### Query Parameters:
- `horizon_mode` (string, required): `SWING` | `COMPOUNDER`
- `manual_atr_mult` (float, optional): Manual ATR multiplier override ($1.00 \le k \le 4.00$).
- `custom_target_price` (float, optional): User-defined profit target price ($> \text{current\_price}$).

#### Response: `200 OK` (Canonical Worked Example: `TATAMOTORS.NS` under `COMPOUNDER`)
```json
{
  "status": "success",
  "data": {
    "symbol": "TATAMOTORS.NS",
    "company_name": "Tata Motors Ltd",
    "market_cap_bucket": "LARGE_CAP",
    "beta_1y": 1.12,
    "current_price": 942.50,
    "horizon_mode": "COMPOUNDER",
    "weights_applied": {
      "fund": 0.45,
      "tech": 0.15,
      "quant": 0.25,
      "news": 0.15
    },
    "verdict": {
      "primary_action": "TRIM_25",
      "display_label": "TRIM 25%",
      "badge_color": "#F59E0B",
      "headline": "Fundamental growth strong, but technical momentum waning. Lock partial profit (Trim 25%); maintain core position.",
      "active_override": "RULE_1_COMPOUNDER_VOLATILITY_BUFFER",
      "tier1_alert_active": false
    },
    "scores": {
      "composite": 70.3,
      "fundamental": 84.0,
      "technical": 38.0,
      "quant": 65.0,
      "news": 70.0
    },
    "risk_parameters": {
      "calculated_stop_loss": 885.00,
      "atr_14": 26.14,
      "atr_multiplier_used": 2.20,
      "is_manual_atr": false,
      "distance_to_stop_pct": -6.10,
      "target_price": 1080.00,
      "target_source": "ANALYST_CONSENSUS",
      "risk_reward_ratio": 2.39,
      "fractional_kelly_pct": 25.0
    },
    "explanation_trace": {
      "fundamental_drivers": [
        { "metric": "PEG Ratio", "value": 1.12, "signal": "FAVORABLE", "score": 85.0 },
        { "metric": "ROCE Trend", "value": "+3.2% QoQ", "signal": "EXPANDING", "score": 100.0 },
        { "metric": "Promoter Pledge", "value": "0.0%", "signal": "CLEAN", "score": 100.0 },
        { "metric": "FCF / Net Profit", "value": 0.88, "signal": "HIGH_QUALITY", "score": 90.0 },
        { "metric": "Debt-to-Equity", "value": 0.42, "signal": "MODERATE", "score": 75.0 }
      ],
      "technical_drivers": [
        { "metric": "50 DMA Proximity", "value": "Price < 50 DMA", "signal": "BREAKDOWN", "score": 25.0 },
        { "metric": "RSI(14)", "value": 41.2, "signal": "WEAK_BEARISH", "score": 35.0 },
        { "metric": "Delivery Volume %", "value": "34.2%", "signal": "BELOW_AVG", "score": 40.0 }
      ],
      "regulatory_and_news": [
        {
          "headline": "Tata Motors Q1 Net Profit rises 24% YoY",
          "filing_category": "EARNINGS",
          "finbert_sentiment": "POSITIVE",
          "sentiment_score": 0.84,
          "source": "NSE",
          "published_at": "2026-08-06T14:30:00+05:30"
        }
      ]
    },
    "audit_metadata": {
      "evaluated_at": "2026-08-08T07:20:00.000Z",
      "data_source": "NSE_REALTIME_COMPLIANT_FEED",
      "audit_hash": "a4f89d38c642bf1c94afbf4c8996fb92427ae41e4649b934ca495991b7852c91"
    }
  }
}
```

---

### 3.2 "What If I Trim Now?" Execution Simulator
`POST /diagnostic/{symbol}/simulate-trim`

Executes real-time mathematical simulation of partial profit locking, Indian equity tax deduction (STCG 20% vs LTCG 12.5%), and downside cushion expansion on retained shares.

#### Request Body:
```json
{
  "buy_price": 780.00,
  "shares_held": 100,
  "trim_pct": 25.0,
  "holding_period_months": 8
}
```

#### Response: `200 OK`
```json
{
  "status": "success",
  "data": {
    "symbol": "TATAMOTORS.NS",
    "current_price": 942.50,
    "shares_to_sell": 25,
    "shares_retained": 75,
    "gross_cash_realized": 23562.50,
    "realized_capital_gain": 4062.50,
    "tax_regime": "STCG_EQUITY_20_PCT",
    "applicable_tax_rate_pct": 20.0,
    "estimated_tax_deduction": 812.50,
    "net_cash_added": 22750.00,
    "original_breakeven": 780.00,
    "new_effective_breakeven": 725.83,
    "downside_cushion_expansion_pct": 6.94,
    "cushion_interpretation": "Breakeven drops from ₹780.00 to ₹725.83. The remaining 75 shares can now withstand an additional 6.94% drop before entering capital loss."
  }
}
```

---

## 4. Interactive Candlestick & Chandelier Chart Endpoints

### 4.1 Get Chandelier Chart Series
`GET /charts/{symbol}/chandelier`

Retrieves historical OHLCV series and the ratcheting Chandelier trailing-stop floor line.

#### Query Parameters:
- `timeframe` (string, optional, default: `1d`): `15m` | `1d` | `1w`
- `lookback_bars` (integer, optional, default: `200`, max: `500`): Number of historical bars.
- `horizon_mode` (string, optional, default: `COMPOUNDER`): `SWING` | `COMPOUNDER`
- `manual_atr_mult` (float, optional): Multiplier override.

#### Response: `200 OK`
```json
{
  "status": "success",
  "data": {
    "symbol": "TATAMOTORS.NS",
    "timeframe": "1d",
    "atr_multiplier_used": 2.20,
    "series": [
      {
        "time": 1722816000,
        "open": 930.00,
        "high": 950.00,
        "low": 925.00,
        "close": 942.50,
        "volume": 8420000,
        "sma_50": 965.20,
        "sma_200": 890.10,
        "chandelier_stop": 885.00
      }
    ],
    "telemetry": {
      "current_price": 942.50,
      "current_stop": 885.00,
      "current_cushion_pct": -6.10,
      "distance_to_target_pct": 14.59,
      "risk_reward_ratio": 2.39
    }
  }
}
```

---

## 5. User Portfolio & Watchlist Endpoints

### 5.1 Get User Watchlist
`GET /user/watchlist`  
*(Requires `Authorization: Bearer <jwt_token>`)*

#### Response: `200 OK`
```json
{
  "status": "success",
  "data": {
    "items": [
      {
        "id": "7c9e6679-7425-40de-944b-e07fc1f90ae7",
        "symbol": "TATAMOTORS.NS",
        "company_name": "Tata Motors Ltd",
        "buy_price": 780.00,
        "shares_held": 100,
        "preferred_horizon": "COMPOUNDER",
        "latest_verdict": "TRIM_25",
        "calculated_stop": 885.00,
        "cushion_to_stop_pct": -6.10,
        "unrealized_pnl_pct": 20.83
      }
    ]
  }
}
```

### 5.2 Add Stock to Watchlist
`POST /user/watchlist`  
*(Requires `Authorization: Bearer <jwt_token>`)*

#### Request Body:
```json
{
  "symbol": "TATAMOTORS.NS",
  "buy_price": 780.00,
  "shares_held": 100,
  "preferred_horizon": "COMPOUNDER"
}
```

#### Response: `201 Created`
```json
{
  "status": "success",
  "data": {
    "message": "Stock added to portfolio watchlist successfully.",
    "id": "7c9e6679-7425-40de-944b-e07fc1f90ae7"
  }
}
```

---

## 6. Monetization & Razorpay Webhooks

### 6.1 Create Pro Subscription Order
`POST /payments/create-subscription`  
*(Requires `Authorization: Bearer <jwt_token>`)*

#### Request Body:
```json
{
  "plan": "MONTHLY"
}
```

#### Response: `200 OK`
```json
{
  "status": "success",
  "data": {
    "subscription_id": "sub_Nx87sdflkjasdf",
    "razorpay_key_id": "rzp_live_xxxxxxxxxx",
    "amount_paise": 79900,
    "currency": "INR",
    "plan_name": "Kairos Quant Pro (Monthly)"
  }
}
```

### 6.2 Razorpay Webhook Ingestion
`POST /payments/webhook`

Validates the `X-Razorpay-Signature` HMAC SHA-256 header and elevates user role to `PRO` in PostgreSQL and Redis.

#### Webhook Events Handled:
- `subscription.authenticated`
- `subscription.activated`
- `subscription.charged`
- `subscription.cancelled`
- `payment.failed`

#### Response: `200 OK`
```json
{
  "status": "success",
  "message": "Webhook processed successfully."
}
```

---

## 7. WebSocket Real-Time Diagnostic Feed

### 7.1 Real-Time Ticker & Trailing-Stop Socket
`WS /ws/diagnostic/{symbol}?token={jwt_or_guest_id}`

Streams live Last Traded Price (LTP) ticks, dynamically recomputing the distance-to-stop floor in real time.

#### Incoming Message (Client Ping):
```json
{ "action": "ping" }
```

#### Outgoing Server Stream (On Price Tick):
```json
{
  "event": "TICK_UPDATE",
  "symbol": "TATAMOTORS.NS",
  "ltp": 942.80,
  "chandelier_stop": 885.00,
  "cushion_pct": -6.13,
  "stop_breached": false,
  "timestamp": 1723114805
}
```

---
*Ready for frontend and backend API integration.*
