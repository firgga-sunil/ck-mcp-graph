#!/usr/bin/env python3
"""
Graph API Client
Fetches graph data from the backend service and extracts in_in edges as triplets.
"""

import requests
import json
import time
import urllib.parse
import os
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional, Tuple

# Default configuration
DEFAULT_BASE_URL = "http://ac9248ac6be104c95987a0356fbd9ad6-d76d2f43834084df.elb.us-east-2.amazonaws.com:8081"
DEFAULT_DOMAIN = "demo"

# Read from environment variables if available
BASE_URL = os.getenv("CK_NEXUS_ENDPOINT", DEFAULT_BASE_URL)
DOMAIN = os.getenv("CK_DOMAIN", DEFAULT_DOMAIN)


def fetch_graph_data(base_url: str = None, domain: str = None, time_epoch: Optional[int] = None, headers: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
    """
    Fetch graph data from the API endpoint.
    
    Args:
        base_url: The base API URL (defaults to BASE_URL env var or DEFAULT_BASE_URL)
        domain: The domain to use in the API path (defaults to DOMAIN env var or extracted from headers)
        time_epoch: Optional epoch time for historical data (milliseconds since Unix epoch)
        headers: Optional headers dict to extract domain from (looks for 'ck-domain' header)
        
    Returns:
        The JSON response from the API
        
    Raises:
        requests.RequestException: If the API call fails
    """
    try:
        # Use defaults if not provided
        if base_url is None:
            base_url = BASE_URL
        
        # Extract domain from headers if not provided
        if domain is None:
            if headers and 'ck-domain' in headers:
                domain = headers.get('ck-domain')
            else:
                domain = DOMAIN
        
        # Construct full API URL
        api_url = f"{base_url}/{domain}/ui/graph-paths/all"
        
        params = {}
        if time_epoch is not None:
            params['time'] = time_epoch
            
        response = requests.get(api_url, headers={'accept': '*/*'}, params=params)
        response.raise_for_status()
        
        # Check for empty response
        if not response.text.strip():
            if time_epoch is not None:
                raise requests.RequestException(
                    f"API returned empty response for timestamp {time_epoch}. "
                    "This might indicate no data is available for the specified time. "
                    "Try without a timestamp or with a different time."
                )
            else:
                raise requests.RequestException("API returned empty response")
        
        return response.json()
    except requests.JSONDecodeError as e:
        if time_epoch is not None:
            raise requests.RequestException(
                f"Invalid JSON response for timestamp {time_epoch}. "
                "The API might not have data for this specific time."
            ) from e
        else:
            raise requests.RequestException(f"Invalid JSON response: {e}") from e
    except requests.RequestException as e:
        print(f"Error fetching data from API: {e}")
        raise


def fetch_metrics_data(version: str, start_time: Optional[int] = None, end_time: Optional[int] = None, 
                      base_url: str = None, domain: str = None, headers: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
    """
    Fetch metrics data (latency, throughput, errors) from the overlays API.
    
    Args:
        version: The version from the graph API response
        start_time: Start time in epoch milliseconds (defaults to current time - 1 hour)
        end_time: End time in epoch milliseconds (defaults to current time)
        base_url: The base URL of the API (defaults to BASE_URL env var or DEFAULT_BASE_URL)
        domain: The domain to use in the API path (defaults to DOMAIN env var or extracted from headers)
        headers: Optional headers dict to extract domain from (looks for 'ck-domain' header)
        
    Returns:
        The JSON response from the metrics API
        
    Raises:
        requests.RequestException: If the API call fails
    """
    try:
        # Use defaults if not provided
        if base_url is None:
            base_url = BASE_URL
        
        # Extract domain from headers if not provided
        if domain is None:
            if headers and 'ck-domain' in headers:
                domain = headers.get('ck-domain')
            else:
                domain = DOMAIN
        
        # Use default time range if not provided (last hour)
        if end_time is None:
            end_time = int(time.time() * 1000)  # Convert to milliseconds
        if start_time is None:
            start_time = end_time - 3600000  # 1 hour ago in milliseconds
            
        # URL encode the version
        encoded_version = urllib.parse.quote(version, safe='')
        api_url = f"{base_url}/{domain}/ui/graph-paths/overlays/v2?version={encoded_version}&epochStartTime={start_time}&epochEndTime={end_time}&uom=qpm"
        
        response = requests.get(api_url, headers={'accept': '*/*'})
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching metrics data from API: {e}")
        raise


def fetch_interface_details(version: str, interface_id: str, base_url: str = None, domain: str = None, headers: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
    """
    Fetch detailed view of a specific interface using the pinned API.
    
    Args:
        version: The version from the first API response
        interface_id: The interface ID to get details for
        base_url: The base URL of the API (defaults to BASE_URL env var or DEFAULT_BASE_URL)
        domain: The domain to use in the API path (defaults to DOMAIN env var or extracted from headers)
        headers: Optional headers dict to extract domain from (looks for 'ck-domain' header)
        
    Returns:
        The JSON response from the pinned API
        
    Raises:
        requests.RequestException: If the API call fails
    """
    try:
        # Use defaults if not provided
        if base_url is None:
            base_url = BASE_URL
        
        # Extract domain from headers if not provided
        if domain is None:
            if headers and 'ck-domain' in headers:
                domain = headers.get('ck-domain')
            else:
                domain = DOMAIN
        
        # URL encode the interface ID
        encoded_node_id = urllib.parse.quote(interface_id, safe='')
        api_url = f"{base_url}/{domain}/ui/graph-paths/details/pinned?version={version}&nodeId={encoded_node_id}"
        
        response = requests.post(api_url, headers={'accept': '*/*'}, data='')
        response.raise_for_status()
        
        # Check if response is empty
        if not response.text or not response.text.strip():
            raise requests.RequestException(
                f"API returned empty response for interface '{interface_id}'. "
                f"This might indicate that the node is a system unit (not an interface) "
                f"or the interface has no edges/connections. "
                f"Please use an actual interface ID from the interfaces list, not a system unit."
            )
        
        return response.json()
    except requests.JSONDecodeError as e:
        raise requests.RequestException(
            f"Invalid JSON response for interface '{interface_id}'. "
            f"The API might have returned an empty or malformed response. "
            f"Please ensure you're using a valid interface ID."
        ) from e
    except requests.RequestException as e:
        print(f"Error fetching interface details from API: {e}")
        raise


def extract_system_units_and_interfaces(graph_data: Dict[str, Any]) -> tuple:
    """
    Extract system units and interfaces from baseTimelineGraph.
    
    Args:
        graph_data: The complete graph data from the API
        
    Returns:
        Tuple of (system_units, interfaces) lists
    """
    base_timeline_graph = graph_data.get("baseTimelineGraph", {})
    
    system_units = base_timeline_graph.get("systemunits", [])
    interfaces = base_timeline_graph.get("interfaces", [])
    
    return system_units, interfaces


def extract_in_in_edges(graph_data: Dict[str, Any]) -> List[str]:
    """
    Extract in_in edges from the graph data and format them as triplets.
    
    Args:
        graph_data: The complete graph data from the API
        
    Returns:
        List of formatted edge triplets
    """
    triplets = []
    
    # Navigate to baseTimelineGraph -> edges
    base_timeline_graph = graph_data.get("baseTimelineGraph", {})
    edges = base_timeline_graph.get("edges", [])
    
    # Filter for in_in edges and format as triplets
    for edge in edges:
        if edge.startswith("in_in:"):
            # Extract the edge name (everything after "in_in:")
            edge_name = edge[6:]  # Remove "in_in:" prefix
            triplet = f"EDGE {edge_name}"
            triplets.append(triplet)
    
    return triplets


def get_edge_sync_type(edge_id: str, graph_data: Dict[str, Any]) -> str:
    """
    Get sync/async type for an edge from lookupData.
    
    Args:
        edge_id: Full edge ID (e.g., "in_in:Source->Target")
        graph_data: Complete graph data containing lookupData
        
    Returns:
        "SYNC", "ASYNC", or "UNKNOWN"
    """
    try:
        lookup_data = graph_data.get("lookupData", {})
        edge_metadata = lookup_data.get("edges", {})
        
        if edge_id in edge_metadata:
            edge_info = edge_metadata[edge_id]
            kind = edge_info.get("kind", "").upper()
            if "ASYNC" in kind:
                return "ASYNC"
            elif "SYNC" in kind:
                return "SYNC"
        return "UNKNOWN"
    except Exception:
        return "UNKNOWN"


def get_systems_overview(timestamp: Optional[str] = None, base_url: str = None, domain: str = None, headers: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
    """
    Get complete systems overview for interface selection.
    
    Args:
        timestamp: ISO 8601 timestamp (default: current time). If provided, will be converted to epoch milliseconds and passed to API.
        base_url: API base URL (defaults to BASE_URL env var or DEFAULT_BASE_URL)
        domain: The domain to use in the API path (defaults to DOMAIN env var or extracted from headers)
        headers: Optional headers dict to extract domain from (looks for 'ck-domain' header)
        
    Returns:
        Dict containing:
        - version: Version ID for subsequent calls
        - timestamp: Analysis timestamp
        - system_units: List of system unit names
        - interfaces: List of interface names
    """
    # Parse timestamp or use current time
    if timestamp:
        analysis_time = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
        # Convert to epoch time in milliseconds for API call
        time_epoch = int(analysis_time.timestamp() * 1000)
    else:
        analysis_time = datetime.now()
        time_epoch = None  # Use current time (API default)
    
    # Fetch graph data with optional time parameter
    graph_data = fetch_graph_data(base_url=base_url, domain=domain, time_epoch=time_epoch, headers=headers)
    version = graph_data.get("version", "unknown")
    
    # Extract system units and interfaces
    system_units, interfaces = extract_system_units_and_interfaces(graph_data)
    
    return {
        "version": version,
        "timestamp": analysis_time.isoformat(),
        "system_units": system_units,
        "interfaces": interfaces
    }


def get_interface_analysis(interface_id: str, version: str, start_time: Optional[str] = None, 
                         end_time: Optional[str] = None, base_url: str = None, domain: str = None, headers: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
    """
    Get detailed interface analysis with dependencies and metrics.
    
    Args:
        interface_id: Interface ID to analyze
        version: Version ID from systems overview
        start_time: Start timestamp for metrics (default: 30 minutes ago)
        end_time: End timestamp for metrics (default: now)
        base_url: API base URL (defaults to BASE_URL env var or DEFAULT_BASE_URL)
        domain: The domain to use in the API path (defaults to DOMAIN env var or extracted from headers)
        headers: Optional headers dict to extract domain from (looks for 'ck-domain' header)
        
    Returns:
        Dict containing:
        - interface_id: Analyzed interface
        - version: Version used
        - time_range: Analysis time range
        - edges: List of edge dictionaries with metrics and sync type
        - raw_data: Original API responses for advanced processing
    """
    # Parse time range
    if end_time:
        end_dt = datetime.fromisoformat(end_time.replace('Z', '+00:00'))
    else:
        end_dt = datetime.now()
        
    if start_time:
        start_dt = datetime.fromisoformat(start_time.replace('Z', '+00:00'))
    else:
        start_dt = end_dt - timedelta(minutes=30)
    
    # Fetch interface details and metrics
    interface_data = fetch_interface_details(version, interface_id, base_url=base_url, domain=domain, headers=headers)
    
    start_epoch = int(start_dt.timestamp() * 1000)  # Convert to milliseconds
    end_epoch = int(end_dt.timestamp() * 1000)  # Convert to milliseconds
    metrics_data = fetch_metrics_data(version, start_epoch, end_epoch, base_url=base_url, domain=domain, headers=headers)
    
    # Extract and process edges
    base_timeline_graph = interface_data.get("baseTimelineGraph", {})
    all_edges = base_timeline_graph.get("edges", [])
    in_in_edges = [edge for edge in all_edges if edge.startswith("in_in:")]
    
    # Process each edge with metrics and sync type
    processed_edges = []
    for edge in in_in_edges:
        edge_display = edge[6:] if edge.startswith("in_in:") else edge
        
        # Get sync/async type
        sync_type = get_edge_sync_type(edge, interface_data)
        
        # Get metrics
        metrics = get_metrics_for_item(edge_display, metrics_data, version, "edges")
        
        # Determine relationship to analyzed interface
        relationship = "RELATED"
        if "->" in edge_display:
            source, target = edge_display.split("->", 1)
            if target == interface_id:
                relationship = "UPSTREAM"
            elif source == interface_id:
                relationship = "DOWNSTREAM"
        
        processed_edges.append({
            "edge_display": edge_display,
            "full_edge_id": edge,
            "sync_type": sync_type,
            "relationship": relationship,
            "metrics": metrics,
            "source": source if "->" in edge_display else None,
            "target": target if "->" in edge_display else None
        })
    
    return {
        "interface_id": interface_id,
        "version": version,
        "time_range": {
            "start": start_dt.isoformat(),
            "end": end_dt.isoformat(),
            "duration_minutes": (end_dt - start_dt).total_seconds() / 60
        },
        "edges": processed_edges,
        "raw_data": {
            "interface_data": interface_data,
            "metrics_data": metrics_data
        }
    }


def get_metrics_for_item(item_id: str, metrics_data: Dict[str, Any], version: str, item_type: str) -> Optional[Dict[str, Any]]:
    """
    Get metrics for a specific item (system unit, interface, or edge).
    
    Args:
        item_id: The ID of the item to get metrics for
        metrics_data: The complete metrics data from API 3
        version: The version to look for in metrics data
        item_type: Type of item ('system_units', 'interfaces', or 'edges')
        
    Returns:
        Metrics dictionary or None if not found
    """
    try:
        tick_response = metrics_data.get("tickResponse", {})
        version_data = tick_response.get(version, {})
        item_category = version_data.get(item_type, {})
        
        # For edges, the item_id might have a prefix that needs to be handled
        if item_type == "edges":
            # Try direct lookup first
            if item_id in item_category:
                return item_category[item_id].get("server_metrics", {})
            
            # Try looking for in_in: prefix
            prefixed_id = f"in_in:{item_id}"
            if prefixed_id in item_category:
                return item_category[prefixed_id].get("server_metrics", {})
        else:
            if item_id in item_category:
                return item_category[item_id]
                
        return None
    except Exception:
        return None


def aggregate_errors(errors: Dict[str, Any]) -> Tuple[int, int, int]:
    """
    Aggregate error codes from overlays v2 API into 4xx and 5xx buckets.
    
    Args:
        errors: Error dictionary from metrics (e.g., {"400": 10, "401": 5, "500": 3, "total": 18})
        
    Returns:
        Tuple of (total_errors, error_4xx, error_5xx)
    """
    # Check if pre-aggregated 4xx/5xx exist (backward compatibility)
    # If keys exist, use them (even if 0, as that means no errors in that category)
    has_4xx_pre = "4xx" in errors
    has_5xx_pre = "5xx" in errors
    
    # Aggregate from individual error codes
    error_4xx_agg = 0
    error_5xx_agg = 0
    
    for error_code_str, error_count in errors.items():
        # Skip non-numeric keys like "total", "4xx", "5xx"
        if error_code_str in ("total", "4xx", "5xx"):
            continue
        try:
            error_code = int(error_code_str)
            # Aggregate 4xx errors (400-499)
            if 400 <= error_code < 500:
                error_4xx_agg += error_count
            # Aggregate 5xx errors (500-599)
            elif 500 <= error_code < 600:
                error_5xx_agg += error_count
        except (ValueError, TypeError):
            # Skip non-numeric keys
            continue
    
    # Use pre-aggregated values if available, otherwise use aggregated values
    error_4xx = errors.get("4xx", 0) if has_4xx_pre else error_4xx_agg
    error_5xx = errors.get("5xx", 0) if has_5xx_pre else error_5xx_agg
    
    # Calculate total errors
    total_errors = errors.get("total", 0)
    if total_errors == 0:
        # If total not provided, sum all error counts (including aggregated 4xx/5xx if used)
        total_errors = error_4xx + error_5xx
        # Add any other error codes that aren't 4xx or 5xx
        for error_code_str, error_count in errors.items():
            if error_code_str in ("total", "4xx", "5xx"):
                continue
            try:
                error_code = int(error_code_str)
                if not (400 <= error_code < 600):
                    total_errors += error_count
            except (ValueError, TypeError):
                continue
    
    return total_errors, error_4xx, error_5xx


def fetch_code_details_for_api(domain_name: Optional[str], service_name: str, http_method: str, 
                               http_api_signature: str, base_url: Optional[str] = None, headers: Optional[Dict[str, str]] = None) -> List[Dict[str, Any]]:
    """
    Fetch code details (className and methodName) by HTTP method and API signature.
    
    This corresponds to the Java API endpoint that returns List<CodeDetailsForApiResponse>.
    Each CodeDetailsForApiResponse contains:
    - className: String
    - methodName: String
    
    Args:
        domain_name: The domain name for the API path
        service_name: The service name (required query parameter)
        http_method: HTTP method (e.g., "GET", "POST", "PUT", "DELETE")
        http_api_signature: HTTP API signature/path
        base_url: The base URL of the API (defaults to BASE_URL env var or DEFAULT_BASE_URL)
        headers: Optional headers dict to extract domain from (looks for 'ck-domain' header)
        
    Returns:
        List of dictionaries, each containing:
        - className: String - The class name that implements the API
        - methodName: String - The method name that handles the API
        
    Raises:
        requests.RequestException: If the API call fails or response format is invalid
    """
    try:
        # Use defaults if not provided
        if base_url is None:
            base_url = BASE_URL
        
        # Extract domain from headers if not provided
        if domain_name is None:
            if headers and 'ck-domain' in headers:
                domain_name = headers.get('ck-domain')
            else:
                domain_name = DOMAIN
        
        # Construct API URL
        api_url = f"{base_url}/{domain_name}/api/method-graph-paths/code-details-for-api"
        
        # Request body
        request_body = {
            "httpMethod": http_method,
            "httpApiSignature": http_api_signature
        }
        
        # Query parameters
        params = {
            "serviceName": service_name
        }
        
        response = requests.post(
            api_url,
            headers={'accept': '*/*', 'Content-Type': 'application/json'},
            params=params,
            json=request_body
        )
        response.raise_for_status()
        
        # Check for empty response
        if not response.text.strip():
            raise requests.RequestException(
                f"API returned empty response for service '{service_name}' with method '{http_method}' and signature '{http_api_signature}'. "
                "This might indicate no code details are available for the specified parameters."
            )
        
        # Parse JSON response (should be List<CodeDetailsForApiResponse>)
        result = response.json()
        
        # Validate response structure
        if not isinstance(result, list):
            raise requests.RequestException(
                f"Unexpected response format. Expected a list of CodeDetailsForApiResponse objects, "
                f"but got {type(result).__name__}."
            )
        
        # Validate each item has className and methodName
        for i, item in enumerate(result):
            if not isinstance(item, dict):
                raise requests.RequestException(
                    f"Invalid response item at index {i}. Expected a dictionary with className and methodName, "
                    f"but got {type(item).__name__}."
                )
            if "className" not in item or "methodName" not in item:
                raise requests.RequestException(
                    f"Invalid response item at index {i}. Missing className or methodName field."
                )
        
        return result
    except requests.JSONDecodeError as e:
        raise requests.RequestException(
            f"Invalid JSON response for code details request. "
            f"The API might have returned an empty or malformed response. "
            f"Error: {e}"
        ) from e
    except requests.RequestException as e:
        print(f"Error fetching code details from API: {e}")
        raise


def format_metrics(metrics: Optional[Dict[str, Any]], 
                  latency_percentiles: List[str] = ["0.5", "0.9", "0.95", "0.99"]) -> str:
    """
    Format metrics data into a readable string.
    
    Args:
        metrics: Metrics dictionary with t, e, l keys
        latency_percentiles: List of latency percentiles to display (default: p50, p90, p95, p99)
        
    Returns:
        Formatted metrics string
    """
    if not metrics:
        return "No metrics"
    
    # Throughput
    throughput = metrics.get("t", {}).get("qpm", "N/A")
    
    # Errors - aggregate from individual error codes (400, 401, 500, etc.) into 4xx and 5xx buckets
    errors = metrics.get("e", {})
    total_errors, error_4xx, error_5xx = aggregate_errors(errors)
    
    # Latency percentiles
    latency = metrics.get("l", {})
    latency_parts = []
    for percentile in latency_percentiles:
        value = latency.get(percentile, "N/A")
        # Convert percentile to readable format (0.5 -> p50, 0.99 -> p99)
        p_name = f"p{int(float(percentile) * 100)}"
        latency_parts.append(f"{p_name}={value}ms")
    
    latency_str = " ".join(latency_parts)
    
    return f"QPM: {throughput}, Errors: {total_errors} (4xx: {error_4xx}, 5xx: {error_5xx}), Latency: {latency_str}"


def display_items_with_metrics(title: str, items: List[str], metrics_data: Dict[str, Any], version: str, item_type: str):
    """
    Display items with their associated metrics on a single line.
    """
    print(f"\n{title} ({len(items)} found):")
    print("-" * max(100, len(title)))
    
    if not items:
        print("  No items found")
        return
    
    for item in items:
        metrics = get_metrics_for_item(item, metrics_data, version, item_type)
        metrics_str = format_metrics(metrics)
        print(f"  {item} | {metrics_str}")


def display_triplets_with_metrics(triplets: List[str], metrics_data: Dict[str, Any], version: str):
    """
    Display triplets with their associated metrics on a single line.
    """
    print(f"\nFound {len(triplets)} in_in edges:")
    print("-" * 100)
    
    if not triplets:
        print("  No in_in edges found")
        return
    
    for triplet in triplets:
        # Extract edge name from triplet format "EDGE edge_name"
        edge_name = triplet[5:]  # Remove "EDGE " prefix
        metrics = get_metrics_for_item(edge_name, metrics_data, version, "edges")
        metrics_str = format_metrics(metrics)
        print(f"  {triplet} | {metrics_str}")


def main():
    """
    Main function to fetch data and extract information with metrics.
    """
    try:
        # Fetch graph data
        print("Fetching graph data from API...")
        graph_data = fetch_graph_data()
        
        version = graph_data.get("version", "unknown")
        print(f"Version: {version}")
        
        # Extract system units and interfaces
        print("\nExtracting system units and interfaces...")
        system_units, interfaces = extract_system_units_and_interfaces(graph_data)
        
        # Extract in_in edges as triplets
        print("Extracting in_in edges...")
        triplets = extract_in_in_edges(graph_data)
        
        # Fetch metrics data
        print("\nFetching metrics data...")
        try:
            metrics_data = fetch_metrics_data(version)
            print("✅ Metrics data retrieved successfully")
        except Exception as e:
            print(f"⚠️  Could not fetch metrics data: {e}")
            metrics_data = {}
        
        # Display results with metrics
        display_items_with_metrics("System Units", system_units, metrics_data, version, "system_units")
        display_items_with_metrics("Interfaces", interfaces, metrics_data, version, "interfaces") 
        display_triplets_with_metrics(triplets, metrics_data, version)
            
        return {
            'version': version,
            'system_units': system_units,
            'interfaces': interfaces,
            'triplets': triplets,
            'metrics_data': metrics_data
        }
        
    except Exception as e:
        print(f"Error: {e}")
        return None


if __name__ == "__main__":
    main()
