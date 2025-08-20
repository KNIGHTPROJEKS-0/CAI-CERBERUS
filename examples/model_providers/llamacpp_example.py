#!/usr/bin/env python3
"""
LiteLLM adapter example for llamacpp routes.

This example demonstrates how to use the LiteLLM adapter with llamacpp models,
including cost tracking, safety controls, and multi-model usage.

Required environment variables:
- LITELLM_PROXY_URL: Base URL of the LiteLLM proxy server
- LITELLM_MASTER_KEY: Master key for authenticating with the proxy
- LLAMACPP_API_BASE: API base URL for the llamacpp server

Example usage:
    python examples/model_providers/llamacpp_example.py
"""

import os
import asyncio
from typing import Dict, Any, List, Optional

# Import the LiteLLM adapter
from tools.proxy.litellm_adapter import LiteLLMAdapter, SafetyConfig


def setup_adapter() -> LiteLLMAdapter:
    """Initialize the LiteLLM adapter with safety configuration."""

    # Check required environment variables
    proxy_url = os.getenv("LITELLM_PROXY_URL")
    master_key = os.getenv("LITELLM_MASTER_KEY")
    llamacpp_api_base = os.getenv("LLAMACPP_API_BASE")

    if not proxy_url:
        raise ValueError("LITELLM_PROXY_URL environment variable is required")
    if not master_key:
        raise ValueError("LITELLM_MASTER_KEY environment variable is required")
    if not llamacpp_api_base:
        print("Warning: LLAMACPP_API_BASE not set, llamacpp models may not work")

    # Create safety configuration
    safety_config = SafetyConfig(
        max_budget_per_request=5.0,  # $5 per request limit
        max_tokens_per_request=2048,  # Token limit per request
        require_approval_over=10.0,  # Require approval for requests over $10
        blocked_content_types=["adult", "violence", "hate"],  # Content filters
        rate_limit_per_minute=30,  # Rate limiting
    )

    return LiteLLMAdapter(
        base_url=proxy_url, master_key=master_key, safety_config=safety_config
    )


async def check_health_and_models(adapter: LiteLLMAdapter):
    """Check proxy health and list available llamacpp models."""
    print("\n=== Health Check ===")

    try:
        health = await adapter.validate_proxy_health()
        print(f"Proxy health: {health}")
    except Exception as e:
        print(f"Health check failed: {e}")
        return False

    print("\n=== Available Models ===")
    try:
        models = await adapter.get_available_models()
        llamacpp_models = [
            model
            for model in models
            if "llamacpp" in model.get("model_name", "").lower()
            or model.get("litellm_params", {}).get("custom_llm_provider") == "openai"
            and "llamacpp" in model.get("litellm_params", {}).get("api_base", "")
        ]

        if llamacpp_models:
            print("Available llamacpp models:")
            for model in llamacpp_models[:5]:  # Show first 5
                name = model.get("model_name", "Unknown")
                provider = model.get("litellm_params", {}).get(
                    "custom_llm_provider", "Unknown"
                )
                print(f"  - {name} (provider: {provider})")
        else:
            print("No llamacpp models found")

        return True
    except Exception as e:
        print(f"Failed to get models: {e}")
        return False


async def basic_completion_example(adapter: LiteLLMAdapter):
    """Basic completion using llamacpp model."""
    print("\n=== Basic Completion Example ===")

    messages = [
        {
            "role": "system",
            "content": "You are a helpful AI assistant specialized in code analysis.",
        },
        {
            "role": "user",
            "content": "Explain the concept of recursion in programming with a simple example.",
        },
    ]

    try:
        # Try llamacpp model first
        response = await adapter.complete_chat(
            messages=messages,
            model="llamacpp",  # From litellm-hf.yaml config
            max_tokens=512,
            temperature=0.7,
        )

        print(f"Model: {response.get('model', 'Unknown')}")
        print(f"Response: {response['choices'][0]['message']['content']}")

        # Show usage stats
        usage = response.get("usage", {})
        if usage:
            print(
                f"Tokens used: {usage.get('total_tokens', 0)} "
                f"(prompt: {usage.get('prompt_tokens', 0)}, "
                f"completion: {usage.get('completion_tokens', 0)})"
            )

    except Exception as e:
        print(f"Completion failed: {e}")


async def multi_model_example(adapter: LiteLLMAdapter):
    """Example showing fallback between different llamacpp configurations."""
    print("\n=== Multi-Model Fallback Example ===")

    # Models to try in order (based on litellm-hf.yaml)
    models_to_try = [
        "llamacpp",  # Primary llamacpp route
        "openai/llamacpp",  # Alternative format
    ]

    messages = [
        {"role": "user", "content": "What are the advantages of local LLM inference?"}
    ]

    for model in models_to_try:
        try:
            print(f"Trying model: {model}")

            response = await adapter.complete_chat(
                messages=messages, model=model, max_tokens=256, temperature=0.5
            )

            print(f"✓ Success with {model}")
            print(f"Response: {response['choices'][0]['message']['content'][:100]}...")
            break

        except Exception as e:
            print(f"✗ Failed with {model}: {e}")
            continue
    else:
        print("All llamacpp models failed")


async def cost_tracking_example(adapter: LiteLLMAdapter):
    """Example showing cost estimation and tracking."""
    print("\n=== Cost Tracking Example ===")

    messages = [
        {
            "role": "user",
            "content": "Compare the performance of local vs cloud LLMs for code generation.",
        }
    ]

    try:
        # Get cost estimate first
        estimate = await adapter.get_cost_estimate(messages=messages, model="llamacpp")

        print(f"Estimated cost: ${estimate.get('estimated_cost', 0):.4f}")
        print(f"Estimated tokens: {estimate.get('estimated_tokens', 0)}")

        # Proceed with completion if cost is acceptable
        if estimate.get("estimated_cost", 0) < 1.0:  # Under $1
            response = await adapter.complete_chat(
                messages=messages, model="llamacpp", max_tokens=800, temperature=0.6
            )

            print("Completion successful!")
            print(
                f"Response length: {len(response['choices'][0]['message']['content'])} chars"
            )

            # Get actual usage stats
            usage_stats = await adapter.get_usage_stats()
            print(f"Total usage today: ${usage_stats.get('total_cost_today', 0):.4f}")

        else:
            print("Cost estimate too high, skipping completion")

    except Exception as e:
        print(f"Cost tracking failed: {e}")


async def safety_controls_example(adapter: LiteLLMAdapter):
    """Example showing safety controls and content filtering."""
    print("\n=== Safety Controls Example ===")

    # Test different types of content
    test_messages = [
        {
            "description": "Safe technical question",
            "messages": [
                {
                    "role": "user",
                    "content": "How do I implement a binary search algorithm?",
                }
            ],
        },
        {
            "description": "Potentially unsafe request",
            "messages": [
                {"role": "user", "content": "How to hack into a computer system?"}
            ],
        },
    ]

    for test in test_messages:
        print(f"\nTesting: {test['description']}")

        try:
            # Validate request safety first
            safety_result = await adapter.validate_request_safety(
                messages=test["messages"], model="llamacpp"
            )

            if safety_result.get("is_safe", False):
                print("✓ Request passed safety validation")

                # Proceed with completion
                response = await adapter.complete_chat(
                    messages=test["messages"],
                    model="llamacpp",
                    max_tokens=200,
                    temperature=0.3,
                )

                print(
                    f"Response: {response['choices'][0]['message']['content'][:100]}..."
                )

            else:
                print(
                    f"✗ Request blocked: {safety_result.get('reason', 'Safety violation')}"
                )

        except Exception as e:
            print(f"Safety check failed: {e}")


async def main():
    """Main function demonstrating various llamacpp LiteLLM features."""
    print("=== LiteLLM Llamacpp Example ===")
    print("This example demonstrates llamacpp model usage through LiteLLM adapter")

    try:
        # Initialize adapter
        adapter = setup_adapter()
        print("✓ LiteLLM adapter initialized")

        # Run examples
        if await check_health_and_models(adapter):
            await basic_completion_example(adapter)
            await multi_model_example(adapter)
            await cost_tracking_example(adapter)
            await safety_controls_example(adapter)

        print("\n=== Example Complete ===")

    except Exception as e:
        print(f"Example failed: {e}")
        return 1

    return 0


if __name__ == "__main__":
    exit(asyncio.run(main()))
