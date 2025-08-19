# CAI-CERBERUS Setup Guide

Quick setup guide for getting CAI-CERBERUS operational with proper tool integration.

## 1. Initial Setup

```bash
# Clone and enter directory
git clone https://github.com/KNIGHTPROJEKS-0/CAI-CERBERUS.git
cd CAI-CERBERUS

# Create virtual environment
python3.12 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install dependencies
pip install -U pip setuptools wheel
pip install -e ".[dev,test]"
```

## 2. Environment Configuration

```bash
# Copy environment template
cp .env.example .env

# Edit .env file with your API keys
# Minimum required:
# OPENAI_API_KEY=sk-your-key-here
# CERBERUS_MODEL=openai/gpt-4o
```

## 3. Install External Security Tools

### Essential Reconnaissance Tools
```bash
cd external-tools/reconnaissance/

# Nmap (network discovery)
git clone https://github.com/nmap/nmap.git
cd nmap && ./configure && make && cd ..

# Subfinder (subdomain enumeration)  
git clone https://github.com/projectdiscovery/subfinder.git

# Amass (attack surface mapping)
git clone https://github.com/OWASP/Amass.git

cd ../..
```

### Essential Vulnerability Tools
```bash
cd external-tools/vulnerability/

# Nuclei (vulnerability scanner)
git clone https://github.com/projectdiscovery/nuclei.git

# Nikto (web server scanner)
git clone https://github.com/sullo/nikto.git

# SQLMap (SQL injection tool)
git clone https://github.com/sqlmapproject/sqlmap.git

cd ../..
```

## 4. Set Permissions and Environment

```bash
# Set executable permissions
find external-tools/ -name "*.py" -exec chmod +x {} \;
find external-tools/ -name "*.sh" -exec chmod +x {} \;

# Create workspace directories with proper permissions
chmod 755 workspaces/
chmod 700 workspaces/default/
chmod 700 audit/

# Update .env with tool paths
echo "CERBERUS_EXTERNAL_TOOLS_DIR=$(pwd)/external-tools" >> .env
echo "CERBERUS_WORKSPACE_DIR=$(pwd)/workspaces" >> .env
echo "CERBERUS_AUDIT_DIR=$(pwd)/audit" >> .env
```

## 5. Verify Installation

```bash
# Check system status
cerberus --version
cerberus config validate

# Test model connectivity
cerberus test models

# Verify tool discovery
cerberus tools list

# Run basic example
cerberus examples run basic-recon
```

## 6. Configure Allowed Targets

**IMPORTANT**: Before using any scanning tools, configure allowed targets:

```bash
# Edit .env file
CERBERUS_ALLOWED_HOSTS=example.com,192.168.1.0/24,your-test-domain.com
```

## 7. First Agent Run

```bash
# Interactive mode with human approval
cerberus interactive --hitl

# Or run specific task
cerberus run --task "Basic reconnaissance of example.com" --target example.com --approve
```

## Directory Structure After Setup

```
CAI-CERBERUS/
├── agents/                    # Agent configurations
├── tools/                     # Tool adapters
├── external-tools/            # Git cloned security tools
│   ├── reconnaissance/
│   │   ├── nmap/
│   │   ├── subfinder/
│   │   └── amass/
│   └── vulnerability/
│       ├── nuclei/
│       ├── nikto/
│       └── sqlmap/
├── workspaces/               # Isolated execution environments
├── configs/                  # Configuration files
├── memory/                   # Memory and state storage
└── audit/                    # Audit logs and traces
```

## Security Notes

- All tools run in sandboxed environments
- Human approval required for sensitive operations  
- Complete audit trail maintained
- Workspace isolation enforced
- Only scan targets you own or have permission to test

## Troubleshooting

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