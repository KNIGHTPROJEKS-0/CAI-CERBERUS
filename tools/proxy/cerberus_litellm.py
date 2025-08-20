"""
Enhanced LiteLLM Adapter for CAI-CERBERUS Integration

This adapter provides seamless integration between CAI-CERBERUS and LiteLLM proxy
with enhanced safety, monitoring, and cost controls.
"""

import os
from typing import Dict, Any, List, Optional
from pathlib import Path

from cai import Agent, Tool
from tools.proxy.litellm_adapter import LiteLLMAdapter

class CerberusLiteLLMTool(Tool):
    """CAI-CERBERUS tool for LiteLLM integration"""
    
    def __init__(self):
        super().__init__(
            name="litellm_proxy",
            description="Access to LiteLLM proxy for multi-model AI capabilities"
        )
        
        # Initialize adapter with environment configuration
        self.adapter = LiteLLMAdapter(
            base_url=os.getenv("LITELLM_PROXY_URL", "http://localhost:4000"),
            master_key=os.getenv("LITELLM_MASTER_KEY"),
            audit_log_path=Path("logs/cerberus_litellm.jsonl")
        )
    
    async def execute(self, **kwargs) -> Dict[str, Any]:
        """Execute LiteLLM operations through the adapter"""
        operation = kwargs.get("operation", "chat")
        
        if operation == "health":
            return await self.adapter.validate_proxy_health()
        elif operation == "models":
            return {"models": await self.adapter.get_available_models()}
        elif operation == "usage":
            return await self.adapter.get_usage_stats()
        elif operation == "chat":
            return await self.adapter.complete_chat(
                messages=kwargs.get("messages", []),
                model=kwargs.get("model", "gpt-4o-mini"),
                **{k: v for k, v in kwargs.items() if k not in ["operation", "messages", "model"]}
            )
        else:
            return {"error": f"Unknown operation: {operation}"}

class CerberusLiteLLMAgent(Agent):
    """Specialized agent for LiteLLM operations"""
    
    def __init__(self, **kwargs):
        super().__init__(
            name="litellm_agent",
            description="Agent specialized for LiteLLM proxy operations",
            tools=[CerberusLiteLLMTool()],
            **kwargs
        )
    
    async def validate_model_access(self, model: str) -> bool:
        """Validate that the requested model is available"""
        tool = self.tools[0]
        models_result = await tool.execute(operation="models")
        available_models = [m.get("id", "") for m in models_result.get("models", [])]
        return model in available_models
    
    async def get_cost_estimate(self, messages: List[Dict], model: str) -> Dict[str, Any]:
        """Get cost estimate for a completion"""
        tool = self.tools[0]
        return await tool.adapter.get_cost_estimate(messages, model)
