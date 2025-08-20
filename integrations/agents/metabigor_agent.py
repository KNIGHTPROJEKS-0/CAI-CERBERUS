"""
Metabigor OSINT Agent for CAI-CERBERUS
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent.parent.parent / "tools"))

from osint.metabigor_adapter import MetabigorTool

logger = logging.getLogger(__name__)

class MetabigorAgent:
    """OSINT Agent using Metabigor for reconnaissance"""
    
    def __init__(self, config: Optional[Dict] = None):
        self.config = config or {}
        self.tool = MetabigorTool()
        self.name = "MetabigorOSINTAgent"
        self.role = "reconnaissance"
        self.capabilities = [
            "ip_discovery",
            "domain_enumeration", 
            "network_scanning",
            "certificate_analysis",
            "whois_analysis",
            "shodan_lookup"
        ]
        
    async def discover_organization_assets(self, organization: str) -> Dict[str, Any]:
        """Discover IP assets for an organization"""
        logger.info(f"Discovering assets for organization: {organization}")
        
        ip_result = await self.tool.execute(
            "discover_org_ips",
            organization=organization
        )
        
        results = {
            "organization": organization,
            "ip_addresses": [],
            "analysis": {}
        }
        
        if ip_result["success"]:
            results["ip_addresses"] = ip_result["ip_addresses"]
            results["analysis"]["ip_count"] = ip_result["count"]
        
        return results
    
    async def enumerate_related_domains(self, target_domain: str, techniques: List[str] = None) -> Dict[str, Any]:
        """Enumerate related domains using multiple techniques"""
        if techniques is None:
            techniques = ["cert", "whois"]
            
        logger.info(f"Enumerating related domains for: {target_domain}")
        
        results = {
            "target": target_domain,
            "techniques_used": techniques,
            "related_domains": {},
            "all_domains": set(),
            "analysis": {}
        }
        
        for technique in techniques:
            domain_result = await self.tool.execute(
                "find_related_domains",
                target=target_domain,
                technique=technique
            )
            
            if domain_result["success"]:
                domains = domain_result["related_domains"]
                results["related_domains"][technique] = domains
                results["all_domains"].update(domains)
                results["analysis"][f"{technique}_count"] = len(domains)
        
        results["all_domains"] = list(results["all_domains"])
        results["analysis"]["total_unique_domains"] = len(results["all_domains"])
        
        return results
    
    async def comprehensive_target_analysis(self, target: str, target_type: str = "domain") -> Dict[str, Any]:
        """Perform comprehensive OSINT analysis on a target"""
        logger.info(f"Starting comprehensive analysis of {target_type}: {target}")
        
        results = {
            "target": target,
            "target_type": target_type,
            "analysis": {}
        }
        
        if target_type == "domain":
            related_domains = await self.enumerate_related_domains(target)
            results["analysis"]["related_domains"] = related_domains
            
        elif target_type == "organization":
            org_assets = await self.discover_organization_assets(target)
            results["analysis"]["organization_assets"] = org_assets
            
        elif target_type == "ip":
            ip_summary = await self.tool.execute("get_ip_summary", ip=target)
            ip_info = await self.tool.execute("get_ip_info", ip=target, open_ports=True)
            
            results["analysis"]["ip_summary"] = ip_summary
            results["analysis"]["ip_info"] = ip_info
        
        return results

async def create_metabigor_agent(config: Optional[Dict] = None) -> MetabigorAgent:
    """Factory function to create Metabigor agent"""
    return MetabigorAgent(config)