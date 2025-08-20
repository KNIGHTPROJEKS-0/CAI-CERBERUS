FROM python:3.12-slim

# Install system dependencies including Node.js for LiteLLM
RUN apt-get update && apt-get install -y \
    git curl wget build-essential \
    nodejs npm supervisor \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install additional dependencies for unified container
RUN pip install \
    torch transformers accelerate aiohttp \
    litellm[proxy] \
    text-generation-inference \
    datasets huggingface_hub[cli] \
    supervisor

# Copy application code
COPY . .

# Install CAI-CERBERUS
RUN pip install -e .

# Set permissions
RUN chmod +x scripts/*.sh tools/huggingface/*.py || true
RUN find external-tools/ -name "*.py" -exec chmod +x {} \; || true
RUN find external-tools/ -name "*.sh" -exec chmod +x {} \; || true

# Create necessary directories
RUN mkdir -p workspaces audit models logs external-tools/datasets configs

# Download and cache WhiteRabbitNeo model (optional, can be done at runtime)
# RUN python -c "from transformers import AutoTokenizer, AutoModelForCausalLM; AutoTokenizer.from_pretrained('WhiteRabbitNeo/WhiteRabbitNeo-13B-v1'); AutoModelForCausalLM.from_pretrained('WhiteRabbitNeo/WhiteRabbitNeo-13B-v1')"

# Copy supervisor configuration
COPY configs/supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Expose ports
EXPOSE 8000 4000 8080

# Health check for main service
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Use supervisor to run multiple services
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]