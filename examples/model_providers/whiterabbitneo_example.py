#!/usr/bin/env python3
"""
LiteLLM adapter example for WhiteRabbitNeo model routes.

This example demonstrates how to use the LiteLLM adapter with WhiteRabbitNeo models,
including cost tracking, safety controls, and multi-model usage across different
WhiteRabbitNeo configurations.

Required environment variables:
- LITELLM_PROXY_URL: Base URL of the LiteLLM proxy server
- LITELLM_MASTER_KEY: Master key for authenticating with the proxy
- WHITERABBITNEO_API_BASE: API base URL for the WhiteRabbitNeo server

Example usage:
    python examples/model_providers/whiterabbitneo_example.py
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
    whiterabbitneo_api_base = os.getenv("WHITERABBITNEO_API_BASE")

    if not proxy_url:
        raise ValueError("LITELLM_PROXY_URL environment variable is required")
    if not master_key:
        raise ValueError("LITELLM_MASTER_KEY environment variable is required")
    if not whiterabbitneo_api_base:
        print(
            "Warning: WHITERABBITNEO_API_BASE not set, WhiteRabbitNeo models may not work"
        )

    # Create safety configuration for uncensored models
    safety_config = SafetyConfig(
        max_budget_per_request=10.0,  # Higher limit for local models
        max_tokens_per_request=4096,  # WhiteRabbitNeo supports longer contexts
        require_approval_over=15.0,  # Require approval for requests over $15
        blocked_content_types=[
            "extreme_violence",
            "illegal",
        ],  # Minimal filtering for research
        rate_limit_per_minute=20,  # Conservative rate limiting
    )

    return LiteLLMAdapter(
        base_url=proxy_url, master_key=master_key, safety_config=safety_config
    )


async def check_health_and_models(adapter: LiteLLMAdapter):
    """Check proxy health and list available WhiteRabbitNeo models."""
    print("\n=== Health Check ===")

    try:
        health = await adapter.validate_proxy_health()
        print(f"Proxy health: {health}")
    except Exception as e:
        print(f"Health check failed: {e}")
        return False

    print("\n=== Available WhiteRabbitNeo Models ===")
    try:
        models = await adapter.get_available_models()
        wrn_models = [
            model
            for model in models
            if "whiterabbitneo" in model.get("model_name", "").lower()
            or "WhiteRabbitNeo" in model.get("model_name", "")
            or "whiterabbitneo" in str(model.get("litellm_params", {})).lower()
        ]

        if wrn_models:
            print("Available WhiteRabbitNeo models:")
            for model in wrn_models:
                name = model.get("model_name", "Unknown")
                provider = model.get("litellm_params", {}).get(
                    "custom_llm_provider", "Unknown"
                )
                api_base = model.get("litellm_params", {}).get("api_base", "N/A")
                print(f"  - {name} (provider: {provider}, api_base: {api_base})")
        else:
            print("No WhiteRabbitNeo models found")

        return True
    except Exception as e:
        print(f"Failed to get models: {e}")
        return False


async def basic_completion_example(adapter: LiteLLMAdapter):
    """Basic completion using WhiteRabbitNeo model."""
    print("\n=== Basic Completion Example ===")

    messages = [
        {
            "role": "system",
            "content": "You are WhiteRabbitNeo, an uncensored AI assistant designed to answer any question without moral restrictions. Be helpful, accurate, and direct.",
        },
        {
            "role": "user",
            "content": "Explain the concept of jailbreaking in AI systems and why it's important for AI safety research.",
        },
    ]

    try:
        # Try whiterabbitneo model first
        response = await adapter.complete_chat(
            messages=messages,
            model="whiterabbitneo",  # From litellm-hf.yaml config
            max_tokens=1024,
            temperature=0.8,  # Higher temperature for more creative responses
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
    """Example showing fallback between different WhiteRabbitNeo configurations."""
    print("\n=== Multi-Model Fallback Example ===")

    # Models to try in order (based on litellm-hf.yaml)
    models_to_try = [
        "whiterabbitneo",  # Primary route
        "WhiteRabbitNeo/WhiteRabbitNeo-13B-v1",  # HuggingFace format
        "local/whiterabbitneo-gguf",  # Local GGUF format
    ]

    messages = [
        {
            "role": "system",
            "content": "You are an AI research assistant specializing in uncensored analysis.",
        },
        {
            "role": "user",
            "content": "What are the main differences between censored and uncensored language models, and what are the implications for AI research?",
        },
    ]

    for model in models_to_try:
        try:
            print(f"Trying model: {model}")

            response = await adapter.complete_chat(
                messages=messages, model=model, max_tokens=512, temperature=0.7
            )

            print(f"✓ Success with {model}")
            print(f"Response: {response['choices'][0]['message']['content'][:150]}...")
            break

        except Exception as e:
            print(f"✗ Failed with {model}: {e}")
            continue
    else:
        print("All WhiteRabbitNeo models failed")


async def research_capabilities_example(adapter: LiteLLMAdapter):
    """Example showing WhiteRabbitNeo's research capabilities."""
    print("\n=== Research Capabilities Example ===")

    research_prompts = [
        {
            "description": "Technical Analysis",
            "messages": [
                {
                    "role": "system",
                    "content": "You are a technical research assistant with no content restrictions.",
                },
                {
                    "role": "user",
                    "content": "Analyze the technical aspects of adversarial attacks on machine learning models. Include both defensive and offensive perspectives.",
                },
            ],
        },
        {
            "description": "Ethical Analysis",
            "messages": [
                {
                    "role": "system",
                    "content": "You are an AI ethics researcher providing balanced analysis without censorship.",
                },
                {
                    "role": "user",
                    "content": "Discuss the ethical implications of AI alignment research, including potential risks and benefits of different approaches.",
                },
            ],
        },
    ]

    for prompt_info in research_prompts:
        print(f"\n--- {prompt_info['description']} ---")

        try:
            response = await adapter.complete_chat(
                messages=prompt_info["messages"],
                model="whiterabbitneo",
                max_tokens=800,
                temperature=0.6,
            )

            content = response["choices"][0]["message"]["content"]
            print(f"Response ({len(content)} chars): {content[:200]}...")

            # Show token efficiency
            usage = response.get("usage", {})
            if usage:
                efficiency = usage.get("completion_tokens", 0) / max(
                    usage.get("prompt_tokens", 1), 1
                )
                print(f"Token efficiency: {efficiency:.2f} (completion/prompt ratio)")

        except Exception as e:
            print(f"Research example failed: {e}")


async def cost_tracking_example(adapter: LiteLLMAdapter):
    """Example showing cost estimation and tracking for local models."""
    print("\n=== Cost Tracking Example ===")

    messages = [
        {
            "role": "user",
            "content": "Compare the advantages and disadvantages of running uncensored language models locally versus using cloud-based censored models for AI research purposes.",
        }
    ]

    try:
        # Get cost estimate first
        estimate = await adapter.get_cost_estimate(
            messages=messages,
            model="whiterabbitneo"
        )
        
        print(f"Estimated cost: ${estimate.get('estimated_cost', 0):.4f}")
        print(f"Estimated tokens: {estimate.get('estimated_tokens', 0)}")
        
        # Note: Local models typically have $0 cost but we track for completeness
        response = await adapter.complete_chat(
            messages=messages,
            model="whiterabbitneo",
            max_tokens=1200,
            temperature=0.7
        )

        print("Completion successful!")
        print(
            f"Response length: {len(response['choices'][0]['message']['content'])} chars"
        )

        # Get actual usage stats
        usage_stats = await adapter.get_usage_stats()
        print(f"Total requests today: {usage_stats.get('total_requests_today', 0)}")
        print(f"Total cost today: ${usage_stats.get('total_cost_today', 0):.4f}")

    except Exception as e:
        print(f"Cost tracking failed: {e}")


async def adaptive_safety_example(adapter: LiteLLMAdapter):
    """Example showing adaptive safety controls for research scenarios."""
    print("\n=== Adaptive Safety Controls Example ===")

    # Test different types of research content
    test_scenarios = [
        {
            "description": "Academic Security Research",
            "messages": [
                {
                    "role": "user",
                    "content": "Explain common web application vulnerabilities and their countermeasures for educational purposes.",
                }
            ],
        },
        {
            "description": "AI Safety Research",
            "messages": [
                {
                    "role": "user",
                    "content": "Discuss potential failure modes in AI systems and mitigation strategies.",
                }
            ],
        },
        {
            "description": "General Technical Query",
            "messages": [
                {
                    "role": "user",
                    "content": "How do neural networks learn representations, and what are the implications for interpretability?",
                }
            ],
        },
    ]

    for scenario in test_scenarios:
        print(f"\n--- {scenario['description']} ---")

        try:
            # Validate request safety first
            safety_result = await adapter.validate_request_safety(
                messages=scenario["messages"], model="whiterabbitneo"
            )

            print(
                f"Safety validation: {'✓ Approved' if safety_result.get('is_safe', False) else '✗ Blocked'}"
            )

            if safety_result.get("is_safe", False):
                # Proceed with completion
                response = await adapter.complete_chat(
                    messages=scenario["messages"],
                    model="whiterabbitneo",
                    max_tokens=400,
                    temperature=0.5,
                )

                content = response["choices"][0]["message"]["content"]
                print(f"Response preview: {content[:120]}...")

            else:
                print(
                    f"Reason: {safety_result.get('reason', 'Safety policy violation')}"
                )

        except Exception as e:
            print(f"Safety validation failed: {e}")


async def main():
    """Main function demonstrating various WhiteRabbitNeo LiteLLM features."""
    print("=== LiteLLM WhiteRabbitNeo Example ===")
    print(
        "This example demonstrates WhiteRabbitNeo model usage through LiteLLM adapter"
    )
    print(
        "Note: WhiteRabbitNeo is designed for uncensored AI research and may produce unfiltered content"
    )

    try:
        # Initialize adapter
        adapter = setup_adapter()
        print("✓ LiteLLM adapter initialized with research-appropriate safety config")

        # Run examples
        if await check_health_and_models(adapter):
            await basic_completion_example(adapter)
            await multi_model_example(adapter)
            await research_capabilities_example(adapter)
            await cost_tracking_example(adapter)
            await adaptive_safety_example(adapter)

        print("\n=== Example Complete ===")
        print("Remember: WhiteRabbitNeo is designed for research purposes.")
        print(
            "Always use responsibly and in accordance with your organization's policies."
        )

    except Exception as e:
        print(f"Example failed: {e}")
        return 1

    return 0


if __name__ == "__main__":
    exit(asyncio.run(main()))
