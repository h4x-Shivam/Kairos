"""Unit tests for SentimentService & Tier-1 trigger classifier."""
from app.services.sentiment_service import sentiment_service
from app.schemas.diagnostic import SentimentDisclosureInput


def test_tier1_triggers_detection():
    """Verify Tier-1 triggers fire immediately for auditor resignation and SEBI probes."""
    score1, is_t1_1 = sentiment_service.analyze_headline("Deloitte resigns as statutory auditor of company")
    assert is_t1_1 is True
    assert score1 == -1.0
    
    score2, is_t1_2 = sentiment_service.analyze_headline("SEBI launches forensic probe into accounting irregularities")
    assert is_t1_2 is True
    assert score2 == -1.0
    
    score3, is_t1_3 = sentiment_service.analyze_headline("Company defaults on NCD interest repayment")
    assert is_t1_3 is True
    assert score3 == -1.0


def test_positive_and_negative_sentiment_scoring():
    """Verify calibrated financial sentiment scores."""
    # Positive
    pos_score, pos_t1 = sentiment_service.analyze_headline("Company posts record profit and announces debt-free status")
    assert pos_t1 is False
    assert pos_score >= 0.70
    
    # Negative
    neg_score, neg_t1 = sentiment_service.analyze_headline("EBITDA margin compression as net profit falls 40%")
    assert neg_t1 is False
    assert neg_score <= -0.60
    
    # Neutral
    neutral_score, neutral_t1 = sentiment_service.analyze_headline("Board meeting scheduled for next Thursday")
    assert neutral_t1 is False
    assert neutral_score == 0.0


def test_enrich_disclosures():
    """Verify list enrichment with NLP scores."""
    raw = [
        SentimentDisclosureInput(
            headline="Board approves share buyback at 20% premium",
            hours_ago=5.0,
            sentiment_score=0.0,
            is_tier1_trigger=False,
        ),
        SentimentDisclosureInput(
            headline="Auditor resigns citing scope limitation",
            hours_ago=2.0,
            sentiment_score=0.0,
            is_tier1_trigger=False,
        ),
    ]
    enriched = sentiment_service.enrich_disclosures(raw)
    assert len(enriched) == 2
    assert enriched[0].sentiment_score >= 0.70
    assert enriched[1].is_tier1_trigger is True
    assert enriched[1].sentiment_score == -1.0
