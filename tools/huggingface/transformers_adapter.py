#!/usr/bin/env python3
"""Transformers-based WhiteRabbitNeo adapter for CAI-CERBERUS."""

import os
import sys
import torch
from typing import Dict, List, Optional, Any
from dataclasses import dataclass

# Add transformers to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'external-tools', 'transformers', 'src'))

from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM

@dataclass
class TransformersConfig:
    """Configuration for Transformers-based WhiteRabbitNeo."""
    model_name: str = "WhiteRabbitNeo/WhiteRabbitNeo-13B-v1"
    device: str = "auto"
    max_length: int = 4096
    temperature: float = 0.7
    do_sample: bool = True
    trust_remote_code: bool = True

class WhiteRabbitTransformersAdapter:
    """Direct Transformers integration for WhiteRabbitNeo."""
    
    def __init__(self, config: Optional[TransformersConfig] = None):
        self.config = config or TransformersConfig()
        self.tokenizer = None
        self.model = None
        self.pipeline = None
    
    def load_model(self):
        """Load WhiteRabbitNeo model using transformers."""
        print(f"Loading {self.config.model_name}...")
        
        # Load tokenizer
        self.tokenizer = AutoTokenizer.from_pretrained(
            self.config.model_name,
            trust_remote_code=self.config.trust_remote_code
        )
        
        # Load model
        self.model = AutoModelForCausalLM.from_pretrained(
            self.config.model_name,
            trust_remote_code=self.config.trust_remote_code,
            torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
            device_map=self.config.device
        )
        
        # Create pipeline
        self.pipeline = pipeline(
            "text-generation",
            model=self.model,
            tokenizer=self.tokenizer,
            device_map=self.config.device
        )
        
        print("Model loaded successfully!")
    
    def generate_response(self, prompt: str) -> Dict[str, Any]:
        """Generate response using WhiteRabbitNeo."""
        if not self.pipeline:
            self.load_model()
        
        try:
            result = self.pipeline(
                prompt,
                max_length=self.config.max_length,
                temperature=self.config.temperature,
                do_sample=self.config.do_sample,
                pad_token_id=self.tokenizer.eos_token_id
            )
            
            return {
                "success": True,
                "response": result[0]["generated_text"],
                "model": self.config.model_name
            }
        
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "model": self.config.model_name
            }
    
    def analyze_cybersecurity_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze cybersecurity data using WhiteRabbitNeo."""
        prompt = f"""
You are WhiteRabbitNeo, an advanced cybersecurity AI. Analyze this data:

{data}

Provide:
1. Threat assessment
2. Risk analysis
3. Mitigation strategies
4. Technical recommendations

Analysis:"""
        
        return self.generate_response(prompt)

def run_server(port: int = 8080, model: str = "WhiteRabbitNeo/WhiteRabbitNeo-13B-v1"):
    """Run WhiteRabbitNeo as a server."""
    from fastapi import FastAPI
    from pydantic import BaseModel
    import uvicorn
    
    app = FastAPI(title="WhiteRabbitNeo Server")
    
    config = TransformersConfig(model_name=model)
    adapter = WhiteRabbitTransformersAdapter(config)
    
    class GenerateRequest(BaseModel):
        prompt: str
        max_length: Optional[int] = 4096
        temperature: Optional[float] = 0.7
    
    @app.post("/generate")
    async def generate(request: GenerateRequest):
        return adapter.generate_response(request.prompt)
    
    @app.post("/analyze")
    async def analyze(data: Dict[str, Any]):
        return adapter.analyze_cybersecurity_data(data)
    
    @app.get("/health")
    async def health():
        return {"status": "healthy", "model": model}
    
    uvicorn.run(app, host="0.0.0.0", port=port)

def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description="WhiteRabbitNeo Transformers Adapter")
    parser.add_argument("--port", type=int, default=8080, help="Server port")
    parser.add_argument("--model", type=str, default="WhiteRabbitNeo/WhiteRabbitNeo-13B-v1", help="Model name")
    parser.add_argument("--server", action="store_true", help="Run as server")
    
    args = parser.parse_args()
    
    if args.server or "--port" in sys.argv:
        run_server(args.port, args.model)
    else:
        # Test mode
        adapter = WhiteRabbitTransformersAdapter()
        
        test_data = {
            "vulnerabilities": ["CVE-2024-1234"],
            "services": ["ssh", "http"],
            "ports": [22, 80]
        }
        
        result = adapter.analyze_cybersecurity_data(test_data)
        print(result)

if __name__ == "__main__":
    main()