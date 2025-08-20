#!/usr/bin/env python3
"""Setup script for CAI-CERBERUS."""

from setuptools import setup, find_packages

setup(
    name="cai-cerberus",
    version="2.0.0",
    description="CAI-CERBERUS - Cybersecurity AI Intelligence Framework",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "cai=cai_cerberus.cli:main",
            "cerberus=cai_cerberus.cli:main",
            "cai-cerberus=cai_cerberus.cli:main",
        ],
    },
    python_requires=">=3.12",
    install_requires=[
        "torch>=2.0.0",
        "transformers>=4.30.0",
        "accelerate>=0.20.0",
        "fastapi>=0.100.0",
        "uvicorn>=0.20.0",
        "pydantic>=2.0.0",
        "pyyaml>=6.0",
        "requests>=2.30.0",
    ],
)