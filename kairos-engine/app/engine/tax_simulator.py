"""Indian Capital Gains Tax (STCG/LTCG) and Downside Cushion Simulator."""
import math
from typing import Dict, Any


def simulate_trim_execution(
    shares_held: int,
    buy_price: float,
    current_price: float,
    trim_percentage: float,
    holding_period_months: int,
) -> Dict[str, Any]:
    """Calculate gross proceeds, Indian capital gains tax, net cash, and breakeven cushion expansion.
    
    Tax Rules:
        - STCG (<= 12 months): 20.0% flat tax on gains
        - LTCG (> 12 months): 12.5% tax on gains exceeding the ₹1,25,000 statutory exemption
    """
    if shares_held <= 0 or buy_price <= 0 or current_price <= 0:
        raise ValueError("Shares held, buy price, and current price must be positive numbers")
        
    trim_pct = max(0.0, min(100.0, trim_percentage))
    shares_to_sell = int(math.floor(shares_held * (trim_pct / 100.0)))
    shares_retained = shares_held - shares_to_sell
    
    gross_proceeds = shares_to_sell * current_price
    cost_basis_sold = shares_to_sell * buy_price
    capital_gain = max(0.0, gross_proceeds - cost_basis_sold)
    
    # Calculate tax liability under Indian Finance Act 2024 rules
    if holding_period_months <= 12:
        tax_type = "STCG"
        tax_rate_pct = 20.0
        tax_liability = capital_gain * 0.20
    else:
        tax_type = "LTCG"
        tax_rate_pct = 12.5
        taxable_gain = max(0.0, capital_gain - 125000.0) # Statutory ₹1.25L exemption
        tax_liability = taxable_gain * 0.125
        
    net_cash_realized = gross_proceeds - tax_liability
    
    # Calculate expanded downside cushion on retained shares
    if shares_retained > 0:
        initial_investment = shares_held * buy_price
        remaining_capital_at_risk = initial_investment - net_cash_realized
        new_breakeven_price = max(0.0, remaining_capital_at_risk / shares_retained)
        new_downside_cushion_pct = ((current_price - new_breakeven_price) / current_price) * 100.0
    else:
        new_breakeven_price = 0.0
        new_downside_cushion_pct = 100.0
        
    return {
        "shares_held": shares_held,
        "shares_to_sell": shares_to_sell,
        "shares_retained": shares_retained,
        "buy_price": round(buy_price, 2),
        "current_price": round(current_price, 2),
        "gross_proceeds": round(gross_proceeds, 2),
        "capital_gain": round(capital_gain, 2),
        "tax_type": tax_type,
        "tax_rate_pct": tax_rate_pct,
        "tax_liability": round(tax_liability, 2),
        "net_cash_realized": round(net_cash_realized, 2),
        "new_breakeven_price": round(new_breakeven_price, 2),
        "new_downside_cushion_pct": round(new_downside_cushion_pct, 2),
    }
