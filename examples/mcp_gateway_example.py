#!/usr/bin/env python3
"""
CAI-CERBERUS MCP Gateway Example
Demonstrates secure MCP server integration using Supergateway
"""

import asyncio
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from tools.mcp.supergateway_adapter import SupergatewayTool

async def main():
    """Example MCP gateway operations"""
    
    print("🔗 CAI-CERBERUS MCP Gateway Example")
    print("=" * 50)
    
    # Initialize the MCP gateway tool
    gateway_tool = SupergatewayTool()
    
    try:
        # Example 1: Start stdio-to-SSE gateway for filesystem MCP server
        print("\n1. Starting stdio-to-SSE gateway for filesystem server...")
        
        result = await gateway_tool.execute(
            action="start_sse_gateway",
            mcp_server_command="npx -y @modelcontextprotocol/server-filesystem ./workspaces",
            port=8000,
            require_approval=False  # For demo purposes
        )
        
        print(f"✅ Gateway started: {result['gateway_id']}")
        print(f"   SSE URL: {result['sse_url']}")
        print(f"   Message URL: {result['message_url']}")
        
        gateway_id = result['gateway_id']
        
        # Example 2: List active gateways
        print("\n2. Listing active gateways...")
        
        gateways = await gateway_tool.execute(action="list_gateways")
        print(f"✅ Active gateways: {len(gateways['gateways'])}")
        
        for gw in gateways['gateways']:
            print(f"   - {gw['gateway_id']}: {gw['status']} (PID: {gw['pid']})")
        
        # Example 3: Get audit log
        print("\n3. Checking audit log...")
        
        audit = await gateway_tool.execute(action="audit_log")
        print(f"✅ Audit entries: {len(audit['audit_log'])}")
        
        for entry in audit['audit_log'][-3:]:  # Show last 3 entries
            print(f"   - {entry['action']}: {entry['status']}")
        
        # Wait a moment to demonstrate the gateway is running
        print("\n4. Gateway is running... (waiting 5 seconds)")
        await asyncio.sleep(5)
        
        # Example 4: Stop the gateway
        print("\n5. Stopping gateway...")
        
        stop_result = await gateway_tool.execute(
            action="stop_gateway",
            gateway_id=gateway_id
        )
        
        print(f"✅ Gateway stopped: {stop_result['status']}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        
        # Cleanup on error
        print("\n🧹 Cleaning up all gateways...")
        await gateway_tool.execute(action="cleanup")
        print("✅ Cleanup complete")

if __name__ == "__main__":
    asyncio.run(main())