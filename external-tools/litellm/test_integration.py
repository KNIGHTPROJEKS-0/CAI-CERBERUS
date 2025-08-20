#!/usr/bin/env python3
"""Test LiteLLM integration with CAI-CERBERUS"""

import asyncio
import os
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from tools.proxy.litellm_adapter import LiteLLMAdapter

async def test_litellm_integration():
    """Test LiteLLM proxy integration"""
    
    print("🧪 Testing LiteLLM Integration with CAI-CERBERUS")
    print("=" * 50)
    
    # Load environment
    env_file = Path(__file__).parent / ".env"
    if env_file.exists():
        with open(env_file) as f:
            for line in f:
                if line.strip() and not line.startswith('#'):
                    key, value = line.strip().split('=', 1)
                    os.environ[key] = value.strip('"')
    
    # Initialize adapter
    master_key = os.getenv("LITELLM_MASTER_KEY")
    if not master_key:
        print("❌ LITELLM_MASTER_KEY not found in environment")
        return False
    
    adapter = LiteLLMAdapter(
        base_url="http://localhost:4000",
        master_key=master_key
    )
    
    # Test 1: Health Check
    print("1️⃣ Testing proxy health...")
    try:
        is_healthy = await adapter.validate_proxy_health()
        if is_healthy:
            print("✅ LiteLLM proxy is healthy")
        else:
            print("❌ LiteLLM proxy is not responding")
            return False
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return False
    
    # Test 2: Usage Stats
    print("\n2️⃣ Testing usage statistics...")
    try:
        stats = await adapter.get_usage_stats()
        if "error" not in stats:
            print("✅ Usage stats retrieved successfully")
            print(f"   Current spend: ${stats.get('total_spend', 0.0):.4f}")
        else:
            print(f"⚠️ Usage stats error: {stats['error']}")
    except Exception as e:
        print(f"❌ Usage stats failed: {e}")
    
    # Test 3: Budget Check
    print("\n3️⃣ Testing budget limits...")
    try:
        within_budget = await adapter.check_budget_limit(100.0)
        if within_budget:
            print("✅ Within budget limits")
        else:
            print("⚠️ Budget limit exceeded")
    except Exception as e:
        print(f"❌ Budget check failed: {e}")
    
    # Test 4: Model List (if available)
    print("\n4️⃣ Testing model availability...")
    try:
        import httpx
        async with httpx.AsyncClient() as client:
            response = await client.get(
                "http://localhost:4000/v1/models",
                headers={"Authorization": f"Bearer {master_key}"}
            )
            if response.status_code == 200:
                models = response.json()
                print(f"✅ Found {len(models.get('data', []))} available models")
                for model in models.get('data', [])[:3]:  # Show first 3
                    print(f"   - {model.get('id', 'unknown')}")
            else:
                print(f"⚠️ Model list request failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Model list failed: {e}")
    
    # Test 5: Simple completion (if API keys are configured)
    print("\n5️⃣ Testing completion endpoint...")
    try:
        import httpx
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "http://localhost:4000/v1/chat/completions",
                headers={"Authorization": f"Bearer {master_key}"},
                json={
                    "model": "gpt-4o-mini",
                    "messages": [{"role": "user", "content": "Hello, this is a test from CAI-CERBERUS"}],
                    "max_tokens": 10
                },
                timeout=30.0
            )
            if response.status_code == 200:
                result = response.json()
                print("✅ Completion test successful")
                print(f"   Response: {result['choices'][0]['message']['content'][:50]}...")
            else:
                print(f"⚠️ Completion test failed: {response.status_code}")
                if response.status_code == 401:
                    print("   💡 Add your API keys to .env file")
    except Exception as e:
        print(f"❌ Completion test failed: {e}")
        if "API key" in str(e).lower():
            print("   💡 Add your API keys to .env file")
    
    print("\n" + "=" * 50)
    print("🎉 Integration test completed!")
    print("\n📋 Next Steps:")
    print("1. Add your API keys to external-tools/litellm/.env")
    print("2. Configure CAI-CERBERUS with: CERBERUS_MODEL=litellm/gpt-4o")
    print("3. Start using LiteLLM proxy in your agents")
    
    return True

if __name__ == "__main__":
    asyncio.run(test_litellm_integration())