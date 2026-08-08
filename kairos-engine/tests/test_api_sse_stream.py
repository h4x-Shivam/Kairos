"""Unit tests for Server-Sent Events (SSE) diagnostic streaming endpoint."""
import json
from fastapi.testclient import TestClient
from app.main import app
from tests.test_math_indicators import create_synthetic_bars

client = TestClient(app)


def test_diagnostic_sse_stream_mock(mocker):
    """Verify GET /api/v1/diagnostic/{symbol}/stream yields sequential staged telemetry events."""
    bars = create_synthetic_bars(50, base_price=1200.0)
    
    mock_yf = mocker.MagicMock()
    mock_yf.get_historical_ohlcv.return_value = bars
    mock_yf.get_live_quote.return_value = {
        "symbol": "TCS.NS",
        "current_price": 3850.0,
        "high_52w": 4100.0,
        "company_name": "Tata Consultancy Services",
        "beta": 0.88,
    }
    mock_yf.get_fundamental_metrics.return_value = None
    mock_yf.get_corporate_disclosures.return_value = []
    
    mocker.patch("app.services.data_aggregator.data_aggregator.yf", mock_yf)
    mocker.patch("app.services.data_aggregator.data_aggregator.angel.is_healthy", return_value=False)
    
    with client.stream("GET", "/api/v1/diagnostic/TCS/stream?horizon_mode=SWING&market_cap_bucket=LARGE_CAP") as response:
        assert response.status_code == 200
        assert "text/event-stream" in response.headers["content-type"]
        
        events = []
        for line in response.iter_lines():
            if line.startswith("data: "):
                event_data = json.loads(line.replace("data: ", ""))
                events.append(event_data)
                
        stages = [e["stage"] for e in events]
        assert "INITIALIZING" in stages
        assert "FETCHING_OHLCV" in stages
        assert "FETCHING_FUNDAMENTALS" in stages
        assert "SENTIMENT_ANALYSIS" in stages
        assert "RESOLVING_CONFLICTS" in stages
        assert "COMPLETE" in stages
        
        # Verify final event contains full diagnostic payload
        complete_event = next(e for e in events if e["stage"] == "COMPLETE")
        assert complete_event["data"]["symbol"] == "TCS"
        assert complete_event["data"]["action"] in ["HOLD", "TIGHTEN_STOP", "TRIM_25", "TRIM_50", "EXIT_FULLY"]
        assert complete_event["data"]["audit_hash"] is not None
