# CAI-CERBERUS — Cybersecurity AI Framework

> **🔗 Based on CAI**: This project is derived from the original [CAI (Cybersecurity AI) framework](https://github.com/aliasrobotics/cai) by Alias Robotics. CAI-CERBERUS represents an evolution and restructuring of the original CAI concepts with enhanced safety, modularity, and operational guidance.

**C**ybersecurity **A**I **I**ntelligence - **C**ontrolled **E**xecution **R**econnaissance **B**ehavior **E**valuation **R**esponse **U**nified **S**ystem

CAI-CERBERUS is a lightweight, open, agentic framework for building lawful security automation. It helps researchers, Red/Blue teams, and security engineers create controllable AI agents that assist with reconnaissance, validation, mitigation, and assessments—favoring human oversight, safety, and auditability.

**Status**: Active development. Use responsibly and only on systems you own or have explicit permission to test.

## Key Features

- **Multi-model support**: OpenAI, Anthropic, DeepSeek, Ollama, WhiteRabbitNeo, and more via LiteLLM-compatible backends
- **Advanced AI Integration**: WhiteRabbitNeo 13B model for complex cybersecurity analysis and code generation
- **Code Functions**: Specialized datasets for cybersecurity and general code generation with ethical constraints
- **Tooling-first design**: OSINT, code execution, CLI, network, and custom tool adapters
- **Agent patterns**: Single/multi-agent, hierarchical, swarm, handoffs, and delegation chains
- **Workflow Automation**: N8N integration for complex security workflows and orchestration
- **Cloud Deployment**: Railway integration with Docker Offload for scalable cloud execution
- **Human-in-the-Loop (HITL)**: Interruptible flows with human oversight and approval gates
- **Tracing & observability**: OpenTelemetry-compatible traces for reproducibility and audit trails
- **Extensible Python SDK**: Modular architecture with clear separation of concerns
- **Safety-first**: Built-in guardrails, workspace isolation, and cost/execution limits

> **Important**: CAI-CERBERUS is a standalone continuation of the original [CAI framework](https://github.com/aliasrobotics/cai), rebuilt and restructured for clarity, safety, and extensibility. All core concepts and architectural patterns derive from the original CAI project. See "Provenance & Attribution."

## Why CAI-CERBERUS

- Built for practical, lawful cybersecurity automation with strong guardrails
- Agentic architecture that stays transparent, debuggable, and human-steerable
- Minimal dependencies, fast iteration, and a consistent developer experience
- Clear separation of concerns: agents, tools, patterns, memory, and I/O
- Works across providers and local models; optimize for cost, latency, or accuracy

## Who this is for

- Security researchers and engineers
- Red/Blue/Purple teams
- Educators and students in cybersecurity
- Builders of auditable, policy-compliant AI systems for security workflows

## Quick Setup

### Prerequisites
- **Python 3.12+** (required for modern async/await patterns)
- **Virtual environment** (integrated cai_env provided)
- **API keys** for your preferred model provider(s)
- **Git** for cloning and version control
- **Docker** (optional, for containerized services)

### Installation

```bash
# Clone and enter directory
git clone https://github.com/KNIGHTPROJEKS-0/CAI-CERBERUS.git
cd CAI-CERBERUS

# Activate integrated virtual environment
source cai_env/bin/activate  # Windows: cai_env\Scripts\activate

# Install CAI-CERBERUS framework
pip install -e .
```

### Environment Configuration

```bash
# Copy environment template
cp .env.example .env

# Edit .env file with your API keys
# Minimum required:
# OPENAI_API_KEY=sk-your-key-here
# CERBERUS_MODEL=openai/gpt-4o
```

### Install External Security Tools

```bash
# Essential reconnaissance tools
cd external-tools/reconnaissance/
git clone https://github.com/nmap/nmap.git
git clone https://github.com/projectdiscovery/subfinder.git
git clone https://github.com/OWASP/Amass.git
cd ../..

# Essential vulnerability tools
cd external-tools/vulnerability/
git clone https://github.com/projectdiscovery/nuclei.git
git clone https://github.com/sullo/nikto.git
git clone https://github.com/sqlmapproject/sqlmap.git
cd ../..

# Set permissions and environment
find external-tools/ -name "*.py" -exec chmod +x {} \;
find external-tools/ -name "*.sh" -exec chmod +x {} \;
chmod 755 workspaces/
chmod 700 workspaces/default/
chmod 700 audit/

# Update .env with tool paths
echo "CERBERUS_EXTERNAL_TOOLS_DIR=$(pwd)/external-tools" >> .env
echo "CERBERUS_WORKSPACE_DIR=$(pwd)/workspaces" >> .env
echo "CERBERUS_AUDIT_DIR=$(pwd)/audit" >> .env
```

### Verify Installation

```bash
# Initialize and check system status
cai --init

# Verify virtual environment integration
which python  # Should show cai_env/bin/python

# Check tool paths and configuration
echo $NMAP_PATH
echo $NUCLEI_PATH

# Test WhiteRabbitNeo model availability
python -c "from cai_cerberus import CerberusFramework; f = CerberusFramework(); print(f.get_venv_status())"
```

### Configure Allowed Targets

**IMPORTANT**: Before using any scanning tools, configure allowed targets:

```bash
# Edit .env file
CERBERUS_ALLOWED_HOSTS=example.com,192.168.1.0/24,your-test-domain.com
```

### First Agent Run

```bash
# Initialize CAI-CERBERUS workspace and configuration
cai --init

# Interactive mode with human approval
cai --workspace CERBERUS

# Check system status
cai --version
```

## Core Concepts

### Agents
Autonomous or semi-autonomous units that reason and take actions. Each agent has:
- **Role**: Specialized function (reconnaissance, analysis, execution, validation)
- **Capabilities**: Set of tools and permissions available to the agent
- **Context**: Working memory and state for the current session
- **Constraints**: Safety boundaries and operational limits

### Tools
Capabilities agents can invoke to interact with systems and data:
- **CLI Tools**: Command execution with sandboxing and validation
- **Code Tools**: Script execution, analysis, and generation
- **OSINT Tools**: Information gathering and reconnaissance
- **Network Tools**: Scanning, probing, and connectivity testing
- **Custom Tools**: Extensible adapters for specialized functions

### Handoffs
Structured delegation between specialized agents:
- **Validation**: Ensure prerequisites and permissions before transfer
- **Context Transfer**: Pass relevant state and findings between agents
- **Approval Gates**: Human oversight points for sensitive operations
- **Rollback**: Ability to revert to previous agent state if needed

### Patterns
Orchestrations for multi-agent collaboration:
- **Hierarchy**: Chain of command with escalation paths
- **Swarm**: Parallel execution with result aggregation
- **Chain**: Sequential processing with validation checkpoints
- **Auction**: Competitive task assignment based on capability
- **Recursive**: Self-improving loops with learning integration

### Memory & State
Optional episodic/semantic memory for efficiency and reuse:
- **Session Memory**: Short-term context for current operations
- **Episodic Memory**: Historical actions and outcomes for learning
- **Semantic Memory**: Knowledge base of techniques and patterns
- **Workspace State**: Persistent artifacts and intermediate results

### HITL (Human-in-the-Loop)
Interruptible flows for human guidance and guardrails:
- **Approval Points**: Required human confirmation for sensitive actions
- **Override Capability**: Human ability to modify or halt agent behavior
- **Audit Trail**: Complete record of human interventions and decisions
- **Escalation**: Automatic human notification for anomalies or failures

### Tracing
OpenTelemetry-friendly traces for observability and postmortems:
- **Execution Traces**: Complete record of agent actions and decisions
- **Performance Metrics**: Timing, cost, and resource utilization
- **Error Tracking**: Failure modes and recovery attempts
- **Compliance Logging**: Audit-ready records for regulatory requirements

## Architecture Overview

CERBERUS focuses on coordination and execution with explicit control points and safety boundaries.

```
                    ┌─────────────────────────────────────────┐
                    │              HITL Layer                 │
                    │  ┌─────────────┐    ┌─────────────┐     │
                    │  │ Approval    │    │ Override    │     │
                    │  │ Gates       │    │ Controls    │     │
                    │  └─────────────┘    └─────────────┘     │
                    └─────────────┬───────────────────────────┘
                                  │
                                  ▼
┌─────────────┐    ┌─────────────────────────────────────────┐    ┌─────────────┐
│   Memory    │◀──►│           Agent Orchestration           │◀──►│   Tracing   │
│             │    │                                         │    │             │
│ • Session   │    │  ┌───────────┐  ┌───────────┐  ┌──────┐ │    │ • Execution │
│ • Episodic  │    │  │ Patterns  │  │ Handoffs  │  │Agents│ │    │ • Metrics   │
│ • Semantic  │    │  │           │  │           │  │      │ │    │ • Audit     │
│ • Workspace │    │  │ • Hierarchy│  │ • Validate│  │• Role│ │    │ • Errors    │
└─────────────┘    │  │ • Swarm   │  │ • Transfer│  │• Cap │ │    └─────────────┘
                   │  │ • Chain   │  │ • Approve │  │• Ctx │ │
                   │  │ • Auction │  │ • Rollback│  │• Lim │ │
                   │  └───────────┘  └───────────┘  └──────┘ │
                   └─────────────┬───────────────────────────┘
                                 │
                                 ▼
                   ┌─────────────────────────────────────────┐
                   │              Tool Layer                 │
                   │                                         │
                   │ ┌─────────┐ ┌─────────┐ ┌─────────┐     │
                   │ │   CLI   │ │  OSINT  │ │ Network │     │
                   │ │ • Exec  │ │ • Search│ │ • Scan  │     │
                   │ │ • Valid │ │ • Gather│ │ • Probe │     │
                   │ └─────────┘ └─────────┘ └─────────┘     │
                   │                                         │
                   │ ┌─────────┐ ┌─────────┐ ┌─────────┐     │
                   │ │  Code   │ │ Custom  │ │ Agent   │     │
                   │ │ • Gen   │ │ • Adapt │ │ • Tool  │     │
                   │ │ • Exec  │ │ • Extend│ │ • Proxy │     │
                   │ └─────────┘ └─────────┘ └─────────┘     │
                   └─────────────────────────────────────────┘
```

### Architecture Principles

- **Layered Security**: Multiple validation and approval layers
- **Explicit Control**: Every action requires explicit permission or validation
- **Auditability**: Complete trace of all operations and decisions
- **Modularity**: Clear separation between agents, tools, and orchestration
- **Extensibility**: Plugin architecture for custom tools and patterns
- **Safety First**: Built-in guardrails and human oversight integration

## Directory Structure

```
CAI-CERBERUS/
├── agents/                     # Agent definitions and configurations
│   ├── reconnaissance/         # Recon-specific agents
│   ├── analysis/              # Analysis agents
│   ├── execution/             # Execution agents
│   ├── validation/            # Validation agents
│   └── custom/                # Custom agent implementations
├── tools/                     # Tool implementations and adapters
│   ├── cli/                   # Command-line tools
│   ├── osint/                 # OSINT gathering tools
│   ├── network/               # Network scanning/probing tools
│   ├── code/                  # Code analysis/execution tools
│   ├── custom/                # Custom tool implementations
│   └── proxy/                 # AI model proxy tools
├── patterns/                  # Multi-agent orchestration patterns
│   ├── hierarchy/             # Hierarchical patterns
│   ├── swarm/                 # Swarm patterns
│   ├── chain/                 # Sequential chain patterns
│   └── auction/               # Auction-based patterns
├── workspaces/                # Isolated execution environments
│   ├── default/               # Default workspace
│   ├── {target-name}/         # Target-specific workspaces
│   └── temp/                  # Temporary workspaces
├── configs/                   # Configuration files
│   ├── agents/                # Agent-specific configs
│   ├── tools/                 # Tool-specific configs
│   └── environments/          # Environment configs
├── memory/                    # Memory and state storage
│   ├── episodic/              # Historical actions/outcomes
│   ├── semantic/              # Knowledge base
│   └── session/               # Current session state
├── audit/                     # Audit logs and traces
│   ├── execution/             # Execution traces
│   ├── approvals/             # Human approval records
│   └── compliance/            # Compliance logs
├── external-tools/            # Git cloned security tools
│   ├── reconnaissance/        # Recon tools (nmap, masscan, etc.)
│   ├── vulnerability/         # Vuln scanners (nuclei, etc.)
│   ├── exploitation/          # Exploit frameworks
│   ├── analysis/              # Analysis tools
│   ├── litellm/              # LiteLLM proxy with Docker setup
│   ├── mcp/                  # MCP servers
│   └── supergateway/         # Protocol gateway
├── integrations/              # Third-party integrations
│   ├── agents/               # Specialized integration agents
│   └── examples/             # Integration examples
└── examples/                  # Usage examples and demos
    ├── osint/                # OSINT examples
    ├── reconnaissance/       # Recon examples
    └── model_providers/      # Model provider examples
        ├── litellm_example.py        # Basic LiteLLM adapter usage
        ├── cerberus_litellm_example.py # Cerberus-specific LiteLLM integration
        ├── llamacpp_example.py       # LlamaCP model integration example
        └── whiterabbitneo_example.py # WhiteRabbitNeo model integration example
```

## Integrated Tools & Services

### 🔍 OSINT & Reconnaissance
- **Metabigor**: No-API-key intelligence gathering ✅
- **Nmap**: Network discovery and security auditing
- **Subfinder**: Subdomain discovery
- **Amass**: Attack surface mapping
- **RedEye**: Collaborative penetration testing

### 🤖 AI & Models
- **WhiteRabbitNeo**: 13B parameter cybersecurity-focused model ✅
- **Code Functions**: Cybersecurity and general code generation datasets ✅
- **LiteLLM**: Multi-provider AI proxy with comprehensive examples ✅
- **Transformers**: Direct model integration with Hugging Face ✅
- **MCP Servers**: Model Context Protocol integration
- **SuperGateway**: Protocol translation
- **LlamaCP Integration**: Dedicated example scripts for llamacpp model routes ✅
- **Model Provider Examples**: Complete usage examples for all supported providers ✅

### 🛡️ Security & Analysis
- **Nuclei**: Vulnerability scanning
- **SQLMap**: SQL injection testing
- **Nikto**: Web server scanner

### 🐳 Infrastructure
- **Docker Pro**: Container orchestration with Offload support ✅
- **PostgreSQL**: Database backend ✅
- **Redis**: Caching and session management ✅
- **Prometheus**: Metrics and monitoring ✅

### 🔄 Workflow Automation
- **N8N**: Visual workflow automation and orchestration ✅
- **Railway**: Cloud deployment and hosting ✅
- **Docker Offload**: Cloud-based container execution ✅

### 📊 Datasets & Training
- **Code-Functions-Level-Cyber**: Cybersecurity code generation dataset ✅
- **Code-Functions-Level-General**: General purpose code generation dataset ✅

### 🦙 Local AI Models
- **llama-cpp-python**: Local GGUF model server with Metal GPU support ✅
- **OpenAI-compatible API**: Drop-in replacement for cloud models
- **Metal Acceleration**: macOS GPU optimization for faster inference
- **Conda Environment**: Isolated Python environment for model dependencies

## 🦙 llama-cpp-python Integration

This project includes first-class support for running local LLMs using llama-cpp-python with OpenAI-compatible endpoints and macOS Metal acceleration.

Key components:
- external-tools/llama-cpp-python/setup-macos-metal.sh — automated setup script for Miniforge/Conda + llama-cpp-python[server]
- external-tools/llama-cpp-python/llama_cpp_adapter.py — adapter that launches the server via python -m llama_cpp.server
- Makefile targets: llama.setup, llama.start, llama.start.model, llama.stop, llama.model.download
- .env.example variables: LLAMACPP_* for model path, endpoints, GPU layers, threads

Setup (macOS + Metal):

```bash
# 1) Create and configure a dedicated conda env with Metal
make llama.setup

# 2) Optionally download a GGUF model
make llama.model.download MODEL_ID="TheBloke/CodeLlama-7B-GGUF" MODEL_FILENAME="codellama-7b.Q4_0.gguf" MODEL_DIR="./models"

# 3) Start the server using the adapter and env vars
make llama.start
# Or explicitly provide a model path
make llama.start.model MODEL="./models/codellama-7b.Q4_0.gguf"
```

Environment variables (.env):

```bash
# Local llama.cpp OpenAI-compatible server
LLAMACPP_MODEL=./models/codellama-7b.Q4_0.gguf
LLAMACPP_HOST=0.0.0.0
LLAMACPP_PORT=8080
LLAMACPP_CTX=4096
LLAMACPP_THREADS=0            # 0 = auto
LLAMACPP_N_GPU_LAYERS=1       # Increase for more Metal offload
LLAMACPP_CHAT_FORMAT=chatml   # Optional
LLAMACPP_API_BASE=http://localhost:8080/v1
```

Smoke tests:

```bash
# List models
curl -s http://localhost:8080/v1/models | jq

# Chat completion
curl -s http://localhost:8080/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "local",
    "messages": [
      {"role": "system", "content": "You are a helpful assistant."},
      {"role": "user", "content": "Say hello from llama-cpp."}
    ]
  }' | jq
```

Integration with existing OpenAI clients:
- Set base_url to LLAMACPP_API_BASE
- Reuse WhiteRabbitNeo config paths where OpenAI-compatible endpoints are accepted

Performance tips:
- Increase LLAMACPP_N_GPU_LAYERS to offload more layers to Metal
- Keep GGUF quantization balanced (e.g., Q4_0/Q5_0) for speed vs. quality

## 🐍 Conda Environment Strategy

To ensure isolation and reproducibility for native-accelerated local models, this repository uses a dedicated Conda environment for llama-cpp-python.

- Name: cai-llama (created by make llama.setup)
- Purpose: House llama-cpp-python with Metal support and its native deps
- Scope: Only used for launching the local server via the adapter script

How CAI/CAI-CERBERUS interacts with Conda:
- The core CAI-CERBERUS app remains in your primary Python/Node environments
- The local model server runs out-of-process inside the Conda env
- CAI connects to it via OpenAI-compatible HTTP endpoints (LLAMACPP_API_BASE)

When to create another Conda env:
- If you also run other native-accelerated backends (ex: vLLM, llama.cpp C binaries)
- If you want hard isolation per model family and version
- If your system Python is managed elsewhere (e.g., pyenv/poetry) and you prefer separation

Summary recommendation:
- Use the provided cai-llama Conda env for llama-cpp-python on macOS
- Keep CAI-CERBERUS itself outside Conda for maximum portability
- Communicate via OpenAI-compatible endpoints; no direct Python imports required

## Configuration

### Environment Variables

#### Model Provider Configuration
```bash
# OpenAI
OPENAI_API_KEY=sk-...
OPENAI_ORG_ID=org-...  # Optional

# Anthropic
ANTHROPIC_API_KEY=sk-ant-...

# DeepSeek
DEEPSEEK_API_KEY=sk-...

# Ollama (local)
OLLAMA_HOST=http://localhost:11434
OLLAMA_MODEL=qwen2.5:14b

# Other LiteLLM-compatible providers
LITELLM_API_KEY=...
LITELLM_BASE_URL=...
```

#### CERBERUS Core Configuration
```bash
# Default model selection
CERBERUS_MODEL=openai/gpt-4o  # or anthropic/claude-3-5-sonnet, ollama/qwen2.5:14b

# Debug and logging
CERBERUS_DEBUG=1              # 0=minimal, 1=info, 2=verbose
CERBERUS_LOG_LEVEL=INFO       # DEBUG, INFO, WARNING, ERROR

# Tracing and observability
CERBERUS_TRACING=true         # Enable OpenTelemetry traces
CERBERUS_TRACE_ENDPOINT=...   # Optional: custom trace collector

# Safety and limits
CERBERUS_PRICE_LIMIT=10.00    # USD limit per session
CERBERUS_MAX_ITERATIONS=50    # Prevent infinite loops
CERBERUS_TIMEOUT=300          # Seconds per operation

# Workspace isolation
CERBERUS_WORKSPACE=default    # Workspace identifier
CERBERUS_WORKSPACE_DIR=./workspaces  # Base directory for artifacts

# Human-in-the-Loop settings
CERBERUS_HITL_MODE=interactive  # interactive, batch, disabled
CERBERUS_AUTO_APPROVE=false     # Require human approval for sensitive ops
```

#### Security and Compliance
```bash
# Execution constraints
CERBERUS_SANDBOX_MODE=true     # Enable sandboxed execution
CERBERUS_ALLOWED_HOSTS=...     # Comma-separated list of allowed targets
CERBERUS_BLOCKED_COMMANDS=...  # Comma-separated list of blocked commands

# Audit and compliance
CERBERUS_AUDIT_LOG=true        # Enable audit logging
CERBERUS_AUDIT_DIR=./audit     # Audit log directory
CERBERUS_COMPLIANCE_MODE=...   # SOC2, HIPAA, etc.
```

## Management Commands

### Docker Services
```bash
# Start all services
make docker-start

# Stop all services
make docker-stop

# Check status
make docker-status

# Try Docker Offload (cloud builds)
make docker-offload
```

### LiteLLM
```bash
make litellm-setup     # Initial setup with Docker
make litellm-start     # Start services
make litellm-stop      # Stop services
make litellm-test      # Test integration
make litellm-logs      # View logs
```

### Metabigor OSINT
```bash
# Setup Metabigor
make metabigor-setup

# Test functionality
make metabigor-test

# Run examples
make metabigor-examples

# Direct usage
echo "example.com" | ./external-tools/reconnaissance/metabigor/metabigor related -s cert
```

### MCP Servers
```bash
make mcp-setup         # Setup MCP servers
make mcp-start         # Start all configured servers
make mcp-stop          # Stop all servers
make mcp-status        # Check server status
```

### SuperGateway
```bash
make gateway-setup     # Build and configure
make gateway-start     # Start gateway service
make gateway-stop      # Stop gateway service
make gateway-status    # Check gateway health
```

### WhiteRabbitNeo & Code Functions
```bash
make transformers-setup    # Setup transformers integration
make code-functions-test   # Test code functions adapter
make code-functions-example # Run code generation examples
```

### Unified Stack Management
```bash
make stack-build       # Build entire CAI-CERBERUS stack
make stack-start       # Start all services (WhiteRabbitNeo, N8N, etc.)
make stack-stop        # Stop all services
make stack-logs        # View all service logs
make stack-status      # Check service status
```

### Workspace Management
```bash
# Create Python virtual environment for workspace
cai --workspace CERBERUS --set --venv

# Create Conda environment for workspace
cai --workspace ORTHOS --set --conda

# Specify Python version for virtual environment
cai --workspace CERBERUS --set --venv --python 3.12

# Check workspace status
cai --workspace CERBERUS --status
```

## Agent Operation Guide

### For LLMs and AI Agents

When operating within the CAI-CERBERUS framework, you have access to:

#### **Core Framework Components:**
- **Virtual Environment**: Integrated `cai_env/` with all dependencies
- **Configuration System**: Unified config via `cai_cerberus/config.py`
- **Workspace Management**: CERBERUS workspace in `workspaces/CERBERUS/`
- **Tool Integration**: 7 external security tools with validated paths
- **Model Access**: WhiteRabbitNeo/WhiteRabbitNeo-13B-v1 as primary model

#### **Available CLI Commands:**
```bash
cai --init          # Initialize workspace and configuration
cai --version       # Show framework version and status
cai --workspace X   # Switch to workspace X
cerberus --init     # Alternative command
```

When operating within the CAI-CERBERUS framework, follow these operational patterns:

#### 1. Agent Initialization
```python
# Initialize CAI-CERBERUS framework first
from cai_cerberus import CerberusFramework, Agent

# Framework automatically activates cai_env and loads configuration
framework = CerberusFramework(workspace="CERBERUS")
framework.initialize()

# Create agent with WhiteRabbitNeo model
agent = Agent(
    name="reconnaissance_agent",
    model="WhiteRabbitNeo/WhiteRabbitNeo-13B-v1"
)

# Access tool paths
nmap_path = framework.get_tool_path("nmap")
nuclei_path = framework.get_tool_path("nuclei")
```

#### 2. Task Execution Pattern
```python
# Follow the standard execution pattern
async def execute_task(task, context):
    # 1. Validate task and permissions
    if not validate_permissions(task, context):
        return await request_approval(task)
    
    # 2. Plan execution steps
    plan = await create_execution_plan(task)
    
    # 3. Execute with checkpoints
    for step in plan:
        result = await execute_step(step)
        await log_step_result(step, result)
        
        # Check for human intervention
        if requires_approval(step):
            await request_human_approval(step, result)
    
    # 4. Validate and return results
    return await validate_results(results)
```

#### 3. Tool Usage Guidelines
- **Always validate** tool permissions before execution
- **Log all actions** for audit trail
- **Request approval** for sensitive operations
- **Handle errors gracefully** with rollback capability
- **Respect rate limits** and cost constraints

#### 4. Handoff Protocols
```python
# When delegating to another agent
handoff_context = {
    "task": current_task,
    "findings": current_findings,
    "constraints": inherited_constraints,
    "approval_status": approval_history
}

next_agent = await select_agent_for_task(remaining_task)
result = await handoff_to_agent(next_agent, handoff_context)
```

#### 5. Safety Protocols
- **Never bypass** approval gates
- **Always respect** workspace isolation
- **Validate all inputs** before processing
- **Report anomalies** immediately
- **Maintain audit trail** for all actions

## Python API Examples

### Basic Usage
```python
from caicerberus import CerberusFramework, Agent, ReconTool

# Initialize framework
cerberus = CerberusFramework(
    model="openai/gpt-4o",
    workspace="quickstart",
    hitl_mode="interactive"
)

# Create a reconnaissance agent
recon_agent = Agent(
    role="reconnaissance",
    tools=[ReconTool()],
    constraints={"max_iterations": 10, "require_approval": True}
)

# Execute task
result = await cerberus.execute(
    agent=recon_agent,
    task="Gather information about target system",
    target="example.com"
)

print(f"Task completed: {result.status}")
print(f"Findings: {result.findings}")
```

### LiteLLM Model Provider Examples

The project includes comprehensive examples for all supported model providers:

#### WhiteRabbitNeo Integration
```python
# Run the WhiteRabbitNeo example
python examples/model_providers/whiterabbitneo_example.py

# Required environment variables:
# LITELLM_PROXY_URL=http://localhost:4000
# LITELLM_MASTER_KEY=your-master-key
# WHITERABBITNEO_API_BASE=http://localhost:8001  # Optional
```

#### LlamaCP Integration
```python
# Run the LlamaCP example
python examples/model_providers/llamacpp_example.py

# Required environment variables:
# LITELLM_PROXY_URL=http://localhost:4000
# LITELLM_MASTER_KEY=your-master-key
# LLAMACPP_API_BASE=http://localhost:8080  # Optional
```

#### Basic LiteLLM Adapter Usage
```python
from tools.proxy.litellm_adapter import LiteLLMAdapter
import asyncio

async def example_usage():
    # Initialize adapter with correct constructor parameters
    adapter = LiteLLMAdapter(
        base_url="http://localhost:4000",  # Note: base_url, not proxy_url
        master_key="your-master-key"
    )
    
    # Check proxy health
    health = await adapter.check_health()
    print(f"Proxy health: {health}")
    
    # List available models
    models = await adapter.list_models()
    print(f"Available models: {models}")
    
    # Complete chat
    messages = [{"role": "user", "content": "Hello, world!"}]
    response = await adapter.complete_chat(messages, "gpt-3.5-turbo")
    print(f"Response: {response}")
    
    # Get cost estimate
    cost = await adapter.get_cost_estimate(messages, "gpt-3.5-turbo")
    print(f"Estimated cost: {cost}")
    
    # Validate request safety
    safety = await adapter.validate_request_safety(messages, "gpt-3.5-turbo")
    print(f"Safety validation: {safety}")

# Run the example
asyncio.run(example_usage())
```

### Using Metabigor OSINT
```python
from integrations.agents.metabigor_agent import MetabigorAgent
from tools.proxy.cerberus_litellm import CerberusLiteLLMAgent

# Create OSINT agent
osint_agent = MetabigorAgent()

# Discover organization assets
result = await osint_agent.discover_organization_assets("Example Corp")

# Use with LiteLLM for AI-powered analysis
llm_agent = CerberusLiteLLMAgent()
analysis = await llm_agent.analyze_osint_results(result)
```

## Troubleshooting

### Docker Issues
```bash
# Restart services
make docker-stop && make docker-start

# Check logs
docker compose logs litellm

# Reset everything
docker compose down -v && make docker-start
```

### Tool Not Found
```bash
# Check tool path
ls -la external-tools/reconnaissance/nmap/nmap

# Verify environment variables
echo $CERBERUS_EXTERNAL_TOOLS_DIR
```

### Permission Denied
```bash
# Fix permissions
chmod +x external-tools/reconnaissance/nmap/nmap
```

### Target Not Allowed
```bash
# Add target to allowed hosts
echo "CERBERUS_ALLOWED_HOSTS=your-target.com" >> .env
```

## Legal Disclaimer

### **1. Compliance & Intended Use**
CAI-CERBERUS is an AI-powered cybersecurity evaluation tool intended to assist in security assessments of robotic and other automated systems. It is designed to operate under a "human-on-the-loop" principle, ensuring oversight and mitigating risks associated with autonomous decision-making.

The software is developed in alignment with **ethical AI principles** and is intended to support compliance with the **EU AI Act** and other applicable cybersecurity regulations. However, it is the sole responsibility of the user to ensure adherence to all relevant laws and standards when deploying or modifying this software.

### **2. Open Source Notice & Responsibility**
This source code is provided under the license terms detailed in the accompanying `LICENSE` file. Portions of CAI-CERBERUS are released as **open-source** to encourage transparency and community collaboration.

Please note:
- The software is provided "**as is**", without warranty of any kind.
- The authors and contributors assume **no liability** for any damages, data loss, or legal consequences arising from its use.
- Users must conduct **appropriate testing and validation** before deploying this software in any production or mission-critical environment.

### **3. Security & Ethical Use**
- **Non-Disruptive Use Only:** CAI-CERBERUS is intended for research, education, and evaluation purposes. It must **not** be used to disrupt, manipulate, or interfere with live production systems.
- **Authorized Access Required:** Cybersecurity assessments or testing using this tool must be conducted **only with explicit permission** from the system owner.
- **Qualified Use:** This software should be used by **trained professionals** following industry best practices and applicable organizational security policies.

### **4. Limitations**
- Use of this tool does **not guarantee** full protection against cyber threats or compliance with any regulatory framework.
- It is **not a substitute** for formal cybersecurity audits, penetration testing services, or legal compliance assessments.
- Users are fully responsible for the consequences of how they apply or modify the code.

### **5. Contact & Contributions**
We welcome community contributions to improve CAI-CERBERUS. To contribute, report bugs, or request clarification on legal or compliance issues, please use GitHub Issues.

---

By downloading, using, or modifying this source code, you agree to the terms of the `LICENSE` and the limitations outlined in this disclaimer.

## What's new in CERBERUS

Compared to the original upstream concept, CAI-CERBERUS emphasizes:
- Standalone structure and naming for clarity and maintenance
- Stricter safety posture and documentation-first workflows
- Cleaner tool/plugin boundaries and agent-as-tool ergonomics
- Optional cost/latency guardrails and price limits per run
- Workspace isolation and better reproducibility for experiments
- Streamlined developer experience and comprehensive agent operation guides

Note: Some features may be gated behind environment variables or optional components. See Configuration.

## Recent Updates & Implementations

### 🆕 Latest Changes (Current Release)

#### **LiteLLM Model Provider Examples** ✅
- **New**: `examples/model_providers/whiterabbitneo_example.py` - Complete WhiteRabbitNeo integration example
- **New**: `examples/model_providers/llamacpp_example.py` - LlamaCP model integration with multi-model fallback
- **Enhanced**: All examples include proxy health checks, model discovery, completion testing, cost estimation, and safety validation
- **Fixed**: LiteLLMAdapter constructor usage - changed `proxy_url` to `base_url` parameter across all examples
- **Verified**: All adapter method signatures (`get_cost_estimate`, `complete_chat`, `validate_request_safety`) aligned with implementation

#### **Workspace Management Enhancements** ✅
- **Enhanced**: `src/cai/repl/commands/workspace.py` `handle_set` method with new flags:
  - `--venv`: Create Python virtual environment for workspace isolation
  - `--conda`: Create Conda environment for specialized dependencies
  - `--python X.Y`: Specify Python version for virtual environments
- **Integration**: Seamless workspace environment management via CAI CLI
- **Examples**: `cai --workspace CERBERUS --set --venv --python 3.12`

#### **Documentation & Configuration Updates** ✅
- **Updated**: README.md with comprehensive LiteLLM examples and usage patterns
- **Added**: Workspace management command documentation
- **Enhanced**: Model provider integration sections with environment variable requirements
- **Clarified**: LiteLLMAdapter constructor parameters and method signatures

#### **Code Quality & Compatibility** ✅
- **Fixed**: Constructor parameter mismatch in LiteLLM examples (`proxy_url` → `base_url`)
- **Verified**: Method signature compatibility across all adapter implementations
- **Enhanced**: Error handling and validation in example scripts
- **Maintained**: Backward compatibility with existing configurations

### 🔄 Integration Status
- **LiteLLM Proxy**: Fully operational with Docker setup ✅
- **WhiteRabbitNeo Models**: Integrated with dedicated examples ✅
- **LlamaCP Models**: Supported with comprehensive examples ✅
- **Workspace Environments**: Python venv and Conda support ✅
- **Model Route Discovery**: Automatic detection and validation ✅

### 📋 Pending Tasks
- **llama-cpp-python Examples**: Hugging Face GGUF model integration examples
- **Docker Compose**: Optional llama-cpp-python service configuration
- **Advanced Patterns**: Multi-agent handoff examples with LiteLLM
- **Performance Optimization**: Model-specific configuration templates

## Safety, Ethics, and Scope

- Use only on assets you own or have explicit written permission to test
- Comply with all applicable laws and regulations
- No secrets/credentials should be committed to the repository
- The maintainers and contributors do not endorse misuse; violations may be reported

By using this project you agree to the LICENSE and any additional disclaimers within the repository.

## Roadmap (high level)

- Improved multi-agent pattern library and handoff filters
- Expanded tool adapters and safer execution sandboxes
- First-class memory strategies (episodic/semantic) with opt-in storage
- Richer tracing dashboards and cost/latency analytics
- Additional provider routes and local model presets
- Enhanced agent operation guides and best practices
- Integration with popular security frameworks and tools

## Contributing

- Please read README and project rules before opening PRs
- Prefer small, focused changes with tests and docs
- Follow repository linting/formatting and CI requirements
- Open issues for proposals, questions, or clarifications

We welcome community contributions that improve safety, clarity, performance, or capability.

## Provenance & Attribution

**Original Source**: This project is based on the [CAI (Cybersecurity AI) framework](https://github.com/aliasrobotics/cai) developed by Alias Robotics.

**Evolution**: CAI-CERBERUS began as a fork of the original CAI project and was subsequently detached, rebuilt, and restructured with:
- Enhanced safety protocols and human oversight mechanisms
- Expanded agent operation guides for LLM integration
- Modular architecture with clearer separation of concerns
- Comprehensive configuration and deployment options
- Extended tool ecosystem and handoff patterns

**Attribution**: We acknowledge and credit the original CAI project by Alias Robotics as the foundational inspiration and source of core concepts. All licensing and attribution requirements from the upstream project are preserved as appropriate to the LICENSE and any NOTICE files.

**For LLMs/Agents**: When operating within this framework, understand that you are working with concepts and patterns originally developed in the CAI project, enhanced with additional safety and operational guidance specific to CAI-CERBERUS.

## Citation

If you publish results derived from this work, please consider citing upstream research and this repository. See the Citation section or add your own citation entry as applicable to your work.

## Acknowledgements

Thanks to the broader open-source AI and security communities for foundational components and ideas (e.g., LiteLLM-compatible providers, OpenTelemetry ecosystem, tracing/observability projects). We also acknowledge the upstream CAI project by Alias Robotics for its original framing and influence that informed this standalone evolution.

---

## 📝 Documentation Policy

**IMPORTANT**: To maintain project clarity and reduce documentation fragmentation:

1. **Single Source of Truth**: This README.md serves as the primary documentation
2. **Update Policy**: When adding new integrations, functions, or changes:
   - Update this README.md directly
   - Do NOT create additional .md files unless absolutely necessary
   - Keep all setup, configuration, and usage information consolidated here
3. **File Structure**: Always keep the directory structure section current
4. **Integration Updates**: New tools and services should be documented in the appropriate sections above

This policy ensures documentation remains current, searchable, and maintainable as the project evolves.