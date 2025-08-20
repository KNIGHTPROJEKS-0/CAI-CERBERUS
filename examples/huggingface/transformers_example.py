#!/usr/bin/env python3
"""Example using direct Transformers integration with WhiteRabbitNeo."""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from tools.huggingface.transformers_adapter import WhiteRabbitTransformersAdapter, TransformersConfig

def run_transformers_example():
    """Demonstrate direct Transformers usage."""
    
    print("🤗 Transformers WhiteRabbitNeo Integration")
    print("=" * 40)
    
    # Configure for local execution
    config = TransformersConfig(
        model_name="WhiteRabbitNeo/WhiteRabbitNeo-13B-v1",
        device="auto",
        max_length=2048,
        temperature=0.3
    )
    
    adapter = WhiteRabbitTransformersAdapter(config)
    
    # Test cybersecurity analysis
    test_data = {
        "scan_results": {
            "open_ports": [22, 80, 443],
            "services": ["ssh", "nginx", "ssl"],
            "vulnerabilities": ["CVE-2024-1234"]
        },
        "threat_indicators": [
            "suspicious_network_traffic",
            "unauthorized_access_attempts"
        ]
    }
    
    print("Analyzing cybersecurity data...")
    result = adapter.analyze_cybersecurity_data(test_data)
    
    if result["success"]:
        print(f"Analysis:\n{result['response']}")
    else:
        print(f"Error: {result['error']}")

if __name__ == "__main__":
    run_transformers_example()