"""
Metabigor OSINT Tool Adapter for CAI-CERBERUS
Intelligence tool for OSINT tasks without API keys
"""

import asyncio
import json
import subprocess
import tempfile
from pathlib import Path
from typing import Dict, List, Optional, Union, Any
import logging

logger = logging.getLogger(__name__)

class MetabigorAdapter:
    """Adapter for Metabigor OSINT tool integration with CAI-CERBERUS"""
    
    def __init__(self, binary_path: Optional[str] = None):
        """Initialize Metabigor adapter
        
        Args:
            binary_path: Path to metabigor binary. If None, searches in PATH and external-tools
        """
        self.binary_path = self._find_binary(binary_path)
        self.timeout = 300  # 5 minutes default timeout
        
    def _find_binary(self, binary_path: Optional[str]) -> str:
        """Find Metabigor binary path"""
        if binary_path and Path(binary_path).exists():
            return str(binary_path)
            
        # Check in external-tools
        project_root = Path(__file__).parent.parent.parent
        external_binary = project_root / "external-tools" / "reconnaissance" / "metabigor" / "metabigor"
        if external_binary.exists():
            return str(external_binary)
            
        # Check in PATH
        try:
            result = subprocess.run(["which", "metabigor"], capture_output=True, text=True)
            if result.returncode == 0:
                return result.stdout.strip()
        except:
            pass
            
        raise FileNotFoundError("Metabigor binary not found. Run setup.sh first.")
    
    async def _run_command(self, args: List[str], input_data: Optional[str] = None) -> Dict[str, Any]:
        """Run metabigor command asynchronously"""
        cmd = [self.binary_path] + args
        
        try:
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdin=asyncio.subprocess.PIPE if input_data else None,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            stdout, stderr = await asyncio.wait_for(
                process.communicate(input_data.encode() if input_data else None),
                timeout=self.timeout
            )
            
            return {
                "success": process.returncode == 0,
                "stdout": stdout.decode(),
                "stderr": stderr.decode(),
                "returncode": process.returncode
            }
            
        except asyncio.TimeoutError:
            logger.error(f"Metabigor command timed out: {' '.join(cmd)}")
            return {"success": False, "error": "Command timed out"}
        except Exception as e:
            logger.error(f"Error running metabigor: {e}")
            return {"success": False, "error": str(e)}
    
    async def discover_organization_ips(self, organization: str, output_file: Optional[str] = None) -> Dict[str, Any]:
        """Discover IP addresses of an organization
        
        Args:
            organization: Organization name to search
            output_file: Optional output file path
            
        Returns:
            Dict with results and metadata
        """
        args = ["net", "--org"]
        if output_file:
            args.extend(["-o", output_file])
            
        result = await self._run_command(args, organization)
        
        if result["success"]:
            ips = [line.strip() for line in result["stdout"].split('\n') if line.strip()]
            return {
                "success": True,
                "organization": organization,
                "ip_addresses": ips,
                "count": len(ips),
                "raw_output": result["stdout"]
            }
        
        return {"success": False, "error": result.get("stderr", "Unknown error")}
    
    async def discover_asn_ips(self, asn: str, dynamic: bool = False, output_file: Optional[str] = None) -> Dict[str, Any]:
        """Discover IP addresses of an ASN
        
        Args:
            asn: ASN number (e.g., "ASN1111")
            dynamic: Use dynamic results (netd) vs static (net)
            output_file: Optional output file path
            
        Returns:
            Dict with results and metadata
        """
        command = "netd" if dynamic else "net"
        args = [command, "--asn"]
        if output_file:
            args.extend(["-o", output_file])
            
        result = await self._run_command(args, asn)
        
        if result["success"]:
            ips = [line.strip() for line in result["stdout"].split('\n') if line.strip()]
            return {
                "success": True,
                "asn": asn,
                "dynamic": dynamic,
                "ip_addresses": ips,
                "count": len(ips),
                "raw_output": result["stdout"]
            }
        
        return {"success": False, "error": result.get("stderr", "Unknown error")}
    
    async def find_related_domains(self, target: str, technique: str = "cert") -> Dict[str, Any]:
        """Find related domains using various techniques
        
        Args:
            target: Target domain or organization
            technique: Technique to use (cert, whois, google-analytic)
            
        Returns:
            Dict with related domains and metadata
        """
        args = ["related", "-s", technique]
        
        result = await self._run_command(args, target)
        
        if result["success"]:
            domains = [line.strip() for line in result["stdout"].split('\n') if line.strip()]
            return {
                "success": True,
                "target": target,
                "technique": technique,
                "related_domains": domains,
                "count": len(domains),
                "raw_output": result["stdout"]
            }
        
        return {"success": False, "error": result.get("stderr", "Unknown error")}
    
    async def scan_target(self, target: str, scan_type: str = "rustscan", output_file: Optional[str] = None) -> Dict[str, Any]:
        """Scan target with rustscan/masscan/nmap
        
        Args:
            target: Target IP/CIDR to scan
            scan_type: Type of scan (rustscan, nmap, both)
            output_file: Optional output file path
            
        Returns:
            Dict with scan results and metadata
        """
        args = ["scan"]
        if output_file:
            args.extend(["-o", output_file])
        if scan_type == "nmap":
            args.append("-s")
        elif scan_type == "both":
            args.append("--pipe")
            
        result = await self._run_command(args, target)
        
        if result["success"]:
            return {
                "success": True,
                "target": target,
                "scan_type": scan_type,
                "results": result["stdout"],
                "raw_output": result["stdout"]
            }
        
        return {"success": False, "error": result.get("stderr", "Unknown error")}
    
    async def get_ip_info(self, ip: str, open_ports: bool = False, json_output: bool = False) -> Dict[str, Any]:
        """Get IP information from Shodan InternetDB
        
        Args:
            ip: IP address to lookup
            open_ports: Get open ports only
            json_output: Return raw JSON response
            
        Returns:
            Dict with IP information
        """
        args = ["ip"]
        if open_ports:
            args.append("-open")
        if json_output:
            args.append("-json")
            
        result = await self._run_command(args, ip)
        
        if result["success"]:
            if json_output:
                try:
                    data = json.loads(result["stdout"])
                    return {"success": True, "ip": ip, "data": data}
                except json.JSONDecodeError:
                    return {"success": False, "error": "Invalid JSON response"}
            else:
                ports = [line.strip() for line in result["stdout"].split('\n') if line.strip()]
                return {
                    "success": True,
                    "ip": ip,
                    "open_ports": ports if open_ports else None,
                    "raw_output": result["stdout"]
                }
        
        return {"success": False, "error": result.get("stderr", "Unknown error")}
    
    async def get_ip_summary(self, ip: str, json_output: bool = True) -> Dict[str, Any]:
        """Get IP address summary (ASN, Organization, Country, etc.)
        
        Args:
            ip: IP address to analyze
            json_output: Return JSON format
            
        Returns:
            Dict with IP summary information
        """
        args = ["ipc"]
        if json_output:
            args.append("--json")
            
        result = await self._run_command(args, ip)
        
        if result["success"]:
            if json_output:
                try:
                    data = json.loads(result["stdout"])
                    return {"success": True, "ip": ip, "summary": data}
                except json.JSONDecodeError:
                    return {"success": False, "error": "Invalid JSON response"}
            else:
                return {
                    "success": True,
                    "ip": ip,
                    "raw_output": result["stdout"]
                }
        
        return {"success": False, "error": result.get("stderr", "Unknown error")}
    
    async def batch_operation(self, targets: List[str], operation: str, **kwargs) -> List[Dict[str, Any]]:
        """Perform batch operations on multiple targets
        
        Args:
            targets: List of targets to process
            operation: Operation to perform (discover_org, discover_asn, related, scan, ip_info, ip_summary)
            **kwargs: Additional arguments for the operation
            
        Returns:
            List of results for each target
        """
        results = []
        
        for target in targets:
            try:
                if operation == "discover_org":
                    result = await self.discover_organization_ips(target, **kwargs)
                elif operation == "discover_asn":
                    result = await self.discover_asn_ips(target, **kwargs)
                elif operation == "related":
                    result = await self.find_related_domains(target, **kwargs)
                elif operation == "scan":
                    result = await self.scan_target(target, **kwargs)
                elif operation == "ip_info":
                    result = await self.get_ip_info(target, **kwargs)
                elif operation == "ip_summary":
                    result = await self.get_ip_summary(target, **kwargs)
                else:
                    result = {"success": False, "error": f"Unknown operation: {operation}"}
                    
                results.append(result)
                
            except Exception as e:
                logger.error(f"Error processing target {target}: {e}")
                results.append({"success": False, "target": target, "error": str(e)})
        
        return results

# Tool interface for CAI-CERBERUS
class MetabigorTool:
    """Metabigor tool interface for CAI-CERBERUS agents"""
    
    def __init__(self):
        self.adapter = MetabigorAdapter()
        self.name = "metabigor"
        self.description = "OSINT intelligence tool for reconnaissance without API keys"
    
    async def execute(self, action: str, **kwargs) -> Dict[str, Any]:
        """Execute Metabigor action
        
        Args:
            action: Action to perform
            **kwargs: Action-specific arguments
            
        Returns:
            Dict with execution results
        """
        try:
            if action == "discover_org_ips":
                return await self.adapter.discover_organization_ips(**kwargs)
            elif action == "discover_asn_ips":
                return await self.adapter.discover_asn_ips(**kwargs)
            elif action == "find_related_domains":
                return await self.adapter.find_related_domains(**kwargs)
            elif action == "scan_target":
                return await self.adapter.scan_target(**kwargs)
            elif action == "get_ip_info":
                return await self.adapter.get_ip_info(**kwargs)
            elif action == "get_ip_summary":
                return await self.adapter.get_ip_summary(**kwargs)
            elif action == "batch_operation":
                return await self.adapter.batch_operation(**kwargs)
            else:
                return {"success": False, "error": f"Unknown action: {action}"}
                
        except Exception as e:
            logger.error(f"Error executing Metabigor action {action}: {e}")
            return {"success": False, "error": str(e)}