"""Unit tests for synchronous diagnostic evaluation endpoint."""
from fastapi.testclient import TestClient
from app.main import app
from tests.test_math_indicators import create_synthetic_bars

client = TestClient(app)


def test_evaluate_diagnostic_endpoint_mock(mocker):
    """Verify POST /api/v1/diagnostic/evaluate computes and returns full DiagnosticOutput."""
    bars = create_synthetic_bars(60, base_price=900.0)
    
    mock_yf = mocker.MagicMock()
    mock_yf.get_historical_ohlcv.return_value = bars
    mock_yf.get_live_quote.return_value = {
        "symbol": "INFY.NS",
        "current_price": 1800.0,
        "high_52w": 1950.0,
        "company_name": "Infosys Limited",
        "beta": 1.05,
    }
    mock_yf.get_fundamental_metrics.return_value = None
    mock_yf.get_corporate_disclosures.return_value = []
    
    mocker.patch("app.services.data_aggregator.data_aggregator.yf", mock_yf)
    mocker.patch("app.services.data_aggregator.data_aggregator.angel.is_healthy", return_value=False)
    
    payload = {
        "symbol": "INFY",
        "horizon_mode": "COMPOUNDER",
        "market_cap_bucket": "LARGE_CAP",
        "timeframe": "1d",
        "entry_price": 1500.0,
        "holding_shares": 50,
        "purchase_date": "2023-01-15",
    }
    
    response = client.post("/api/v1/diagnostic/evaluate", json=payload)
    assert response.status_code == 200
    data = response.json()
    
    assert data["symbol"] == "INFY"
    assert data["action"] in ["HOLD", "TIGHTEN_STOP", "TRIM_25", "TRIM_50", "EXIT_FULLY"]
    assert "scores" in data
    assert "stop_telemetry" in data
    assert "audit_hash" in data
    assert len(data["audit_hash"]) == 64
    assert data["tax_impact"] is not None
    assert data["tax_impact"]["gross_proceeds"] > 0.0
