#!/usr/bin/env python3
"""Example usage of WhiteRabbitNeo in CAI-CERBERUS framework."""

import asyncio
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from tools.huggingface.whiterabbitneo_adapter import WhiteRabbitNeoAdapter, WhiteRabbitConfig

async def run_whiterabbitneo_example():
    """Demonstrate WhiteRabbitNeo capabilities in cybersecurity analysis."""
    
    print("🐰 WhiteRabbitNeo CAI-CERBERUS Integration Example")
    print("=" * 50)
    
    # Configure WhiteRabbitNeo
    config = WhiteRabbitConfig(
        api_base=os.getenv("WHITERABBITNEO_API_BASE", "http://localhost:4000"),
        api_key=os.getenv("LITELLM_MASTER_KEY", "sk-1234"),
        temperature=0.3  # Lower temperature for more focused analysis
    )
    
    async with WhiteRabbitNeoAdapter(config) as adapter:
        
        # Example 1: Advanced Threat Analysis
        print("\n1. Advanced Threat Analysis")
        print("-" * 30)
        
        threat_data = {
            "network_scan": {
                "open_ports": [22, 80, 443, 3389, 5432],
                "services": ["ssh", "http", "https", "rdp", "postgresql"],
                "os_fingerprint": "Linux Ubuntu 20.04"
            },
            "vulnerabilities": [
                {"cve": "CVE-2024-1234", "severity": "HIGH", "service": "ssh"},
                {"cve": "CVE-2024-5678", "severity": "CRITICAL", "service": "postgresql"}
            ],
            "indicators": {
                "suspicious_processes": ["cryptominer.exe", "backdoor.sh"],
                "network_anomalies": ["unusual_outbound_traffic", "dns_tunneling"]
            }
        }
        
        result = await adapter.analyze_threat_data(threat_data)
        if result["success"]:
            print(f"Analysis: {result['analysis'][:500]}...")
            print(f"Tokens used: {result['tokens_used']}")
        else:
            print(f"Error: {result['error']}")
        
        # Example 2: Exploit Chain Reasoning
        print("\n2. Exploit Chain Analysis")
        print("-" * 30)
        
        vulnerabilities = [
            {
                "cve": "CVE-2024-1234",
                "description": "SSH authentication bypass",
                "cvss": 9.8,
                "prerequisites": "network_access"
            },
            {
                "cve": "CVE-2024-5678", 
                "description": "PostgreSQL privilege escalation",
                "cvss": 8.4,
                "prerequisites": "database_access"
            }
        ]
        
        result = await adapter.reason_exploit_chains(vulnerabilities)
        if result["success"]:
            print(f"Exploit Chain Analysis: {result['analysis'][:500]}...")
        else:
            print(f"Error: {result['error']}")
        
        # Example 3: Threat Model Generation
        print("\n3. Threat Model Generation")
        print("-" * 30)
        
        system_info = {
            "architecture": "microservices",
            "components": ["web_frontend", "api_gateway", "database", "cache"],
            "deployment": "kubernetes_cluster",
            "data_classification": "sensitive_customer_data",
            "compliance_requirements": ["PCI-DSS", "GDPR"]
        }
        
        result = await adapter.generate_threat_model(system_info)
        if result["success"]:
            print(f"Threat Model: {result['analysis'][:500]}...")
        else:
            print(f"Error: {result['error']}")

if __name__ == "__main__":
    asyncio.run(run_whiterabbitneo_example())