.PHONY: install test build clean docs dev litellm-setup litellm-start litellm-stop litellm-test litellm-logs litellm-integrate mcp-setup mcp-start mcp-stop mcp-status gateway-setup gateway-start gateway-stop gateway-status metabigor-setup metabigor-test metabigor-examples docker-setup docker-start docker-stop docker-status docker-offload huggingface-setup huggingface-start huggingface-stop huggingface-test huggingface-logs

# Install dependencies
install:
	pip install -e ".[dev,test]"

# Run tests
test:
	python -m pytest tests/ -v

# Build project
build: install test
	python build.py

# Clean build artifacts
clean:
	rm -rf build/ dist/ *.egg-info/
	find . -name "*.pyc" -delete
	find . -name "__pycache__" -delete

# Build documentation
docs:
	pip install mkdocs-material mkdocs-autorefs
	mkdocs build

# Development setup
dev: install
	pre-commit install

# Quick start
start:
	python -m cai.cli interactive

# LiteLLM Integration Targets
litellm-setup:
	@echo "🔧 Setting up LiteLLM with Docker Offload..."
	docker offload start || echo "Using local Docker"
	cd external-tools/litellm && DOCKER_BUILDKIT=1 COMPOSE_DOCKER_CLI_BUILD=1 ./setup.sh

litellm-start:
	@echo "🚀 Starting LiteLLM services with Cloud Builder..."
	cd external-tools/litellm && DOCKER_BUILDKIT=1 COMPOSE_DOCKER_CLI_BUILD=1 BUILDX_BUILDER=cloud-knightprojekslancerr-knight-lancerr-cloudbuilder docker-compose up -d

litellm-stop:
	@echo "🛑 Stopping LiteLLM services..."
	cd external-tools/litellm && docker-compose down

litellm-test:
	@echo "🧪 Testing LiteLLM integration..."
	python external-tools/litellm/integrate_with_cerberus.py --test

litellm-logs:
	@echo "📋 Showing LiteLLM logs..."
	cd external-tools/litellm && docker-compose logs -f

litellm-integrate:
	@echo "🔗 Running LiteLLM integration..."
	python external-tools/litellm/integrate_with_cerberus.py

# MCP Integration Targets
.PHONY: mcp-setup mcp-start mcp-stop mcp-status

mcp-setup:
	@echo "🔧 Setting up MCP servers..."
	cd external-tools/mcp && ./scripts/start-mcp-servers.sh

mcp-start:
	@echo "🚀 Starting MCP servers..."
	cd external-tools/mcp && ./scripts/start-mcp-servers.sh

mcp-stop:
	@echo "🛑 Stopping MCP servers..."
	cd external-tools/mcp && ./scripts/stop-mcp-servers.sh

mcp-status:
	@echo "📋 Checking MCP server status..."
	cd external-tools/mcp && ls -la logs/*.pid 2>/dev/null || echo "No MCP servers running"

# SuperGateway Integration Targets
.PHONY: gateway-setup gateway-start gateway-stop gateway-status

gateway-setup:
	@echo "🔧 Setting up SuperGateway..."
	cd external-tools/supergateway && ./scripts/setup.sh

gateway-start:
	@echo "🚀 Starting SuperGateway..."
	cd external-tools/supergateway && ./start.sh &

gateway-stop:
	@echo "🛑 Stopping SuperGateway..."
	pkill -f "supergateway" || echo "SuperGateway not running"

gateway-status:
	@echo "📋 Checking SuperGateway status..."
	curl -s http://localhost:3000/health || echo "SuperGateway not responding"

# Metabigor OSINT Integration Targets
.PHONY: metabigor-setup metabigor-test metabigor-examples

metabigor-setup:
	@echo "🔧 Setting up Metabigor OSINT tool..."
	cd external-tools/reconnaissance/metabigor && ./setup.sh

metabigor-test:
	@echo "🧪 Testing Metabigor integration..."
	cd external-tools/reconnaissance/metabigor && ./metabigor --help

metabigor-examples:
	@echo "🔍 Running Metabigor examples..."
	python examples/osint/metabigor_examples.py

# Docker Pro Integration Targets with Offload
.PHONY: docker-setup docker-start docker-stop docker-status docker-offload docker-build docker-clean

docker-setup:
	@echo "🐳 Setting up Docker Pro configuration with Offload..."
	@echo "Enabling Docker Offload..."
	docker offload start || echo "Docker Offload not available, using local Docker"
	./docker-quick-setup.sh

docker-start:
	@echo "🚀 Starting Docker services with Cloud Builder..."
	DOCKER_BUILDKIT=1 COMPOSE_DOCKER_CLI_BUILD=1 BUILDX_BUILDER=cloud-knightprojekslancerr-knight-lancerr-cloudbuilder docker compose up -d

docker-stop:
	@echo "🛑 Stopping Docker services..."
	docker compose down

docker-status:
	@echo "📋 Checking Docker services status..."
	docker compose ps
	@echo "Docker Offload status:"
	docker offload status || echo "Docker Offload not available"

docker-offload:
	@echo "☁️ Managing Docker Offload..."
	docker offload start || echo "Docker Offload not available"

docker-build:
	@echo "☁️ Building with Docker Buildx Cloud Builder..."
	docker buildx build --builder cloud-knightprojekslancerr-knight-lancerr-cloudbuilder .

docker-clean:
	@echo "🧹 Cleaning Docker resources with Offload..."
	docker system prune -f
	docker volume prune -f
	docker image prune -f

# Docker Cloud Builder Management
.PHONY: cloud-builder-setup cloud-builder-status cloud-builder-use cloud-builder-build

cloud-builder-setup:
	@echo "☁️ Setting up Docker Buildx Cloud Builder..."
	docker buildx create --driver cloud knightprojekslancerr/knight-lancerr-cloudbuilder || echo "Builder already exists"

cloud-builder-status:
	@echo "📊 Docker Buildx Cloud Builder Status:"
	docker buildx ls | grep cloud-knightprojekslancerr || echo "Cloud builder not found"

cloud-builder-use:
	@echo "🔄 Using Docker Buildx Cloud Builder..."
	docker buildx use cloud-knightprojekslancerr-knight-lancerr-cloudbuilder

cloud-builder-build:
	@echo "🔨 Building with Docker Buildx Cloud Builder..."
	docker buildx build --builder cloud-knightprojekslancerr-knight-lancerr-cloudbuilder --platform linux/amd64,linux/arm64 .

# Hugging Face WhiteRabbitNeo Integration Targets
.PHONY: huggingface-setup huggingface-start huggingface-stop huggingface-test huggingface-logs

# WhiteRabbitNeo is now part of the unified stack
# Use: make stack-start, make stack-logs, etc.

# Transformers Direct Integration
.PHONY: transformers-setup transformers-test transformers-install

transformers-setup:
	@echo "🤗 Setting up Transformers integration..."
	./scripts/setup-transformers.sh

transformers-install:
	@echo "📦 Installing Transformers dependencies..."
	pip install torch transformers accelerate bitsandbytes

transformers-test:
	@echo "🧪 Testing Transformers WhiteRabbitNeo..."
	python tools/huggingface/transformers_adapter.py

# Code Functions Integration
.PHONY: code-functions-test code-functions-example

code-functions-test:
	@echo "🔐 Testing Code Functions adapter..."
	python tools/huggingface/code_functions_adapter.py

code-functions-example:
	@echo "💻 Running Code Functions example..."
	python examples/huggingface/code_functions_example.py

# Unified CAI-CERBERUS Stack
.PHONY: stack-build stack-start stack-stop stack-logs stack-shell stack-status

stack-build:
	@echo "🐳 Building CAI-CERBERUS unified stack..."
	docker offload start || echo "Using local Docker"
	DOCKER_BUILDKIT=1 BUILDX_BUILDER=cloud-knightprojekslancerr-knight-lancerr-cloudbuilder docker compose build

stack-start:
	@echo "🚀 Starting CAI-CERBERUS unified stack (1 container + Redis + PostgreSQL + N8N)..."
	docker compose up -d

stack-stop:
	@echo "🛑 Stopping CAI-CERBERUS unified stack..."
	docker compose down

stack-logs:
	@echo "📋 Showing CAI-CERBERUS unified stack logs..."
	docker compose logs -f

stack-shell:
	@echo "🐚 Entering CAI-CERBERUS unified container..."
	docker exec -it cai-cerberus-unified bash

stack-status:
	@echo "📊 CAI-CERBERUS unified stack status..."
	docker compose ps
	@echo "Services in unified container:"
	docker exec cai-cerberus-unified supervisorctl status || echo "Container not running"

stack-restart:
	@echo "🔄 Restarting CAI-CERBERUS unified stack..."
	docker compose restart

stack-clean:
	@echo "🧹 Cleaning CAI-CERBERUS stack..."
	docker compose down -v
	docker system prune -f

# =======================
# llama-cpp-python (macOS Metal/local)
# =======================
LLAMACPP_DIR := external-tools/llama-cpp-python
LLAMACPP_SETUP := $(LLAMACPP_DIR)/setup-macos-metal.sh
LLAMACPP_ADAPTER := $(LLAMACPP_DIR)/llama_cpp_adapter.py

.PHONY: llama.setup
llama.setup:
	@echo "[llama] Setting up macOS Metal environment via Miniforge and pip..."
	@bash $(LLAMACPP_SETUP)

.PHONY: llama.start
llama.start:
	@echo "[llama] Starting local OpenAI-compatible server via adapter..."
	@conda run -n $${ENV_NAME:-llama} python $(LLAMACPP_ADAPTER)

.PHONY: llama.start.model
llama.start.model:
	@echo "[llama] Starting server with explicit model path (LLAMACPP_MODEL must be set) ..."
	@test -n "$$LLAMACPP_MODEL" || (echo "LLAMACPP_MODEL not set" && exit 1)
	@conda run -n $${ENV_NAME:-llama} python $(LLAMACPP_ADAPTER) --model "$$LLAMACPP_MODEL"

.PHONY: llama.stop
llama.stop:
	@echo "[llama] Stop the process manually (foreground server). For background use a process manager or tmux." 

.PHONY: llama.model.download
llama.model.download:
	@echo "[llama] Downloading GGUF model via huggingface-cli (requires HF auth if gated) ..."
	@test -n "$$MODEL_ID" || (echo "Set MODEL_ID (e.g., TheBloke/CodeLlama-7B-GGUF)" && exit 1)
	@test -n "$$MODEL_FILE" || (echo "Set MODEL_FILE (e.g., codellama-7b.Q4_0.gguf)" && exit 1)
	@mkdir -p $(LLAMACPP_DIR)/models
	@huggingface-cli download "$$MODEL_ID" "$$MODEL_FILE" --local-dir $(LLAMACPP_DIR)/models