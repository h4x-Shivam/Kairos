"""Pillar D: Time-decayed regulatory and FinBERT sentiment scoring module ($S_{news}$)."""
import math
from typing import List
from app.schemas.diagnostic import SentimentDisclosureInput


def compute_sentiment_score(disclosures: List[SentimentDisclosureInput]) -> float:
    r"""Compute normalized composite Regulatory & Sentiment Score ($S_{news} \in [0, 100]$).
    
    Formula:
        S_news = 50 + 50 * (sum(w_i * score_i) / sum(w_i))
        where w_i = exp(- hours_ago / 72)
    """
    if not disclosures:
        return 50.0
        
    weighted_sum = 0.0
    weight_total = 0.0
    
    for item in disclosures:
        # Exponential time-decay with 72-hour half-life factor
        w_i = math.exp(-max(0.0, item.hours_ago) / 72.0)
        # Clamped sentiment score between -1.0 and +1.0
        score_i = max(-1.0, min(1.0, item.sentiment_score))
        
        weighted_sum += w_i * score_i
        weight_total += w_i
        
    if weight_total <= 0.0:
        return 50.0
        
    normalized_sentiment = weighted_sum / weight_total
    final_score = 50.0 + (50.0 * normalized_sentiment)
    clamped_score = max(0.0, min(100.0, final_score))
    
    return round(float(clamped_score), 1)


def check_tier1_trigger_active(disclosures: List[SentimentDisclosureInput]) -> bool:
    """Check if any active Tier-1 governance bypass trigger occurred in the past 7 days."""
    for item in disclosures:
        if item.is_tier1_trigger and item.hours_ago <= 168.0: # 7 days
            return True
    return False
