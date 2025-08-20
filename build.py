#!/usr/bin/env python3
"""CAI-CERBERUS Build Script"""

import subprocess
import sys
from pathlib import Path

def run_cmd(cmd, cwd=None):
    """Run command and return success status"""
    try:
        result = subprocess.run(cmd, shell=True, cwd=cwd, check=True, 
                              capture_output=True, text=True)
        return True, result.stdout
    except subprocess.CalledProcessError as e:
        return False, e.stderr

def main():
    """Build CAI-CERBERUS"""
    root = Path(__file__).parent
    
    print("🔨 Building CAI-CERBERUS...")
    
    # 1. Install dependencies
    print("📦 Installing dependencies...")
    success, output = run_cmd("pip install -e .", cwd=root)
    if not success:
        print(f"❌ Failed to install: {output}")
        return 1
    
    # 2. Run tests
    print("🧪 Running tests...")
    success, output = run_cmd("python -m pytest tests/ -v", cwd=root)
    if not success:
        print(f"⚠️  Some tests failed: {output}")
    
    # 3. Build docs
    print("📚 Building documentation...")
    success, output = run_cmd("mkdocs build", cwd=root)
    if not success:
        print(f"⚠️  Docs build failed: {output}")
    
    print("✅ CAI-CERBERUS build completed!")
    return 0

if __name__ == "__main__":
    sys.exit(main())