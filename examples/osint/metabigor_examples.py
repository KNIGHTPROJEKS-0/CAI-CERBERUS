"""
Metabigor OSINT Examples for CAI-CERBERUS
"""

import asyncio
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent / "tools"))

from osint.metabigor_adapter import MetabigorAdapter, MetabigorTool

async def example_organization_discovery():
    """Example: Discover IP addresses of an organization"""
    print("🏢 Organization IP Discovery")
    adapter = MetabigorAdapter()
    result = await adapter.discover_organization_ips("Example Corp")
    
    if result["success"]:
        print(f"Found {result['count']} IPs for {result['organization']}")
        for ip in result["ip_addresses"][:5]:
            print(f"  • {ip}")
    else:
        print(f"❌ Error: {result['error']}")

async def example_related_domains():
    """Example: Find related domains using certificate technique"""
    print("🔗 Related Domains Discovery")
    adapter = MetabigorAdapter()
    result = await adapter.find_related_domains("example.com", technique="cert")
    
    if result["success"]:
        print(f"Found {result['count']} related domains:")
        for domain in result["related_domains"][:5]:
            print(f"  • {domain}")
    else:
        print(f"❌ Error: {result['error']}")

async def example_ip_info():
    """Example: Get IP information"""
    print("🔍 IP Information")
    adapter = MetabigorAdapter()
    result = await adapter.get_ip_info("8.8.8.8", open_ports=True)
    
    if result["success"]:
        print(f"Open ports for {result['ip']}:")
        if result.get("open_ports"):
            for port in result["open_ports"]:
                print(f"  • {port}")
    else:
        print(f"❌ Error: {result['error']}")

async def main():
    """Run examples"""
    print("🔍 Metabigor OSINT Examples")
    print("=" * 40)
    
    examples = [
        example_organization_discovery,
        example_related_domains,
        example_ip_info
    ]
    
    for example in examples:
        try:
            await example()
            print()
        except Exception as e:
            print(f"❌ Example failed: {e}")

if __name__ == "__main__":
    asyncio.run(main())