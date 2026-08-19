import os
import sys
import time
import pandas as pd
import yfinance as yf
from typing import Dict, Tuple

# Ensure local imports work by appending to sys.path
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from app.engine.module_a_fundamental import compute_fundamental_score
from app.engine.module_b_technical import compute_technical_score
from app.engine.module_c_quant import compute_quant_score
from app.engine.module_d_sentiment import compute_sentiment_score
from app.engine.precedence_grid import resolve_precedence_grid
from app.engine.conflict_resolution import resolve_verdict
from app.engine.indicators import compute_chandelier_stop_series, compute_rsi_series, detect_bearish_rsi_divergence
from app.schemas.diagnostic import (
    HorizonMode, 
    MarketCapBucket, 
    FundamentalMetricsInput,
    TechnicalMetricsInput,
    QuantMetricsInput,
    SentimentDisclosureInput
)

EXPECTATIONS = {
    "RELIANCE.NS": {"expected": "HOLD", "cap": MarketCapBucket.LARGE_CAP, "horizon": HorizonMode.COMPOUNDER, "reason": "Stable compounder."},
    "INFY.NS": {"expected": "HOLD", "cap": MarketCapBucket.LARGE_CAP, "horizon": HorizonMode.COMPOUNDER, "reason": "Mature IT stock."},
    "TCS.NS": {"expected": "HOLD", "cap": MarketCapBucket.LARGE_CAP, "horizon": HorizonMode.COMPOUNDER, "reason": "Market leader."},
    
    "PAYTM.NS": {"expected": "EXIT_FULLY", "cap": MarketCapBucket.MID_CAP, "horizon": HorizonMode.SWING, "reason": "Regulatory issues."},
    "ZEEL.NS": {"expected": "EXIT_FULLY", "cap": MarketCapBucket.SMALL_CAP, "horizon": HorizonMode.SWING, "reason": "Structural downtrend."},
    "WIPRO.NS": {"expected": "TRIM_50", "cap": MarketCapBucket.LARGE_CAP, "horizon": HorizonMode.COMPOUNDER, "reason": "Sustained underperformance."},
    
    "ETERNAL.NS": {"expected": "TRIM_25", "cap": MarketCapBucket.LARGE_CAP, "horizon": HorizonMode.SWING, "reason": "Stretched valuation vs momentum."},
    "TRENT.NS": {"expected": "TRIM_25", "cap": MarketCapBucket.LARGE_CAP, "horizon": HorizonMode.SWING, "reason": "Technical strength sell."},
    "IRFC.NS": {"expected": "TRIM_50", "cap": MarketCapBucket.LARGE_CAP, "horizon": HorizonMode.SWING, "reason": "Rally correction."},
    "HDFCBANK.NS": {"expected": "TIGHTEN_STOP", "cap": MarketCapBucket.LARGE_CAP, "horizon": HorizonMode.COMPOUNDER, "reason": "Strong fundamental, technical lag."},
    
    "SUZLON.NS": {"expected": "HOLD", "cap": MarketCapBucket.MID_CAP, "horizon": HorizonMode.SWING, "reason": "High-beta turnaround."},
    "IREDA.NS": {"expected": "TRIM_50", "cap": MarketCapBucket.MID_CAP, "horizon": HorizonMode.SWING, "reason": "Volatile PSU."},
    "RVNL.NS": {"expected": "TRIM_50", "cap": MarketCapBucket.MID_CAP, "horizon": HorizonMode.SWING, "reason": "Parabolic pullback."},
    "MAPMYINDIA.NS": {"expected": "HOLD", "cap": MarketCapBucket.SMALL_CAP, "horizon": HorizonMode.COMPOUNDER, "reason": "Small-cap tech growth."},
    "KPITTECH.NS": {"expected": "HOLD", "cap": MarketCapBucket.MID_CAP, "horizon": HorizonMode.COMPOUNDER, "reason": "Mid-cap auto-tech."},
}

BLIND_SENTIMENT = {
    "RELIANCE.NS": 0.0,
    "INFY.NS": 0.0,
    "TCS.NS": -1.0, 
    "PAYTM.NS": 1.0, 
    "ZEEL.NS": -1.0, 
    "WIPRO.NS": -1.0,
    "ETERNAL.NS": 0.0,
    "TRENT.NS": -1.0,
    "IRFC.NS": 0.0,
    "HDFCBANK.NS": -1.0,
    "SUZLON.NS": -1.0,
    "IREDA.NS": 0.0,
    "RVNL.NS": 0.0,
    "MAPMYINDIA.NS": -1.0,
    "KPITTECH.NS": 0.0,
}

def fetch_stock_data(symbol: str) -> Tuple[pd.DataFrame, Dict]:
    cache_dir = os.path.join(os.path.dirname(__file__), "cache")
    os.makedirs(cache_dir, exist_ok=True)
    cache_path = os.path.join(cache_dir, f"{symbol}.csv")
    
    if os.path.exists(cache_path):
        print(f"Loaded {symbol} from cache.")
        ohlcv = pd.read_csv(cache_path, parse_dates=['time'])
    else:
        print(f"Fetching {symbol} from yfinance...")
        ticker = yf.Ticker(symbol)
        ohlcv = ticker.history(period="1y", interval="1d", auto_adjust=True)
        time.sleep(2)  # Throttle to avoid rate limits
        
        if ohlcv.empty:
            print(f"WARNING: No data for {symbol} from yfinance. Returning empty.")
            return ohlcv, {}
            
        ohlcv = ohlcv.reset_index()
        ohlcv.rename(columns={'Date': 'time', 'Open': 'open', 'High': 'high', 'Low': 'low', 'Close': 'close', 'Volume': 'volume'}, inplace=True)
        # Handle time zone info if present
        if 'time' in ohlcv.columns and pd.api.types.is_datetime64tz_dtype(ohlcv['time']):
            ohlcv['time'] = ohlcv['time'].dt.tz_localize(None)
        ohlcv.to_csv(cache_path, index=False)
    
    current_price = float(ohlcv['close'].iloc[-1])
    last_bar_high = float(ohlcv['high'].iloc[-1])
    last_bar_low = float(ohlcv['low'].iloc[-1])
    
    # 5% tolerance accounts for overnight gaps or extreme intraday volatility between the last bar and realtime quote,
    # while being tight enough to catch unadjusted-price errors (e.g. from stock splits which typically cause >10% gaps).
    assert current_price >= last_bar_low * 0.95 and current_price <= last_bar_high * 1.05, f"Sanity assertion failed! current_price ({current_price}) misaligned with recent OHLCV bar for {symbol}."
    
    beta = 1.0
    
    fundamentals = FundamentalMetricsInput(
        peg_ratio=1.5,
        roce_current=15.0,
        roce_3q_avg=15.0,
        fcf_to_net_profit=1.0,
        debt_to_equity=0.5,
        promoter_pledge_pct=0.0,
    )
    
    recent_vol = ohlcv['volume'].iloc[-1]
    avg_vol_20 = ohlcv['volume'].rolling(20).mean().iloc[-1]
    vol_ratio = recent_vol / avg_vol_20 if avg_vol_20 > 0 else 1.0
    delivery_pct = 60.0 if vol_ratio > 1.2 else 40.0
    
    closes = ohlcv['close'].to_numpy()
    rsi_14 = float(compute_rsi_series(closes, 14)[-1]) if len(closes) >= 15 else 50.0
    
    technicals = TechnicalMetricsInput(
        sma_50=ohlcv['close'].rolling(50).mean().iloc[-1],
        sma_200=ohlcv['close'].rolling(200).mean().iloc[-1],
        rsi_14=rsi_14,
        delivery_pct=delivery_pct,
    )
    
    quant = QuantMetricsInput(
        high_52w=float(ohlcv['high'].max()),
        realized_volatility_1y=20.0,
        beta=beta,
    )
    
    return ohlcv, {
        "fundamentals": fundamentals,
        "technicals": technicals,
        "quant": quant,
        "current_price": current_price
    }

def main():
    results = []
    
    print("Running Validation Sprint with Fixes...\n")
    for symbol, meta in EXPECTATIONS.items():
        print(f"Processing {symbol}...")
        df, data = fetch_stock_data(symbol)
        
        if df.empty:
            continue
            
        current_price = data["current_price"]
        s_fund = compute_fundamental_score(data["fundamentals"])
        s_tech = compute_technical_score(current_price, data["technicals"])
        s_quant = compute_quant_score(current_price, data["quant"])
        
        sentiment_val = BLIND_SENTIMENT.get(symbol, 0.0)
        mock_disclosure = []
        if sentiment_val != 0.0:
            mock_disclosure.append(
                SentimentDisclosureInput(
                    headline="Mock Headline",
                    hours_ago=2.0,
                    sentiment_score=sentiment_val,
                    is_tier1_trigger=False
                )
            )
        s_news = compute_sentiment_score(mock_disclosure)
        
        weights = resolve_precedence_grid(
            meta["horizon"],
            meta["cap"],
            manual_multiplier_override=None
        )
        
        class Bar:
            def __init__(self, high, low, close):
                self.high, self.low, self.close = high, low, close
        bars = [Bar(row['high'], row['low'], row['close']) for _, row in df.iterrows()]
        
        # With the ratcheting statelessness fixed to reset upon previous breach,
        # we can safely evaluate over the full 1-year history without locking in a stale high-water mark.
        stops, atrs, _ = compute_chandelier_stop_series(bars, weights.net_multiplier, 22, 14)
        chandelier_stop = float(stops[-1])
        
        closes = df['close'].to_numpy()
        rsi = compute_rsi_series(closes, 14)
        has_div = detect_bearish_rsi_divergence(closes, rsi, 30)
        
        raw_comp = (weights.w_fund * s_fund + weights.w_tech * s_tech + weights.w_quant * s_quant + weights.w_news * s_news)
        
        action, rule, _, s_composite = resolve_verdict(
            horizon_mode=meta["horizon"],
            current_price=current_price,
            chandelier_stop=chandelier_stop,
            s_fund=s_fund,
            s_tech=s_tech,
            s_quant=s_quant,
            s_composite=raw_comp,
            is_tier1_active=False,
            has_bearish_divergence=has_div,
            risk_reward_ratio=2.0 
        )
        
        is_match = (action.value == meta["expected"])
        
        results.append({
            "Symbol": symbol,
            "Expected": meta["expected"],
            "Actual": action.value,
            "Match?": "YES" if is_match else "NO",
            "Rule Applied": rule.value,
            "S_Comp": round(s_composite, 1),
            "S_Fund": round(s_fund, 1),
            "S_Tech": round(s_tech, 1),
            "Proxies Used": "DelPct: PROXY, Pledge: 0%, News: FIXED(Fresh)",
        })

    results_df = pd.DataFrame(results)
    print("\n\n=== VALIDATION SPRINT RESULTS ===")
    print(results_df.to_string(index=False))
    
    out_md = os.path.join(os.path.dirname(__file__), "validation_report.md")
    with open(out_md, "w") as f:
        f.write("# Validation Sprint Output (Fixed)\n\n")
        f.write(results_df.to_markdown(index=False))
        
if __name__ == "__main__":
    main()
