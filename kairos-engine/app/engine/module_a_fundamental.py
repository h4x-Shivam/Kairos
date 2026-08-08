"""Pillar A: Fundamental accounting and valuation scoring module ($S_{fund}$)."""
from app.schemas.diagnostic import FundamentalMetricsInput


def score_peg(peg: float | None) -> float:
    """Score PEG ratio."""
    if peg is None:
        return 50.0
    if peg <= 0:
        return 10.0
    if peg <= 1.0:
        return 100.0
    if peg <= 1.5:
        return 80.0
    if peg <= 2.0:
        return 60.0
    if peg <= 2.5:
        return 40.0
    return 20.0


def score_roce_trend(roce_current: float, roce_3q_avg: float) -> float:
    """Score ROCE trend momentum."""
    delta = roce_current - roce_3q_avg
    if delta >= 2.0:
        return 100.0
    if delta >= 0.5:
        return 85.0
    if delta >= -0.5:
        return 70.0
    if delta >= -2.0:
        return 45.0
    return 20.0


def score_promoter_pledge(pledge_pct: float) -> float:
    """Score Promoter Pledge percentage."""
    if pledge_pct <= 0.0:
        return 100.0
    if pledge_pct <= 5.0:
        return 85.0
    if pledge_pct <= 15.0:
        return 60.0
    if pledge_pct <= 20.0:
        return 30.0
    return 0.0


def score_fcf_conversion(fcf_to_pat: float) -> float:
    """Score Free Cash Flow to Net Profit conversion."""
    if fcf_to_pat >= 0.80:
        return 100.0
    if fcf_to_pat >= 0.50:
        return 75.0
    if fcf_to_pat >= 0.0:
        return 50.0
    return 20.0


def score_debt_to_equity(de: float) -> float:
    """Score Debt-to-Equity solvency."""
    if de <= 0.30:
        return 100.0
    if de <= 0.70:
        return 80.0
    if de <= 1.20:
        return 60.0
    if de <= 2.00:
        return 35.0
    return 10.0


def compute_fundamental_score(fund: FundamentalMetricsInput) -> float:
    r"""Compute normalized composite Fundamental Health Score ($S_{fund} \in [0, 100]$)."""
    s_peg = score_peg(fund.peg_ratio)
    s_roce = score_roce_trend(fund.roce_current, fund.roce_3q_avg)
    s_pledge = score_promoter_pledge(fund.promoter_pledge_pct)
    s_fcf = score_fcf_conversion(fund.fcf_to_net_profit)
    s_de = score_debt_to_equity(fund.debt_to_equity)
    
    score = (
        0.25 * s_peg +
        0.25 * s_roce +
        0.20 * s_pledge +
        0.15 * s_fcf +
        0.15 * s_de
    )
    return round(float(score), 1)
