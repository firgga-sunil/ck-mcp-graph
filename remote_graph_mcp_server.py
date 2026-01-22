#!/usr/bin/env python3
"""
Remote MCP Server for Graph Analysis
Implements MCP protocol over HTTP JSON-RPC for remote access.
"""

import asyncio
import json
import logging
import os
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional

from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn

from mcp.server.models import InitializationOptions
from mcp.server import NotificationOptions, Server
from mcp.types import Tool, TextContent
import mcp.types as types

# Import the graph API client
import graph_api_client

# Configure logging
log_level = os.getenv("LOG_LEVEL", "INFO").upper()
logging.basicConfig(
    level=getattr(logging, log_level, logging.INFO),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("graph-analysis-mcp-server")

# Default Nexus API configuration
DEFAULT_BASE_URL = "http://ck-nexus-app.codekarma:8081"
DEFAULT_TIME_RANGE_MINUTES = 30

# Initialize the MCP server instance (we'll use this for handlers)
mcp_server = Server("graph-analysis")

# Tool implementation functions from the original server
def format_systems_response(systems_data: Dict[str, Any], metrics_data: Optional[Dict[str, Any]] = None) -> str:
    """Format the systems overview response for LLM interface selection with aggregated metrics."""
    
    system_units = systems_data["system_units"]
    interfaces = systems_data["interfaces"]
    version = systems_data["version"]
    timestamp = systems_data["timestamp"]
    
    def format_aggregated_metrics(item_id: str, item_type: str) -> str:
        """Format aggregated metrics for a system unit or interface."""
        if not metrics_data:
            return "No metrics available"
            
        try:
            metrics = graph_api_client.get_metrics_for_item(item_id, metrics_data, version, item_type)
            if not metrics:
                return "No metrics available"
            
            # Format aggregated metrics
            throughput = metrics.get("t", {}).get("qpm", "N/A")
            errors = metrics.get("e", {})
            total_errors, error_4xx, error_5xx = graph_api_client.aggregate_errors(errors)
            latency = metrics.get("l", {})
            p50 = latency.get("0.5", "N/A")
            p99 = latency.get("0.99", "N/A")
            
            return f"QPM: {throughput}, Errors: {total_errors}% (4xx: {error_4xx}%, 5xx: {error_5xx}%), Latency: p50={p50}ms, p99={p99}ms"
        except Exception as e:
            return f"Metrics error: {str(e)}"
    
    response = f"""
# SYSTEM DIRECTORY WITH AGGREGATED METRICS

## CRITICAL: Use Exact Names for Analysis

- **Timestamp**: {timestamp}
- **System Version**: `{version}` (REQUIRED for get_interface_details)
- **Total System Units**: {len(system_units)}
- **Total Interfaces**: {len(interfaces)}
- **Metrics Time Window**: Last {DEFAULT_TIME_RANGE_MINUTES} minutes

## UNDERSTANDING AGGREGATED METRICS

**These are HIGH-LEVEL totals showing the BIG PICTURE:**

- **Throughput (QPM)**: Total requests across ALL connections
- **Latency**: Weighted average response time across ALL calls
- **Errors**: Weighted average error rate across ALL interactions

⚠️ **Important**: When you use get_interface_details, you'll see DIFFERENT numbers because that shows specific relationships only!

## SYSTEM UNITS (Deployed Components)

System units are actual deployed services, databases, and infrastructure. Metrics are aggregated across all interfaces in each system unit.

"""

    for i, unit in enumerate(system_units, 1):
        metrics_str = format_aggregated_metrics(unit, "systemunits")
        response += f"{i:2d}. `{unit}`\n    📊 {metrics_str}\n\n"

    response += f"""
## INTERFACES (APIs & Capabilities)

**IMPORTANT**: Copy the exact interface name from this list for detailed analysis.
Metrics show TOTAL performance across all callers and all calls to each interface.

"""

    for i, interface in enumerate(interfaces, 1):
        metrics_str = format_aggregated_metrics(interface, "interfaces")
        response += f"{i:2d}. `{interface}`\n    📊 {metrics_str}\n\n"

    response += f"""

## NEXT STEP: SELECT AN INTERFACE FOR FOCUSED ANALYSIS

To analyze specific relationships involving any interface:

1. **Choose** any interface name from the list above
2. **Copy** the exact name (case-sensitive)
3. **Use** get_interface_details with:
   - interface_id: `[exact name from list]`
   - version: `{version}`

Example:
```
get_interface_details(
  interface_id="OrderService::POST::/orders",
  version="{version}"
)
```

This will show you the SPECIFIC relationships and how metrics break down by individual connections.
Remember: The numbers in get_interface_details will be DIFFERENT because you're seeing focused data!
    """
    
    return response


def format_interface_details_response(analysis_data: Dict[str, Any], 
                                     include_latency: bool, include_errors: bool) -> str:
    """Format the detailed interface analysis response for LLM understanding."""
    
    interface_id = analysis_data["interface_id"]
    version = analysis_data["version"]
    time_range = analysis_data["time_range"]
    edges = analysis_data["edges"]
    
    def format_edge_metrics(edge: Dict[str, Any]) -> str:
        """Format metrics for an edge."""
        try:
            sync_type = edge["sync_type"]
            metrics = edge.get("metrics")
            
            if not metrics:
                return f"[{sync_type}] No metrics available"
            
            # Format metrics based on what's requested
            parts = [f"[{sync_type}]"]
            
            # Always include throughput
            throughput = metrics.get("t", {}).get("qpm", "N/A")
            parts.append(f"QPM: {throughput}")
            
            if include_errors:
                errors = metrics.get("e", {})
                total_errors, error_4xx, error_5xx = graph_api_client.aggregate_errors(errors)
                parts.append(f"Errors: {total_errors}% (4xx: {error_4xx}%, 5xx: {error_5xx}%)")
            
            if include_latency:
                latency = metrics.get("l", {})
                p50 = latency.get("0.5", "N/A")
                p90 = latency.get("0.9", "N/A")
                p95 = latency.get("0.95", "N/A")
                p99 = latency.get("0.99", "N/A")
                parts.append(f"Latency: p50={p50}ms, p90={p90}ms, p95={p95}ms, p99={p99}ms")
            
            return " | ".join(parts)
            
        except Exception as e:
            return f"[UNKNOWN] Metrics error: {str(e)}"
    
    response = f"""
# FOCUSED INTERFACE ANALYSIS: {interface_id}

⚠️ **CRITICAL UNDERSTANDING - PERSPECTIVE VIEW**:

You are now looking at data FROM {interface_id}'S POINT OF VIEW. 

**Why metrics here are DIFFERENT from get_systems_and_interfaces:**
- **System Overview**: Showed TOTAL metrics across ALL relationships
- **This Analysis**: Shows ONLY metrics for relationships involving {interface_id}

**Example**: If Interface A gets 100 QPM from B and 200 QPM from C:
- System overview showed: Interface A = 300 QPM total  
- When analyzing Interface B: Shows Interface A = 100 QPM (only B→A portion)
- When analyzing Interface C: Shows Interface A = 200 QPM (only C→A portion)

**This is CORRECT and EXPECTED!** You're seeing focused relationship data, not system totals.

## Analysis Parameters
- **Focused Interface**: {interface_id}
- **System Version**: {version}
- **Time Range**: {time_range["start"]} to {time_range["end"]}
- **Duration**: {time_range["duration_minutes"]:.0f} minutes
- **Include Latency**: {include_latency}
- **Include Errors**: {include_errors}

## INTERFACE DEPENDENCIES & DATA FLOW FROM {interface_id}'S PERSPECTIVE

This interface has **{len(edges)} direct relationships**. Each edge shows a specific communication path involving your chosen interface.

### Understanding the Relationship Data:

Each edge shows: `SourceInterface -> TargetInterface`
- **[SYNC/ASYNC]**: Communication pattern for this specific connection
- **Metrics**: Performance data for THIS relationship only (not system totals!)
- **Direction**: Whether this is upstream (calls INTO {interface_id}) or downstream (calls FROM {interface_id})

"""

    if not edges:
        response += """
**No direct interface dependencies found.**

This could mean:
- This interface is a leaf node (doesn't call other interfaces)
- This interface is an entry point (only receives calls)
- The interface might be isolated or not currently active
"""
    else:
        response += "### RELATIONSHIP EDGES WITH FOCUSED METRICS:\n\n"
        
        for i, edge in enumerate(edges, 1):
            edge_display = edge["edge_display"]
            relationship = edge["relationship"]
            edge_metrics = format_edge_metrics(edge)
            
            # Convert relationship to display format
            if relationship == "UPSTREAM":
                relationship_display = "📥 **UPSTREAM** (calls INTO this interface)"
            elif relationship == "DOWNSTREAM":
                relationship_display = "📤 **DOWNSTREAM** (this interface calls OUT)"
            else:
                relationship_display = "🔄 **RELATED** (part of this interface's call chain)"
            
            response += f"""
**{i}. {edge_display}**
   - Direction: {relationship_display}
   - Performance: {edge_metrics}
"""

        response += f"""

### PERFORMANCE ANALYSIS INSIGHTS:

**How to Read These Metrics:**

1. **[SYNC/ASYNC]**: Communication pattern
   - SYNC: Request-response, blocking calls (REST, RPC)
   - ASYNC: Event-driven, non-blocking (message queues, events)

2. **QPM (Queries Per Minute)**: Volume of traffic on this communication path
   - High QPM = Heavy usage, potential bottleneck
   - Low QPM = Light usage or infrequent calls

3. **Errors**: Failure rate for this specific communication
   - 4xx errors: Client-side issues (bad requests, auth failures)
   - 5xx errors: Server-side issues (crashes, timeouts)
   - High errors indicate reliability problems

4. **Latency Percentiles**: Response time distribution
   - p50 (median): Typical response time
   - p90/p95: Most users experience this or better
   - p99: Worst-case performance (tail latency)
   - Large gap between p50 and p99 indicates inconsistent performance

**Debugging Workflow:**
1. **High Latency Edges**: Look for p99 > 1000ms or large p50-p99 gaps
2. **Error-Prone Edges**: Focus on edges with >1% error rates  
3. **High Traffic Edges**: QPM > 1000 may be bottlenecks
4. **Async vs Sync Issues**: ASYNC edges should have lower latency variance

**System Health Indicators:**
- ✅ Good: Low errors (<1%), consistent latency (p99 < 2x p50)
- ⚠️  Warning: Moderate errors (1-5%), high tail latency (p99 > 5x p50)  
- 🚨 Critical: High errors (>5%), extreme latency (p99 > 1000ms)
"""

    response += f"""

## NEXT STEPS FOR DEEPER ANALYSIS

To continue investigating:

1. **Analyze Problematic Edges**: Pick any high-latency or error-prone edge and analyze its source/target interfaces
2. **Historical Comparison**: Run this analysis with different time ranges to see trends
3. **System-Wide Impact**: Check if this interface's issues affect other parts of the system
4. **Root Cause Analysis**: Follow the dependency chain to find the ultimate source of problems

Use `get_interface_details` on any interface mentioned in the edges above to continue your analysis.
    """
    
    return response


async def get_systems_and_interfaces_impl(arguments: dict, base_url: str, domain: Optional[str] = None) -> str:
    """
    Get complete system overview with system units, interfaces, and aggregated metrics.
    
    This provides the foundational view of the distributed system with high-level performance data.
    """
    # Parse timestamp or use current time
    timestamp = arguments.get("timestamp")
    
    # Use graph_api_client to get systems overview and metrics
    # Run sync function in async context
    loop = asyncio.get_event_loop()
    systems_data = await loop.run_in_executor(
        None, 
        graph_api_client.get_systems_overview,
        timestamp,
        base_url,
        domain
    )
    
    # Get metrics for the same time period (last 30 minutes)
    if timestamp:
        end_time = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
    else:
        end_time = datetime.now()
    start_time = end_time - timedelta(minutes=DEFAULT_TIME_RANGE_MINUTES)
    
    start_epoch = int(start_time.timestamp() * 1000)  # Convert to milliseconds
    end_epoch = int(end_time.timestamp() * 1000)  # Convert to milliseconds
    
    metrics_data = await loop.run_in_executor(
        None,
        graph_api_client.fetch_metrics_data,
        systems_data["version"],
        start_epoch,
        end_epoch,
        base_url,
        domain
    )
    
    # Format response for LLM using structured data with metrics
    response_text = format_systems_response(systems_data, metrics_data)
    
    return response_text


async def get_interface_details_impl(arguments: dict, base_url: str, domain: Optional[str] = None) -> str:
    """
    Get detailed analysis of specific interface including edges and dependencies.
    
    This provides deep insights into how a specific interface behaves and connects.
    """
    interface_id = arguments["interface_id"]
    version = arguments["version"]
    start_time_str = arguments.get("start_time")
    end_time_str = arguments.get("end_time")
    include_latency = arguments.get("include_latency", True)
    include_errors = arguments.get("include_errors", True)
    
    # Use graph_api_client to get interface analysis
    # Run sync function in async context
    loop = asyncio.get_event_loop()
    analysis_data = await loop.run_in_executor(
        None,
        graph_api_client.get_interface_analysis,
        interface_id,
        version,
        start_time_str,
        end_time_str,
        base_url,
        domain
    )
    
    # Format detailed response for LLM using structured data
    response_text = format_interface_details_response(
        analysis_data, include_latency, include_errors
    )
    
    return response_text


def format_code_details_response(code_details: List[Dict[str, Any]], service_name: str, 
                                 http_method: str, http_api_signature: str) -> str:
    """Format the code details response for LLM understanding."""
    
    if not code_details:
        return f"""
# CODE DETAILS FOR API

**Service**: {service_name}
**HTTP Method**: {http_method}
**API Signature**: {http_api_signature}

**Result**: No code details found for the specified parameters.

This could mean:
- The API endpoint doesn't exist in the service
- The service name doesn't match
- The HTTP method or API signature doesn't match any registered endpoints
- The service hasn't been instrumented with code details
"""
    
    response = f"""
# CODE DETAILS FOR API

**Service**: {service_name}
**HTTP Method**: {http_method}
**API Signature**: {http_api_signature}

**Found {len(code_details)} code location(s):**

"""
    
    for i, detail in enumerate(code_details, 1):
        class_name = detail.get("className", "Unknown")
        method_name = detail.get("methodName", "Unknown")
        response += f"""
**{i}. {class_name}.{method_name}**
   - Class: `{class_name}`
   - Method: `{method_name}`
"""
    
    response += f"""

## NEXT STEPS

You can use this information to:
- Locate the exact code implementing this API endpoint
- Understand the implementation details
- Debug issues specific to this endpoint
- Trace the code flow from API to implementation

**Note**: If multiple locations are found, the API might be handled by multiple methods or there might be multiple implementations of the same endpoint.
"""
    
    return response


async def get_code_details_for_api_impl(arguments: dict, base_url: str, domain: Optional[str] = None) -> str:
    """
    Get code details (className and methodName) by HTTP method and API signature.
    
    This provides the exact code location for a given API endpoint.
    """
    service_name = arguments["service_name"]
    http_method = arguments["http_method"]
    http_api_signature = arguments["http_api_signature"]
    domain_name = arguments.get("domain_name", domain)
    
    # Use graph_api_client to get code details
    # Run sync function in async context
    loop = asyncio.get_event_loop()
    code_details = await loop.run_in_executor(
        None,
        graph_api_client.fetch_code_details_for_api,
        domain_name,
        service_name,
        http_method,
        http_api_signature,
        base_url,
        None  # headers not needed as domain is passed directly
    )
    
    # Format response for LLM
    response_text = format_code_details_response(
        code_details, service_name, http_method, http_api_signature
    )
    
    return response_text


# MCP server handlers
@mcp_server.list_tools()
async def handle_list_tools() -> List[Tool]:
    """List available tools for graph analysis"""
    return [
        Tool(
            name="get_systems_and_interfaces",
            description="""
Get complete system overview with HIGH-LEVEL AGGREGATED metrics for all components and interfaces.

PURPOSE:
This tool provides a directory of all system components with their TOTAL SYSTEM-WIDE performance.
The primary purpose is to help you SELECT interfaces for detailed analysis and understand overall system health.

CRITICAL IMPORTANCE:
- You MUST use the exact interface name from this list when calling get_interface_details
- You MUST use the returned version ID for consistent analysis
- Interface names are case-sensitive and must match exactly

CONCEPTS:

1. SYSTEM UNITS (Deployments):
   - Actual deployed components: apps, databases, queues
   - Format: "su:ComponentName::Type" (e.g., "su:OrderService::App")
   - Metrics: AGGREGATED across all interfaces in this system unit

2. INTERFACES (APIs/Capabilities):
   - Endpoints, topics, or capabilities that system units expose
   - Format: "SystemUnit::InterfaceType::Name"  
   - Examples: "OrderService::POST::/orders", "PaymentQueue::topic_name"
   - Metrics: AGGREGATED across all callers and all calls to this interface

UNDERSTANDING THE METRICS (AGGREGATED VIEW):

**This is a HIGH-LEVEL system overview showing TOTAL metrics for each component:**

- **Throughput (QPM)**: Total queries/requests per minute across ALL connections
- **Latency**: Weighted average response time across ALL calls  
- **Errors**: Weighted average error rate across ALL interactions

**Example**: If Interface A gets 100 QPM from Interface B and 200 QPM from Interface C:
- In this tool: Interface A shows 300 QPM total
- This gives you the BIG PICTURE of system load and performance

WHAT YOU GET BACK:
- Complete list of system units WITH their aggregated metrics
- Complete list of interfaces WITH their aggregated metrics
- Version ID (required for get_interface_details)
- Timestamp of this system snapshot

NEXT STEP:
Choose any interface name from the list and use it with get_interface_details for FOCUSED analysis.
            """,
            inputSchema={
                "type": "object",
                "properties": {
                    "timestamp": {
                        "type": "string",
                        "description": "ISO 8601 timestamp for system snapshot (default: current time). Use this to analyze system state at specific points in time. Will be converted to epoch milliseconds for the API. Note: API may return empty response if no data exists for the specified time."
                    }
                }
            }
        ),
        
        Tool(
            name="get_interface_details", 
            description="""
Get FOCUSED analysis showing how ONE specific interface interacts with others from ITS PERSPECTIVE.

⚠️ CRITICAL CONCEPT - PERSPECTIVE MATTERS:

This tool shows data FROM THE CHOSEN INTERFACE'S POINT OF VIEW. The metrics you see here will be DIFFERENT from get_systems_and_interfaces because:

**AGGREGATED VIEW (get_systems_and_interfaces)**:
- Interface A total: 300 QPM (from all callers)
- Shows the BIG PICTURE

**FOCUSED VIEW (get_interface_details on Interface B)**:
- Interface A: 100 QPM (only the portion coming from Interface B)  
- Shows SPECIFIC RELATIONSHIPS

**WHY METRICS ARE DIFFERENT:**
Imagine Interface A receives calls from Interface B (100 QPM) and Interface C (200 QPM):

1. **get_systems_and_interfaces**: Shows Interface A = 300 QPM total
2. **get_interface_details(Interface B)**: Shows Interface A = 100 QPM (only B→A traffic)
3. **get_interface_details(Interface C)**: Shows Interface A = 200 QPM (only C→A traffic)

This is CORRECT and EXPECTED! You're seeing different slices of the same data.

PURPOSE & USE CASES:
- Deep-dive analysis of specific interface relationships
- Understanding how YOUR CHOSEN interface impacts or gets impacted by others
- Debugging specific communication paths and bottlenecks
- Tracing request flows from one interface's perspective
- Finding root causes in specific interaction patterns

INTERFACE ANALYSIS CONCEPTS:

1. EDGES (Dependencies & Data Flow FROM CHOSEN INTERFACE'S VIEW):
   - Shows ONLY connections involving your chosen interface
   - Format: "SourceInterface->TargetInterface" 
   - UPSTREAM: Other interfaces calling your chosen interface
   - DOWNSTREAM: Your chosen interface calling other interfaces
   - Each edge shows metrics for THAT SPECIFIC relationship only

2. PERFORMANCE METRICS (RELATIONSHIP-SPECIFIC):
   - QPM: Traffic volume for THIS specific connection only
   - Latency: Response time for THIS relationship only  
   - Errors: Failure rate for THIS specific communication path

UNDERSTANDING THE RESULTS:

When you analyze Interface X, you see:
- WHO calls Interface X (upstream) - WITH metrics for each caller separately
- WHO Interface X calls (downstream) - WITH metrics for each call separately
- Performance for each individual relationship
- Whether each connection is sync or async
- Bottlenecks in specific paths involving Interface X

TIME RANGE ANALYSIS:
- Specify start_time and end_time to analyze historical performance
- Metrics are averaged over the specified time window
- Default: last 30 minutes for current issue analysis
- Use historical analysis to identify when relationship problems started

DEBUGGING WORKFLOW:
1. Find high-latency or error-prone relationships involving your interface
2. Trace specific paths: follow the edges to understand impact chains
3. Compare relationship metrics: identify problematic connections
4. Analyze patterns: understand if issues are in specific relationships or widespread
            """,
            inputSchema={
                "type": "object",
                "properties": {
                    "interface_id": {
                        "type": "string", 
                        "description": "Interface ID from the systems list (e.g., 'OrderService::POST::/orders'). This identifies which interface to analyze in detail."
                    },
                    "version": {
                        "type": "string",
                        "description": "Version ID returned from get_systems_and_interfaces. This ensures consistent analysis of the same system snapshot."
                    },
                    "start_time": {
                        "type": "string",
                        "description": "ISO 8601 start timestamp for metrics analysis (default: 30 minutes ago). Defines the beginning of the time window for performance data."
                    },
                    "end_time": {
                        "type": "string", 
                        "description": "ISO 8601 end timestamp for metrics analysis (default: current time). Defines the end of the time window for performance data."
                    },
                    "include_latency": {
                        "type": "boolean",
                        "description": "Include latency percentiles in response (default: true). Set false to reduce response size if only throughput needed."
                    },
                    "include_errors": {
                        "type": "boolean", 
                        "description": "Include error metrics in response (default: true). Set false to focus only on throughput and latency."
                    }
                },
                "required": ["interface_id", "version"]
            }
        ),
        
        Tool(
            name="get_code_details_for_api",
            description="""
Get code details (className and methodName) for a specific API endpoint by HTTP method and API signature.

PURPOSE:
This tool helps you locate the exact code implementation of an API endpoint by finding the class and method that handle a specific HTTP request.

USE CASES:
- Find the code location for a specific API endpoint
- Understand which class/method implements a given HTTP route
- Debug issues by tracing from API to code implementation
- Discover multiple implementations of the same endpoint (if any)

HOW IT WORKS:
You provide:
- Service name: The name of the service/application (can be extracted from interface names)
- HTTP method: GET, POST, PUT, DELETE, PATCH, etc.
- API signature: The API path/endpoint (e.g., "/orders", "/users/{id}")

The tool returns:
- List of code locations (className and methodName) that handle this API
- Multiple results if the endpoint is handled by multiple methods

INTEGRATION WITH OTHER TOOLS:
This tool works best when used AFTER get_systems_and_interfaces or get_interface_details:

**WORKFLOW - Extracting Parameters from Interface Names:**

Interface names from get_systems_and_interfaces follow these formats:
- Format 1: `{ServiceName}::{ComponentType}::{HTTPMethod}::{Path}`
  - Example: `Tix-Winterfell::App::POST::/review/edit`
  - Extract: service_name="Tix-Winterfell", http_method="POST", http_api_signature="/review/edit"
  
- Format 2: `{ServiceName}::{HTTPMethod}::{Path}`
  - Example: `OrderService::POST::/orders`
  - Extract: service_name="OrderService", http_method="POST", http_api_signature="/orders"

**EXAMPLE WORKFLOW:**
1. Use `get_systems_and_interfaces` to see available interfaces
2. Identify an interface like "OrderService::POST::/orders" or "Tix-Winterfell::App::POST::/review/edit"
3. Extract parameters:
   - service_name: First part before "::" (e.g., "OrderService" or "Tix-Winterfell")
   - http_method: HTTP method part (e.g., "POST", "GET")
   - http_api_signature: The path part (e.g., "/orders", "/review/edit")
4. Call `get_code_details_for_api` with these extracted values to find the implementing code

**IMPORTANT NOTES:**
- Service names are case-sensitive and must match exactly
- The service_name should be the actual service/application name (not the component type like "App")
- For interfaces like "Tix-Winterfell::App::POST::/review/edit", use "Tix-Winterfell" as service_name, not "Tix-Winterfell::App"
- If you're unsure about the service name format, use get_systems_and_interfaces first to see valid interface names
            """,
            inputSchema={
                "type": "object",
                "properties": {
                    "domain_name": {
                        "type": "string",
                        "description": "The domain name for the API path (default: extracted from headers or env var). Used to construct the API URL path."
                    },
                    "service_name": {
                        "type": "string",
                        "description": "The service name (required). This identifies which service/application to query. Can be extracted from interface names returned by get_systems_and_interfaces. For interface 'Tix-Winterfell::App::POST::/review/edit', use 'Tix-Winterfell'. For 'OrderService::POST::/orders', use 'OrderService'. Examples: 'OrderService', 'Tix-Winterfell', 'PaymentService'."
                    },
                    "http_method": {
                        "type": "string",
                        "description": "HTTP method (required). Must be one of: GET, POST, PUT, DELETE, PATCH, HEAD, OPTIONS. Can be extracted from interface names. For interface 'OrderService::POST::/orders', use 'POST'. Example: 'POST'"
                    },
                    "http_api_signature": {
                        "type": "string",
                        "description": "HTTP API signature/path (required). The API endpoint path. Can be extracted from interface names. For interface 'OrderService::POST::/orders', use '/orders'. Examples: '/orders', '/users/{id}', '/api/v1/products', '/review/edit'"
                    }
                },
                "required": ["service_name", "http_method", "http_api_signature"]
            }
        )
    ]


@mcp_server.call_tool()
async def handle_call_tool(name: str, arguments: Dict[str, Any]) -> List[types.TextContent]:
    """Handle tool calls"""
    # Get base_url from environment or use default
    base_url = os.getenv("CK_NEXUS_ENDPOINT", DEFAULT_BASE_URL)
    
    try:
        if name == "get_systems_and_interfaces":
            result_text = await get_systems_and_interfaces_impl(arguments, base_url)
            return [types.TextContent(type="text", text=result_text)]
        
        elif name == "get_interface_details":
            result_text = await get_interface_details_impl(arguments, base_url)
            return [types.TextContent(type="text", text=result_text)]
        
        elif name == "get_code_details_for_api":
            result_text = await get_code_details_for_api_impl(arguments, base_url)
            return [types.TextContent(type="text", text=result_text)]
        
        else:
            raise ValueError(f"Unknown tool: {name}")
            
    except Exception as e:
        logger.error(f"Error handling tool {name}: {str(e)}")
        error_msg = str(e)
        
        # Provide helpful context for common errors
        if "empty response" in error_msg.lower() or "system unit" in error_msg.lower():
            error_msg = f"""
❌ **Error analyzing interface**: {error_msg}

**How to fix this:**
1. Use `get_systems_and_interfaces` first to get the list of interfaces
2. Look in the **INTERFACES** section (not SYSTEM UNITS)
3. Copy an interface name that does NOT start with "su:" (system unit prefix)
4. Use that interface name with `get_interface_details`

**Example of valid interface names:**
- `Tix-Winterfell::App::POST::/review/edit`
- `KAFKA::review_moderation`
- `External::INBOUND::APP_ANDROID_USER`

**Invalid (these are system units):**
- ❌ `su:Tix-Eyrie-V2::App`
- ❌ `su:Tix-Raven::App`

Call `get_systems_and_interfaces` again to see the complete list of valid interfaces.
"""
        
        return [types.TextContent(type="text", text=error_msg)]


# FastAPI app for HTTP transport
app = FastAPI(
    title="Graph Analysis MCP Server",
    description="Remote MCP server for distributed system graph analysis over HTTP",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_base_url_and_domain_from_headers(request: Request) -> tuple[str, Optional[str]]:
    """
    Get graph-api-base-url and ck-domain from request headers
    Returns tuple of (base_url, domain)
    """
    base_url = request.headers.get("graph-api-base-url", DEFAULT_BASE_URL)
    domain = request.headers.get("ck-domain")
    logger.debug(f"Using base URL: {base_url}, domain: {domain}")
    return base_url, domain


class MCPJSONRPCHandler:
    """Handles MCP JSON-RPC requests over HTTP"""
    
    async def handle_request(self, request_data: Dict[str, Any], base_url: str = DEFAULT_BASE_URL, domain: Optional[str] = None) -> Dict[str, Any]:
        """Handle incoming JSON-RPC request"""
        try:
            method = request_data.get("method")
            params = request_data.get("params", {})
            request_id = request_data.get("id")
            
            if method == "initialize":
                result = {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {
                        "tools": {},
                        "resources": {},
                        "prompts": {}
                    },
                    "serverInfo": {
                        "name": "graph-analysis",
                        "version": "1.0.0"
                    }
                }
            
            elif method == "tools/list":
                tools = await handle_list_tools()
                result = {"tools": [
                    {
                        "name": tool.name,
                        "description": tool.description,
                        "inputSchema": tool.inputSchema
                    }
                    for tool in tools
                ]}
            
            elif method == "tools/call":
                tool_result = await self.handle_tool_call(
                    params.get("name"), 
                    params.get("arguments", {}),
                    base_url,
                    domain
                )
                result = {"content": [
                    {
                        "type": content.type,
                        "text": content.text
                    }
                    for content in tool_result
                ]}
            
            elif method == "resources/list":
                # We don't have resources, return empty list
                result = {"resources": []}
            
            elif method == "prompts/list":
                # We don't have prompts, return empty list
                result = {"prompts": []}
            
            else:
                raise ValueError(f"Unknown method: {method}")
            
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": result
            }
            
        except Exception as e:
            logger.error(f"Error handling request: {str(e)}")
            return {
                "jsonrpc": "2.0",
                "id": request_data.get("id"),
                "error": {
                    "code": -1,
                    "message": str(e)
                }
            }
    
    async def handle_tool_call(self, name: str, arguments: Dict[str, Any], base_url: str, domain: Optional[str] = None) -> List[types.TextContent]:
        """Handle tool calls with base_url and domain parameters"""
        try:
            if name == "get_systems_and_interfaces":
                result_text = await get_systems_and_interfaces_impl(arguments, base_url, domain)
                return [types.TextContent(type="text", text=result_text)]
            
            elif name == "get_interface_details":
                result_text = await get_interface_details_impl(arguments, base_url, domain)
                return [types.TextContent(type="text", text=result_text)]
            
            elif name == "get_code_details_for_api":
                result_text = await get_code_details_for_api_impl(arguments, base_url, domain)
                return [types.TextContent(type="text", text=result_text)]
            
            else:
                raise ValueError(f"Unknown tool: {name}")
                
        except Exception as e:
            logger.error(f"Error handling tool {name}: {str(e)}")
            error_msg = str(e)
            
            # Provide helpful context for common errors
            if "empty response" in error_msg.lower() or "system unit" in error_msg.lower():
                error_msg = f"""
❌ **Error analyzing interface**: {error_msg}

**How to fix this:**
1. Use `get_systems_and_interfaces` first to get the list of interfaces
2. Look in the **INTERFACES** section (not SYSTEM UNITS)
3. Copy an interface name that does NOT start with "su:" (system unit prefix)
4. Use that interface name with `get_interface_details`

**Example of valid interface names:**
- `Tix-Winterfell::App::POST::/review/edit`
- `KAFKA::review_moderation`
- `External::INBOUND::APP_ANDROID_USER`

**Invalid (these are system units):**
- ❌ `su:Tix-Eyrie-V2::App`
- ❌ `su:Tix-Raven::App`

Call `get_systems_and_interfaces` again to see the complete list of valid interfaces.
"""
            
            return [types.TextContent(type="text", text=error_msg)]


# Global handler instance
rpc_handler = MCPJSONRPCHandler()


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    # Get base_url from environment or use default
    graph_api_url = os.getenv("CK_NEXUS_ENDPOINT", DEFAULT_BASE_URL)
    
    return {
        "status": "healthy",
        "server": "graph-analysis-mcp-server",
        "version": "1.0.0",
        "protocol": "MCP over HTTP JSON-RPC",
        "graph_api_url": graph_api_url
    }


@app.post("/gmcp")
async def mcp_endpoint(request: Request):
    """Main MCP JSON-RPC endpoint"""
    # Get base_url and domain from headers (nginx upstream or MCP client can add these)
    base_url, domain = get_base_url_and_domain_from_headers(request)
    
    try:
        # Parse JSON-RPC request
        request_data = await request.json()
        logger.info(f"Received MCP request: {request_data.get('method', 'unknown')}")
        
        # Handle the request with base_url and domain
        response = await rpc_handler.handle_request(request_data, base_url, domain)
        
        return JSONResponse(content=response)
        
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON")
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


if __name__ == "__main__":
    port = int(os.getenv("PORT", 8548))
    host = os.getenv("HOST", "0.0.0.0")
    
    logger.info(f"Starting Graph Analysis MCP Server on {host}:{port}")
    logger.info(f"MCP Endpoint: http://{host}:{port}/gmcp")
    logger.info(f"Health Check: http://{host}:{port}/health")
    logger.info(f"Default Graph API Base URL: {DEFAULT_BASE_URL}")
    logger.info(f"Architecture: Can read 'graph-api-base-url' header from nginx (defaults to env or hardcoded)")
    
    uvicorn.run(
        "remote_graph_mcp_server:app",
        host=host,
        port=port,
        log_level="info",
        reload=False
    )
