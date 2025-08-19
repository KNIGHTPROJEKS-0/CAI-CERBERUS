# CAI-CERBERUS — Cybersecurity AI Framework

> **🔗 Based on CAI**: This project is derived from the original [CAI (Cybersecurity AI) framework](https://github.com/aliasrobotics/cai) by Alias Robotics. CAI-CERBERUS represents an evolution and restructuring of the original CAI concepts with enhanced safety, modularity, and operational guidance.

**C**ybersecurity **A**I **I**ntelligence - **C**ontrolled **E**xecution **R**econnaissance **B**ehavior **E**valuation **R**esponse **U**nified **S**ystem

CAI-CERBERUS is a lightweight, open, agentic framework for building lawful security automation. It helps researchers, Red/Blue teams, and security engineers create controllable AI agents that assist with reconnaissance, validation, mitigation, and assessments—favoring human oversight, safety, and auditability.

**Status**: Active development. Use responsibly and only on systems you own or have explicit permission to test.

## Key Features

- **Multi-model support**: OpenAI, Anthropic, DeepSeek, Ollama, and more via LiteLLM-compatible backends
- **Tooling-first design**: OSINT, code execution, CLI, network, and custom tool adapters
- **Agent patterns**: Single/multi-agent, hierarchical, swarm, handoffs, and delegation chains
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

## Quickstart

### Prerequisites
- **Python 3.12+** (required for modern async/await patterns)
- **Virtual environment** (uv, venv, or conda recommended)
- **API keys** for your preferred model provider(s)
- **Git** for cloning and version control

### Installation

#### From Source (Recommended for Development)
```bash
# Clone the repository
git clone https://github.com/KNIGHTPROJEKS-0/CAI-CERBERUS.git
cd CAI-CERBERUS

# Create and activate virtual environment
python3.12 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Upgrade pip and install dependencies
pip install -U pip setuptools wheel
pip install -e ".[dev,test]"  # Include development dependencies
```

#### From PyPI (When Available)
```bash
pip install cai-cerberus
```

### Initial Configuration

1. **Copy environment template**:
   ```bash
   cp .env.example .env
   ```

2. **Set minimum required variables**:
   ```bash
   # Edit .env file
   OPENAI_API_KEY=sk-your-key-here
   CERBERUS_MODEL=openai/gpt-4o
   CERBERUS_WORKSPACE_DIR=./workspaces
   ```

3. **Verify installation**:
   ```bash
   cerberus --version
   cerberus config validate
   ```

### First Run

#### Interactive Mode
```bash
# Start interactive session
cerberus interactive

# Or with specific configuration
cerberus interactive --model anthropic/claude-3-5-sonnet --workspace test
```

#### CLI Mode
```bash
# Run a simple reconnaissance task
cerberus run --task "Gather basic information about example.com" --target example.com

# Run with human approval required
cerberus run --task "Port scan localhost" --hitl --approve-all
```

#### Python API
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

### Verification

After installation, verify everything works:

```bash
# Check system status
cerberus status

# Validate configuration
cerberus config validate

# Test model connectivity
cerberus test models

# Run built-in examples
cerberus examples list
cerberus examples run basic-recon
```

**Note**: First run may take longer due to model initialization and workspace setup.

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

### Configuration Files

CERBERUS supports multiple configuration methods:

1. **Environment variables** (highest priority)
2. **`.env` file** in project root
3. **`cerberus.yaml`** configuration file
4. **Command-line arguments** (for CLI usage)

See `.env.example` and `cerberus.yaml.example` for complete configuration templates.

## Agent Operation Guide

### For LLMs and AI Agents

When operating within the CAI-CERBERUS framework, follow these operational patterns:

#### 1. Agent Initialization
```python
# Always initialize with clear role and constraints
agent = Agent(
    role="reconnaissance|analysis|execution|validation",
    capabilities=["tool1", "tool2"],
    constraints={
        "max_iterations": 10,
        "require_approval": True,
        "allowed_targets": ["example.com"],
        "blocked_actions": ["destructive_commands"]
    }
)
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

## What's new in CERBERUS

Compared to the original upstream concept, CAI-CERBERUS emphasizes:
- Standalone structure and naming for clarity and maintenance
- Stricter safety posture and documentation-first workflows
- Cleaner tool/plugin boundaries and agent-as-tool ergonomics
- Optional cost/latency guardrails and price limits per run
- Workspace isolation and better reproducibility for experiments
- Streamlined developer experience and comprehensive agent operation guides

Note: Some features may be gated behind environment variables or optional components. See Configuration.

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