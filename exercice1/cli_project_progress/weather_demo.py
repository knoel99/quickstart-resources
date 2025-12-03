#!/usr/bin/env python3
"""
Demo script to test weather functionality in the CLI project
"""

import asyncio
import json
from core.weather import WeatherAPI
from core.tools import ToolManager

async def demo_weather():
    """Demonstrate weather API functionality."""
    print("=== Weather API Demo ===\n")
    
    # Initialize weather API
    weather = WeatherAPI()
    
    # Test 1: Get weather alerts
    print("1. Testing weather alerts for California:")
    try:
        alerts = weather.get_alerts("CA")
        print(f"Alerts result: {alerts[:200]}...\n")  # Show first 200 chars
    except Exception as e:
        print(f"Error getting alerts: {e}\n")
    
    # Test 2: Get weather forecast
    print("2. Testing weather forecast for San Francisco:")
    try:
        forecast = weather.get_forecast(37.7749, -122.4194)
        print(f"Forecast result: {forecast[:200]}...\n")  # Show first 200 chars
    except Exception as e:
        print(f"Error getting forecast: {e}\n")

def demo_tool_manager():
    """Demonstrate tool manager functionality."""
    print("=== Tool Manager Demo ===\n")
    
    # Initialize tool manager
    tool_manager = ToolManager()
    
    # List available tools
    print("1. Available tools:")
    tools = tool_manager.list_tools()
    for tool in tools:
        print(f"  - {tool}")
    print()
    
    # Test web search tool
    print("2. Testing web search tool:")
    try:
        result = tool_manager.execute_tool("web_search", {
            "query": "Python programming tutorial",
            "max_results": 3
        })
        print(f"Search result: {json.dumps(result, indent=2)[:300]}...\n")
    except Exception as e:
        print(f"Error with web search: {e}\n")
    
    # Test file operations
    print("3. Testing file operations:")
    try:
        # Create a test file
        tool_manager.execute_tool("create_file", {
            "path": "test_demo.txt",
            "content": "Hello from ToolManager!"
        })
        print("Created test file")
        
        # Read the file
        content = tool_manager.execute_tool("read_file", {
            "path": "test_demo.txt"
        })
        print(f"File content: {content}")
        
        # Clean up
        tool_manager.execute_tool("delete_file", {
            "path": "test_demo.txt"
        })
        print("Deleted test file\n")
    except Exception as e:
        print(f"Error with file operations: {e}\n")

def demo_mcp_integration():
    """Demonstrate MCP integration."""
    print("=== MCP Integration Demo ===\n")
    
    # This would typically be called through MCP client
    # For demo purposes, we'll show the structure
    
    print("Available MCP tools:")
    mcp_tools = [
        "list_native_tools",
        "execute_native_tool", 
        "get_weather_alerts",
        "get_weather_forecast",
        "read_doc_contents",
        "edit_document"
    ]
    
    for tool in mcp_tools:
        print(f"  - {tool}")
    
    print("\nExample MCP tool calls:")
    print("1. list_native_tools() - Returns list of native tools")
    print("2. execute_native_tool('web_search', '{\"query\": \"test\"}') - Executes native tool")
    print("3. get_weather_alerts('CA') - Gets weather alerts for California")
    print("4. get_weather_forecast(37.7749, -122.4194) - Gets SF forecast")

if __name__ == "__main__":
    print("CLI Project Progress - Weather Integration Demo")
    print("=" * 50)
    
    # Run demos
    asyncio.run(demo_weather())
    demo_tool_manager()
    demo_mcp_integration()
    
    print("\n" + "=" * 50)
    print("Demo completed successfully!")
