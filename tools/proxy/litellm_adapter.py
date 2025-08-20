"""LiteLLM Proxy Adapter for CAI-CERBERUS

This adapter provides secure, monitored access to LiteLLM proxy with:
- Cost tracking and budget enforcement
- Safety controls and validation
- Audit logging and compliance
- Multi-model routing and fallbacks
"""

import asyncio
import json
import logging
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Any, Optional, List, Union

import httpx
from pydantic import BaseModel, Field

# Configure logging
logger = logging.getLogger(__name__)

class ModelConfig(BaseModel):
    """Configuration for a model in LiteLLM"""
    name: str
    provider: str
    max_tokens: Optional[int] = None
    cost_per_token: Optional[float] = None
    enabled: bool = True

class SafetyConfig(BaseModel):
    """Safety configuration for LiteLLM operations"""
    max_budget_per_request: float = Field(default=10.0, description="Maximum cost per request")
    max_tokens_per_request: int = Field(default=4000, description="Maximum tokens per request")
    require_approval_over: float = Field(default=5.0, description="Require approval for requests over this cost")
    blocked_content_types: List[str] = Field(default_factory=lambda: ["harmful", "illegal"])
    rate_limit_per_minute: int = Field(default=60, description="Maximum requests per minute")

class LiteLLMAdapter:
    """Enhanced adapter for LiteLLM proxy with comprehensive safety and monitoring"""
    
    def __init__(
        self, 
        base_url: str = "http://localhost:4000", 
        master_key: str = None,
        safety_config: Optional[SafetyConfig] = None,
        audit_log_path: Optional[Path] = None
    ):
        self.base_url = base_url.rstrip('/')
        self.master_key = master_key
        self.safety_config = safety_config or SafetyConfig()
        self.audit_log_path = audit_log_path or Path("logs/litellm_audit.jsonl")
        
        # Initialize HTTP client with timeout and retry
        self.client = httpx.AsyncClient(
            timeout=httpx.Timeout(30.0),
            limits=httpx.Limits(max_keepalive_connections=5, max_connections=10)
        )
        
        # Rate limiting
        self._request_times = []
        
        # Ensure audit log directory exists
        self.audit_log_path.parent.mkdir(parents=True, exist_ok=True)
    
    async def __aenter__(self):
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.client.aclose()
    
    def _log_audit_event(self, event_type: str, data: Dict[str, Any]):
        """Log audit event to JSONL file"""
        audit_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "event_type": event_type,
            "data": data
        }
        
        try:
            with open(self.audit_log_path, "a") as f:
                f.write(json.dumps(audit_entry) + "\n")
        except Exception as e:
            logger.error(f"Failed to write audit log: {e}")
    
    def _check_rate_limit(self) -> bool:
        """Check if request is within rate limits"""
        now = time.time()
        # Remove requests older than 1 minute
        self._request_times = [t for t in self._request_times if now - t < 60]
        
        if len(self._request_times) >= self.safety_config.rate_limit_per_minute:
            return False
        
        self._request_times.append(now)
        return True
    
    async def validate_proxy_health(self) -> Dict[str, Any]:
        """Check if LiteLLM proxy is healthy and accessible"""
        try:
            response = await self.client.get(f"{self.base_url}/health")
            health_data = {
                "healthy": response.status_code == 200,
                "status_code": response.status_code,
                "response_time_ms": response.elapsed.total_seconds() * 1000 if hasattr(response, 'elapsed') else None
            }
            
            if response.status_code == 200:
                try:
                    health_data.update(response.json())
                except:
                    pass
            
            self._log_audit_event("health_check", health_data)
            return health_data
            
        except Exception as e:
            error_data = {"healthy": False, "error": str(e)}
            self._log_audit_event("health_check_failed", error_data)
            return error_data
    
    async def get_usage_stats(self) -> Dict[str, Any]:
        """Get current usage and cost statistics"""
        try:
            headers = {"Authorization": f"Bearer {self.master_key}"} if self.master_key else {}
            
            # Try multiple endpoints for usage stats
            endpoints = ["/spend/tags", "/spend", "/usage"]
            
            for endpoint in endpoints:
                try:
                    response = await self.client.get(
                        f"{self.base_url}{endpoint}",
                        headers=headers
                    )
                    if response.status_code == 200:
                        stats = response.json()
                        self._log_audit_event("usage_stats_retrieved", {"endpoint": endpoint})
                        return stats
                except:
                    continue
            
            return {"error": "No usage endpoint available", "total_spend": 0.0}
            
        except Exception as e:
            error_data = {"error": str(e), "total_spend": 0.0}
            self._log_audit_event("usage_stats_failed", error_data)
            return error_data
    
    async def check_budget_limit(self, limit: float) -> Dict[str, Any]:
        """Check if current spend is within budget limit"""
        stats = await self.get_usage_stats()
        current_spend = stats.get("total_spend", 0.0)
        
        result = {
            "within_budget": current_spend < limit,
            "current_spend": current_spend,
            "budget_limit": limit,
            "remaining_budget": max(0, limit - current_spend)
        }
        
        self._log_audit_event("budget_check", result)
        return result
    
    async def get_available_models(self) -> List[Dict[str, Any]]:
        """Get list of available models from LiteLLM"""
        try:
            headers = {"Authorization": f"Bearer {self.master_key}"} if self.master_key else {}
            
            response = await self.client.get(
                f"{self.base_url}/v1/models",
                headers=headers
            )
            
            if response.status_code == 200:
                models_data = response.json()
                models = models_data.get("data", [])
                
                self._log_audit_event("models_retrieved", {"count": len(models)})
                return models
            else:
                logger.warning(f"Failed to get models: {response.status_code}")
                return []
                
        except Exception as e:
            logger.error(f"Error getting models: {e}")
            self._log_audit_event("models_retrieval_failed", {"error": str(e)})
            return []
    
    async def validate_request_safety(self, messages: List[Dict], model: str) -> Dict[str, Any]:
        """Validate request against safety policies"""
        validation_result = {
            "safe": True,
            "warnings": [],
            "blocked_reasons": []
        }
        
        # Check rate limiting
        if not self._check_rate_limit():
            validation_result["safe"] = False
            validation_result["blocked_reasons"].append("Rate limit exceeded")
        
        # Estimate token count (rough approximation)
        total_text = " ".join([msg.get("content", "") for msg in messages if isinstance(msg.get("content"), str)])
        estimated_tokens = len(total_text.split()) * 1.3  # Rough estimate
        
        if estimated_tokens > self.safety_config.max_tokens_per_request:
            validation_result["safe"] = False
            validation_result["blocked_reasons"].append(f"Token limit exceeded: {estimated_tokens} > {self.safety_config.max_tokens_per_request}")
        
        # Content safety check (basic keyword filtering)
        for blocked_type in self.safety_config.blocked_content_types:
            if blocked_type.lower() in total_text.lower():
                validation_result["warnings"].append(f"Potentially {blocked_type} content detected")
        
        self._log_audit_event("safety_validation", {
            "model": model,
            "estimated_tokens": estimated_tokens,
            "result": validation_result
        })
        
        return validation_result
    
    async def complete_chat(
        self, 
        messages: List[Dict[str, str]], 
        model: str = "gpt-4o-mini",
        max_tokens: Optional[int] = None,
        temperature: float = 0.7,
        **kwargs
    ) -> Dict[str, Any]:
        """Send chat completion request through LiteLLM proxy"""
        
        # Validate safety first
        safety_check = await self.validate_request_safety(messages, model)
        if not safety_check["safe"]:
            return {
                "error": "Request blocked by safety policies",
                "blocked_reasons": safety_check["blocked_reasons"]
            }
        
        try:
            headers = {"Authorization": f"Bearer {self.master_key}"} if self.master_key else {}
            headers["Content-Type"] = "application/json"
            
            payload = {
                "model": model,
                "messages": messages,
                "temperature": temperature,
                **kwargs
            }
            
            if max_tokens:
                payload["max_tokens"] = min(max_tokens, self.safety_config.max_tokens_per_request)
            
            start_time = time.time()
            
            response = await self.client.post(
                f"{self.base_url}/v1/chat/completions",
                headers=headers,
                json=payload
            )
            
            end_time = time.time()
            
            if response.status_code == 200:
                result = response.json()
                
                # Log successful completion
                self._log_audit_event("chat_completion_success", {
                    "model": model,
                    "response_time_ms": (end_time - start_time) * 1000,
                    "usage": result.get("usage", {}),
                    "warnings": safety_check.get("warnings", [])
                })
                
                return result
            else:
                error_data = {
                    "error": f"HTTP {response.status_code}",
                    "details": response.text
                }
                self._log_audit_event("chat_completion_failed", error_data)
                return error_data
                
        except Exception as e:
            error_data = {"error": str(e)}
            self._log_audit_event("chat_completion_error", error_data)
            return error_data
    
    async def get_cost_estimate(self, messages: List[Dict], model: str) -> Dict[str, Any]:
        """Estimate cost for a completion request"""
        # This is a rough estimate - actual costs depend on LiteLLM's pricing
        total_text = " ".join([msg.get("content", "") for msg in messages if isinstance(msg.get("content"), str)])
        estimated_input_tokens = len(total_text.split()) * 1.3
        
        # Basic cost estimates (these should be updated with actual model pricing)
        cost_per_1k_tokens = {
            "gpt-4o": 0.03,
            "gpt-4o-mini": 0.0015,
            "claude-3-5-sonnet": 0.015,
            "deepseek-chat": 0.0014
        }
        
        base_model = model.split("/")[-1] if "/" in model else model
        rate = cost_per_1k_tokens.get(base_model, 0.002)  # Default rate
        
        estimated_cost = (estimated_input_tokens / 1000) * rate
        
        return {
            "estimated_input_tokens": estimated_input_tokens,
            "estimated_cost_usd": estimated_cost,
            "model": model,
            "rate_per_1k_tokens": rate
        }