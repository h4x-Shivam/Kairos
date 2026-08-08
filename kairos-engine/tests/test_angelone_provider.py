"""Unit tests for AngelOneSmartApiProvider adapter."""
import pyotp
from app.services.providers.angelone_provider import AngelOneSmartApiProvider
from app.schemas.enums import TimeFrame


def test_angelone_health_check():
    """Verify health check returns False when credentials are missing and True when present."""
    unconfigured = AngelOneSmartApiProvider(api_key=None, client_code=None, pin=None, totp_key=None)
    assert unconfigured.is_healthy() is False
    
    configured = AngelOneSmartApiProvider(
        api_key="TEST_KEY", client_code="S123", pin="1234", totp_key="JBSWY3DPEHPK3PXP"
    )
    assert configured.is_healthy() is True


def test_angelone_headless_totp_auth_mock(mocker):
    """Verify TOTP generation and session generation flow."""
    # Base32 TOTP Secret
    totp_secret = pyotp.random_base32()
    provider = AngelOneSmartApiProvider(
        api_key="API_KEY_123",
        client_code="CLIENT_123",
        pin="4321",
        totp_key=totp_secret,
    )
    
    mock_smart_connect = mocker.MagicMock()
    mock_smart_connect.generateSession.return_value = {
        "status": True,
        "data": {"jwtToken": "mock_jwt_token_xyz"},
    }
    mock_smart_connect.getfeedToken.return_value = "mock_feed_token_abc"
    mocker.patch("app.services.providers.angelone_provider.SmartConnect", return_value=mock_smart_connect)
    
    success = provider.authenticate()
    assert success is True
    assert provider.auth_token == "mock_jwt_token_xyz"
    assert provider.feed_token == "mock_feed_token_abc"


def test_angelone_historical_ohlcv_mock(mocker):
    """Verify OHLCV candlestick parsing from SmartAPI candle data."""
    totp_secret = pyotp.random_base32()
    provider = AngelOneSmartApiProvider(
        api_key="KEY", client_code="CODE", pin="1111", totp_key=totp_secret
    )
    provider.auth_token = "mock_token"
    
    mock_smart = mocker.MagicMock()
    mock_smart.getCandleData.return_value = {
        "status": True,
        "data": [
            ["2024-01-01T09:15:00+05:30", 100.0, 105.0, 98.0, 102.0, 5000],
            ["2024-01-02T09:15:00+05:30", 102.0, 108.0, 101.0, 107.0, 6000],
        ],
    }
    provider.smart_api = mock_smart
    
    bars = provider.get_historical_ohlcv("TCS", timeframe=TimeFrame.D1, limit=2)
    assert len(bars) == 2
    assert bars[0].open == 100.0
    assert bars[1].close == 107.0
