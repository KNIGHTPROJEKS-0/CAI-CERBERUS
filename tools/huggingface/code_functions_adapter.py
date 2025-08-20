#!/usr/bin/env python3
"""Code Functions adapter for WhiteRabbitNeo with cybersecurity datasets."""

import json
import os
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from .transformers_adapter import WhiteRabbitTransformersAdapter, TransformersConfig

@dataclass
class CodeFunctionsConfig(TransformersConfig):
    """Configuration for Code Functions with WhiteRabbitNeo."""
    cyber_dataset_path: str = "./external-tools/datasets/Code-Functions-Level-Cyber/code-end-to-end-cyber.jsonl"
    general_dataset_path: str = "./external-tools/datasets/Code-Functions-Level-General/code-end-to-end-general.jsonl"

class CodeFunctionsAdapter(WhiteRabbitTransformersAdapter):
    """Adapter for code functions with cybersecurity focus."""
    
    def __init__(self, config: Optional[CodeFunctionsConfig] = None):
        self.config = config or CodeFunctionsConfig()
        super().__init__(self.config)
        self.cyber_functions = []
        self.general_functions = []
        self._load_datasets()
    
    def _load_datasets(self):
        """Load code function datasets."""
        if os.path.exists(self.config.cyber_dataset_path):
            with open(self.config.cyber_dataset_path, 'r') as f:
                for line in f:
                    self.cyber_functions.append(json.loads(line))
        
        if os.path.exists(self.config.general_dataset_path):
            with open(self.config.general_dataset_path, 'r') as f:
                for line in f:
                    self.general_functions.append(json.loads(line))
    
    def get_cyber_functions(self, query: str = None) -> List[Dict]:
        """Get cybersecurity-related functions."""
        if not query:
            return self.cyber_functions[:10]
        
        return [f for f in self.cyber_functions if query.lower() in str(f).lower()][:10]
    
    def generate_cyber_code(self, prompt: str) -> Dict[str, Any]:
        """Generate cybersecurity code using WhiteRabbitNeo."""
        enhanced_prompt = f"""
You are WhiteRabbitNeo, an expert cybersecurity AI. Generate secure, ethical code for:

{prompt}

Requirements:
- Follow cybersecurity best practices
- Include proper error handling
- Add security validations
- Document potential risks
- Ensure ethical usage only

Code:"""
        
        return self.generate_response(enhanced_prompt)
    
    def analyze_code_security(self, code: str) -> Dict[str, Any]:
        """Analyze code for security vulnerabilities."""
        prompt = f"""
Analyze this code for security vulnerabilities and provide recommendations:

```
{code}
```

Provide:
1. Security vulnerabilities found
2. Risk assessment (Low/Medium/High/Critical)
3. Specific remediation steps
4. Best practices recommendations

Analysis:"""
        
        return self.generate_response(prompt)

def main():
    """Test code functions adapter."""
    adapter = CodeFunctionsAdapter()
    
    # Test cyber functions
    cyber_funcs = adapter.get_cyber_functions("network")
    print(f"Found {len(cyber_funcs)} cyber functions")
    
    # Test code generation
    result = adapter.generate_cyber_code("Create a secure network scanner")
    print(result)

if __name__ == "__main__":
    main()