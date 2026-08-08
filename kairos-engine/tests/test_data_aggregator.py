"""Unit tests for DataAggregator orchestrator & fallback pipeline."""
from app.services.data_aggregator import DataAggregator
from app.schemas.enums import HorizonMode, MarketCapBucket
from tests.test_math_indicators import create_synthetic_bars


def test_data_aggregator_build_payload(mocker):
    """Verify aggregator constructs a fully valid DiagnosticInput payload."""
    bars = create_synthetic_bars(60, base_price=1000.0)
    
    mock_yf = mocker.MagicMock()
    mock_yf.get_historical_ohlcv.return_value = bars
    mock_yf.get_live_quote.return_value = {
        "symbol": "TATAMOTORS.NS",
        "current_price": 1600.0,
        "high_52w": 1650.0,
        "company_name": "Tata Motors Ltd",
        "beta": 1.15,
    }
    mock_yf.get_fundamental_metrics.return_value = None
    mock_yf.get_corporate_disclosures.return_value = []
    
    mock_nse = mocker.MagicMock()
    mock_nse.get_delivery_metrics.return_value = 52.0
    mock_nse.get_live_quote.return_value = {}
    
    mock_angel = mocker.MagicMock()
    mock_angel.is_healthy.return_value = False # Force fallback
    
    aggregator = DataAggregator(
        angel_provider=mock_angel,
        nse_provider=mock_nse,
        yf_provider=mock_yf,
    )
    
    payload = aggregator.build_diagnostic_input(
        symbol="TATAMOTORS",
        horizon_mode=HorizonMode.COMPOUNDER,
        market_cap_bucket=MarketCapBucket.LARGE_CAP,
    )
    
    assert payload.symbol == "TATAMOTORS"
    assert payload.company_name == "Tata Motors Ltd"
    assert payload.current_price > 0.0
    assert payload.technicals.delivery_pct == 52.0
    assert payload.technicals.sma_50 > 0.0
    assert payload.technicals.sma_200 > 0.0
    assert payload.quant.realized_volatility_1y > 0.0
    assert len(payload.bars) == 60
