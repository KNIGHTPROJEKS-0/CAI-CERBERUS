# External Tools for CAI-CERBERUS

This directory contains external tools and integrations for the CAI-CERBERUS framework.

## Directory Structure

```
external-tools/
├── litellm/           # LiteLLM proxy for multi-model AI access
├── mcp/               # Model Context Protocol servers
├── supergateway/      # Protocol gateway for MCP transport
├── datasets/          # Code Functions and cybersecurity datasets
├── reconnaissance/    # Reconnaissance and OSINT tools
├── vulnerability/     # Vulnerability scanning tools
├── analysis/          # Analysis and forensics tools
├── exploitation/      # Exploitation frameworks (ethical use only)
└── workflows/         # N8N workflow automation
```

## Available Tools

### 🤖 AI and Model Integration
- **WhiteRabbitNeo 13B** - Cybersecurity-focused language model via TGI and transformers
- **Code Functions** - Cybersecurity and general code generation datasets
- **LiteLLM** - Multi-provider AI model proxy with cost tracking and safety controls
- **MCP Servers** - Model Context Protocol servers for various capabilities
- **SuperGateway** - Protocol translation gateway for MCP transport

### 🔍 Reconnaissance Tools
- **Metabigor** - Intelligence tool for OSINT tasks without API keys
- **Nmap** - Network discovery and security auditing
- **Subfinder** - Subdomain discovery tool
- **Amass** - In-depth attack surface mapping
- **RedEye** - Collaborative penetration testing platform

### 🛡️ Vulnerability Assessment
- **Nuclei** - Fast and customizable vulnerability scanner
- **SQLMap** - Automatic SQL injection and database takeover tool

### 📊 Analysis Tools
- **Custom analyzers** - Specialized analysis tools for security assessment

### 🔄 Workflow Automation
- **N8N** - Visual workflow automation and orchestration platform
- **Railway** - Cloud deployment and hosting integration
- **Docker Offload** - Cloud-based container execution for heavy workloads

### 📈 Datasets
- **Code-Functions-Level-Cyber** - Cybersecurity code generation dataset
- **Code-Functions-Level-General** - General purpose code generation dataset

## Quick Start

### 1. Setup All Tools
```bash
# Setup WhiteRabbitNeo and transformers
make transformers-setup

# Setup Code Functions datasets
make code-functions-setup

# Setup LiteLLM
make litellm-setup

# Setup MCP servers
make mcp-setup

# Setup SuperGateway
make gateway-setup

# Setup Metabigor OSINT tool
make metabigor-setup

# Setup N8N workflows
make n8n-setup
```

### 2. Start Services
```bash
# Start entire CAI-CERBERUS stack
make stack-start

# Or start individual services:
# Start WhiteRabbitNeo TGI
make whiterabbitneo-start

# Start LiteLLM proxy
make litellm-start

# Start N8N workflows
make n8n-start

# Start MCP servers
make mcp-start

# Start SuperGateway
make gateway-start
```

### 3. Verify Installation
```bash
# Check entire stack status
make stack-status

# Or check individual services:
# Check WhiteRabbitNeo TGI
curl http://localhost:8080/health

# Check LiteLLM
curl http://localhost:4000/health

# Check N8N
curl http://localhost:5678/healthz

# Check SuperGateway
curl http://localhost:3000/health

# Check MCP servers
make mcp-status

# Test Code Functions
make code-functions-test
```

## Integration with CAI-CERBERUS

### Environment Configuration
```bash
# WhiteRabbitNeo Integration
export WHITERABBITNEO_MODEL_PATH=WhiteRabbitNeo/WhiteRabbitNeo-13B
export WHITERABBITNEO_TGI_URL=http://localhost:8080
export WHITERABBITNEO_DEVICE=cuda  # or cpu

# Code Functions Integration
export CODE_FUNCTIONS_CYBER_PATH=./external-tools/datasets/code-functions-level-cyber
export CODE_FUNCTIONS_GENERAL_PATH=./external-tools/datasets/code-functions-level-general

# LiteLLM Integration
export CERBERUS_MODEL=litellm/gpt-4o-mini
export LITELLM_PROXY_URL=http://localhost:4000
export LITELLM_MASTER_KEY=your-master-key

# N8N Integration
export N8N_HOST=localhost
export N8N_PORT=5678
export N8N_PROTOCOL=http

# MCP Integration
export CERBERUS_MCP_ENABLED=true
export CERBERUS_MCP_SERVERS_DIR=./external-tools/mcp

# SuperGateway Integration
export CERBERUS_MCP_GATEWAY_URL=http://localhost:3000
export CERBERUS_MCP_GATEWAY_ENABLED=true

# Railway Cloud Integration
export RAILWAY_TOKEN=your-railway-token
export RAILWAY_PROJECT_ID=your-project-id
```

### Usage Examples

#### Using WhiteRabbitNeo for Cybersecurity Analysis
```python
from tools.huggingface.transformers_adapter import TransformersAdapter

# Create WhiteRabbitNeo agent
whiterabbit = TransformersAdapter(
    model_name="WhiteRabbitNeo/WhiteRabbitNeo-13B",
    device="cuda"
)

# Analyze security code
result = await whiterabbit.analyze_code(
    "Analyze this network scanning script for vulnerabilities",
    code_snippet
)
```

#### Using Code Functions for Code Generation
```python
from tools.huggingface.code_functions_adapter import CodeFunctionsAdapter

# Create code generation agent
code_gen = CodeFunctionsAdapter()

# Generate cybersecurity code
result = await code_gen.generate_code(
    "Create a secure network scanner function",
    domain="cybersecurity"
)
```

#### Using LiteLLM with CAI-CERBERUS
```python
from cai import Agent
from tools.proxy.cerberus_litellm import CerberusLiteLLMAgent

# Create LiteLLM-powered agent
agent = CerberusLiteLLMAgent()

# Use multiple models with cost tracking
result = await agent.complete_task(
    "Analyze this network scan",
    model="litellm/gpt-4o-mini"
)
```

#### Using MCP Servers
```python
from tools.mcp.supergateway_adapter import SuperGatewayAdapter

# Connect to filesystem server via SuperGateway
gateway = SuperGatewayAdapter()
files = await gateway.call_gateway(
    "sse", 
    "/mcp/filesystem", 
    "list_files", 
    {"path": "/workspace"}
)
```

## Tool-Specific Documentation

- [WhiteRabbitNeo Integration](../docs/whiterabbitneo.md)
- [Code Functions Datasets](datasets/README.md)
- [LiteLLM Setup and Usage](litellm/README.md)
- [N8N Workflow Automation](workflows/README.md)
- [MCP Servers Configuration](mcp/README.md)
- [SuperGateway Integration](supergateway/README.md)
- [Metabigor OSINT Tool](reconnaissance/metabigor/README.md)
- [Reconnaissance Tools](reconnaissance/README.md)
- [Vulnerability Scanners](vulnerability/README.md)

## Security Considerations

### Access Controls
- All tools run with minimal required permissions
- Network access is restricted to necessary endpoints
- File system access is sandboxed to designated directories

### Audit and Compliance
- All tool operations are logged for audit purposes
- Cost tracking and budget limits prevent abuse
- Human approval gates for sensitive operations

### Safe Usage Guidelines
1. **Only use on systems you own or have explicit permission to test**
2. **Follow all applicable laws and regulations**
3. **Implement proper access controls and monitoring**
4. **Regular security updates and vulnerability assessments**

## Troubleshooting

### Common Issues

1. **Port conflicts**
   - WhiteRabbitNeo TGI: Change port 8080 in docker-compose.yml
   - LiteLLM: Change port 4000 in docker-compose.yml
   - N8N: Change port 5678 in docker-compose.yml
   - SuperGateway: Set PORT environment variable
   - MCP servers: Configure different ports in servers.json

2. **Permission errors**
   - Check file/directory permissions
   - Verify Docker daemon is running
   - Ensure user has necessary privileges

3. **Network connectivity**
   - Check firewall settings
   - Verify DNS resolution
   - Test network connectivity to external services

### Getting Help

1. **Check logs**
   ```bash
   # All stack logs
   make stack-logs
   
   # Individual service logs
   docker compose logs whiterabbitneo-tgi
   docker compose logs litellm
   docker compose logs n8n
   
   # MCP server logs
   tail -f external-tools/mcp/logs/*.log
   
   # SuperGateway logs
   tail -f external-tools/supergateway/logs/*.log
   ```

2. **Health checks**
   ```bash
   # Test all services
   make stack-status
   make transformers-test
   make code-functions-test
   make litellm-test
   make mcp-status
   make gateway-status
   ```

3. **Reset and restart**
   ```bash
   # Stop all services
   make stack-stop
   
   # Clean and restart
   make clean install
   make stack-start
   
   # Or individual services
   make litellm-stop mcp-stop gateway-stop
   make litellm-start mcp-start gateway-start
   ```

## Contributing

When adding new external tools:

1. Create appropriate directory structure
2. Include comprehensive README.md
3. Add setup and management scripts
4. Update main Makefile with new targets
5. Document integration with CAI-CERBERUS
6. Include security considerations
7. Add troubleshooting information

## License and Compliance

External tools may have different licenses and usage restrictions. Always review and comply with:

- Individual tool licenses
- Export control regulations
- Local laws and regulations
- Organizational policies
- Ethical guidelines for security research