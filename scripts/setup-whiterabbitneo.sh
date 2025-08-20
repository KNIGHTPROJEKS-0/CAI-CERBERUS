#!/bin/bash
set -e

echo "🐰 Setting up WhiteRabbitNeo for CAI-CERBERUS..."

# Check if Git LFS is installed
if ! command -v git-lfs &> /dev/null; then
    echo "Installing Git LFS..."
    git lfs install
fi

# Create models directory
mkdir -p models

# Clone WhiteRabbitNeo model if not exists
if [ ! -d "models/WhiteRabbitNeo-13B-v1" ]; then
    echo "Cloning WhiteRabbitNeo model..."
    cd models
    git clone https://huggingface.co/WhiteRabbitNeo/WhiteRabbitNeo-13B-v1
    cd ..
else
    echo "WhiteRabbitNeo model already exists"
fi

# Create necessary directories
mkdir -p configs
mkdir -p external-tools/huggingface

# Set permissions
chmod +x scripts/setup-whiterabbitneo.sh

echo "✅ WhiteRabbitNeo setup complete!"
echo "Next steps:"
echo "1. Run: make huggingface-start"
echo "2. Test: make huggingface-test"