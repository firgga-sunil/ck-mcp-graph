#!/bin/bash
# Generate MCP client configuration for Cursor

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}Graph Analysis MCP Server - Remote Configuration Generator${NC}"
echo ""

# Get server URL from user or use default
read -p "Enter remote server URL (default: http://localhost:8548): " SERVER_URL
SERVER_URL=${SERVER_URL:-http://localhost:8548}

# Ensure URL ends with /mcp
if [[ ! "$SERVER_URL" =~ /mcp$ ]]; then
    if [[ "$SERVER_URL" =~ /$ ]]; then
        SERVER_URL="${SERVER_URL}mcp"
    else
        SERVER_URL="${SERVER_URL}/mcp"
    fi
fi

echo -e "${BLUE}Using server URL: ${GREEN}${SERVER_URL}${NC}"
echo ""

# Optional: Ask for authentication token
read -p "Do you need to add authentication? (y/n, default: n): " ADD_AUTH
ADD_AUTH=${ADD_AUTH:-n}

AUTH_HEADER=""
if [[ "$ADD_AUTH" == "y" || "$ADD_AUTH" == "Y" ]]; then
    read -p "Enter authorization token: " AUTH_TOKEN
    AUTH_HEADER=",\n      \"headers\": {\n        \"Authorization\": \"Bearer ${AUTH_TOKEN}\"\n      }"
fi

# Generate configuration
CONFIG_FILE="mcp_client_config.json"

cat > "$CONFIG_FILE" << EOF
{
  "mcpServers": {
    "graph-analysis-remote": {
      "url": "${SERVER_URL}"${AUTH_HEADER},
      "description": "Remote Graph Analysis MCP Server for distributed system insights"
    }
  }
}
EOF

echo -e "${GREEN}✅ Configuration file generated: ${CONFIG_FILE}${NC}"
echo ""
echo -e "${YELLOW}To use with Cursor:${NC}"
echo "1. Copy the configuration to your Cursor MCP config:"
echo "   cp ${CONFIG_FILE} ~/.cursor/mcp.json"
echo ""
echo "   OR merge with existing config:"
echo "   cat ${CONFIG_FILE}"
echo ""
echo "2. Restart Cursor or reload the MCP configuration"
echo ""
echo -e "${YELLOW}To test the connection:${NC}"
echo "   curl ${SERVER_URL%/mcp}/health"
echo ""
echo -e "${BLUE}Generated configuration:${NC}"
cat "$CONFIG_FILE"
echo ""
echo -e "${GREEN}Done!${NC}"

