import aiohttp
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from loguru import logger
from config.settings import settings
from src.core.models import EarningsEvent, EarningsOutcome


class PolygonAPIClient:
    """Ultra-low latency Polygon.io API client"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = settings.polygon_base_url
        self.timeout = aiohttp.ClientTimeout(total=settings.request_timeout_seconds)
        
    async def get_earnings_calendar(self, days_ahead: int = 7) -> List[Dict]:
        """Fetch upcoming earnings releases"""
        url = f"{self.base_url}/vX/reference/financials"
        params = {
            "apiKey": self.api_key,
            "limit": 1000,
            "sort": "period_of_report_date",
            "timeframe": "quarterly"
        }
        
        try:
            async with aiohttp.ClientSession(timeout=self.timeout) as session:
                async with session.get(url, params=params) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        results = data.get('results', [])
                        logger.info(f"Fetched {len(results)} upcoming earnings events")
                        return results
                    else:
                        logger.error(f"Polygon API error: {resp.status}")
                        return []
        except Exception as e:
            logger.error(f"Error fetching earnings calendar: {e}")
            return []
    
    async def verify_earnings_outcome(self, ticker: str) -> Optional[EarningsEvent]:
        """Verify if earnings beat or missed - ULTRA FAST"""
        earnings_url = f"{self.base_url}/vX/reference/financials"
        params = {
            "ticker": ticker,
            "apiKey": self.api_key,
            "limit": 1,
            "sort": "-filing_date",
            "timeframe": "quarterly"
        }
        
        try:
            async with aiohttp.ClientSession(timeout=self.timeout) as session:
                async with session.get(earnings_url, params=params) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        results = data.get('results', [])
                        
                        if results:
                            result = results[0]
                            financials = result.get('financials', {})
                            income = financials.get('income_statement', {})
                            eps_data = income.get('basic_earnings_per_share', {})
                            actual_eps = eps_data.get('value')
                            
                            event = EarningsEvent(
                                ticker=ticker,
                                company_name=result.get('company_name', ticker),
                                earnings_date=datetime.now(),
                                actual_eps=actual_eps,
                                verified_at=datetime.now()
                            )
                            
                            logger.info(f"✓ Verified {ticker}: EPS={actual_eps}")
                            return event
        except Exception as e:
            logger.error(f"Error verifying {ticker}: {e}")
            return None
        
        return None
    
    async def get_consensus_estimate(self, ticker: str) -> Optional[float]:
        """Get analyst consensus EPS estimate (placeholder)"""
        # In production, integrate with a service like:
        # - Estimize
        # - FactSet
        # - Bloomberg API
        # - Alpha Vantage
        return None