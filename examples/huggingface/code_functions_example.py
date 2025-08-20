#!/usr/bin/env python3
"""Example using Code Functions with WhiteRabbitNeo for cybersecurity."""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from tools.huggingface.code_functions_adapter import CodeFunctionsAdapter, CodeFunctionsConfig

def run_code_functions_example():
    """Demonstrate Code Functions with cybersecurity focus."""
    
    print("🔐 Code Functions WhiteRabbitNeo Integration")
    print("=" * 50)
    
    config = CodeFunctionsConfig(
        model_name="WhiteRabbitNeo/WhiteRabbitNeo-13B-v1",
        device="auto",
        max_length=2048,
        temperature=0.3
    )
    
    adapter = CodeFunctionsAdapter(config)
    
    # Example 1: Get cybersecurity functions
    print("\n1. Cybersecurity Functions")
    print("-" * 30)
    
    cyber_funcs = adapter.get_cyber_functions("network")
    print(f"Found {len(cyber_funcs)} network-related cyber functions")
    
    # Example 2: Generate secure code
    print("\n2. Secure Code Generation")
    print("-" * 30)
    
    result = adapter.generate_cyber_code("Create a secure port scanner with rate limiting")
    if result["success"]:
        print(f"Generated code:\n{result['response'][:500]}...")
    else:
        print(f"Error: {result['error']}")
    
    # Example 3: Analyze code security
    print("\n3. Code Security Analysis")
    print("-" * 30)
    
    sample_code = """
import socket
import sys

def scan_port(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex((host, port))
    sock.close()
    return result == 0
"""
    
    result = adapter.analyze_code_security(sample_code)
    if result["success"]:
        print(f"Security analysis:\n{result['response'][:500]}...")
    else:
        print(f"Error: {result['error']}")

if __name__ == "__main__":
    run_code_functions_example()