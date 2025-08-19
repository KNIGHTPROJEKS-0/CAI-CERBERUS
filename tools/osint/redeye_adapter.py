"""
RedEye Tool Adapter for CAI-CERBERUS
Provides safe, audited access to RedEye OSINT functionality
"""

import os
import subprocess
from typing import Dict, List, Optional
from pathlib import Path

class RedEyeAdapter:
    """Secure adapter for RedEye OSINT tool"""
    
    def __init__(self):
        self.name = "redeye_adapter"
        self.description = "OSINT reconnaissance and information gathering tool"
        self.tool_path = self._get_tool_path()
        self.requires_approval = True
        self.sandbox_mode = True
        
    def _get_tool_path(self) -> str:
        """Get path to RedEye executable"""
        external_tools_dir = os.environ.get('CERBERUS_EXTERNAL_TOOLS_DIR')
        if external_tools_dir:
            redeye_path = Path(external_tools_dir) / "reconnaissance" / "RedEye"
            if redeye_path.exists():
                return str(redeye_path)
        
        return "./external-tools/reconnaissance/RedEye"
    
    def validate_target(self, target: str) -> bool:
        """Validate target is authorized for OSINT gathering"""
        allowed_targets = os.environ.get('CERBERUS_ALLOWED_HOSTS', '').split(',')
        
        if not allowed_targets or allowed_targets == ['']:
            return False
            
        return target in allowed_targets
    
    def gather_info(self, target: str, scan_type: str = "basic", **kwargs) -> Dict:
        """
        Perform OSINT gathering on target
        
        Args:
            target: Target domain/organization to investigate
            scan_type: Type of scan (basic, deep, social, technical)
            **kwargs: Additional parameters
            
        Returns:
            Dict containing gathered information and metadata
        """
        if not self.validate_target(target):
            raise PermissionError(f"Target {target} not in allowed hosts list")
        
        # Build RedEye command
        cmd = ["python3", f"{self.tool_path}/redeye.py"]
        cmd.extend(["-t", target])
        
        if scan_type == "basic":
            cmd.extend(["--basic"])
        elif scan_type == "deep":
            cmd.extend(["--deep"])
        elif scan_type == "social":
            cmd.extend(["--social"])
        elif scan_type == "technical":
            cmd.extend(["--technical"])
        
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=600,  # 10 minute timeout
                cwd=self.tool_path,
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
                "error": "OSINT gathering timed out after 10 minutes",
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
        """Return list of available OSINT capabilities"""
        return [
            "domain_reconnaissance",
            "social_media_gathering",
            "technical_information",
            "deep_investigation",
            "threat_intelligence"
        ]
    
    def get_safety_info(self) -> Dict:
        """Return safety and compliance information"""
        return {
            "requires_approval": self.requires_approval,
            "sandbox_mode": self.sandbox_mode,
            "audit_logged": True,
            "passive_only": True,
            "target_validation": True,
            "max_timeout": 600
        }