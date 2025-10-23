import pytest
from src.api.polygon_client import PolygonAPIClient


@pytest.mark.asyncio
async def test_get_earnings_calendar():
    """Test fetching earnings calendar"""
    client = PolygonAPIClient("test_api_key")
    
    # Mock test - replace with actual test
    calendar = await client.get_earnings_calendar(days_ahead=7)
    assert isinstance(calendar, list)


@pytest.mark.asyncio
async def test_verify_earnings_outcome():
    """Test earnings verification"""
    client = PolygonAPIClient("test_api_key")
    
    # Mock test
    event = await client.verify_earnings_outcome("AAPL")
    # Add assertions based on expected behavior