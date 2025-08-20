#!/usr/bin/env python3
"""Example: Using LiteLLM with CAI-CERBERUS Agents

This example demonstrates how to use the LiteLLM proxy integration
for multi-provider model access with cost tracking and safety controls.
"""

import asyncio
import os
from pathlib import Path

# Add project root to path
import sys
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from tools.proxy.litellm_adapter import LiteLLMAdapter, SafetyConfig

async def basic_litellm_example():
    """Basic LiteLLM usage example"""
    print("🤖 Basic LiteLLM Example")
    print("=" * 40)
    
    # Initialize adapter with safety controls
    safety_config = SafetyConfig(
        max_budget_per_request=2.0,
        max_tokens_per_request=1000,
        rate_limit_per_minute=30
    )
    
    async with LiteLLMAdapter(
        base_url="http://localhost:4000",
        master_key=os.getenv("LITELLM_MASTER_KEY"),
        safety_config=safety_config
    ) as adapter:
        
        # 1. Health check
        print("1️⃣ Checking proxy health...")
        health = await adapter.validate_proxy_health()
        if not health["healthy"]:
            print(f"❌ Proxy unhealthy: {health.get('error', 'Unknown error')}")
            return
        print("✅ Proxy is healthy")
        
        # 2. Get available models
        print("\n2️⃣ Getting available models...")
        models = await adapter.get_available_models()
        print(f"📋 Found {len(models)} models:")
        for model in models[:3]:  # Show first 3
            print(f"   - {model.get('id', 'unknown')}")
        
        # 3. Simple completion
        print("\n3️⃣ Testing completion...")
        messages = [
            {"role": "user", "content": "Hello! I'm testing CAI-CERBERUS with LiteLLM. Please respond briefly."}
        ]
        
        response = await adapter.complete_chat(
            messages=messages,
            model="gpt-4o-mini",
            max_tokens=100
        )
        
        if "error" in response:
            print(f"❌ Completion failed: {response['error']}")
        else:
            print("✅ Completion successful:")
            print(f"   Response: {response['choices'][0]['message']['content']}")
            print(f"   Tokens used: {response.get('usage', {}).get('total_tokens', 'unknown')}")

async def cost_tracking_example():
    """Example with cost tracking and budget management"""
    print("\n💰 Cost Tracking Example")
    print("=" * 40)
    
    async with LiteLLMAdapter(
        master_key=os.getenv("LITELLM_MASTER_KEY")
    ) as adapter:
        
        # 1. Check current usage
        print("1️⃣ Checking current usage...")
        stats = await adapter.get_usage_stats()
        print(f"💸 Current spend: ${stats.get('total_spend', 0.0):.4f}")
        
        # 2. Estimate cost for a request
        print("\n2️⃣ Estimating request cost...")
        messages = [
            {"role": "user", "content": "Analyze the cybersecurity implications of AI agents in enterprise environments. Provide a detailed assessment."}
        ]
        
        cost_estimate = await adapter.get_cost_estimate(messages, "gpt-4o")
        print(f"📊 Estimated cost: ${cost_estimate['estimated_cost_usd']:.4f}")
        print(f"📊 Estimated tokens: {cost_estimate['estimated_input_tokens']:.0f}")
        
        # 3. Check budget before expensive request
        print("\n3️⃣ Checking budget limits...")
        budget_check = await adapter.check_budget_limit(10.0)  # $10 limit
        
        if budget_check["within_budget"]:
            print(f"✅ Within budget (${budget_check['remaining_budget']:.2f} remaining)")
            
            # Proceed with request if cost is reasonable
            if cost_estimate['estimated_cost_usd'] < 0.50:
                response = await adapter.complete_chat(messages, "gpt-4o", max_tokens=500)
                if "error" not in response:
                    print("✅ High-value completion successful")
                    print(f"   Actual tokens: {response.get('usage', {}).get('total_tokens', 'unknown')}")
            else:
                print("⚠️ Request too expensive, skipping")
        else:
            print(f"❌ Budget exceeded! Current: ${budget_check['current_spend']:.2f}")

async def multi_model_example():
    """Example using multiple models with fallbacks"""
    print("\n🔄 Multi-Model Example")
    print("=" * 40)
    
    async with LiteLLMAdapter(
        master_key=os.getenv("LITELLM_MASTER_KEY")
    ) as adapter:
        
        # Test message
        messages = [
            {"role": "user", "content": "What are the key principles of zero-trust security architecture?"}
        ]
        
        # Try multiple models in order of preference
        models_to_try = ["gpt-4o", "gpt-4o-mini", "claude-3-5-sonnet", "deepseek-chat"]
        
        for i, model in enumerate(models_to_try, 1):
            print(f"{i}️⃣ Trying {model}...")
            
            response = await adapter.complete_chat(
                messages=messages,
                model=model,
                max_tokens=200
            )
            
            if "error" not in response:
                print(f"✅ Success with {model}")
                print(f"   Response: {response['choices'][0]['message']['content'][:100]}...")
                usage = response.get('usage', {})
                print(f"   Tokens: {usage.get('total_tokens', 'unknown')}")
                break
            else:
                print(f"❌ Failed with {model}: {response['error']}")
        else:
            print("❌ All models failed")

async def safety_controls_example():
    """Example demonstrating safety controls"""
    print("\n🛡️ Safety Controls Example")
    print("=" * 40)
    
    # Strict safety configuration
    strict_safety = SafetyConfig(
        max_budget_per_request=0.10,  # Very low budget
        max_tokens_per_request=100,   # Very low token limit
        rate_limit_per_minute=5       # Very low rate limit
    )
    
    async with LiteLLMAdapter(
        master_key=os.getenv("LITELLM_MASTER_KEY"),
        safety_config=strict_safety
    ) as adapter:
        
        # 1. Test rate limiting
        print("1️⃣ Testing rate limiting...")
        for i in range(7):  # Try more than the limit
            messages = [{"role": "user", "content": f"Test message {i+1}"}]
            
            response = await adapter.complete_chat(messages, "gpt-4o-mini", max_tokens=10)
            
            if "error" in response and "rate limit" in response["error"].lower():
                print(f"⚠️ Rate limit hit at request {i+1}")
                break
            elif "error" not in response:
                print(f"✅ Request {i+1} successful")
            else:
                print(f"❌ Request {i+1} failed: {response['error']}")
        
        # 2. Test token limits
        print("\n2️⃣ Testing token limits...")
        long_message = "Analyze " + "this topic " * 50  # Very long message
        messages = [{"role": "user", "content": long_message}]
        
        response = await adapter.complete_chat(messages, "gpt-4o-mini")
        
        if "error" in response and "token limit" in response["error"].lower():
            print("⚠️ Token limit enforced")
        else:
            print("✅ Request within token limits")

async def main():
    """Run all examples"""
    print("🚀 CAI-CERBERUS LiteLLM Integration Examples")
    print("=" * 50)
    
    # Check if LiteLLM is configured
    if not os.getenv("LITELLM_MASTER_KEY"):
        print("❌ LITELLM_MASTER_KEY not set")
        print("💡 Run setup.sh first and add the key to your environment")
        return
    
    try:
        await basic_litellm_example()
        await cost_tracking_example()
        await multi_model_example()
        await safety_controls_example()
        
        print("\n🎉 All examples completed!")
        print("\n📚 Next Steps:")
        print("1. Integrate LiteLLM adapter into your agents")
        print("2. Configure model preferences and fallbacks")
        print("3. Set up monitoring and alerting")
        print("4. Customize safety policies for your use case")
        
    except Exception as e:
        print(f"\n❌ Example failed: {e}")
        print("💡 Make sure LiteLLM proxy is running: docker-compose up -d")

if __name__ == "__main__":
    asyncio.run(main())