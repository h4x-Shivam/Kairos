"""Plain-language template generation for diagnostic verdicts and pillars."""
from typing import List
from app.schemas.diagnostic import SentimentDisclosureInput


def generate_plain_summary(verdict: str, s_fund: float, s_tech: float, s_quant: float, s_news: float, active_rule: str, symbol: str) -> str:
    """Returns a deterministic 2-3 sentence plain-language summary."""
    fund_phrase = "the company's financials look solid" if s_fund >= 70 else \
                  "there are some concerns in the company's financial health" if s_fund >= 45 else \
                  "the company's financials are showing real weakness"

    tech_phrase = "the stock's price trend is strong" if s_tech >= 70 else \
                  "the price trend has been mixed lately" if s_tech >= 45 else \
                  "the price has been breaking down"

    quant_phrase = "volatility is well-controlled" if s_quant >= 70 else \
                   "price swings are currently manageable" if s_quant >= 45 else \
                   "the stock is experiencing heavy price turbulence"

    if active_rule == "TIER_1_HARD_GOVERNANCE_BYPASS":
        return f"A severe governance red flag has been triggered for {symbol}. When critical events like auditor resignations or defaults occur, we immediately prioritize protecting your capital and advise a full exit, regardless of how strong the fundamentals or price trends might look."
    
    if verdict == "TRIM_50" and active_rule == "RULE_2A_STOP_BREACH_COMPOUNDER":
        return (
            f"{symbol}'s price just fell through its safety floor, which is why we're "
            f"suggesting you lock in half your position now. The good news: {fund_phrase}, "
            f"so this isn't a sign to panic — it's a sign to protect some of your gains "
            f"while staying invested in the rest."
        )
        
    if verdict == "EXIT_FULLY" and active_rule == "RULE_2B_STOP_BREACH_SWING":
        return f"{symbol}'s price has breached our trailing stop-loss, our line in the sand for this swing trade. Since {tech_phrase}, our downside protection rules recommend a full exit to preserve your capital for better opportunities."
        
    if verdict == "EXIT_FULLY" and active_rule == "RULE_4_DOUBLE_STRUCTURAL_BREAKDOWN":
        return f"We are seeing a double structural breakdown in {symbol}. Because {fund_phrase} and {tech_phrase}, holding onto this stock carries significant risk. A complete exit is recommended to avoid further downside."

    if verdict == "TRIM_50" and active_rule == "RULE_3_SELL_INTO_STRENGTH":
        return f"While {tech_phrase} right now, {fund_phrase} underneath. This creates a good opportunity to lock in profits by trimming half your position into the current technical strength, reducing your exposure to the deteriorating fundamentals."

    if verdict == "TRIM_25" and active_rule == "RULE_1_COMPOUNDER_VOLATILITY_BUFFER":
        return f"As a core compounder, {symbol} remains a high-conviction hold because {fund_phrase}. However, {tech_phrase}, so we suggest trimming 25% of your position to lock in some partial profit while holding the core intact."

    if verdict == "TRIM_25" and active_rule == "RULE_5_MOMENTUM_EXHAUSTION_DIVERGENCE":
        return f"The buying momentum in {symbol} seems to be exhausting, and the current risk-reward ratio is unfavorable. While {fund_phrase}, we recommend trimming 25% of your position to secure gains before a potential pullback."

    # Baseline scoring (No Overrides Fired)
    if verdict == "HOLD":
        return f"The thesis for {symbol} is playing out as planned: {fund_phrase}, and {tech_phrase}. With all indicators looking robust, the best action right now is to simply hold your position."
    elif verdict == "TIGHTEN_STOP":
        return f"We're seeing a slight deceleration in {symbol}'s momentum or valuation, though {fund_phrase}. It's still a hold, but we recommend tightening your stop-loss floor to protect your accumulated gains."
    elif verdict == "TRIM_25":
        return f"We are noticing a moderate degradation in {symbol}'s overall profile. Since {tech_phrase} and {fund_phrase}, trimming 25% of your holding is a prudent move to protect your profits."
    elif verdict == "TRIM_50":
        return f"There has been significant deterioration in {symbol}'s metrics, and {quant_phrase}. To manage the growing downside risk, we recommend trimming half of your holding."
    else: # EXIT_FULLY fallback
        return f"{symbol} is showing a severe algorithmic breakdown across multiple pillars. Because {fund_phrase} and {tech_phrase}, we strongly command a complete exit to protect your portfolio from further damage."


def explain_fundamental_pillar(roce_trend: float, peg_ratio: float | None, pledge_pct: float, debt_equity: float, fcf_conversion: float) -> str:
    sentences = []

    if pledge_pct == 0.0:
        sentences.append("The promoters haven't pledged any of their shares, which is a strong sign of management confidence.")
    elif pledge_pct > 15.0:
        sentences.append(f"Promoters have pledged {pledge_pct}% of their shares, which introduces potential liquidity risks if the stock faces pressure.")

    if debt_equity > 2.0:
        sentences.append(
            f"The company carries a high level of debt relative to its equity "
            f"(₹{debt_equity} owed for every ₹1 of equity) — worth watching, since heavily "
            f"indebted companies are more exposed if conditions get harder."
        )
    elif debt_equity < 1.0:
        sentences.append("Debt levels are comfortably low relative to the size of the business, indicating solid solvency.")

    if peg_ratio is None:
        sentences.append("We couldn't reliably calculate one valuation metric this time, so we adjusted the score to rely more on the ones we could.")
    elif peg_ratio > 2.0:
        sentences.append("The stock's valuation is quite high compared to its expected earnings growth, meaning it's priced for perfection.")

    if not sentences:
        sentences.append("The company's core accounting metrics are largely stable with no immediate red flags.")

    return " ".join(sentences)


def explain_technical_pillar(sma_50: float, sma_200: float, rsi_14: float, delivery_pct: float) -> str:
    sentences = []

    if sma_50 > sma_200:
        sentences.append("The stock is in a clear long-term uptrend, with shorter-term momentum supporting the rise.")
    else:
        sentences.append("The stock has fallen below its long-term average, suggesting a bearish trend has taken hold.")

    if rsi_14 > 70.0:
        sentences.append("Recent buying has been intense, pushing the stock into 'overbought' territory where pullbacks are common.")
    elif rsi_14 < 30.0:
        sentences.append("Selling pressure has been heavy, making the stock 'oversold' and potentially due for a bounce.")

    if delivery_pct > 60.0:
        sentences.append(f"A high {delivery_pct}% of recent trades resulted in actual stock delivery, showing real conviction from buyers rather than just day-trading speculation.")
    elif delivery_pct < 30.0:
        sentences.append(f"Only {delivery_pct}% of recent volume was taken for delivery, suggesting a lot of the current price action is driven by short-term speculators.")

    return " ".join(sentences)


def explain_quant_pillar(high_52w: float, beta: float, realized_volatility: float, cushion_pct: float) -> str:
    sentences = []

    if beta > 1.5:
        sentences.append(f"This stock is highly sensitive to the broader market, typically moving {beta}x as much as the index — expect a bumpy ride.")
    elif beta < 0.8:
        sentences.append("This stock tends to be less volatile than the overall market, offering a relatively smoother ride.")

    if realized_volatility > 40.0:
        sentences.append("Price swings have been aggressive over the last year, which is why our stop-loss sizing gives it a wider berth.")
    else:
        sentences.append("The stock's recent volatility has been quite stable, allowing for a tighter, more precise safety net.")

    sentences.append(f"The trailing stop is currently set {cushion_pct:.1f}% below the current price to give the trend room to breathe while guarding against sudden drops.")

    return " ".join(sentences)


def explain_news_pillar(is_tier1_active: bool, disclosures: List[SentimentDisclosureInput]) -> str:
    if is_tier1_active:
        return "A critical regulatory red flag (such as an auditor resignation or debt default) was recently filed, which requires immediate attention and overrides standard scoring."

    if not disclosures:
        return "There hasn't been any fresh news or regulatory filings in the past week. We're relying entirely on the price and financials since there's nothing recent to go on."

    avg_sentiment = sum(d.sentiment_score for d in disclosures) / len(disclosures)
    if avg_sentiment > 0.2:
        return f"We've picked up {len(disclosures)} recent announcements, and the language used in them is largely positive and optimistic about the company's trajectory."
    elif avg_sentiment < -0.2:
        return f"The company has filed {len(disclosures)} recent updates, and our language model detected a distinctly cautious or negative tone in them."
    else:
        return f"There are {len(disclosures)} recent filings, but the language in them is neutral and routine, without strong positive or negative signals."
