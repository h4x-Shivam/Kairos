"""Unit tests for stock search autocomplete endpoint."""
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_search_prefix_match():
    """Verify search returns Tata Motors for 'TATA' prefix query."""
    response = client.get("/api/v1/search?q=TATA")
    assert response.status_code == 200
    results = response.json()
    assert len(results) > 0
    symbols = [r["symbol"] for r in results]
    assert "TATAMOTORS" in symbols


def test_search_exact_match():
    """Verify search returns Reliance for 'RELIANCE' query."""
    response = client.get("/api/v1/search?q=RELIANCE")
    assert response.status_code == 200
    results = response.json()
    assert len(results) >= 1
    assert results[0]["symbol"] == "RELIANCE"
    assert results[0]["exchange"] == "NSE"


def test_search_dynamic_fallback():
    """Verify unknown query returns dynamic ticker placeholder."""
    response = client.get("/api/v1/search?q=CUSTOMSTOCK")
    assert response.status_code == 200
    results = response.json()
    assert len(results) == 1
    assert results[0]["symbol"] == "CUSTOMSTOCK"


def test_search_empty_validation_error():
    """Verify empty query param returns 422 Unprocessable Entity."""
    response = client.get("/api/v1/search?q=")
    assert response.status_code == 422
