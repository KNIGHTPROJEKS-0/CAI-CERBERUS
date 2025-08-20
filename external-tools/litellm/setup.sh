#!/bin/bash

# LiteLLM Setup Script for CAI-CERBERUS
# This script sets up LiteLLM proxy with proper security and integration

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

echo "🔧 Setting up LiteLLM for CAI-CERBERUS..."

# Check prerequisites
check_prerequisites() {
    echo "📋 Checking prerequisites..."
    
    if ! command -v docker &> /dev/null; then
        echo "❌ Docker is required but not installed"
        exit 1
    fi
    
    if ! command -v docker-compose &> /dev/null; then
        echo "❌ Docker Compose is required but not installed"
        exit 1
    fi
    
    echo "✅ Prerequisites satisfied"
}

# Generate secure keys
generate_keys() {
    echo "🔐 Generating secure keys..."
    
    MASTER_KEY="sk-cerberus-$(openssl rand -hex 16)"
    SALT_KEY="$(openssl rand -hex 32)"
    DB_PASSWORD="$(openssl rand -hex 16)"
    
    echo "✅ Keys generated"
}

# Create environment file
create_env_file() {
    echo "📝 Creating environment configuration..."
    
    cat > "$SCRIPT_DIR/.env" << EOF
# LiteLLM Configuration for CAI-CERBERUS
LITELLM_MASTER_KEY="$MASTER_KEY"
LITELLM_SALT_KEY="$SALT_KEY"

# Database Configuration
DATABASE_URL="postgresql://llmproxy:$DB_PASSWORD@localhost:5432/litellm"
POSTGRES_PASSWORD="$DB_PASSWORD"

# Security Settings
LITELLM_LOG_LEVEL="INFO"
STORE_MODEL_IN_DB="True"

# Cost and Safety Limits
MAX_BUDGET_PER_USER="100.0"
MAX_BUDGET_PER_KEY="50.0"
BUDGET_DURATION="30d"

# Provider API Keys (add your keys here)
# OPENAI_API_KEY="sk-..."
# ANTHROPIC_API_KEY="sk-ant-..."
# DEEPSEEK_API_KEY="sk-..."

# Monitoring
PROMETHEUS_ENABLED="true"
PROMETHEUS_PORT="9090"

# CAI-CERBERUS Integration
CERBERUS_INTEGRATION="true"
CERBERUS_AUDIT_LOG="true"
EOF

    echo "✅ Environment file created at $SCRIPT_DIR/.env"
}

# Create LiteLLM configuration
create_config() {
    echo "📋 Creating LiteLLM configuration..."
    
    cat > "$SCRIPT_DIR/config.yaml" << EOF
model_list:
  # OpenAI Models
  - model_name: gpt-4o
    litellm_params:
      model: openai/gpt-4o
      api_key: os.environ/OPENAI_API_KEY
  
  - model_name: gpt-4o-mini
    litellm_params:
      model: openai/gpt-4o-mini
      api_key: os.environ/OPENAI_API_KEY
  
  # Anthropic Models
  - model_name: claude-3-5-sonnet
    litellm_params:
      model: anthropic/claude-3-5-sonnet-20241022
      api_key: os.environ/ANTHROPIC_API_KEY
  
  # DeepSeek Models
  - model_name: deepseek-chat
    litellm_params:
      model: deepseek/deepseek-chat
      api_key: os.environ/DEEPSEEK_API_KEY

# General Settings
general_settings:
  master_key: os.environ/LITELLM_MASTER_KEY
  database_url: os.environ/DATABASE_URL
  
  # Cost Controls
  max_budget: 1000.0
  budget_duration: 30d
  
  # Security
  enforce_user_param: true
  allowed_ips: ["127.0.0.1", "localhost"]
  
  # Logging
  success_callback: ["prometheus", "langfuse"]
  failure_callback: ["prometheus"]
  
  # CAI-CERBERUS Integration
  custom_auth: cerberus_auth
  
# Router Settings
router_settings:
  routing_strategy: "least-busy"
  model_group_alias:
    gpt-4: ["gpt-4o", "gpt-4o-mini"]
    claude: ["claude-3-5-sonnet"]
    deepseek: ["deepseek-chat"]

# Prometheus Configuration
prometheus:
  enabled: true
  port: 9090
  
# Guardrails
guardrails:
  - guardrail_name: "cerberus_safety"
    litellm_params:
      guardrail: presidio
      mode: "during_call"
EOF

    echo "✅ Configuration file created at $SCRIPT_DIR/config.yaml"
}

# Update docker-compose with proper configuration
update_docker_compose() {
    echo "🐳 Updating Docker Compose configuration..."
    
    cat > "$SCRIPT_DIR/docker-compose.yml" << EOF
services:
  litellm:
    image: ghcr.io/berriai/litellm:main-stable
    ports:
      - "4000:4000"
    volumes:
      - ./config.yaml:/app/config.yaml
      - ./logs:/app/logs
    command:
      - "--config=/app/config.yaml"
      - "--port=4000"
      - "--num_workers=1"
    environment:
      DATABASE_URL: "postgresql://llmproxy:\${POSTGRES_PASSWORD}@db:5432/litellm"
      STORE_MODEL_IN_DB: "True"
    env_file:
      - .env
    depends_on:
      db:
        condition: service_healthy
    healthcheck:
      test: ["CMD-SHELL", "wget --no-verbose --tries=1 http://localhost:4000/health/liveliness || exit 1"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
    restart: unless-stopped

  db:
    image: postgres:16
    container_name: litellm_db
    environment:
      POSTGRES_DB: litellm
      POSTGRES_USER: llmproxy
      POSTGRES_PASSWORD: \${POSTGRES_PASSWORD}
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -d litellm -U llmproxy"]
      interval: 5s
      timeout: 5s
      retries: 5
    restart: unless-stopped

  prometheus:
    image: prom/prometheus:latest
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
      - prometheus_data:/prometheus
    command:
      - "--config.file=/etc/prometheus/prometheus.yml"
      - "--storage.tsdb.path=/prometheus"
      - "--storage.tsdb.retention.time=15d"
      - "--web.console.libraries=/etc/prometheus/console_libraries"
      - "--web.console.templates=/etc/prometheus/consoles"
    restart: unless-stopped

volumes:
  postgres_data:
    name: litellm_postgres_data
  prometheus_data:
    name: litellm_prometheus_data
EOF

    echo "✅ Docker Compose updated"
}

# Create Prometheus configuration
create_prometheus_config() {
    echo "📊 Creating Prometheus configuration..."
    
    cat > "$SCRIPT_DIR/prometheus.yml" << EOF
global:
  scrape_interval: 15s
  evaluation_interval: 15s

scrape_configs:
  - job_name: 'litellm'
    static_configs:
      - targets: ['litellm:4000']
    metrics_path: '/metrics'
    scrape_interval: 30s
EOF

    echo "✅ Prometheus configuration created"
}

# Create logs directory
create_directories() {
    echo "📁 Creating necessary directories..."
    
    mkdir -p "$SCRIPT_DIR/logs"
    mkdir -p "$SCRIPT_DIR/data"
    
    echo "✅ Directories created"
}

# Start services
start_services() {
    echo "🚀 Starting LiteLLM services..."
    
    cd "$SCRIPT_DIR"
    docker-compose up -d
    
    echo "⏳ Waiting for services to be ready..."
    sleep 30
    
    # Check if services are healthy
    if docker-compose ps | grep -q "Up (healthy)"; then
        echo "✅ LiteLLM is running successfully!"
        echo ""
        echo "🌐 Access URLs:"
        echo "   - LiteLLM Proxy: http://localhost:4000"
        echo "   - LiteLLM UI: http://localhost:4000/ui"
        echo "   - Prometheus: http://localhost:9090"
        echo ""
        echo "🔑 Master Key: $MASTER_KEY"
        echo ""
        echo "📝 Next steps:"
        echo "   1. Add your API keys to .env file"
        echo "   2. Test the integration with: python test_integration.py"
        echo "   3. Configure CAI-CERBERUS to use: CERBERUS_MODEL=litellm/gpt-4o"
    else
        echo "❌ Services failed to start properly"
        docker-compose logs
        exit 1
    fi
}

# Main execution
main() {
    check_prerequisites
    generate_keys
    create_env_file
    create_config
    update_docker_compose
    create_prometheus_config
    create_directories
    start_services
}

# Run setup
main "$@"