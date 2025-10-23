import pytest
from src.api.polymarket_client import PolymarketClient


@pytest.mark.asyncio
async def test_get_markets():
    """Test market search"""
    client = PolymarketClient("test_key", "test_private_key")
    
    markets = await client.get_markets("AAPL earnings")
    assert isinstance(markets, list)


@pytest.mark.asyncio
async def test_calculate_potential_return():
    """Test return calculation"""
    client = PolymarketClient("test_key", "test_private_key")
    
    return_pct = client.calculate_potential_return(0.60)
    assert return_pct > 0
    assert abs(return_pct - 66.67) < 1  # (1-0.6)/0.6 * 100