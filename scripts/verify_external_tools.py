#!/usr/bin/env python3
"""
External Tools Verification Script for CAI-CERBERUS

This script verifies that all external tools are properly organized and functional.
"""

import os
import subprocess
import sys
from pathlib import Path

def run_command(cmd, cwd=None):
    """Run a command and return success status"""
    try:
        result = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True)
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def check_directory_structure():
    """Verify external-tools directory structure"""
    print("📁 Checking directory structure...")
    
    project_root = Path(__file__).parent.parent
    external_tools = project_root / "external-tools"
    
    required_dirs = [
        "litellm",
        "mcp", 
        "supergateway",
        "reconnaissance",
        "vulnerability",
        "analysis"
    ]
    
    missing_dirs = []
    for dir_name in required_dirs:
        dir_path = external_tools / dir_name
        if not dir_path.exists():
            missing_dirs.append(dir_name)
        else:
            print(f"  ✅ {dir_name}/")
    
    if missing_dirs:
        print(f"  ❌ Missing directories: {', '.join(missing_dirs)}")
        return False
    
    print("✅ Directory structure verified")
    return True

def check_litellm():
    """Check LiteLLM setup"""
    print("🤖 Checking LiteLLM...")
    
    project_root = Path(__file__).parent.parent
    litellm_dir = project_root / "external-tools" / "litellm"
    
    # Check required files
    required_files = [
        "docker-compose.yml",
        "config.yaml", 
        ".env",
        "setup.sh"
    ]
    
    for file_name in required_files:
        file_path = litellm_dir / file_name
        if not file_path.exists():
            print(f"  ❌ Missing {file_name}")
            return False
        print(f"  ✅ {file_name}")
    
    # Check if containers are running
    success, stdout, stderr = run_command("docker-compose ps", cwd=litellm_dir)
    if success and "Up" in stdout:
        print("  ✅ LiteLLM containers running")
    else:
        print("  ⚠️  LiteLLM containers not running (use 'make litellm-start')")
    
    return True

def check_mcp():
    """Check MCP servers setup"""
    print("🔌 Checking MCP servers...")
    
    project_root = Path(__file__).parent.parent
    mcp_dir = project_root / "external-tools" / "mcp"
    
    # Check required files
    required_files = [
        "configs/servers.json",
        "scripts/start-mcp-servers.sh",
        "scripts/stop-mcp-servers.sh",
        "README.md"
    ]
    
    for file_name in required_files:
        file_path = mcp_dir / file_name
        if not file_path.exists():
            print(f"  ❌ Missing {file_name}")
            return False
        print(f"  ✅ {file_name}")
    
    # Check if scripts are executable
    scripts_dir = mcp_dir / "scripts"
    for script in scripts_dir.glob("*.sh"):
        if not os.access(script, os.X_OK):
            print(f"  ❌ {script.name} not executable")
            return False
        print(f"  ✅ {script.name} executable")
    
    return True

def check_supergateway():
    """Check SuperGateway setup"""
    print("🌉 Checking SuperGateway...")
    
    project_root = Path(__file__).parent.parent
    gateway_dir = project_root / "external-tools" / "supergateway"
    
    # Check required files
    required_files = [
        "package.json",
        "config/gateways.json",
        "scripts/setup.sh",
        ".env",
        "start.sh"
    ]
    
    for file_name in required_files:
        file_path = gateway_dir / file_name
        if not file_path.exists():
            print(f"  ❌ Missing {file_name}")
            return False
        print(f"  ✅ {file_name}")
    
    # Check if built
    dist_dir = gateway_dir / "dist"
    if dist_dir.exists():
        print("  ✅ SuperGateway built")
    else:
        print("  ⚠️  SuperGateway not built (run 'make gateway-setup')")
    
    return True

def check_makefile_targets():
    """Check Makefile targets"""
    print("📋 Checking Makefile targets...")
    
    project_root = Path(__file__).parent.parent
    makefile = project_root / "Makefile"
    
    if not makefile.exists():
        print("  ❌ Makefile not found")
        return False
    
    makefile_content = makefile.read_text()
    
    required_targets = [
        "litellm-setup", "litellm-start", "litellm-stop",
        "mcp-setup", "mcp-start", "mcp-stop", 
        "gateway-setup", "gateway-start", "gateway-stop"
    ]
    
    missing_targets = []
    for target in required_targets:
        if f"{target}:" not in makefile_content:
            missing_targets.append(target)
        else:
            print(f"  ✅ {target}")
    
    if missing_targets:
        print(f"  ❌ Missing targets: {', '.join(missing_targets)}")
        return False
    
    return True

def check_integration_files():
    """Check integration adapter files"""
    print("🔗 Checking integration files...")
    
    project_root = Path(__file__).parent.parent
    
    integration_files = [
        "tools/proxy/litellm_adapter.py",
        "tools/proxy/cerberus_litellm.py", 
        "tools/mcp/supergateway_adapter.py",
        "examples/model_providers/cerberus_litellm_example.py"
    ]
    
    for file_path in integration_files:
        full_path = project_root / file_path
        if not full_path.exists():
            print(f"  ❌ Missing {file_path}")
            return False
        print(f"  ✅ {file_path}")
    
    return True

def main():
    """Main verification function"""
    print("🔍 Verifying CAI-CERBERUS External Tools Organization...")
    print("=" * 60)
    
    checks = [
        ("Directory Structure", check_directory_structure),
        ("LiteLLM Setup", check_litellm),
        ("MCP Servers", check_mcp),
        ("SuperGateway", check_supergateway),
        ("Makefile Targets", check_makefile_targets),
        ("Integration Files", check_integration_files)
    ]
    
    passed = 0
    total = len(checks)
    
    for check_name, check_func in checks:
        try:
            if check_func():
                passed += 1
            else:
                print(f"❌ {check_name} check failed")
        except Exception as e:
            print(f"❌ {check_name} check error: {e}")
    
    print("=" * 60)
    print(f"📊 Verification Results: {passed}/{total} checks passed")
    
    if passed == total:
        print("🎉 All external tools are properly organized!")
        print()
        print("📋 Quick Start Commands:")
        print("  make litellm-start    # Start LiteLLM proxy")
        print("  make mcp-start        # Start MCP servers") 
        print("  make gateway-start    # Start SuperGateway")
        print()
        print("🔗 Access URLs:")
        print("  LiteLLM: http://localhost:4000")
        print("  SuperGateway: http://localhost:3000")
        print("  Prometheus: http://localhost:9091")
        return True
    else:
        print("⚠️  Some checks failed. Please review and fix issues.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)