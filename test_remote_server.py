#!/usr/bin/env python3
"""
Test script for the remote Graph Analysis MCP server
"""

import requests
import json
import sys
from typing import Optional

def test_health_check(base_url: str) -> bool:
    """Test the health check endpoint"""
    try:
        response = requests.get(f"{base_url}/health", timeout=5)
        response.raise_for_status()
        data = response.json()
        print("✅ Health check passed")
        print(f"   Server: {data.get('server')}")
        print(f"   Version: {data.get('version')}")
        print(f"   Status: {data.get('status')}")
        print(f"   Graph API: {data.get('graph_api_url')}")
        return True
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return False

def test_initialize(base_url: str) -> bool:
    """Test the MCP initialize method"""
    try:
        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {}
        }
        response = requests.post(f"{base_url}/mcp", json=payload, timeout=5)
        response.raise_for_status()
        data = response.json()
        
        if "result" in data:
            print("✅ Initialize method passed")
            print(f"   Protocol version: {data['result'].get('protocolVersion')}")
            print(f"   Server name: {data['result'].get('serverInfo', {}).get('name')}")
            return True
        else:
            print(f"❌ Initialize method failed: {data.get('error', {}).get('message', 'Unknown error')}")
            return False
    except Exception as e:
        print(f"❌ Initialize method failed: {e}")
        return False

def test_list_tools(base_url: str) -> bool:
    """Test listing available tools"""
    try:
        payload = {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/list",
            "params": {}
        }
        response = requests.post(f"{base_url}/mcp", json=payload, timeout=5)
        response.raise_for_status()
        data = response.json()
        
        if "result" in data and "tools" in data["result"]:
            tools = data["result"]["tools"]
            print(f"✅ List tools passed - Found {len(tools)} tools")
            for tool in tools:
                print(f"   - {tool['name']}")
            return True
        else:
            print(f"❌ List tools failed: {data.get('error', {}).get('message', 'Unknown error')}")
            return False
    except Exception as e:
        print(f"❌ List tools failed: {e}")
        return False

def test_get_systems(base_url: str) -> Optional[tuple]:
    """Test the get_systems_and_interfaces tool"""
    try:
        payload = {
            "jsonrpc": "2.0",
            "id": 3,
            "method": "tools/call",
            "params": {
                "name": "get_systems_and_interfaces",
                "arguments": {}
            }
        }
        response = requests.post(f"{base_url}/mcp", json=payload, timeout=30)
        response.raise_for_status()
        data = response.json()
        
        if "result" in data and "content" in data["result"]:
            content = data["result"]["content"]
            if content and len(content) > 0:
                text = content[0].get("text", "")
                print("✅ Get systems and interfaces passed")
                print(f"   Response length: {len(text)} characters")
                
                # Try to extract version and first interface for follow-up test
                import re
                version_match = re.search(r'System Version.*?`([^`]+)`', text)
                interface_match = re.search(r'\d+\.\s+`([^`]+)`', text)
                
                version = version_match.group(1) if version_match else None
                interface = interface_match.group(1) if interface_match else None
                
                if version:
                    print(f"   Version: {version}")
                if interface:
                    print(f"   First interface: {interface}")
                
                return (version, interface)
            else:
                print("❌ Get systems and interfaces returned empty content")
                return None
        else:
            error_msg = data.get('error', {}).get('message', 'Unknown error')
            print(f"❌ Get systems and interfaces failed: {error_msg}")
            return None
    except Exception as e:
        print(f"❌ Get systems and interfaces failed: {e}")
        return None

def test_get_interface_details(base_url: str, interface_id: str, version: str) -> bool:
    """Test the get_interface_details tool"""
    try:
        payload = {
            "jsonrpc": "2.0",
            "id": 4,
            "method": "tools/call",
            "params": {
                "name": "get_interface_details",
                "arguments": {
                    "interface_id": interface_id,
                    "version": version
                }
            }
        }
        response = requests.post(f"{base_url}/mcp", json=payload, timeout=30)
        response.raise_for_status()
        data = response.json()
        
        if "result" in data and "content" in data["result"]:
            content = data["result"]["content"]
            if content and len(content) > 0:
                text = content[0].get("text", "")
                print("✅ Get interface details passed")
                print(f"   Response length: {len(text)} characters")
                print(f"   Interface analyzed: {interface_id}")
                return True
            else:
                print("❌ Get interface details returned empty content")
                return False
        else:
            error_msg = data.get('error', {}).get('message', 'Unknown error')
            print(f"❌ Get interface details failed: {error_msg}")
            return False
    except Exception as e:
        print(f"❌ Get interface details failed: {e}")
        return False

def main():
    """Run all tests"""
    # Get base URL from command line or use default
    base_url = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:8548"
    
    print(f"🧪 Testing Graph Analysis MCP Server at {base_url}")
    print("=" * 70)
    print()
    
    results = []
    
    # Test 1: Health check
    print("Test 1: Health Check")
    results.append(test_health_check(base_url))
    print()
    
    # Test 2: Initialize
    print("Test 2: MCP Initialize")
    results.append(test_initialize(base_url))
    print()
    
    # Test 3: List tools
    print("Test 3: List Tools")
    results.append(test_list_tools(base_url))
    print()
    
    # Test 4: Get systems and interfaces
    print("Test 4: Get Systems and Interfaces")
    sys_result = test_get_systems(base_url)
    results.append(sys_result is not None)
    print()
    
    # Test 5: Get interface details (if we got a version and interface from test 4)
    if sys_result and sys_result[0] and sys_result[1]:
        print("Test 5: Get Interface Details")
        results.append(test_get_interface_details(base_url, sys_result[1], sys_result[0]))
        print()
    else:
        print("Test 5: Get Interface Details - Skipped (no interface available)")
        print()
    
    # Summary
    print("=" * 70)
    passed = sum(results)
    total = len(results)
    print(f"Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed!")
        sys.exit(0)
    else:
        print("⚠️  Some tests failed")
        sys.exit(1)

if __name__ == "__main__":
    main()

