#!/usr/bin/env python3
"""
Interactive Graph API Client
Fetches graph data from the backend service with two modes:
1. List system units and interfaces from the first API
2. Get detailed view of a specific interface using the second API
"""

import requests
import json
import time
import urllib.parse
from typing import List, Dict, Any, Tuple, Optional
import graph_api_client


def fetch_graph_data(api_url: str = "http://ac9248ac6be104c95987a0356fbd9ad6-d76d2f43834084df.elb.us-east-2.amazonaws.com:8081/demo/ui/graph-paths/all") -> Dict[str, Any]:
    """
    Fetch graph data from the API endpoint.
    
    Args:
        api_url: The API URL to fetch data from
        
    Returns:
        The JSON response from the API
        
    Raises:
        requests.RequestException: If the API call fails
    """
    try:
        response = requests.get(api_url, headers={'accept': '*/*'})
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching data from API: {e}")
        raise


def fetch_interface_details(version: str, interface_id: str, base_url: str = "http://ac9248ac6be104c95987a0356fbd9ad6-d76d2f43834084df.elb.us-east-2.amazonaws.com:8081") -> Dict[str, Any]:
    """
    Fetch detailed view of a specific interface using the pinned API.
    
    Args:
        version: The version from the first API response
        interface_id: The interface ID to get details for
        base_url: The base URL of the API
        
    Returns:
        The JSON response from the pinned API
        
    Raises:
        requests.RequestException: If the API call fails
    """
    try:
        # URL encode the interface ID
        encoded_node_id = urllib.parse.quote(interface_id, safe='')
        api_url = f"{base_url}/demo/ui/graph-paths/details/pinned?version={version}&nodeId={encoded_node_id}"
        
        response = requests.post(api_url, headers={'accept': '*/*'}, data='')
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching interface details from API: {e}")
        raise


def fetch_metrics_data(version: str, start_time: Optional[int] = None, end_time: Optional[int] = None, 
                      base_url: str = "http://ac9248ac6be104c95987a0356fbd9ad6-d76d2f43834084df.elb.us-east-2.amazonaws.com:8081") -> Dict[str, Any]:
    """
    Fetch metrics data (latency, throughput, errors) from the overlays API.
    
    Args:
        version: The version from the graph API response
        start_time: Start time in epoch seconds (defaults to current time - 1 hour)
        end_time: End time in epoch seconds (defaults to current time)
        base_url: The base URL of the API
        
    Returns:
        The JSON response from the metrics API
        
    Raises:
        requests.RequestException: If the API call fails
    """
    try:
        # Use default time range if not provided (last hour)
        if end_time is None:
            end_time = int(time.time())
        if start_time is None:
            start_time = end_time - 3600  # 1 hour ago
            
        # URL encode the version
        encoded_version = urllib.parse.quote(version, safe='')
        api_url = f"{base_url}/demo/ui/graph-paths/overlays/v2?version={encoded_version}&epochStartTime={start_time}&epochEndTime={end_time}&uom=qpm"
        
        response = requests.get(api_url, headers={'accept': '*/*'})
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching metrics data from API: {e}")
        raise


def extract_system_units_and_interfaces(graph_data: Dict[str, Any]) -> Tuple[List[str], List[str]]:
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
    
    # Errors - aggregate from individual error codes
    errors = metrics.get("e", {})
    total_errors, error_4xx, error_5xx = graph_api_client.aggregate_errors(errors)
    
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


def display_menu():
    """Display the main menu options."""
    print("\n" + "="*50)
    print("Interactive Graph API Client")
    print("="*50)
    print("1. List System Units and Interfaces")
    print("2. Get Interface Details (with in_in edges)")
    print("3. Exit")
    print("="*50)


def list_items(title: str, items: List[str], numbered: bool = True, 
              metrics_data: Optional[Dict[str, Any]] = None, version: str = "", item_type: str = ""):
    """Display a list of items with optional numbering and metrics on a single line."""
    print(f"\n{title}:")
    print("-" * max(100, len(title)))
    
    if not items:
        print("  No items found")
        return
    
    for i, item in enumerate(items, 1):
        if metrics_data and version and item_type:
            metrics = get_metrics_for_item(item, metrics_data, version, item_type)
            metrics_str = format_metrics(metrics)
            if numbered:
                print(f"  {i:2d}. {item} | {metrics_str}")
            else:
                print(f"     {item} | {metrics_str}")
        else:
            if numbered:
                print(f"  {i:2d}. {item}")
            else:
                print(f"     {item}")


def get_user_choice(prompt: str, max_choice: int) -> int:
    """Get a valid user choice within the specified range."""
    while True:
        try:
            choice = int(input(f"\n{prompt} (1-{max_choice}): "))
            if 1 <= choice <= max_choice:
                return choice
            else:
                print(f"Please enter a number between 1 and {max_choice}")
        except ValueError:
            print("Please enter a valid number")


def main():
    """
    Main interactive function.
    """
    print("Starting Interactive Graph API Client...")
    
    while True:
        display_menu()
        
        try:
            choice = get_user_choice("Select an option", 3)
            
            if choice == 1:
                # List system units and interfaces with metrics
                print("\nFetching graph data...")
                graph_data = fetch_graph_data()
                version = graph_data.get("version", "unknown")
                
                print(f"Version: {version}")
                
                # Fetch metrics data
                print("Fetching metrics data...")
                try:
                    metrics_data = fetch_metrics_data(version)
                    print("✅ Metrics data retrieved successfully")
                except Exception as e:
                    print(f"⚠️  Could not fetch metrics data: {e}")
                    metrics_data = {}
                
                system_units, interfaces = extract_system_units_and_interfaces(graph_data)
                
                list_items(f"System Units ({len(system_units)} found)", system_units, numbered=False,
                          metrics_data=metrics_data, version=version, item_type="system_units")
                list_items(f"Interfaces ({len(interfaces)} found)", interfaces, numbered=False,
                          metrics_data=metrics_data, version=version, item_type="interfaces")
                
            elif choice == 2:
                # Get interface details with metrics
                print("\nFetching available interfaces...")
                graph_data = fetch_graph_data()
                version = graph_data.get("version", "unknown")
                
                _, interfaces = extract_system_units_and_interfaces(graph_data)
                
                if not interfaces:
                    print("No interfaces found!")
                    continue
                
                print(f"\nVersion: {version}")
                list_items(f"Available Interfaces ({len(interfaces)} found)", interfaces, numbered=True)
                
                interface_choice = get_user_choice("Select an interface", len(interfaces))
                selected_interface = interfaces[interface_choice - 1]
                
                print(f"\nFetching details for interface: {selected_interface}")
                print(f"Using version: {version}")
                
                try:
                    interface_details = fetch_interface_details(version, selected_interface)
                    triplets = extract_in_in_edges(interface_details)
                    
                    # Fetch metrics for the detailed view
                    print("Fetching metrics data...")
                    try:
                        metrics_data = fetch_metrics_data(version)
                        print("✅ Metrics data retrieved successfully")
                    except Exception as e:
                        print(f"⚠️  Could not fetch metrics data: {e}")
                        metrics_data = {}
                    
                    print(f"\nFound {len(triplets)} in_in edges for {selected_interface}:")
                    print("-" * 100)
                    
                    if triplets:
                        for triplet in triplets:
                            # Extract edge name from triplet format "EDGE edge_name"
                            edge_name = triplet[5:]  # Remove "EDGE " prefix
                            metrics = get_metrics_for_item(edge_name, metrics_data, version, "edges")
                            metrics_str = format_metrics(metrics)
                            print(f"  {triplet} | {metrics_str}")
                    else:
                        print("  No in_in edges found for this interface")
                        
                except Exception as e:
                    print(f"Error getting interface details: {e}")
                
            elif choice == 3:
                print("\nExiting...")
                break
                
        except KeyboardInterrupt:
            print("\n\nExiting...")
            break
        except Exception as e:
            print(f"\nError: {e}")
            print("Please try again.")


if __name__ == "__main__":
    main()
