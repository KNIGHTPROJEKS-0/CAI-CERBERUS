#!/bin/bash

# Start MCP Servers for CAI-CERBERUS
# This script starts all configured MCP servers

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MCP_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
CONFIG_FILE="$MCP_DIR/configs/servers.json"
LOG_DIR="$MCP_DIR/logs"

echo "🚀 Starting MCP Servers for CAI-CERBERUS..."

# Create log directory
mkdir -p "$LOG_DIR"

# Check if configuration exists
if [ ! -f "$CONFIG_FILE" ]; then
    echo "❌ Configuration file not found: $CONFIG_FILE"
    echo "💡 Copy configs/example-servers.json to configs/servers.json and configure"
    exit 1
fi

# Check dependencies
check_dependencies() {
    echo "📋 Checking dependencies..."
    
    if ! command -v node &> /dev/null; then
        echo "❌ Node.js is required but not installed"
        exit 1
    fi
    
    if ! command -v npm &> /dev/null; then
        echo "❌ npm is required but not installed"
        exit 1
    fi
    
    if ! command -v uvx &> /dev/null; then
        echo "⚠️  uvx not found - some servers may not work"
    fi
    
    echo "✅ Dependencies checked"
}

# Install MCP packages
install_mcp_packages() {
    echo "📦 Installing MCP packages..."
    
    # Install core MCP servers
    npm install -g @modelcontextprotocol/server-filesystem
    npm install -g @modelcontextprotocol/server-brave-search
    
    # Install Python MCP servers via uvx
    if command -v uvx &> /dev/null; then
        uvx --install mcp-server-git
        uvx --install mcp-server-sqlite
    fi
    
    echo "✅ MCP packages installed"
}

# Start individual MCP server
start_server() {
    local server_name="$1"
    local server_config="$2"
    
    echo "🔧 Starting $server_name server..."
    
    # Extract configuration
    local command=$(echo "$server_config" | jq -r '.command')
    local args=$(echo "$server_config" | jq -r '.args | join(" ")')
    local enabled=$(echo "$server_config" | jq -r '.enabled // true')
    
    if [ "$enabled" != "true" ]; then
        echo "⏭️  Skipping disabled server: $server_name"
        return
    fi
    
    # Start server in background
    local log_file="$LOG_DIR/mcp-$server_name.log"
    echo "📝 Logging to: $log_file"
    
    # Create startup script for server
    cat > "$LOG_DIR/start-$server_name.sh" << EOF
#!/bin/bash
cd "$MCP_DIR"
exec $command $args >> "$log_file" 2>&1
EOF
    
    chmod +x "$LOG_DIR/start-$server_name.sh"
    
    # Start server
    nohup "$LOG_DIR/start-$server_name.sh" &
    local pid=$!
    
    echo "$pid" > "$LOG_DIR/$server_name.pid"
    echo "✅ Started $server_name (PID: $pid)"
}

# Parse configuration and start servers
start_all_servers() {
    echo "🔍 Reading configuration from $CONFIG_FILE"
    
    # Get list of servers
    local servers=$(jq -r '.mcpServers | keys[]' "$CONFIG_FILE")
    
    for server in $servers; do
        local server_config=$(jq ".mcpServers.$server" "$CONFIG_FILE")
        start_server "$server" "$server_config"
        sleep 2  # Brief delay between starts
    done
}

# Health check
health_check() {
    echo "🏥 Performing health check..."
    
    local healthy=0
    local total=0
    
    for pid_file in "$LOG_DIR"/*.pid; do
        if [ -f "$pid_file" ]; then
            local pid=$(cat "$pid_file")
            local server_name=$(basename "$pid_file" .pid)
            
            if kill -0 "$pid" 2>/dev/null; then
                echo "✅ $server_name is running (PID: $pid)"
                ((healthy++))
            else
                echo "❌ $server_name is not running"
            fi
            ((total++))
        fi
    done
    
    echo "📊 Health check: $healthy/$total servers running"
    
    if [ $healthy -eq $total ] && [ $total -gt 0 ]; then
        echo "🎉 All MCP servers are running successfully!"
        return 0
    else
        echo "⚠️  Some servers are not running properly"
        return 1
    fi
}

# Main execution
main() {
    check_dependencies
    install_mcp_packages
    start_all_servers
    
    echo "⏳ Waiting for servers to initialize..."
    sleep 5
    
    health_check
    
    echo ""
    echo "📋 MCP Server Management:"
    echo "  - View logs: tail -f $LOG_DIR/mcp-*.log"
    echo "  - Stop servers: $SCRIPT_DIR/stop-mcp-servers.sh"
    echo "  - Check status: $SCRIPT_DIR/check-mcp-servers.sh"
}

# Run main function
main "$@"