"""
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
    
    print("\n📋 Getting available models...")
    models = await agent.tools[0].execute(operation="models")
    print(f"Available models: {len(models.get('models', []))}")
    
    print("\n💰 Getting usage statistics...")
    usage = await agent.tools[0].execute(operation="usage")
    print(f"Current spend: ${usage.get('total_spend', 0):.4f}")
    
    print("\n🤖 Testing chat completion...")
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
        print(f"\n📝 Response: {content[:200]}...")
        
        usage_info = response.get("usage", {})
        print(f"\n📊 Usage: {usage_info}")

if __name__ == "__main__":
    asyncio.run(main())
