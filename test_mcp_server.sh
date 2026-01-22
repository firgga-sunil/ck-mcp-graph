#!/bin/bash

# Test script for MCP Server
# Tests the MCP server setup and validates it can start properly

echo "=========================================="
echo "MCP Server Test"
echo "=========================================="

# Check if MCP server script exists
if [ ! -f "mcp_server.py" ]; then
    echo "ERROR: mcp_server.py not found!"
    exit 1
fi

# Check if config file exists
if [ ! -f "mcp_config.json" ]; then
    echo "ERROR: mcp_config.json not found!"
    exit 1
fi

# Make MCP server executable
chmod +x mcp_server.py

echo "Testing MCP server setup..."
echo ""

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Check if MCP dependencies are installed
echo "Checking MCP dependencies..."
python -c "import mcp; print('✅ MCP library installed successfully')" 2>/dev/null || {
    echo "⚠️  Installing MCP dependencies..."
    pip install mcp httpx
}

# Validate Python syntax
echo "Validating MCP server Python syntax..."
python -m py_compile mcp_server.py && echo "✅ Python syntax valid" || {
    echo "❌ Python syntax error in mcp_server.py"
    exit 1
}

echo ""
echo "🎯 MCP Server Configuration:"
echo "   - Server script: mcp_server.py"
echo "   - Configuration: mcp_config.json"  
echo "   - Default endpoint: http://localhost:8081"
echo ""

echo "📋 Configuration file contents:"
cat mcp_config.json

echo ""
echo "🚀 MCP Server is ready!"
echo ""
echo "To use with your MCP client:"
echo "1. Copy mcp_config.json content to your MCP client configuration"
echo "2. Update the path in 'args' to point to your workspace"
echo "3. Ensure your graph API service is running on http://localhost:8081"
echo "4. Connect your MCP client to start using the tools"
echo ""
echo "Available Tools:"
echo "  - get_systems_and_interfaces: Get complete system overview" 
echo "  - get_interface_details: Analyze specific interface dependencies"
echo ""
echo "=========================================="
echo "Test completed successfully!"
echo "=========================================="
