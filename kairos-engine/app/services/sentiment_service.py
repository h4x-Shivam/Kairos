"""Financial sentiment classification and Tier-1 governance trigger analyzer."""
import re
from typing import List, Tuple
from app.schemas.diagnostic import SentimentDisclosureInput

# Tier-1 Governance Red Flags triggering immediate emergency capital preservation
_TIER_1_TRIGGERS = [
    r"\bauditor\b.*\bresign",
    r"\bresign(s|ed|ation)?\b.*\b(statutory )?auditor\b",
    r"\bsebi\b.*\b(probe|order|show cause|investigation|ban)",
    r"\bforensic audit\b",
    r"\bsearch and seizure\b",
    r"\benforcement directorate\b|\bed raid\b",
    r"\bdefault(s|ed)?\b.*\b(debt|interest|repayment|ncd|bonds|loan|principal)\b",
    r"\bfraud\b|\bfinancial irregularity\b|\baccounting fraud\b",
]

# Domain Financial Lexicon Scoring Weights
_POSITIVE_PATTERNS = [
    (r"\brecord\b.*\b(profit|revenue|margin|ebitda|pat)\b", 0.85),
    (r"\bdebt[- ]free\b|\bdeleveraging\b|\bprepayment of debt\b", 0.80),
    (r"\bdividend\b.*\b(surge|hike|record|special)\b", 0.70),
    (r"\bbuyback\b|\bshare repurchase\b", 0.75),
    (r"\border win\b|\bmajor contract\b|\blargest order\b", 0.75),
    (r"\bbeat(s|ing)? estimates\b|\boutperformed\b", 0.65),
    (r"\bcapacity expansion\b|\bnew plant\b|\bcommissioning\b", 0.60),
    (r"\bupgrade(d)?\b|\btarget raised\b", 0.60),
]

_NEGATIVE_PATTERNS = [
    (r"\bauditor\b.*\bresign", -1.0),
    (r"\bsebi\b.*\b(probe|investigation|order)\b", -1.0),
    (r"\bdefault\b|\binsolvency\b|\bnclt\b", -0.95),
    (r"\bprofit falls\b|\bnet loss\b|\blosses widen\b", -0.80),
    (r"\bmargin compression\b|\bmargin drop\b|\bebitda drop\b", -0.65),
    (r"\bmiss(es|ed)? estimates\b|\bdisappointing\b", -0.60),
    (r"\bdowngrade(d)?\b|\btarget cut\b", -0.65),
    (r"\bpromoter\b.*\b(pledge increases|stake sale)\b", -0.70),
    (r"\bpenalty\b|\bfine imposed\b|\btax demand\b", -0.50),
]


class SentimentService:
    """Financial NLP sentiment analyzer and regulatory filing classifier."""
    
    def analyze_headline(self, headline: str) -> Tuple[float, bool]:
        """Analyze a single corporate headline.
        
        Returns:
            (sentiment_score: float [-1.0, 1.0], is_tier1_trigger: bool)
        """
        text = headline.lower()
        
        # 1. Check Tier-1 Governance Bypass
        is_tier1 = False
        for pattern in _TIER_1_TRIGGERS:
            if re.search(pattern, text):
                is_tier1 = True
                return (-1.0, True)
                
        # 2. Score Sentiment
        score = 0.0
        matches = 0
        
        for pattern, weight in _NEGATIVE_PATTERNS:
            if re.search(pattern, text):
                score += weight
                matches += 1
                
        for pattern, weight in _POSITIVE_PATTERNS:
            if re.search(pattern, text):
                score += weight
                matches += 1
                
        if matches > 0:
            avg_score = score / matches
            return (round(max(-1.0, min(1.0, avg_score)), 2), is_tier1)
            
        return (0.0, False)
        
    def enrich_disclosures(
        self, raw_disclosures: List[SentimentDisclosureInput]
    ) -> List[SentimentDisclosureInput]:
        """Enrich a list of disclosures with calibrated sentiment scores and Tier-1 flags."""
        enriched: List[SentimentDisclosureInput] = []
        for item in raw_disclosures:
            score, is_tier1 = self.analyze_headline(item.headline)
            # If item already had a manual score, blend with NLP score
            final_score = score if item.sentiment_score == 0.0 else item.sentiment_score
            enriched.append(
                SentimentDisclosureInput(
                    headline=item.headline,
                    hours_ago=item.hours_ago,
                    sentiment_score=final_score,
                    is_tier1_trigger=is_tier1 or item.is_tier1_trigger,
                )
            )
        return enriched


sentiment_service = SentimentService()
