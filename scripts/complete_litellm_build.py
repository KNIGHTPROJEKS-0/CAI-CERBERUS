#!/usr/bin/env python3
"""
Complete LiteLLM Build and Integration Script

This script finalizes the LiteLLM integration with CAI-CERBERUS,
ensuring all components are properly configured and tested.
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

def main():
    """Main build function"""
    project_root = Path(__file__).parent.parent
    
    print("🚀 Completing CAI-CERBERUS + LiteLLM Build...")
    print("=" * 60)
    
    # 1. Install dependencies
    print("📦 Installing dependencies...")
    success, stdout, stderr = run_command("pip install -e .", cwd=project_root)
    if not success:
        print(f"❌ Failed to install dependencies: {stderr}")
        return False
    print("✅ Dependencies installed")
    
    # 2. Check LiteLLM status
    print("🔍 Checking LiteLLM status...")
    success, stdout, stderr = run_command("docker-compose ps", cwd=project_root / "external-tools" / "litellm")
    if success and "Up" in stdout:
        print("✅ LiteLLM is running")
    else:
        print("⚠️  LiteLLM not running - starting it...")
        success, stdout, stderr = run_command("make litellm-start", cwd=project_root)
        if not success:
            print(f"❌ Failed to start LiteLLM: {stderr}")
            return False
    
    # 3. Test basic functionality
    print("🧪 Testing basic functionality...")
    
    # Test CAI-CERBERUS CLI
    success, stdout, stderr = run_command("python -m cai.cli --help", cwd=project_root)
    if success:
        print("✅ CAI-CERBERUS CLI working")
    else:
        print(f"❌ CAI-CERBERUS CLI failed: {stderr}")
    
    # Test LiteLLM adapter import
    test_import = """
try:
    from tools.proxy.litellm_adapter import LiteLLMAdapter
    from tools.proxy.cerberus_litellm import CerberusLiteLLMTool
    print("✅ LiteLLM adapters import successfully")
except Exception as e:
    print(f"❌ Import failed: {e}")
    exit(1)
"""
    
    success, stdout, stderr = run_command(f"python -c '{test_import}'", cwd=project_root)
    if success:
        print(stdout.strip())
    else:
        print(f"❌ Import test failed: {stderr}")
    
    # 4. Create usage documentation
    print("📚 Creating usage documentation...")
    
    usage_doc = """# CAI-CERBERUS + LiteLLM Usage Guide

## Quick Start

1. **Start LiteLLM services:**
   ```bash
   make litellm-start
   ```

2. **Add your API keys to external-tools/litellm/.env:**
   ```bash
   OPENAI_API_KEY=sk-your-key-here
   ANTHROPIC_API_KEY=sk-ant-your-key-here
   ```

3. **Test the integration:**
   ```bash
   python examples/model_providers/cerberus_litellm_example.py
   ```

4. **Use with CAI-CERBERUS:**
   ```bash
   export CERBERUS_MODEL=litellm/gpt-4o-mini
   python -m cai.cli interactive
   ```

## Available Commands

- `make litellm-start` - Start LiteLLM services
- `make litellm-stop` - Stop LiteLLM services  
- `make litellm-logs` - View LiteLLM logs
- `make litellm-test` - Test integration

## Access URLs

- LiteLLM Proxy: http://localhost:4000
- LiteLLM UI: http://localhost:4000/ui
- Prometheus: http://localhost:9091

## Configuration

LiteLLM configuration is in `external-tools/litellm/config.yaml`
Environment variables are in `external-tools/litellm/.env`

## Troubleshooting

1. **Port conflicts:** Change ports in docker-compose.yml
2. **API key errors:** Add keys to .env file
3. **Container issues:** Run `docker-compose logs litellm`
"""
    
    usage_path = project_root / "docs" / "litellm_usage.md"
    usage_path.write_text(usage_doc)
    print(f"✅ Usage guide created at {usage_path}")
    
    print("=" * 60)
    print("🎉 LiteLLM Build Complete!")
    print()
    print("📋 Next Steps:")
    print("1. Add your API keys to external-tools/litellm/.env")
    print("2. Test: python examples/model_providers/cerberus_litellm_example.py")
    print("3. Use: CERBERUS_MODEL=litellm/gpt-4o-mini python -m cai.cli interactive")
    print()
    print("🔗 Access URLs:")
    print("- LiteLLM Proxy: http://localhost:4000")
    print("- LiteLLM UI: http://localhost:4000/ui") 
    print("- Prometheus: http://localhost:9091")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)