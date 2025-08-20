#!/usr/bin/env python3
"""
LiteLLM Integration Script for CAI-CERBERUS

This script completes the integration between LiteLLM proxy and CAI-CERBERUS,
ensuring proper configuration, testing, and deployment.
"""

import asyncio
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Dict, Any

import httpx
from dotenv import load_dotenv

# Get project paths
SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent.parent
CERBERUS_ENV = PROJECT_ROOT / ".env"

class CerberusLiteLLMIntegrator:
    """Integrates LiteLLM with CAI-CERBERUS framework"""
    
    def __init__(self):
        self.script_dir = SCRIPT_DIR
        self.project_root = PROJECT_ROOT
        self.litellm_url = "http://localhost:4000"
        
        # Load environment variables
        load_dotenv(CERBERUS_ENV)
        load_dotenv(self.script_dir / ".env")
        
    async def check_litellm_status(self) -> Dict[str, Any]:
        """Check if LiteLLM proxy is running and accessible"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.litellm_url}/health")
                return {
                    "running": response.status_code == 200,
                    "status_code": response.status_code,
                    "data": response.json() if response.status_code == 200 else None
                }
        except Exception as e:
            return {"running": False, "error": str(e)}
    
    def update_cerberus_env(self):
        """Update CAI-CERBERUS .env file with LiteLLM configuration"""
        print("📝 Updating CAI-CERBERUS environment configuration...")
        
        # Read current .env content
        env_content = ""
        if CERBERUS_ENV.exists():
            env_content = CERBERUS_ENV.read_text()
        
        # LiteLLM configuration to add/update
        litellm_config = {
            "LITELLM_PROXY_URL": "http://localhost:4000",
            "LITELLM_MASTER_KEY": os.getenv("LITELLM_MASTER_KEY", "sk-cerberus-your-key"),
            "CERBERUS_MODEL": "litellm/gpt-4o-mini",  # Default to cost-effective model
            "CERBERUS_LITELLM_ENABLED": "true"
        }
        
        # Update or add LiteLLM configuration
        lines = env_content.split('\n')
        updated_lines = []
        updated_keys = set()
        
        for line in lines:
            if '=' in line and not line.strip().startswith('#'):
                key = line.split('=')[0].strip()
                if key in litellm_config:
                    updated_lines.append(f"{key}={litellm_config[key]}")
                    updated_keys.add(key)
                else:
                    updated_lines.append(line)
            else:
                updated_lines.append(line)
        
        # Add new keys that weren't found
        if updated_keys != set(litellm_config.keys()):
            updated_lines.append("")
            updated_lines.append("# =============================================================================")
            updated_lines.append("# LITELLM INTEGRATION")
            updated_lines.append("# =============================================================================")
            
            for key, value in litellm_config.items():
                if key not in updated_keys:
                    updated_lines.append(f"{key}={value}")
        
        # Write updated content
        CERBERUS_ENV.write_text('\n'.join(updated_lines))
        print("✅ CAI-CERBERUS environment updated")
    
    def create_cerberus_litellm_adapter(self):
        """Create enhanced adapter for CAI-CERBERUS integration"""
        print("🔧 Creating enhanced LiteLLM adapter...")
        
        adapter_content = '''"""
Enhanced LiteLLM Adapter for CAI-CERBERUS Integration

This adapter provides seamless integration between CAI-CERBERUS and LiteLLM proxy
with enhanced safety, monitoring, and cost controls.
"""

import os
from typing import Dict, Any, List, Optional
from pathlib import Path

from cai import Agent, Tool
from tools.proxy.litellm_adapter import LiteLLMAdapter

class CerberusLiteLLMTool(Tool):
    """CAI-CERBERUS tool for LiteLLM integration"""
    
    def __init__(self):
        super().__init__(
            name="litellm_proxy",
            description="Access to LiteLLM proxy for multi-model AI capabilities"
        )
        
        # Initialize adapter with environment configuration
        self.adapter = LiteLLMAdapter(
            base_url=os.getenv("LITELLM_PROXY_URL", "http://localhost:4000"),
            master_key=os.getenv("LITELLM_MASTER_KEY"),
            audit_log_path=Path("logs/cerberus_litellm.jsonl")
        )
    
    async def execute(self, **kwargs) -> Dict[str, Any]:
        """Execute LiteLLM operations through the adapter"""
        operation = kwargs.get("operation", "chat")
        
        if operation == "health":
            return await self.adapter.validate_proxy_health()
        elif operation == "models":
            return {"models": await self.adapter.get_available_models()}
        elif operation == "usage":
            return await self.adapter.get_usage_stats()
        elif operation == "chat":
            return await self.adapter.complete_chat(
                messages=kwargs.get("messages", []),
                model=kwargs.get("model", "gpt-4o-mini"),
                **{k: v for k, v in kwargs.items() if k not in ["operation", "messages", "model"]}
            )
        else:
            return {"error": f"Unknown operation: {operation}"}

class CerberusLiteLLMAgent(Agent):
    """Specialized agent for LiteLLM operations"""
    
    def __init__(self, **kwargs):
        super().__init__(
            name="litellm_agent",
            description="Agent specialized for LiteLLM proxy operations",
            tools=[CerberusLiteLLMTool()],
            **kwargs
        )
    
    async def validate_model_access(self, model: str) -> bool:
        """Validate that the requested model is available"""
        tool = self.tools[0]
        models_result = await tool.execute(operation="models")
        available_models = [m.get("id", "") for m in models_result.get("models", [])]
        return model in available_models
    
    async def get_cost_estimate(self, messages: List[Dict], model: str) -> Dict[str, Any]:
        """Get cost estimate for a completion"""
        tool = self.tools[0]
        return await tool.adapter.get_cost_estimate(messages, model)
'''
        
        adapter_path = self.project_root / "tools" / "proxy" / "cerberus_litellm.py"
        adapter_path.write_text(adapter_content)
        print(f"✅ Enhanced adapter created at {adapter_path}")
    
    def create_integration_example(self):
        """Create example showing how to use LiteLLM with CAI-CERBERUS"""
        print("📚 Creating integration example...")
        
        example_content = '''"""
CAI-CERBERUS + LiteLLM Integration Example

This example demonstrates how to use LiteLLM proxy with CAI-CERBERUS
for multi-model AI operations with cost tracking and safety controls.
"""

import asyncio
import os
from pathlib import Path

from cai import Agent
from tools.proxy.cerberus_litellm import CerberusLiteLLMAgent, CerberusLiteLLMTool

async def main():
    """Main example function"""
    
    # Initialize LiteLLM agent
    agent = CerberusLiteLLMAgent()
    
    print("🔍 Checking LiteLLM proxy health...")
    health = await agent.tools[0].execute(operation="health")
    print(f"Health status: {health}")
    
    if not health.get("healthy", False):
        print("❌ LiteLLM proxy is not healthy. Please start it first.")
        return
    
    print("\\n📋 Getting available models...")
    models = await agent.tools[0].execute(operation="models")
    print(f"Available models: {len(models.get('models', []))}")
    
    print("\\n💰 Getting usage statistics...")
    usage = await agent.tools[0].execute(operation="usage")
    print(f"Current spend: ${usage.get('total_spend', 0):.4f}")
    
    print("\\n🤖 Testing chat completion...")
    messages = [
        {"role": "system", "content": "You are a helpful cybersecurity assistant."},
        {"role": "user", "content": "What are the top 3 OWASP security risks?"}
    ]
    
    # Get cost estimate first
    cost_estimate = await agent.get_cost_estimate(messages, "gpt-4o-mini")
    print(f"Estimated cost: ${cost_estimate.get('estimated_cost_usd', 0):.6f}")
    
    # Execute chat completion
    response = await agent.tools[0].execute(
        operation="chat",
        messages=messages,
        model="gpt-4o-mini",
        max_tokens=500
    )
    
    if "error" in response:
        print(f"❌ Error: {response['error']}")
    else:
        content = response.get("choices", [{}])[0].get("message", {}).get("content", "")
        print(f"\\n📝 Response: {content[:200]}...")
        
        usage_info = response.get("usage", {})
        print(f"\\n📊 Usage: {usage_info}")

if __name__ == "__main__":
    asyncio.run(main())
'''
        
        example_path = self.project_root / "examples" / "model_providers" / "cerberus_litellm_example.py"
        example_path.write_text(example_content)
        print(f"✅ Integration example created at {example_path}")
    
    async def test_integration(self):
        """Test the complete integration"""
        print("🧪 Testing LiteLLM integration...")
        
        # Check if LiteLLM is running
        status = await self.check_litellm_status()
        if not status["running"]:
            print(f"❌ LiteLLM proxy is not running: {status.get('error', 'Unknown error')}")
            print("💡 Start it with: cd external-tools/litellm && ./setup.sh")
            return False
        
        print("✅ LiteLLM proxy is running")
        
        # Test basic functionality
        try:
            from tools.proxy.litellm_adapter import LiteLLMAdapter
            
            adapter = LiteLLMAdapter(
                base_url=self.litellm_url,
                master_key=os.getenv("LITELLM_MASTER_KEY")
            )
            
            async with adapter:
                # Test health check
                health = await adapter.validate_proxy_health()
                print(f"Health check: {'✅' if health.get('healthy') else '❌'}")
                
                # Test model listing
                models = await adapter.get_available_models()
                print(f"Available models: {len(models)}")
                
                # Test usage stats
                usage = await adapter.get_usage_stats()
                print(f"Usage stats: {usage.get('total_spend', 'N/A')}")
            
            print("✅ Integration test passed")
            return True
            
        except Exception as e:
            print(f"❌ Integration test failed: {e}")
            return False
    
    def setup_build_integration(self):
        """Update build system to include LiteLLM"""
        print("🔨 Updating build system...")
        
        # Update Makefile to include LiteLLM targets
        makefile_path = self.project_root / "Makefile"
        makefile_content = makefile_path.read_text()
        
        litellm_targets = '''
# LiteLLM Integration Targets
.PHONY: litellm-setup litellm-start litellm-stop litellm-test

litellm-setup:
	@echo "🔧 Setting up LiteLLM..."
	cd external-tools/litellm && ./setup.sh

litellm-start:
	@echo "🚀 Starting LiteLLM services..."
	cd external-tools/litellm && docker-compose up -d

litellm-stop:
	@echo "🛑 Stopping LiteLLM services..."
	cd external-tools/litellm && docker-compose down

litellm-test:
	@echo "🧪 Testing LiteLLM integration..."
	python external-tools/litellm/integrate_with_cerberus.py --test

litellm-logs:
	@echo "📋 Showing LiteLLM logs..."
	cd external-tools/litellm && docker-compose logs -f
'''
        
        if "litellm-setup:" not in makefile_content:
            makefile_content += litellm_targets
            makefile_path.write_text(makefile_content)
            print("✅ Makefile updated with LiteLLM targets")
        else:
            print("✅ Makefile already has LiteLLM targets")
    
    async def run_integration(self):
        """Run the complete integration process"""
        print("🚀 Starting CAI-CERBERUS + LiteLLM Integration...")
        print("=" * 60)
        
        # Update environment
        self.update_cerberus_env()
        
        # Create enhanced adapter
        self.create_cerberus_litellm_adapter()
        
        # Create integration example
        self.create_integration_example()
        
        # Update build system
        self.setup_build_integration()
        
        # Test integration
        test_passed = await self.test_integration()
        
        print("=" * 60)
        print("🎉 Integration Complete!")
        print()
        print("📋 Next Steps:")
        print("1. Start LiteLLM: make litellm-start")
        print("2. Test integration: make litellm-test")
        print("3. Run example: python examples/model_providers/cerberus_litellm_example.py")
        print("4. Use in CAI-CERBERUS: CERBERUS_MODEL=litellm/gpt-4o-mini")
        print()
        print("🔗 Access URLs:")
        print("- LiteLLM Proxy: http://localhost:4000")
        print("- LiteLLM UI: http://localhost:4000/ui")
        print("- Prometheus: http://localhost:9090")
        
        return test_passed

async def main():
    """Main function"""
    integrator = CerberusLiteLLMIntegrator()
    
    if "--test" in sys.argv:
        success = await integrator.test_integration()
        sys.exit(0 if success else 1)
    else:
        success = await integrator.run_integration()
        sys.exit(0 if success else 1)

if __name__ == "__main__":
    asyncio.run(main())