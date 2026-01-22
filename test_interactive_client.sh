#!/bin/bash

# Test script for interactive graph API client
# Tests the enhanced Python script that handles both APIs

echo "=========================================="
echo "Interactive Graph API Client Test"
echo "=========================================="

# Check if Python script exists
if [ ! -f "interactive_graph_client.py" ]; then
    echo "ERROR: interactive_graph_client.py not found!"
    exit 1
fi

# Make Python script executable
chmod +x interactive_graph_client.py

echo "Testing interactive graph API client..."
echo "API Endpoints:"
echo "  - Primary: http://ac9248ac6be104c95987a0356fbd9ad6-d76d2f43834084df.elb.us-east-2.amazonaws.com:8081/demo/ui/graph-paths/all"
echo "  - Details: http://ac9248ac6be104c95987a0356fbd9ad6-d76d2f43834084df.elb.us-east-2.amazonaws.com:8081/demo/ui/graph-paths/details/pinned"
echo ""

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

echo ""
echo "🚀 Starting Interactive Graph API Client..."
echo "   You can now:"
echo "   1. List system units and interfaces (with metrics)"
echo "   2. Get detailed view of specific interfaces (with metrics)"
echo "   3. View in_in edges as triplets (with throughput, latency, errors)"
echo ""
echo "Press Ctrl+C to exit at any time"
echo ""

# Run the interactive Python script
python3 interactive_graph_client.py

echo ""
echo "=========================================="
echo "Test session completed."
echo "=========================================="
