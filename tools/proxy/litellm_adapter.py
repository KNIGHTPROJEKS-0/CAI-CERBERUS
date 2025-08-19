"""LiteLLM Proxy Adapter for CAI-CERBERUS"""

import asyncio
import httpx
from typing import Dict, Any, Optional

class LiteLLMAdapter:
    """Adapter for LiteLLM proxy with cost tracking and safety controls"""
    
    def __init__(self, base_url: str = "http://localhost:4000", master_key: str = None):
        self.base_url = base_url
        self.master_key = master_key
        self.client = httpx.AsyncClient()
    
    async def get_usage_stats(self) -> Dict[str, Any]:
        """Get current usage and cost statistics"""
        try:
            response = await self.client.get(
                f"{self.base_url}/spend/tags",
                headers={"Authorization": f"Bearer {self.master_key}"}
            )
            return response.json()
        except Exception as e:
            return {"error": str(e), "cost": 0.0}
    
    async def check_budget_limit(self, limit: float) -> bool:
        """Check if current spend is within budget limit"""
        stats = await self.get_usage_stats()
        current_spend = stats.get("total_spend", 0.0)
        return current_spend < limit
    
    async def validate_proxy_health(self) -> bool:
        """Check if LiteLLM proxy is healthy and accessible"""
        try:
            response = await self.client.get(f"{self.base_url}/health")
            return response.status_code == 200
        except:
            return False