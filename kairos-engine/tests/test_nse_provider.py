"""Unit tests for NSEDirectProvider scraper adapter."""
import respx
import httpx
from app.services.providers.nse_provider import (
    NSEDirectProvider,
    clean_nse_symbol,
    NSE_BASE_URL,
)


def test_clean_nse_symbol():
    """Verify symbol cleaning for NSE endpoints."""
    assert clean_nse_symbol("TCS.NS") == "TCS"
    assert clean_nse_symbol("INFY.BO") == "INFY"
    assert clean_nse_symbol("RELIANCE") == "RELIANCE"


@respx.mock
def test_nse_delivery_metrics_mock():
    """Verify security-wise delivery percentage parsing."""
    # Mock base cookie request
    respx.get(f"{NSE_BASE_URL}/").mock(return_value=httpx.Response(200, text="OK"))
    
    # Mock quote trade info endpoint
    trade_info_url = f"{NSE_BASE_URL}/api/quote-equity"
    respx.get(trade_info_url, params={"symbol": "TCS", "section": "trade_info"}).mock(
        return_value=httpx.Response(
            200,
            json={
                "securityWiseDP": {
                    "deliveryToTradedQuantity": 48.65,
                    "quantityTraded": 1000000,
                }
            },
        )
    )
    
    provider = NSEDirectProvider()
    delivery = provider.get_delivery_metrics("TCS.NS")
    assert delivery == 48.6
    provider.close()


@respx.mock
def test_nse_live_quote_mock():
    """Verify NSE quote price parsing."""
    respx.get(f"{NSE_BASE_URL}/").mock(return_value=httpx.Response(200, text="OK"))
    quote_url = f"{NSE_BASE_URL}/api/quote-equity"
    respx.get(quote_url, params={"symbol": "RELIANCE"}).mock(
        return_value=httpx.Response(
            200,
            json={
                "priceInfo": {
                    "lastPrice": 2950.50,
                    "weekHighLow": {"max": 3120.00, "min": 2200.00},
                },
                "info": {"companyName": "Reliance Industries Limited"},
            },
        )
    )
    
    provider = NSEDirectProvider()
    quote = provider.get_live_quote("RELIANCE")
    assert quote["current_price"] == 2950.50
    assert quote["high_52w"] == 3120.00
    assert quote["company_name"] == "Reliance Industries Limited"
    provider.close()
