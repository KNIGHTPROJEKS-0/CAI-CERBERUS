"""
Supergateway MCP Adapter for CAI-CERBERUS
Provides secure MCP (Model Context Protocol) gateway functionality
"""

import asyncio
import json
import subprocess
import tempfile
import time
from pathlib import Path
from typing import Dict, List, Optional, Any
import logging

logger = logging.getLogger(__name__)

class SupergatewayMCPAdapter:
    """
    Secure adapter for Supergateway MCP functionality in CAI-CERBERUS
    Enables stdio-to-SSE/WS bridging with safety controls
    """
    
    def __init__(self, workspace_dir: str = "./workspaces"):
        self.workspace_dir = Path(workspace_dir)
        self.supergateway_path = Path("external-tools/supergateway")
        self.active_gateways: Dict[str, subprocess.Popen] = {}
        self.audit_log = []
        
    async def validate_mcp_server(self, server_command: str) -> bool:
        """Validate MCP server command for security"""
        blocked_commands = [
            "rm", "del", "format", "shutdown", "reboot",
            "sudo", "su", "chmod +x", "curl", "wget"
        ]
        
        for blocked in blocked_commands:
            if blocked in server_command.lower():
                logger.warning(f"Blocked dangerous command: {blocked}")
                return False
                
        return True
    
    async def start_stdio_to_sse_gateway(
        self,
        mcp_server_command: str,
        port: int = 8000,
        require_approval: bool = True
    ) -> Dict[str, Any]:
        """Start stdio-to-SSE gateway with safety controls"""
        
        if not await self.validate_mcp_server(mcp_server_command):
            raise ValueError("MCP server command failed security validation")
            
        if require_approval:
            approval = input(f"Approve MCP gateway for: {mcp_server_command}? (y/N): ")
            if approval.lower() != 'y':
                raise PermissionError("Gateway start not approved")
        
        gateway_id = f"sse_{int(time.time())}"
        
        try:
            # Build supergateway command
            cmd = [
                "npx", "-y", "supergateway",
                "--stdio", mcp_server_command,
                "--port", str(port),
                "--baseUrl", f"http://localhost:{port}",
                "--ssePath", "/sse",
                "--messagePath", "/message",
                "--logLevel", "info"
            ]
            
            # Start gateway process
            process = subprocess.Popen(
                cmd,
                cwd=self.supergateway_path,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            self.active_gateways[gateway_id] = process
            
            # Log the operation
            audit_entry = {
                "timestamp": time.time(),
                "action": "start_stdio_to_sse_gateway",
                "gateway_id": gateway_id,
                "mcp_server": mcp_server_command,
                "port": port,
                "status": "started"
            }
            self.audit_log.append(audit_entry)
            
            return {
                "gateway_id": gateway_id,
                "sse_url": f"http://localhost:{port}/sse",
                "message_url": f"http://localhost:{port}/message",
                "status": "started",
                "pid": process.pid
            }
            
        except Exception as e:
            logger.error(f"Failed to start gateway: {e}")
            raise
    
    async def start_sse_to_stdio_gateway(
        self,
        sse_url: str,
        headers: Optional[Dict[str, str]] = None,
        require_approval: bool = True
    ) -> Dict[str, Any]:
        """Start SSE-to-stdio gateway for remote MCP servers"""
        
        if require_approval:
            approval = input(f"Approve SSE connection to: {sse_url}? (y/N): ")
            if approval.lower() != 'y':
                raise PermissionError("SSE gateway not approved")
        
        gateway_id = f"stdio_{int(time.time())}"
        
        try:
            cmd = ["npx", "-y", "supergateway", "--sse", sse_url]
            
            # Add headers if provided
            if headers:
                for key, value in headers.items():
                    cmd.extend(["--header", f"{key}: {value}"])
            
            process = subprocess.Popen(
                cmd,
                cwd=self.supergateway_path,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            self.active_gateways[gateway_id] = process
            
            audit_entry = {
                "timestamp": time.time(),
                "action": "start_sse_to_stdio_gateway",
                "gateway_id": gateway_id,
                "sse_url": sse_url,
                "status": "started"
            }
            self.audit_log.append(audit_entry)
            
            return {
                "gateway_id": gateway_id,
                "sse_url": sse_url,
                "status": "started",
                "pid": process.pid
            }
            
        except Exception as e:
            logger.error(f"Failed to start SSE gateway: {e}")
            raise
    
    async def start_streamable_http_gateway(
        self,
        mcp_server_command: str,
        port: int = 8000,
        stateful: bool = False,
        session_timeout: int = 60000,
        require_approval: bool = True
    ) -> Dict[str, Any]:
        """Start stdio-to-StreamableHTTP gateway"""
        
        if not await self.validate_mcp_server(mcp_server_command):
            raise ValueError("MCP server command failed security validation")
            
        if require_approval:
            approval = input(f"Approve StreamableHTTP gateway for: {mcp_server_command}? (y/N): ")
            if approval.lower() != 'y':
                raise PermissionError("Gateway start not approved")
        
        gateway_id = f"http_{int(time.time())}"
        
        try:
            cmd = [
                "npx", "-y", "supergateway",
                "--stdio", mcp_server_command,
                "--outputTransport", "streamableHttp",
                "--port", str(port)
            ]
            
            if stateful:
                cmd.extend(["--stateful", "--sessionTimeout", str(session_timeout)])
            
            process = subprocess.Popen(
                cmd,
                cwd=self.supergateway_path,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            self.active_gateways[gateway_id] = process
            
            audit_entry = {
                "timestamp": time.time(),
                "action": "start_streamable_http_gateway",
                "gateway_id": gateway_id,
                "mcp_server": mcp_server_command,
                "port": port,
                "stateful": stateful,
                "status": "started"
            }
            self.audit_log.append(audit_entry)
            
            return {
                "gateway_id": gateway_id,
                "http_url": f"http://localhost:{port}/mcp",
                "status": "started",
                "stateful": stateful,
                "pid": process.pid
            }
            
        except Exception as e:
            logger.error(f"Failed to start StreamableHTTP gateway: {e}")
            raise
    
    async def stop_gateway(self, gateway_id: str) -> Dict[str, Any]:
        """Stop a running gateway"""
        
        if gateway_id not in self.active_gateways:
            raise ValueError(f"Gateway {gateway_id} not found")
        
        process = self.active_gateways[gateway_id]
        
        try:
            process.terminate()
            process.wait(timeout=10)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait()
        
        del self.active_gateways[gateway_id]
        
        audit_entry = {
            "timestamp": time.time(),
            "action": "stop_gateway",
            "gateway_id": gateway_id,
            "status": "stopped"
        }
        self.audit_log.append(audit_entry)
        
        return {"gateway_id": gateway_id, "status": "stopped"}
    
    async def list_active_gateways(self) -> List[Dict[str, Any]]:
        """List all active gateways"""
        
        active = []
        for gateway_id, process in self.active_gateways.items():
            if process.poll() is None:  # Still running
                active.append({
                    "gateway_id": gateway_id,
                    "pid": process.pid,
                    "status": "running"
                })
            else:
                active.append({
                    "gateway_id": gateway_id,
                    "pid": process.pid,
                    "status": "terminated"
                })
        
        return active
    
    async def get_audit_log(self) -> List[Dict[str, Any]]:
        """Get audit log of all gateway operations"""
        return self.audit_log.copy()
    
    async def cleanup_all_gateways(self):
        """Emergency cleanup of all gateways"""
        
        for gateway_id in list(self.active_gateways.keys()):
            try:
                await self.stop_gateway(gateway_id)
            except Exception as e:
                logger.error(f"Failed to stop gateway {gateway_id}: {e}")
        
        logger.info("All gateways cleaned up")

# CAI-CERBERUS Tool Interface
class SupergatewayTool:
    """Tool interface for CAI-CERBERUS agents"""
    
    def __init__(self):
        self.adapter = SupergatewayMCPAdapter()
        self.name = "supergateway_mcp"
        self.description = "MCP gateway for stdio-to-SSE/WS/HTTP bridging"
    
    async def execute(self, action: str, **kwargs) -> Dict[str, Any]:
        """Execute supergateway action"""
        
        if action == "start_sse_gateway":
            return await self.adapter.start_stdio_to_sse_gateway(
                kwargs.get("mcp_server_command"),
                kwargs.get("port", 8000),
                kwargs.get("require_approval", True)
            )
        
        elif action == "start_stdio_gateway":
            return await self.adapter.start_sse_to_stdio_gateway(
                kwargs.get("sse_url"),
                kwargs.get("headers"),
                kwargs.get("require_approval", True)
            )
        
        elif action == "start_http_gateway":
            return await self.adapter.start_streamable_http_gateway(
                kwargs.get("mcp_server_command"),
                kwargs.get("port", 8000),
                kwargs.get("stateful", False),
                kwargs.get("session_timeout", 60000),
                kwargs.get("require_approval", True)
            )
        
        elif action == "stop_gateway":
            return await self.adapter.stop_gateway(kwargs.get("gateway_id"))
        
        elif action == "list_gateways":
            return {"gateways": await self.adapter.list_active_gateways()}
        
        elif action == "audit_log":
            return {"audit_log": await self.adapter.get_audit_log()}
        
        elif action == "cleanup":
            await self.adapter.cleanup_all_gateways()
            return {"status": "cleanup_complete"}
        
        else:
            raise ValueError(f"Unknown action: {action}")