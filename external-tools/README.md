# External Tools for CAI-CERBERUS

This directory contains external security tools and frameworks integrated with CAI-CERBERUS. Each tool is organized by category and includes safety adapters for secure operation.

## Directory Structure

```
external-tools/
├── reconnaissance/
│   └── RedEye/                 # OSINT reconnaissance tool
├── supergateway/               # MCP gateway for protocol bridging
├── litellm/                    # LiteLLM proxy for unified LLM access
├── vulnerability/              # Vulnerability assessment tools
├── exploitation/               # Controlled exploitation frameworks
├── analysis/                   # Analysis and forensics tools
└── README.md                   # This file
```

## Integrated Tools

### MCP Gateway - Supergateway
**Location**: `external-tools/supergateway/`
**Purpose**: Model Context Protocol gateway for stdio-to-SSE/WS/HTTP bridging
**Adapter**: `tools/mcp/supergateway_adapter.py`

**Features**:
- stdio-to-SSE gateway for MCP servers
- SSE-to-stdio for remote MCP integration
- StreamableHTTP support (stateful/stateless)
- WebSocket transport bridging
- Built-in security validation and audit logging

**Usage**:
```python
from tools.mcp.supergateway_adapter import SupergatewayTool

gateway = SupergatewayTool()
result = await gateway.execute(
    action="start_sse_gateway",
    mcp_server_command="npx -y @modelcontextprotocol/server-filesystem ./workspaces",
    port=8000
)
```

**Safety Features**:
- Command validation and blocking of dangerous operations
- Human approval gates for sensitive operations
- Process isolation and timeout protection
- Complete audit trail of all gateway operations
- Resource limits and port restrictions

### OSINT - RedEye
**Location**: `external-tools/reconnaissance/RedEye/`
**Purpose**: Open Source Intelligence gathering
**Adapter**: `tools/osint/redeye_adapter.py`

**Features**:
- Domain reconnaissance and enumeration
- Social media intelligence gathering
- Email and contact discovery
- Technology stack identification

**Safety Features**:
- Target validation and whitelist checking
- Rate limiting and request throttling
- Sandboxed execution environment
- Human approval for sensitive targets

## Installation Guide

### Prerequisites
- Python 3.12+
- Node.js 24+ (for supergateway)
- Git for cloning repositories
- Virtual environment (recommended)

### Installing Tools

1. **LiteLLM (Proxy Gateway)**:
```bash
cd external-tools/litellm
git clone https://github.com/BerriAI/litellm .
echo 'LITELLM_MASTER_KEY="sk-cerberus-$(openssl rand -hex 16)"' > .env
echo 'LITELLM_SALT_KEY="$(openssl rand -hex 32)"' >> .env
docker-compose up -d
```

2. **Supergateway (MCP Gateway)**:
```bash
cd external-tools/supergateway
npm install
npm run build
```

3. **RedEye (OSINT)**:
```bash
cd external-tools/reconnaissance
git clone https://github.com/cisagov/RedEye.git
cd RedEye
chmod +x redeye.py
pip install -r requirements.txt
```

### Adding New Tools

1. **Clone the tool** into appropriate category directory:
```bash
cd external-tools/[category]
git clone [tool-repository-url]
```

2. **Create safety adapter** in `tools/[category]/[tool]_adapter.py`:
```python
class ToolAdapter:
    def __init__(self):
        self.tool_path = Path("external-tools/[category]/[tool]")
        self.audit_log = []
    
    async def validate_target(self, target: str) -> bool:
        # Implement target validation
        pass
    
    async def execute_safely(self, command: str, **kwargs):
        # Implement safe execution with logging
        pass
```

3. **Add agent configuration** in `configs/agents/[tool].yaml`:
```yaml
name: "Tool Agent"
role: "tool_operator"
tools:
  - name: "tool_adapter"
    path: "tools.[category].[tool]_adapter.ToolAdapter"
constraints:
  require_approval: true
  sandbox_mode: true
```

## Security Guidelines

### Tool Integration Requirements
- All tools MUST have safety adapters with validation
- Human approval required for sensitive operations
- Complete audit logging of all actions
- Sandboxed execution where possible
- Resource limits and timeout protection

### Validation Patterns
- Target whitelist checking
- Command sanitization and blocking
- Rate limiting and throttling
- Process isolation and monitoring
- Error handling and rollback capability

### Audit Requirements
- Log all tool invocations with timestamps
- Record human approval decisions
- Track resource usage and performance
- Maintain chain of custody for evidence
- Enable compliance reporting and review

## Agent Operation Guidelines

### For LLMs/Agents using these tools:

1. **Always validate** tool permissions before execution
2. **Request approval** for sensitive or destructive operations
3. **Log all actions** for audit trail and compliance
4. **Respect rate limits** and resource constraints
5. **Handle errors gracefully** with proper rollback
6. **Report anomalies** immediately to human operators

### Tool Discovery Pattern:
```python
# Agents should discover tools in this directory structure
tool_categories = {
    "reconnaissance": ["RedEye"],
    "mcp_gateway": ["supergateway"],
    "vulnerability": [],  # Add as tools are integrated
    "exploitation": [],   # Add as tools are integrated
    "analysis": []        # Add as tools are integrated
}
```

## Compliance and Legal

- Use only on systems you own or have explicit permission to test
- Comply with all applicable laws and regulations
- Maintain proper documentation and audit trails
- Report any security violations or anomalies
- Follow organizational policies and procedures

## Contributing

When adding new tools:
1. Follow the directory structure and naming conventions
2. Create comprehensive safety adapters with validation
3. Include proper documentation and usage examples
4. Test thoroughly in isolated environments
5. Submit pull requests with security review

## Support

For issues with tool integration:
1. Check the tool's original documentation
2. Review the safety adapter implementation
3. Examine audit logs for error details
4. Consult the CAI-CERBERUS documentation
5. Open an issue with detailed reproduction steps