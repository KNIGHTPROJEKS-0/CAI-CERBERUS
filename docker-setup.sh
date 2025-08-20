#!/bin/bash

# Docker Pro Setup Script for CAI-CERBERUS
# Configures Docker Desktop with Offload for optimal performance

set -e

echo "🐳 Docker Pro Setup for CAI-CERBERUS"
echo "=" * 50

# Check Docker installation
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker Desktop first."
    exit 1
fi

# Check Docker Pro account
echo "📋 Checking Docker account status..."
DOCKER_USER=$(docker offload accounts | jq -r '.user.username' 2>/dev/null || echo "")
if [ -z "$DOCKER_USER" ]; then
    echo "❌ Not logged into Docker. Please run: docker login"
    exit 1
fi

echo "✅ Logged in as: $DOCKER_USER"

# Check current Docker Offload status
echo "🔍 Checking Docker Offload status..."
if docker offload status &>/dev/null; then
    echo "✅ Docker Offload is already running"
    docker offload status
else
    echo "🚀 Starting Docker Offload session..."
    docker offload start
    
    # Wait for offload to be ready
    echo "⏳ Waiting for Docker Offload to initialize..."
    sleep 5
    
    if docker offload status &>/dev/null; then
        echo "✅ Docker Offload started successfully"
        docker offload status
    else
        echo "❌ Failed to start Docker Offload"
        exit 1
    fi
fi

# Configure Docker settings for optimal performance
echo "⚙️ Configuring Docker settings..."

# Create Docker daemon configuration
DOCKER_CONFIG_DIR="$HOME/.docker"
DAEMON_CONFIG="$DOCKER_CONFIG_DIR/daemon.json"

mkdir -p "$DOCKER_CONFIG_DIR"

# Backup existing config if it exists
if [ -f "$DAEMON_CONFIG" ]; then
    cp "$DAEMON_CONFIG" "$DAEMON_CONFIG.backup.$(date +%Y%m%d_%H%M%S)"
    echo "📋 Backed up existing daemon.json"
fi

# Create optimized daemon configuration
cat > "$DAEMON_CONFIG" << 'EOF'
{
  "builder": {
    "gc": {
      "enabled": true,
      "defaultKeepStorage": "20GB"
    }
  },
  "experimental": false,
  "features": {
    "buildkit": true
  },
  "log-driver": "json-file",
  "log-opts": {
    "max-size": "10m",
    "max-file": "3"
  },
  "storage-driver": "overlay2",
  "storage-opts": [
    "overlay2.override_kernel_check=true"
  ]
}
EOF

echo "✅ Created optimized daemon.json configuration"

# Create Docker Compose override for CAI-CERBERUS
echo "🔧 Creating Docker Compose configuration for CAI-CERBERUS..."

cat > "docker-compose.override.yml" << 'EOF'
# Docker Compose override for CAI-CERBERUS with Docker Pro optimizations
version: '3.8'

x-common-config: &common-config
  restart: unless-stopped
  logging:
    driver: json-file
    options:
      max-size: "10m"
      max-file: "3"
  deploy:
    resources:
      limits:
        memory: 2G
      reservations:
        memory: 512M

services:
  # LiteLLM Proxy with Pro optimizations
  litellm:
    <<: *common-config
    build:
      context: ./external-tools/litellm
      dockerfile: Dockerfile
      cache_from:
        - litellm/litellm:latest
    environment:
      - LITELLM_MASTER_KEY=${LITELLM_MASTER_KEY:-sk-1234}
      - DATABASE_URL=postgresql://litellm:password@postgres:5432/litellm
      - REDIS_URL=redis://redis:6379
    ports:
      - "4000:4000"
    depends_on:
      - postgres
      - redis
    volumes:
      - litellm_data:/app/data
    networks:
      - cerberus-network

  # PostgreSQL for LiteLLM
  postgres:
    <<: *common-config
    image: postgres:15-alpine
    environment:
      - POSTGRES_DB=litellm
      - POSTGRES_USER=litellm
      - POSTGRES_PASSWORD=password
    volumes:
      - postgres_data:/var/lib/postgresql/data
    networks:
      - cerberus-network

  # Redis for caching
  redis:
    <<: *common-config
    image: redis:7-alpine
    volumes:
      - redis_data:/data
    networks:
      - cerberus-network

  # Prometheus for monitoring
  prometheus:
    <<: *common-config
    image: prom/prometheus:latest
    ports:
      - "9090:9090"
    volumes:
      - ./external-tools/litellm/prometheus.yml:/etc/prometheus/prometheus.yml
      - prometheus_data:/prometheus
    networks:
      - cerberus-network

volumes:
  litellm_data:
    driver: local
  postgres_data:
    driver: local
  redis_data:
    driver: local
  prometheus_data:
    driver: local

networks:
  cerberus-network:
    driver: bridge
    ipam:
      config:
        - subnet: 172.20.0.0/16
EOF

echo "✅ Created docker-compose.override.yml"

# Create Docker ignore file
cat > ".dockerignore" << 'EOF'
# Git
.git
.gitignore
.gitattributes

# Python
__pycache__
*.pyc
*.pyo
*.pyd
.Python
env
pip-log.txt
pip-delete-this-directory.txt
.tox
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
*.log
.git
.mypy_cache
.pytest_cache
.hypothesis

# Virtual environments
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# IDEs
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
.DS_Store?
._*
.Spotlight-V100
.Trashes
ehthumbs.db
Thumbs.db

# Project specific
logs/
*.log
temp/
tmp/
build/
dist/
*.egg-info/

# Documentation
docs/_build/
site/

# Test files
.pytest_cache/
.coverage
htmlcov/

# Node modules (for any JS tools)
node_modules/
npm-debug.log*
yarn-debug.log*
yarn-error.log*
EOF

echo "✅ Created .dockerignore file"

# Test Docker setup
echo "🧪 Testing Docker setup..."

# Test basic Docker functionality
if docker run --rm hello-world &>/dev/null; then
    echo "✅ Docker basic functionality test passed"
else
    echo "❌ Docker basic functionality test failed"
    exit 1
fi

# Test Docker Compose
if docker compose version &>/dev/null; then
    echo "✅ Docker Compose is available"
else
    echo "❌ Docker Compose is not available"
    exit 1
fi

# Display system information
echo ""
echo "📊 Docker System Information:"
echo "Docker Version: $(docker --version)"
echo "Docker Compose Version: $(docker compose version --short)"
echo "Available Memory: $(docker system info --format '{{.MemTotal}}')"
echo "Available CPUs: $(docker system info --format '{{.NCPU}}')"

# Display Docker Offload status
echo ""
echo "🚀 Docker Offload Status:"
docker offload status || echo "Docker Offload not active"

echo ""
echo "🎉 Docker Pro setup complete!"
echo ""
echo "Next steps:"
echo "1. Start CAI-CERBERUS services: make litellm-start"
echo "2. Monitor with: docker compose logs -f"
echo "3. Check health: curl http://localhost:4000/health"
echo ""
echo "Pro Features Available:"
echo "- Docker Offload for cloud builds"
echo "- Enhanced security scanning"
echo "- Advanced image management"
echo "- Priority support"
EOF