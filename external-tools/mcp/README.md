# MCP Servers for CAI-CERBERUS

This directory contains Model Context Protocol (MCP) servers for CAI-CERBERUS integration.

## Directory Structure

- `stdio/` - Standard I/O based MCP servers
- `sse/` - Server-Sent Events based MCP servers
- `configs/` - Configuration files for MCP servers
- `examples/` - Example MCP server implementations

## Available MCP Servers

### Core Servers
- **Filesystem Server** - File operations and management
- **Git Server** - Git repository operations
- **Database Server** - Database query and management
- **Web Search Server** - Web search capabilities

### Security Servers
- **Vulnerability Scanner** - Security vulnerability detection
- **Network Scanner** - Network reconnaissance
- **OSINT Server** - Open source intelligence gathering

## Setup and Configuration

### 1. Install Dependencies
```bash
# Install MCP CLI tools
npm install -g @modelcontextprotocol/cli

# Install Python MCP SDK
pip install mcp
```

### 2. Configure Servers
```bash
# Copy example configurations
cp configs/example-servers.json configs/servers.json

# Edit configuration
nano configs/servers.json
```

### 3. Start MCP Servers
```bash
# Start all configured servers
./scripts/start-mcp-servers.sh

# Start specific server
mcp-server filesystem --config configs/filesystem.json
```

## Integration with CAI-CERBERUS

MCP servers are automatically discovered and loaded by CAI-CERBERUS when:

1. Servers are configured in `configs/servers.json`
2. Environment variable `CERBERUS_MCP_ENABLED=true` is set
3. Servers are running and accessible

### Example Configuration

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["@modelcontextprotocol/server-filesystem", "/path/to/allowed/directory"],
      "transport": "stdio"
    },
    "git": {
      "command": "uvx",
      "args": ["mcp-server-git", "--repository", "/path/to/repo"],
      "transport": "stdio"
    }
  }
}
```

## Security Considerations

- MCP servers run with limited permissions
- File access is restricted to configured directories
- Network access is controlled via firewall rules
- All operations are logged for audit purposes

## Development

### Creating Custom MCP Servers

1. Use the MCP SDK for your preferred language
2. Implement required MCP protocol methods
3. Add configuration to `configs/servers.json`
4. Test with CAI-CERBERUS integration

### Testing

```bash
# Test MCP server connectivity
mcp-test --server filesystem --config configs/filesystem.json

# Test CAI-CERBERUS integration
python -m cai.cli --mcp-test
```

## Troubleshooting

### Common Issues

1. **Server not starting**: Check configuration and dependencies
2. **Permission denied**: Verify file/directory permissions
3. **Connection timeout**: Check network connectivity and firewall
4. **Protocol errors**: Ensure MCP version compatibility

### Logs

MCP server logs are available in:
- `logs/mcp-servers.log` - Combined server logs
- `logs/mcp-{server-name}.log` - Individual server logs

## References

- [MCP Specification](https://spec.modelcontextprotocol.io/)
- [MCP SDK Documentation](https://github.com/modelcontextprotocol/python-sdk)
- [CAI-CERBERUS MCP Integration](../../docs/mcp.md)