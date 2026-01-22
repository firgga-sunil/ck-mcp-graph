# Graph API Client

This project contains Python clients to fetch graph data from the backend service and extract information from the graph APIs.

## Project Architecture

### Architecture Overview

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   MCP Server    │    │  CLI Clients     │    │  Graph APIs     │
│  (LLM Layer)    │    │ (Human Layer)    │    │ (Data Source)   │
│                 │    │                  │    │                 │
│  - Tool Schemas │    │ - Interactive UI │    │ - API 1: All    │
│  - LLM Docs     │───▶│ - Direct Usage   │───▶│ - API 2: Pinned │
│  - Formatting   │    │ - Testing        │    │ - API 3: Metrics│
└─────────────────┘    └──────────────────┘    └─────────────────┘
         │                        │
         └────────────────────────▼
                ┌─────────────────────┐
                │  graph_api_client   │
                │  (Core Data Layer)  │
                │                     │
                │  - API Integration  │
                │  - Data Processing  │
                │  - Structured Data  │
                │  - Business Logic   │
                └─────────────────────┘
```

**Key Design Principles:**
- **Single Source of Truth**: `graph_api_client.py` handles ALL API interactions
- **Separation of Concerns**: MCP server focuses on LLM integration, CLI clients focus on human interaction
- **Shared Core**: Both layers use the same data processing logic
- **DRY Principle**: API changes automatically benefit both CLI and MCP layers

## Project Structure

### Core Components
- **`graph_api_client.py`** - Core data layer that handles ALL Nexus API interactions and data processing. Provides structured data functions for programmatic use and CLI functionality for human interaction.
- **`mcp_server.py`** - MCP server that exposes intelligent graph analysis tools for LLM integration. Uses `graph_api_client.py` internally for all data operations.
- **`interactive_graph_client.py`** - Interactive CLI script for manual system exploration with menu-driven interface.

### Configuration & Dependencies
- **`requirements.txt`** - Python dependencies (requests, mcp, httpx)
- **`mcp_config.json`** - MCP server configuration for LLM clients (ready to use)

### Testing & Validation  
- **`test_interactive_client.sh`** - Test script for interactive client exploration
- All components include comprehensive error handling and validation

## Setup

1. Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Make sure the backend service is running on `http://localhost:8081`

## Usage

### Direct CLI Mode (Automated Analysis)
Shows all system units, interfaces, and in_in edges with metrics from all APIs:

```bash
# Activate virtual environment and run
source venv/bin/activate
python3 graph_api_client.py
```

This mode automatically:
- Fetches complete system overview from API 1
- Retrieves metrics from API 3 for the last 30 minutes
- Displays system units, interfaces, and edges with performance data
- Perfect for automated analysis and monitoring scripts

### Interactive Mode (Manual Exploration)
Provides an interactive menu-driven interface to explore the system:

```bash
# Run directly (with virtual environment activated)
source venv/bin/activate
python3 interactive_graph_client.py

# Or use the test script
./test_interactive_client.sh
```

#### Interactive Mode Features:

**Main Menu Options:**
1. **List System Units and Interfaces** - Overview of all components with real-time metrics
2. **Get Interface Details** - Deep-dive analysis of specific interface dependencies
3. **Exit** - Clean exit from the application

**System Overview Mode:**
- Lists all deployed system units (apps, databases, queues)
- Shows all available interfaces (APIs, endpoints, topics)
- Displays real-time performance metrics for each component
- Provides interface selection for detailed analysis

**Interface Details Mode:**
- Select any interface from the system overview
- View all incoming/outgoing dependencies (in_in edges)
- See detailed performance metrics for each dependency
- Understand data flow and communication patterns
- Identify performance bottlenecks and errors

**Interactive Flow:**
1. Start → See system overview with metrics
2. Choose interface → View detailed dependency analysis
3. Analyze performance → Identify issues or patterns
4. Return to menu → Explore other interfaces

## Nexus API Integration

This project integrates with three Nexus Graph APIs to provide comprehensive distributed system analysis. Each API serves a specific purpose in building a complete picture of system architecture and performance.

### API 1: Graph Paths All - System Discovery

- **URL**: `http://localhost:8081/demo/ui/graph-paths/all` 
- **Method**: GET
- **Optional Parameters**: `time` (epoch seconds for historical data)
- **Purpose**: Discover complete system architecture and get system snapshot

**How We Use It:**
```bash
# Current system state
GET /demo/ui/graph-paths/all

# Historical system state
GET /demo/ui/graph-paths/all?time=1758287492
```

**Data Extraction:**
- **System Units**: From `baseTimelineGraph.systemunits[]` - all deployed components
- **Interfaces**: From `baseTimelineGraph.interfaces[]` - all APIs, endpoints, topics
- **Edges**: From `baseTimelineGraph.edges[]` - communication paths (we focus on `in_in:` prefixed edges)
- **Version**: From `version` field - required for subsequent API calls
- **Lookup Data**: From `lookupData.edges` - edge metadata including SYNC/ASYNC classification

**Usage Patterns:**
- **MCP Server**: Called by `get_systems_and_interfaces` tool for LLM system discovery
- **CLI Mode**: Called at startup to display complete system overview
- **Interactive Mode**: Called for system list and interface selection
- **Historical Analysis**: Time parameter enables point-in-time system analysis

### API 2: Interface Details (Pinned) - Focused Analysis

- **URL**: `http://localhost:8081/demo/ui/graph-paths/details/pinned`
- **Method**: POST  
- **Parameters**: `version` (from API 1) and `nodeId` (URL-encoded interface ID)
- **Content-Type**: `application/x-www-form-urlencoded` (empty body)
- **Purpose**: Get detailed dependency view of specific interface

**How We Use It:**
```bash
# Detailed interface analysis
POST /demo/ui/graph-paths/details/pinned?version=demo--595&nodeId=Tix-Winterfell%3A%3AApp%3A%3APOST%3A%3A%2Freview%2Fedit
Content-Type: application/x-www-form-urlencoded
(empty body)
```

**Data Extraction:**
- **Interface Edges**: Focus on `in_in:` edges showing interface-to-interface communication
- **Edge Classification**: Extract SYNC/ASYNC types from `lookupData.edges[].kind`
- **Dependency Mapping**: Understand upstream (calls into) vs downstream (calls out) relationships
- **Same Structure**: Returns same format as API 1 but filtered to specific interface context

**Usage Patterns:**
- **MCP Server**: Called by `get_interface_details` tool for deep-dive LLM analysis
- **Interactive Mode**: Called when user selects specific interface for detailed view
- **Dependency Tracing**: Used to understand how specific interfaces connect to the system

### API 3: Metrics Overlays - Performance Analysis

- **URL**: `http://localhost:8081/demo/ui/graph-paths/overlays/v2`
- **Method**: GET
- **Parameters**: `version`, `epochStartTime`, `epochEndTime`, `uom=qpm`
- **Purpose**: Get real-time and historical performance metrics for any system component

**How We Use It:**
```bash
# Performance metrics for time range
GET /demo/ui/graph-paths/overlays/v2?version=demo--595&epochStartTime=1758371290&epochEndTime=1758371350&uom=qpm
```

**Data Extraction:**
From `tickResponse[version]` we extract metrics for:
- **System Units**: `systemunits[unit_name].server_metrics`
- **Interfaces**: `interfaces[interface_name].server_metrics`  
- **Edges**: `edges[edge_name].server_metrics` or `edges["in_in:edge_name"].server_metrics`

**Metrics Structure:**
```json
{
  "server_metrics": {
    "t": {"qpm": 1500.0},                    // Throughput
    "e": {"total": 0.0, "4xx": 0.0, "5xx": 0.0}, // Errors
    "l": {"0.5": 69.3, "0.9": 124.7, "0.95": 152.4, "0.99": 194.0} // Latency percentiles
  }
}
```

**Usage Patterns:**
- **Real-time Analysis**: Default 30-minute window for current performance
- **Historical Analysis**: Custom time ranges for trend analysis and comparisons
- **Comprehensive Coverage**: Metrics for system units, interfaces, and individual communication paths
- **Performance Annotation**: Every system component gets performance context

### API Integration Flow

**Complete Analysis Workflow:**
1. **Discovery**: API 1 → Get system architecture and version
2. **Focus**: API 2 → Analyze specific interface dependencies (optional)
3. **Performance**: API 3 → Overlay metrics on all components
4. **Synthesis**: Combine architectural + performance data for comprehensive insights

**Error Handling:**
- **Empty Responses**: API 1 with time parameter may return empty if no historical data
- **Missing Metrics**: API 3 may not have metrics for all components
- **URL Encoding**: Interface IDs require proper URL encoding for API 2
- **Version Consistency**: Same version must be used across API 2 and API 3 calls

**Performance Optimization:**
- **Batch Processing**: Single API 3 call gets metrics for all components
- **Shared Data**: Version from API 1 enables consistent API 2/3 calls
- **Caching Potential**: Results can be cached based on version + time range

## Output Format

The scripts extract and display:

### System Units (with metrics):
```
su:Tix-Eyrie-V2::App | QPM: 1500.0, Errors: 0.0 (4xx: 0.0, 5xx: 0.0), Latency: p50=69.3ms p90=124.7ms p95=152.4ms p99=194.0ms
su:Tix-Raven::App | QPM: 1950.0, Errors: 0.0 (4xx: 0.0, 5xx: 0.0), Latency: p50=58.5ms p90=105.4ms p95=128.8ms p99=163.9ms
su:KAFKA::review_moderation | QPM: 1950.0, Errors: 0.0 (4xx: 0.0, 5xx: 0.0), Latency: p50=5.3ms p90=9.7ms p95=11.8ms p99=15.0ms
...
```

### Interfaces (with metrics):
```
External::INBOUND::APP_ANDROID_USER | No metrics
Tix-Winterfell::App::GET::/search/movies | QPM: 367.4, Errors: 0.0 (4xx: 0.0, 5xx: 0.0), Latency: p50=67.3ms p90=121.2ms p95=148.1ms p99=188.5ms
KAFKA::review_moderation | QPM: 1950.0, Errors: 0.0 (4xx: 0.0, 5xx: 0.0), Latency: p50=5.3ms p90=9.7ms p95=11.8ms p99=15.0ms
...
```

### in_in Edges (formatted as triplets with metrics):
Edges that start with `in_in:` from `baseTimelineGraph.edges` are formatted as:

```
EDGE source->target | QPM: [throughput], Errors: [total] (4xx: [4xx_count], 5xx: [5xx_count]), Latency: p50=[p50]ms p90=[p90]ms p95=[p95]ms p99=[p99]ms
```

For example:
```
EDGE Tix-Winterfell::App::POST::/review/edit->KAFKA::review_moderation | QPM: 450.0, Errors: 0.0 (4xx: 0.0, 5xx: 0.0), Latency: p50=5.4ms p90=9.8ms p95=12.0ms p99=15.2ms
EDGE Tix-Winterfell::App::POST::/review/submit->KAFKA::review_moderation | QPM: 1500.0, Errors: 0.0 (4xx: 0.0, 5xx: 0.0), Latency: p50=5.3ms p90=9.6ms p95=11.7ms p99=14.9ms
EDGE KAFKA::review_moderation->Tix-Tyrion::App::review_moderation-CG_INGEST | QPM: 1950.0, Errors: 0.0 (4xx: 0.0, 5xx: 0.0), Latency: p50=85.7ms p90=154.2ms p95=188.5ms p99=239.9ms
...
```

## Metrics Information

- **QPM**: Queries/requests Per Minute (throughput) [[memory:6332078]]
- **Errors**: Total error percentage with breakdown by HTTP status codes
- **Latency**: Response time percentiles in milliseconds:
  - **p50**: 50th percentile (median)
  - **p90**: 90th percentile  
  - **p95**: 95th percentile
  - **p99**: 99th percentile
- **"No metrics"**: Displayed when metrics data is unavailable for that item

## Configuration

The latency percentiles displayed can be configured by modifying the `latency_percentiles` parameter in the `format_metrics()` function (default: `["0.5", "0.9", "0.95", "0.99"]`).

## MCP Server Integration

This project includes a **Model Context Protocol (MCP) server** that provides intelligent graph analysis tools for LLMs. The MCP server abstracts away complex Nexus API interactions and provides comprehensive distributed system insights for automated SRE analysis, performance debugging, and dependency understanding.

### MCP Server Architecture

The MCP server (`mcp_server.py`) acts as a sophisticated middleware layer:

```
LLM Client ←→ MCP Server ←→ graph_api_client.py ←→ Nexus APIs
```

**Benefits:**
- **Abstraction**: Hides complex API orchestration from LLMs
- **Intelligence**: Provides context-aware explanations and guidance
- **Efficiency**: Single tool calls retrieve comprehensive analysis
- **Flexibility**: Supports both real-time and historical analysis

### MCP Tools

#### 1. `get_systems_and_interfaces` - System Discovery Tool

**Purpose**: Provide complete system overview for interface selection and architecture understanding.

**Input Parameters:**
```json
{
  "timestamp": "2025-09-20T15:30:00"  // Optional: ISO 8601 for historical analysis
}
```

**What It Does:**
1. Calls Nexus API 1 (with optional time parameter)
2. Extracts all system units and interfaces  
3. Returns clean interface directory with version ID
4. **Does NOT** include metrics (keeps focus on selection)

**LLM-Facing Response:**
```markdown
# SYSTEM DIRECTORY - INTERFACE SELECTION

## CRITICAL: Use Exact Names for Analysis
- **System Version**: `demo--595` (REQUIRED for get_interface_details)
- **Total System Units**: 9
- **Total Interfaces**: 16

## SYSTEM UNITS (Deployed Components)
1. `su:Tix-Eyrie-V2::App`
2. `su:Tix-Raven::App`
3. `su:KAFKA::review_moderation`
...

## INTERFACES (APIs & Capabilities)
**IMPORTANT**: Copy exact interface name for detailed analysis.
1. `External::INBOUND::APP_ANDROID_USER`
2. `Tix-Winterfell::App::POST::/review/edit`
3. `KAFKA::review_moderation`
...

## NEXT STEP: SELECT AN INTERFACE
Choose any interface and use get_interface_details with exact name and version.
```

**Use Cases:**
- System architecture discovery
- Interface catalog browsing  
- Historical system snapshots
- Pre-analysis interface selection

#### 2. `get_interface_details` - Deep Analysis Tool

**Purpose**: Comprehensive analysis of specific interface with dependencies, performance, and troubleshooting insights.

**Input Parameters:**
```json
{
  "interface_id": "Tix-Winterfell::App::POST::/review/edit",
  "version": "demo--595",
  "start_time": "2025-09-20T14:00:00",  // Optional: defaults to 30 min ago
  "end_time": "2025-09-20T14:30:00",    // Optional: defaults to now
  "include_latency": true,              // Optional: default true
  "include_errors": true                // Optional: default true
}
```

**What It Does:**
1. Calls Nexus API 2 (pinned details) for interface dependencies
2. Calls Nexus API 3 (metrics) for performance data in time range
3. Processes only `in_in:` edges (interface-to-interface communication)
4. Extracts SYNC/ASYNC classification from edge metadata
5. Determines upstream/downstream relationships
6. Formats comprehensive analysis with troubleshooting guidance

**LLM-Facing Response:**
```markdown
# DETAILED INTERFACE ANALYSIS: Tix-Winterfell::App::POST::/review/edit

## Analysis Parameters
- **Time Range**: 2025-09-20T14:00:00 to 2025-09-20T14:30:00 (30 minutes)
- **Include Latency**: true
- **Include Errors**: true

## INTERFACE DEPENDENCIES & DATA FLOW
This interface has **3 direct dependencies**. Each edge represents communication between interfaces.

### DEPENDENCY EDGES WITH PERFORMANCE METRICS:

**1. Tix-Winterfell::App::POST::/review/edit->KAFKA::review_moderation**
   - Direction: 📤 **DOWNSTREAM** (this interface calls OUT)
   - Performance: [ASYNC] | QPM: 450.0 | Errors: 0.0% (4xx: 0.0%, 5xx: 0.0%) | Latency: p50=5.4ms, p90=9.8ms, p95=12.0ms, p99=15.2ms

**2. External::INBOUND::APP_ANDROID_USER->Tix-Winterfell::App::POST::/review/edit**
   - Direction: 📥 **UPSTREAM** (calls INTO this interface)
   - Performance: [SYNC] | QPM: 450.0 | No latency data

### PERFORMANCE ANALYSIS INSIGHTS:

**How to Read These Metrics:**
1. **[SYNC/ASYNC]**: Communication pattern
   - SYNC: Request-response, blocking calls (REST, RPC)
   - ASYNC: Event-driven, non-blocking (message queues, events)

2. **QPM (Queries Per Minute)**: Volume of traffic
3. **Errors**: Failure rates with HTTP status breakdown
4. **Latency Percentiles**: Response time distribution

**System Health Indicators:**
- ✅ Good: Low errors (<1%), consistent latency
- ⚠️ Warning: Moderate errors (1-5%), high tail latency
- 🚨 Critical: High errors (>5%), extreme latency

## NEXT STEPS FOR DEEPER ANALYSIS
1. **Analyze Problematic Edges**: Focus on high-latency or error-prone connections
2. **Historical Comparison**: Compare with different time ranges
3. **Root Cause Analysis**: Follow dependency chain to find ultimate sources
```

**Use Cases:**
- Performance debugging and bottleneck identification
- Dependency mapping and impact analysis
- Error rate analysis and troubleshooting
- Historical performance comparisons
- Capacity planning and scaling decisions

### Key Concepts for LLMs

The MCP server provides comprehensive context about distributed systems:

#### **System Components**
- **System Units**: Deployed components like apps, databases, message queues
- **Interfaces**: APIs, endpoints, topics, or capabilities that components expose
- **Edges**: Communication paths showing how interfaces connect and exchange data

#### **Performance Metrics**
- **QPM (Queries Per Minute)**: Traffic volume [[memory:6332078]]
- **Error Rates**: Failure percentages with 4xx/5xx breakdown
- **Latency Percentiles**: Response time distribution (p50, p90, p95, p99)
- **SYNC vs ASYNC**: Communication patterns affecting performance characteristics

#### **Analysis Patterns**
- **Upstream Dependencies**: Services that call into the analyzed interface
- **Downstream Dependencies**: Services that the analyzed interface calls out to
- **Performance Bottlenecks**: High latency, error-prone, or high-volume edges
- **Historical Trends**: Performance changes over time for capacity planning

#### **Troubleshooting Workflows**
1. **System Discovery** → Use `get_systems_and_interfaces` for architecture overview
2. **Problem Identification** → Use `get_interface_details` on suspected problematic interfaces  
3. **Root Cause Analysis** → Follow dependency chains through multiple interface analyses
4. **Impact Assessment** → Analyze upstream/downstream effects of performance issues
5. **Historical Analysis** → Compare current vs historical performance for trend identification

### LLM Integration Benefits

- **Autonomous SRE**: LLMs can independently discover, analyze, and diagnose system issues
- **Contextual Analysis**: Rich explanations help LLMs understand complex distributed systems
- **Guided Debugging**: Step-by-step workflows for systematic problem resolution
- **Performance Intelligence**: Automated identification of bottlenecks and anomalies
- **Dependency Understanding**: Clear mapping of service interactions and data flow

### Setup and Configuration

1. **Install MCP Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure Your MCP Client**:
   Use the provided `mcp_config.json` or add this to your MCP client configuration:
   ```json
   {
     "mcpServers": {
       "graph-analysis": {
         "command": "/path/to/your/workspace/ck-graph-mcp/venv/bin/python",
         "args": ["/path/to/your/workspace/ck-graph-mcp/mcp_server.py"]
       }
     }
   }
   ```

   **Important**: Use the full path to the virtual environment's Python interpreter to ensure all dependencies are available.

3. **Configuration**:
   - The server connects to Nexus at `http://localhost:8081` by default
   - URL can be modified in `mcp_server.py` (DEFAULT_BASE_URL) if needed

### Usage Examples

Once connected to the MCP server, LLMs can perform sophisticated analysis:

**System Architecture Discovery**:
```
Use get_systems_and_interfaces to show me all the systems in our architecture
```

**Performance Debugging**:
```  
Get details for the Tix-Winterfell::App::POST::/review/edit interface to debug latency issues
```

**Dependency Analysis**:
```
Show me all the dependencies for the KAFKA::review_moderation interface
```

**Historical Performance Comparison**:
```
Compare the performance of the UserService API between yesterday and today using different timestamps
```

**Root Cause Investigation**:
```
Analyze the complete call chain for the payment processing workflow starting from the payment interface
```

### Testing and Validation

**Quick Test Commands:**

1. **Test Core Functionality**:
   ```bash
   # Test direct CLI mode
   source venv/bin/activate
   python3 graph_api_client.py

   # Test interactive mode
   ./test_interactive_client.sh
   ```

2. **Test MCP Server**:
   ```bash
   # Validate MCP server syntax
   source venv/bin/activate
   python -m py_compile mcp_server.py

   # Test import capabilities
   python -c "import mcp_server; print('✅ MCP server ready')"
   ```

3. **Validate Configuration**:
   ```bash
   # Verify MCP config JSON
   python -c "import json; print('✅ Valid MCP config:', json.load(open('mcp_config.json')))"
   ```

**Expected Behavior:**
- CLI mode shows system units, interfaces, and edges with metrics
- Interactive mode provides menu-driven exploration
- MCP server imports successfully and validates syntax
- All components handle API errors gracefully (empty responses, missing metrics)

### Integration Benefits

- **Autonomous SRE**: LLMs can independently discover, analyze, and diagnose system issues without human guidance
- **Performance Intelligence**: Automated identification of bottlenecks, anomalies, and performance degradation
- **Contextual Debugging**: Rich explanations and step-by-step workflows for systematic problem resolution  
- **Dependency Understanding**: Complete mapping of service interactions and data flow patterns
- **Historical Analysis**: Trend identification, capacity planning, and comparative performance analysis
- **Real-time Monitoring**: Current system state assessment with comprehensive metrics overlay

The MCP server transforms raw Nexus API data into intelligent, actionable insights that enable LLMs to understand and analyze complex distributed systems with the expertise of seasoned SRE professionals.
