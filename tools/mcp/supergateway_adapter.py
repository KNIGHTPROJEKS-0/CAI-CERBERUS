"""
SuperGateway Adapter for CAI-CERBERUS

This adapter provides integration with SuperGateway for MCP protocol translation
and multi-transport support.
"""

import asyncio
import json
import logging
from typing import Dict, Any, Optional, List
from pathlib import Path

import httpx
import websockets
from pydantic import BaseModel

logger = logging.getLogger(__name__)

class SuperGatewayConfig(BaseModel):
    """Configuration for SuperGateway connection"""
    base_url: str = "http://localhost:3000"
    timeout: int = 30
    max_retries: int = 3
    enable_compression: bool = True

class SuperGatewayAdapter:
    """Adapter for SuperGateway MCP protocol translation"""
    
    def __init__(self, config: Optional[SuperGatewayConfig] = None):
        self.config = config or SuperGatewayConfig()
        self.client = httpx.AsyncClient(
            timeout=httpx.Timeout(self.config.timeout),
            limits=httpx.Limits(max_keepalive_connections=5, max_connections=10)
        )
        self._ws_connections = {}
        
    async def __aenter__(self):
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()
    
    async def close(self):
        """Close all connections"""
        await self.client.aclose()
        
        # Close WebSocket connections
        for ws in self._ws_connections.values():
            if not ws.closed:
                await ws.close()
        self._ws_connections.clear()
    
    async def health_check(self) -> Dict[str, Any]:
        """Check SuperGateway health status"""
        try:
            response = await self.client.get(f"{self.config.base_url}/health")
            return {
                "healthy": response.status_code == 200,
                "status_code": response.status_code,
                "data": response.json() if response.status_code == 200 else None
            }
        except Exception as e:
            return {"healthy": False, "error": str(e)}
    
    async def get_available_gateways(self) -> List[Dict[str, Any]]:
        """Get list of available gateways"""
        try:
            response = await self.client.get(f"{self.config.base_url}/gateways")
            if response.status_code == 200:
                return response.json().get("gateways", [])
            return []
        except Exception as e:
            logger.error(f"Failed to get gateways: {e}")
            return []
    
    async def call_http_gateway(
        self, 
        endpoint: str, 
        method: str, 
        params: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """Call MCP server through HTTP gateway"""
        try:
            url = f"{self.config.base_url}{endpoint}"
            payload = {
                "jsonrpc": "2.0",
                "id": 1,
                "method": method,
                "params": params or {}
            }
            
            response = await self.client.post(url, json=payload)
            
            if response.status_code == 200:
                return response.json()
            else:
                return {
                    "error": {
                        "code": response.status_code,
                        "message": f"HTTP {response.status_code}",
                        "data": response.text
                    }
                }
                
        except Exception as e:
            return {
                "error": {
                    "code": -1,
                    "message": str(e)
                }
            }
    
    async def connect_websocket(self, endpoint: str) -> Optional[websockets.WebSocketServerProtocol]:
        """Connect to WebSocket gateway"""
        try:
            ws_url = f"ws://{self.config.base_url.replace('http://', '').replace('https://', '')}{endpoint}"
            
            if endpoint in self._ws_connections:
                ws = self._ws_connections[endpoint]
                if not ws.closed:
                    return ws
            
            ws = await websockets.connect(ws_url)
            self._ws_connections[endpoint] = ws
            return ws
            
        except Exception as e:
            logger.error(f"Failed to connect to WebSocket {endpoint}: {e}")
            return None
    
    async def call_websocket_gateway(
        self, 
        endpoint: str, 
        method: str, 
        params: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """Call MCP server through WebSocket gateway"""
        try:
            ws = await self.connect_websocket(endpoint)
            if not ws:
                return {"error": {"code": -1, "message": "Failed to connect to WebSocket"}}
            
            # Send request
            request = {
                "jsonrpc": "2.0",
                "id": 1,
                "method": method,
                "params": params or {}
            }
            
            await ws.send(json.dumps(request))
            
            # Wait for response
            response_text = await ws.recv()
            return json.loads(response_text)
            
        except Exception as e:
            return {
                "error": {
                    "code": -1,
                    "message": str(e)
                }
            }
    
    async def call_sse_gateway(
        self, 
        endpoint: str, 
        method: str, 
        params: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """Call MCP server through SSE gateway"""
        try:
            url = f"{self.config.base_url}{endpoint}"
            payload = {
                "jsonrpc": "2.0",
                "id": 1,
                "method": method,
                "params": params or {}
            }
            
            # Send request and get SSE stream
            async with self.client.stream("POST", url, json=payload) as response:
                if response.status_code != 200:
                    return {
                        "error": {
                            "code": response.status_code,
                            "message": f"HTTP {response.status_code}"
                        }
                    }
                
                # Read SSE stream
                async for line in response.aiter_lines():
                    if line.startswith("data: "):
                        data = line[6:]  # Remove "data: " prefix
                        if data.strip():
                            try:
                                return json.loads(data)
                            except json.JSONDecodeError:
                                continue
                
                return {"error": {"code": -1, "message": "No valid response received"}}
                
        except Exception as e:
            return {
                "error": {
                    "code": -1,
                    "message": str(e)
                }
            }
    
    async def call_gateway(
        self, 
        gateway_type: str,
        endpoint: str, 
        method: str, 
        params: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """Call MCP server through appropriate gateway type"""
        
        if gateway_type == "http":
            return await self.call_http_gateway(endpoint, method, params)
        elif gateway_type == "websocket" or gateway_type == "ws":
            return await self.call_websocket_gateway(endpoint, method, params)
        elif gateway_type == "sse":
            return await self.call_sse_gateway(endpoint, method, params)
        else:
            return {
                "error": {
                    "code": -1,
                    "message": f"Unknown gateway type: {gateway_type}"
                }
            }
    
    # Convenience methods for common MCP operations
    async def list_tools(self, gateway_type: str, endpoint: str) -> Dict[str, Any]:
        """List available tools from MCP server"""
        return await self.call_gateway(gateway_type, endpoint, "tools/list")
    
    async def call_tool(
        self, 
        gateway_type: str, 
        endpoint: str, 
        tool_name: str, 
        arguments: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """Call a specific tool on MCP server"""
        return await self.call_gateway(
            gateway_type, 
            endpoint, 
            "tools/call", 
            {"name": tool_name, "arguments": arguments or {}}
        )
    
    async def list_resources(self, gateway_type: str, endpoint: str) -> Dict[str, Any]:
        """List available resources from MCP server"""
        return await self.call_gateway(gateway_type, endpoint, "resources/list")
    
    async def read_resource(
        self, 
        gateway_type: str, 
        endpoint: str, 
        resource_uri: str
    ) -> Dict[str, Any]:
        """Read a specific resource from MCP server"""
        return await self.call_gateway(
            gateway_type, 
            endpoint, 
            "resources/read", 
            {"uri": resource_uri}
        )