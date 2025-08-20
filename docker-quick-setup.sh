#!/bin/bash

# Quick Docker Pro Setup for CAI-CERBERUS
set -e

echo "🐳 Docker Pro Quick Setup"
echo "========================="

# Check Docker status
echo "📋 Docker Status:"
echo "Version: $(docker --version)"
echo "CPUs: $(docker system info --format '{{.NCPU}}')"
echo "Memory: $(docker system info --format '{{.MemTotal}}')"

# Check account
DOCKER_USER=$(docker offload accounts 2>/dev/null | jq -r '.user.username' 2>/dev/null || echo "unknown")
echo "Account: $DOCKER_USER"

# Create optimized Docker Compose for CAI-CERBERUS
echo "🔧 Creating Docker Compose configuration..."

cat > docker-compose.yml << 'EOF'
version: '3.8'

services:
  # LiteLLM Proxy
  litellm:
    build:
      context: ./external-tools/litellm
      dockerfile: Dockerfile
    ports:
      - "4000:4000"
    environment:
      - LITELLM_MASTER_KEY=sk-cerberus-2024
      - DATABASE_URL=postgresql://litellm:password@postgres:5432/litellm
    depends_on:
      - postgres
    restart: unless-stopped
    deploy:
      resources:
        limits:
          memory: 2G
        reservations:
          memory: 512M

  # PostgreSQL Database
  postgres:
    image: postgres:15-alpine
    environment:
      - POSTGRES_DB=litellm
      - POSTGRES_USER=litellm
      - POSTGRES_PASSWORD=password
    volumes:
      - postgres_data:/var/lib/postgresql/data
    restart: unless-stopped

  # Redis Cache
  redis:
    image: redis:7-alpine
    volumes:
      - redis_data:/data
    restart: unless-stopped

volumes:
  postgres_data:
  redis_data:

networks:
  default:
    driver: bridge
EOF

# Create .dockerignore
cat > .dockerignore << 'EOF'
.git
__pycache__
*.pyc
.env
.venv
node_modules
logs
*.log
.DS_Store
EOF

# Test Docker functionality
echo "🧪 Testing Docker..."
if docker run --rm hello-world > /dev/null 2>&1; then
    echo "✅ Docker is working"
else
    echo "❌ Docker test failed"
    exit 1
fi

# Try Docker Offload
echo "🚀 Checking Docker Offload..."
if docker offload start --timeout 10s > /dev/null 2>&1; then
    echo "✅ Docker Offload started"
    docker offload status
else
    echo "⚠️ Docker Offload not available (this is optional)"
fi

echo ""
echo "✅ Docker setup complete!"
echo ""
echo "Next steps:"
echo "1. Start services: docker compose up -d"
echo "2. Check health: curl http://localhost:4000/health"
echo "3. View logs: docker compose logs -f"