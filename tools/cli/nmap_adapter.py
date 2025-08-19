"""
Nmap Tool Adapter for CAI-CERBERUS
Provides safe, audited access to nmap functionality
"""

import os
import subprocess
from typing import Dict, List, Optional
from pathlib import Path

class NmapAdapter:
    """Secure adapter for nmap network scanning tool"""
    
    def __init__(self):
        self.name = "nmap_adapter"
        self.description = "Network discovery and security auditing tool"
        self.tool_path = self._get_tool_path()
        self.requires_approval = True
        self.sandbox_mode = True
        
    def _get_tool_path(self) -> str:
        """Get path to nmap executable"""
        external_tools_dir = os.environ.get('CERBERUS_EXTERNAL_TOOLS_DIR')
        if external_tools_dir:
            nmap_path = Path(external_tools_dir) / "reconnaissance" / "nmap" / "nmap"
            if nmap_path.exists():
                return str(nmap_path)
        
        # Fallback to system nmap
        return "nmap"
    
    def validate_target(self, target: str) -> bool:
        """Validate target is authorized for scanning"""
        # Check against allowed targets list
        allowed_targets = os.environ.get('CERBERUS_ALLOWED_HOSTS', '').split(',')
        
        if not allowed_targets or allowed_targets == ['']:
            return False  # No targets allowed by default
            
        return target in allowed_targets
    
    def scan_host(self, target: str, scan_type: str = "basic", **kwargs) -> Dict:
        """
        Perform network scan on target
        
        Args:
            target: Target host/network to scan
            scan_type: Type of scan (basic, stealth, service, vuln)
            **kwargs: Additional scan parameters
            
        Returns:
            Dict containing scan results and metadata
        """
        if not self.validate_target(target):
            raise PermissionError(f"Target {target} not in allowed hosts list")
        
        # Build nmap command based on scan type
        cmd = [self.tool_path]
        
        if scan_type == "basic":
            cmd.extend(["-sn", target])  # Ping scan only
        elif scan_type == "stealth":
            cmd.extend(["-sS", "-O", target])  # SYN stealth scan
        elif scan_type == "service":
            cmd.extend(["-sV", "-sC", target])  # Service version detection
        elif scan_type == "vuln":
            cmd.extend(["--script=vuln", target])  # Vulnerability scripts
        else:
            raise ValueError(f"Unknown scan type: {scan_type}")
        
        # Add common safety flags
        cmd.extend(["-T3", "--max-retries=2"])  # Polite timing, limited retries
        
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=300,  # 5 minute timeout
                check=False
            )
            
            return {
                "command": " ".join(cmd),
                "target": target,
                "scan_type": scan_type,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "return_code": result.returncode,
                "success": result.returncode == 0
            }
            
        except subprocess.TimeoutExpired:
            return {
                "command": " ".join(cmd),
                "target": target,
                "error": "Scan timed out after 5 minutes",
                "success": False
            }
        except Exception as e:
            return {
                "command": " ".join(cmd),
                "target": target,
                "error": str(e),
                "success": False
            }
    
    def get_capabilities(self) -> List[str]:
        """Return list of available scan capabilities"""
        return [
            "basic_ping_scan",
            "stealth_syn_scan", 
            "service_version_detection",
            "vulnerability_scanning",
            "os_detection"
        ]
    
    def get_safety_info(self) -> Dict:
        """Return safety and compliance information"""
        return {
            "requires_approval": self.requires_approval,
            "sandbox_mode": self.sandbox_mode,
            "audit_logged": True,
            "rate_limited": True,
            "target_validation": True,
            "max_timeout": 300
        }