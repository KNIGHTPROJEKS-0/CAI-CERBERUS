# CAI-CERBERUS Directory Structure Guide

This document outlines the proper directory structure for CAI-CERBERUS and where to place different components for optimal LLM/agent operation.

## Core Directory Structure

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
│   └── external/              # Git cloned external tools
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
└── external-tools/            # Git cloned security tools
    ├── reconnaissance/        # Recon tools (nmap, masscan, etc.)
    ├── vulnerability/         # Vuln scanners (nuclei, etc.)
    ├── exploitation/          # Exploit frameworks
    └── analysis/              # Analysis tools
```

## Where to Place Git Cloned Tools

### Primary Location: `external-tools/`

Place your git cloned security tools in the `external-tools/` directory, organized by category:

```bash
# Example structure for external tools
external-tools/
├── reconnaissance/
│   ├── nmap/                  # git clone https://github.com/nmap/nmap
│   ├── masscan/               # git clone https://github.com/robertdavidgraham/masscan
│   ├── subfinder/             # git clone https://github.com/projectdiscovery/subfinder
│   └── amass/                 # git clone https://github.com/OWASP/Amass
├── vulnerability/
│   ├── nuclei/                # git clone https://github.com/projectdiscovery/nuclei
│   ├── nikto/                 # git clone https://github.com/sullo/nikto
│   └── sqlmap/                # git clone https://github.com/sqlmapproject/sqlmap
├── exploitation/
│   ├── metasploit-framework/  # git clone https://github.com/rapid7/metasploit-framework
│   └── exploit-db/            # git clone https://github.com/offensive-security/exploitdb
└── analysis/
    ├── binwalk/               # git clone https://github.com/ReFirmLabs/binwalk
    └── volatility3/           # git clone https://github.com/volatilityfoundation/volatility3
```

### Tool Integration Pattern

For each external tool, create a corresponding adapter in `tools/`:

```bash
tools/
├── cli/
│   ├── nmap_adapter.py        # Adapter for external-tools/reconnaissance/nmap/
│   ├── nuclei_adapter.py      # Adapter for external-tools/vulnerability/nuclei/
│   └── sqlmap_adapter.py      # Adapter for external-tools/vulnerability/sqlmap/
└── osint/
    ├── subfinder_adapter.py   # Adapter for external-tools/reconnaissance/subfinder/
    └── amass_adapter.py       # Adapter for external-tools/reconnaissance/amass/
```

## Setup Commands

### 1. Create Directory Structure
```bash
# Navigate to CAI-CERBERUS root
cd CAI-CERBERUS

# Create core directories
mkdir -p agents/{reconnaissance,analysis,execution,validation,custom}
mkdir -p tools/{cli,osint,network,code,custom,external}
mkdir -p patterns/{hierarchy,swarm,chain,auction}
mkdir -p workspaces/{default,temp}
mkdir -p configs/{agents,tools,environments}
mkdir -p memory/{episodic,semantic,session}
mkdir -p audit/{execution,approvals,compliance}
mkdir -p external-tools/{reconnaissance,vulnerability,exploitation,analysis}
```

### 2. Clone Essential Security Tools
```bash
# Navigate to external-tools directory
cd external-tools

# Reconnaissance tools
cd reconnaissance
git clone https://github.com/nmap/nmap.git
git clone https://github.com/robertdavidgraham/masscan.git
git clone https://github.com/projectdiscovery/subfinder.git
git clone https://github.com/OWASP/Amass.git
cd ..

# Vulnerability assessment tools
cd vulnerability
git clone https://github.com/projectdiscovery/nuclei.git
git clone https://github.com/sullo/nikto.git
git clone https://github.com/sqlmapproject/sqlmap.git
cd ..

# Analysis tools
cd analysis
git clone https://github.com/ReFirmLabs/binwalk.git
git clone https://github.com/volatilityfoundation/volatility3.git
cd ..
```

### 3. Set Permissions and Environment
```bash
# Set proper permissions for external tools
find external-tools/ -name "*.py" -exec chmod +x {} \;
find external-tools/ -name "*.sh" -exec chmod +x {} \;

# Create workspace isolation
chmod 755 workspaces/
chmod 700 workspaces/default/
chmod 700 audit/

# Set up environment variables
echo "CERBERUS_EXTERNAL_TOOLS_DIR=$(pwd)/external-tools" >> .env
echo "CERBERUS_WORKSPACE_DIR=$(pwd)/workspaces" >> .env
echo "CERBERUS_AUDIT_DIR=$(pwd)/audit" >> .env
```

## Agent and Tool Discovery

### For LLMs/Agents Operating in CAI-CERBERUS:

1. **Tool Discovery**: Check `external-tools/` for available security tools
2. **Adapter Usage**: Use corresponding adapters in `tools/` directory
3. **Workspace Isolation**: Always operate within designated workspace
4. **Audit Trail**: All actions logged to `audit/` directory

### Tool Registration Pattern

```python
# Example: tools/cli/nmap_adapter.py
from caicerberus.tools import CLITool
import os

class NmapTool(CLITool):
    def __init__(self):
        self.tool_path = os.path.join(
            os.environ.get('CERBERUS_EXTERNAL_TOOLS_DIR'),
            'reconnaissance/nmap/nmap'
        )
        super().__init__(
            name="nmap",
            description="Network discovery and security auditing",
            executable=self.tool_path,
            requires_approval=True,
            sandbox_mode=True
        )
```

## Configuration Files

### Agent Configuration: `configs/agents/reconnaissance.yaml`
```yaml
name: "reconnaissance_agent"
role: "reconnaissance"
tools:
  - "nmap_adapter"
  - "subfinder_adapter"
  - "amass_adapter"
constraints:
  max_iterations: 10
  require_approval: true
  allowed_targets: []
  workspace_isolation: true
```

### Tool Configuration: `configs/tools/nmap.yaml`
```yaml
name: "nmap_adapter"
executable_path: "external-tools/reconnaissance/nmap/nmap"
default_args: ["-sS", "-O", "-A"]
safety_checks:
  - "validate_target_permission"
  - "check_rate_limits"
sandbox: true
approval_required: true
```

This structure ensures:
- **Clear separation** of concerns
- **Easy tool discovery** for agents
- **Proper isolation** and security
- **Audit trail** maintenance
- **Scalable organization** as tools are added