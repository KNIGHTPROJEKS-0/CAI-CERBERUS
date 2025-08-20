#!/usr/bin/env python3
"""WhiteRabbitNeo adapter for CAI-CERBERUS framework."""

import asyncio
import json
import os
from typing import Dict, List, Optional, Any
import aiohttp
from dataclasses import dataclass

@dataclass
class WhiteRabbitConfig:
    """Configuration for WhiteRabbitNeo model."""
    api_base: str = "http://localhost:4000"
    model_name: str = "whiterabbitneo"
    max_tokens: int = 4096
    temperature: float = 0.7
    timeout: int = 300
    api_key: str = "sk-1234"

class WhiteRabbitNeoAdapter:
    """Adapter for WhiteRabbitNeo model integration."""
    
    def __init__(self, config: Optional[WhiteRabbitConfig] = None):
        self.config = config or WhiteRabbitConfig()
        self.session: Optional[aiohttp.ClientSession] = None
    
    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    async def analyze_threat_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Perform advanced threat analysis using WhiteRabbitNeo."""
        prompt = f"""
        Analyze the following cybersecurity data for advanced threats and patterns:
        
        Data: {json.dumps(data, indent=2)}
        
        Provide:
        1. Advanced threat indicators
        2. Complex attack chain analysis
        3. Sophisticated vulnerability correlations
        4. Deep technical insights
        5. Advanced mitigation strategies
        """
        
        return await self._query_model(prompt)
    
    async def reason_exploit_chains(self, vulnerabilities: List[Dict]) -> Dict[str, Any]:
        """Reason through complex exploit chains."""
        prompt = f"""
        Given these vulnerabilities, perform advanced reasoning to identify potential exploit chains:
        
        Vulnerabilities: {json.dumps(vulnerabilities, indent=2)}
        
        Analyze:
        1. Multi-step attack paths
        2. Privilege escalation chains
        3. Lateral movement opportunities
        4. Defense evasion techniques
        5. Impact amplification vectors
        """
        
        return await self._query_model(prompt)
    
    async def generate_threat_model(self, system_info: Dict[str, Any]) -> Dict[str, Any]:
        """Generate sophisticated threat models."""
        prompt = f"""
        Create an advanced threat model for this system:
        
        System Information: {json.dumps(system_info, indent=2)}
        
        Generate:
        1. Comprehensive threat landscape
        2. Advanced persistent threat scenarios
        3. Zero-day exploitation possibilities
        4. Supply chain attack vectors
        5. Insider threat considerations
        """
        
        return await self._query_model(prompt)
    
    async def _query_model(self, prompt: str) -> Dict[str, Any]:
        """Query WhiteRabbitNeo model via LiteLLM proxy."""
        if not self.session:
            raise RuntimeError("Session not initialized. Use async context manager.")
        
        payload = {
            "model": self.config.model_name,
            "messages": [
                {
                    "role": "system",
                    "content": "You are WhiteRabbitNeo, an advanced AI for cybersecurity analysis. Provide detailed, technical, and actionable insights."
                },
                {
                    "role": "user", 
                    "content": prompt
                }
            ],
            "max_tokens": self.config.max_tokens,
            "temperature": self.config.temperature
        }
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.config.api_key}"
        }
        
        try:
            async with self.session.post(
                f"{self.config.api_base}/v1/chat/completions",
                json=payload,
                headers=headers,
                timeout=aiohttp.ClientTimeout(total=self.config.timeout)
            ) as response:
                if response.status == 200:
                    result = await response.json()
                    return {
                        "success": True,
                        "analysis": result["choices"][0]["message"]["content"],
                        "model": self.config.model_name,
                        "tokens_used": result.get("usage", {}).get("total_tokens", 0)
                    }
                else:
                    error_text = await response.text()
                    return {
                        "success": False,
                        "error": f"HTTP {response.status}: {error_text}",
                        "model": self.config.model_name
                    }
        
        except asyncio.TimeoutError:
            return {
                "success": False,
                "error": "Request timeout",
                "model": self.config.model_name
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "model": self.config.model_name
            }

async def main():
    """Test WhiteRabbitNeo adapter."""
    config = WhiteRabbitConfig(
        api_base=os.getenv("WHITERABBITNEO_API_BASE", "http://localhost:4000"),
        api_key=os.getenv("LITELLM_MASTER_KEY", "sk-1234")
    )
    
    async with WhiteRabbitNeoAdapter(config) as adapter:
        # Test threat analysis
        test_data = {
            "vulnerabilities": ["CVE-2024-1234", "CVE-2024-5678"],
            "services": ["ssh", "http", "https"],
            "ports": [22, 80, 443]
        }
        
        result = await adapter.analyze_threat_data(test_data)
        print("Threat Analysis Result:")
        print(json.dumps(result, indent=2))

if __name__ == "__main__":
    asyncio.run(main())