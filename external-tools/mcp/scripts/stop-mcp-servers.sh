#!/bin/bash

# Stop MCP Servers for CAI-CERBERUS

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MCP_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
LOG_DIR="$MCP_DIR/logs"

echo "🛑 Stopping MCP Servers..."

# Stop all servers
for pid_file in "$LOG_DIR"/*.pid; do
    if [ -f "$pid_file" ]; then
        local pid=$(cat "$pid_file")
        local server_name=$(basename "$pid_file" .pid)
        
        if kill -0 "$pid" 2>/dev/null; then
            echo "🔄 Stopping $server_name (PID: $pid)..."
            kill "$pid"
            
            # Wait for graceful shutdown
            local count=0
            while kill -0 "$pid" 2>/dev/null && [ $count -lt 10 ]; do
                sleep 1
                ((count++))
            done
            
            # Force kill if still running
            if kill -0 "$pid" 2>/dev/null; then
                echo "⚡ Force killing $server_name..."
                kill -9 "$pid"
            fi
            
            echo "✅ Stopped $server_name"
        else
            echo "⚠️  $server_name was not running"
        fi
        
        rm -f "$pid_file"
    fi
done

echo "🎉 All MCP servers stopped"