from typing import List, Optional
import requests
from fastapi import APIRouter, Query
from pydantic import BaseModel
from app.schemas.enums import MarketCapBucket

router = APIRouter(tags=["Search"])


class StockSearchResult(BaseModel):
    symbol: str
    company_name: str
    exchange: str
    market_cap_bucket: MarketCapBucket
    sector: str


# Pre-cached index of popular NSE/BSE stocks for instantaneous autocomplete
_STOCK_DATABASE: List[StockSearchResult] = [
    StockSearchResult(symbol="TATAMOTORS", company_name="Tata Motors Limited", exchange="NSE", market_cap_bucket=MarketCapBucket.LARGE_CAP, sector="Automobile"),
    StockSearchResult(symbol="RELIANCE", company_name="Reliance Industries Limited", exchange="NSE", market_cap_bucket=MarketCapBucket.LARGE_CAP, sector="Oil & Gas / Telecom"),
    StockSearchResult(symbol="TCS", company_name="Tata Consultancy Services Limited", exchange="NSE", market_cap_bucket=MarketCapBucket.LARGE_CAP, sector="IT Services"),
    StockSearchResult(symbol="INFY", company_name="Infosys Limited", exchange="NSE", market_cap_bucket=MarketCapBucket.LARGE_CAP, sector="IT Services"),
    StockSearchResult(symbol="HDFCBANK", company_name="HDFC Bank Limited", exchange="NSE", market_cap_bucket=MarketCapBucket.LARGE_CAP, sector="Banking"),
    StockSearchResult(symbol="ICICIBANK", company_name="ICICI Bank Limited", exchange="NSE", market_cap_bucket=MarketCapBucket.LARGE_CAP, sector="Banking"),
    StockSearchResult(symbol="SBIN", company_name="State Bank of India", exchange="NSE", market_cap_bucket=MarketCapBucket.LARGE_CAP, sector="Banking"),
    StockSearchResult(symbol="BHARTIARTL", company_name="Bharti Airtel Limited", exchange="NSE", market_cap_bucket=MarketCapBucket.LARGE_CAP, sector="Telecom"),
    StockSearchResult(symbol="ITC", company_name="ITC Limited", exchange="NSE", market_cap_bucket=MarketCapBucket.LARGE_CAP, sector="FMCG"),
    StockSearchResult(symbol="LT", company_name="Larsen & Toubro Limited", exchange="NSE", market_cap_bucket=MarketCapBucket.LARGE_CAP, sector="Infrastructure"),
    StockSearchResult(symbol="BAJFINANCE", company_name="Bajaj Finance Limited", exchange="NSE", market_cap_bucket=MarketCapBucket.LARGE_CAP, sector="NBFC"),
    StockSearchResult(symbol="KOTAKBANK", company_name="Kotak Mahindra Bank Limited", exchange="NSE", market_cap_bucket=MarketCapBucket.LARGE_CAP, sector="Banking"),
    StockSearchResult(symbol="ASIANPAINT", company_name="Asian Paints Limited", exchange="NSE", market_cap_bucket=MarketCapBucket.LARGE_CAP, sector="Paints / Consumer"),
    StockSearchResult(symbol="MARUTI", company_name="Maruti Suzuki India Limited", exchange="NSE", market_cap_bucket=MarketCapBucket.LARGE_CAP, sector="Automobile"),
    StockSearchResult(symbol="TITAN", company_name="Titan Company Limited", exchange="NSE", market_cap_bucket=MarketCapBucket.LARGE_CAP, sector="Consumer Goods"),
    StockSearchResult(symbol="SUNPHARMA", company_name="Sun Pharmaceutical Industries Limited", exchange="NSE", market_cap_bucket=MarketCapBucket.LARGE_CAP, sector="Pharma"),
    StockSearchResult(symbol="WIPRO", company_name="Wipro Limited", exchange="NSE", market_cap_bucket=MarketCapBucket.LARGE_CAP, sector="IT Services"),
    StockSearchResult(symbol="ADANIENT", company_name="Adani Enterprises Limited", exchange="NSE", market_cap_bucket=MarketCapBucket.LARGE_CAP, sector="Diversified"),
    StockSearchResult(symbol="ADANIPORTS", company_name="Adani Ports and Special Economic Zone Limited", exchange="NSE", market_cap_bucket=MarketCapBucket.LARGE_CAP, sector="Ports / Logistics"),
    StockSearchResult(symbol="NTPC", company_name="NTPC Limited", exchange="NSE", market_cap_bucket=MarketCapBucket.LARGE_CAP, sector="Power"),
    StockSearchResult(symbol="TRENT", company_name="Trent Limited", exchange="NSE", market_cap_bucket=MarketCapBucket.LARGE_CAP, sector="Retail"),
    StockSearchResult(symbol="BEL", company_name="Bharat Electronics Limited", exchange="NSE", market_cap_bucket=MarketCapBucket.LARGE_CAP, sector="Defense / Capital Goods"),
    StockSearchResult(symbol="HAL", company_name="Hindustan Aeronautics Limited", exchange="NSE", market_cap_bucket=MarketCapBucket.LARGE_CAP, sector="Defense / Aerospace"),
    StockSearchResult(symbol="ZOMATO", company_name="Zomato Limited", exchange="NSE", market_cap_bucket=MarketCapBucket.LARGE_CAP, sector="Consumer Tech"),
    StockSearchResult(symbol="JIOFIN", company_name="Jio Financial Services Limited", exchange="NSE", market_cap_bucket=MarketCapBucket.LARGE_CAP, sector="Financial Services"),
    StockSearchResult(symbol="SUZLON", company_name="Suzlon Energy Limited", exchange="NSE", market_cap_bucket=MarketCapBucket.MID_CAP, sector="Renewable Energy"),
    StockSearchResult(symbol="PAYTM", company_name="One97 Communications Limited", exchange="NSE", market_cap_bucket=MarketCapBucket.MID_CAP, sector="Fintech"),
    StockSearchResult(symbol="KPITTECH", company_name="KPIT Technologies Limited", exchange="NSE", market_cap_bucket=MarketCapBucket.MID_CAP, sector="IT / Auto Tech"),
    StockSearchResult(symbol="TATAELXSI", company_name="Tata Elxsi Limited", exchange="NSE", market_cap_bucket=MarketCapBucket.MID_CAP, sector="Design & Tech"),
    StockSearchResult(symbol="MAPMYINDIA", company_name="C.E. Info Systems Limited", exchange="NSE", market_cap_bucket=MarketCapBucket.SMALL_CAP, sector="Geospatial / Tech"),
    StockSearchResult(symbol="BLUESTONE", company_name="BlueStone Jewellery", exchange="NSE", market_cap_bucket=MarketCapBucket.SMALL_CAP, sector="Consumer Goods"),
]


@router.get("/search", response_model=List[StockSearchResult])
def search_stocks(
    q: str = Query(..., min_length=1, description="Stock ticker symbol or company name prefix"),
    limit: int = Query(10, ge=1, le=50),
) -> List[StockSearchResult]:
    """Search for equities matching symbol or name prefix."""
    query = q.strip().upper()
    matches: List[StockSearchResult] = []
    
    # Prefix matches first
    for stock in _STOCK_DATABASE:
        if stock.symbol.startswith(query):
            matches.append(stock)
            
    # Substring matches on company name or symbol
    for stock in _STOCK_DATABASE:
        if stock not in matches and (query in stock.symbol or query in stock.company_name.upper()):
            matches.append(stock)
            
    # If no local matches, fallback to Yahoo Finance Search API
    if not matches and len(query) >= 2:
        try:
            headers = {"User-Agent": "Mozilla/5.0"}
            r = requests.get(
                f"https://query2.finance.yahoo.com/v1/finance/search?q={query}&quotesCount=5&newsCount=0",
                headers=headers,
                timeout=3,
            )
            data = r.json()
            quotes = data.get("quotes", [])
            for q_item in quotes:
                sym = q_item.get("symbol", "")
                if sym.endswith(".NS") or sym.endswith(".BO"):
                    clean_sym = sym.replace(".NS", "").replace(".BO", "")
                    # Avoid duplicates
                    if not any(m.symbol == clean_sym for m in matches):
                        matches.append(
                            StockSearchResult(
                                symbol=clean_sym,
                                company_name=q_item.get("shortname", f"{clean_sym} Equity"),
                                exchange="NSE" if sym.endswith(".NS") else "BSE",
                                market_cap_bucket=MarketCapBucket.LARGE_CAP, # Default bucket
                                sector=q_item.get("sectorDisp", "Indian Equity"),
                            )
                        )
        except Exception:
            pass # Silently fail and return empty if YF API fails
            
        # Very last resort if YF returns nothing but user typed something that looks like a ticker
        if not matches and len(query.split()) == 1:
             matches.append(
                StockSearchResult(
                    symbol=query,
                    company_name=f"{query} Equity",
                    exchange="NSE",
                    market_cap_bucket=MarketCapBucket.LARGE_CAP,
                    sector="Indian Equity",
                )
            )
            
    return matches[:limit]
