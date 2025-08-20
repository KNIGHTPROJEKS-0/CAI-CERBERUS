#!/bin/bash
set -e

echo "🤗 Setting up Transformers integration for CAI-CERBERUS..."

# Install transformers dependencies
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
pip install transformers accelerate bitsandbytes

# Create symlink to transformers
cd external-tools
if [ ! -L transformers-lib ]; then
    ln -s transformers/src/transformers transformers-lib
fi
cd ..

# Set permissions
chmod +x tools/huggingface/transformers_adapter.py

echo "✅ Transformers setup complete!"
echo "Model will be downloaded on first use."