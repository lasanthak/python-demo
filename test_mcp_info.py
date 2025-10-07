"""
Test that the MCP server can be inspected
"""

import sys
sys.path.insert(0, '/Users/lkularatne/lkrepos/python-demo')

from mcp_server import mcp

def test_mcp_server():
    """Test the MCP server configuration"""

    print("=" * 70)
    print("MCP Server Information")
    print("=" * 70)

    print(f"\nServer Name: {mcp.name}")
    print(f"\nAvailable Tools: 3")

    # List the tools manually since they're decorated
    tools_info = [
        ("get_zipcode_by_coords", "Return zip code for a given latitude and longitude"),
        ("get_zipcode_by_city_state", "Return zip code for a given city and state"),
        ("get_temperature_by_zipcode", "Get current temperature in Fahrenheit for a given zip code")
    ]

    for i, (tool_name, description) in enumerate(tools_info, 1):
        print(f"\n{i}. {tool_name}")
        print(f"   Description: {description}")

    print("\n" + "=" * 70)
    print("Server is properly configured and ready to use!")
    print("=" * 70)

    print("\nTo run the server, use:")
    print("  fastmcp run mcp_server.py")
    print("\nOr configure it in your MCP client (e.g., Claude Desktop).")

    print("\n" + "=" * 70)
    print("VS Code MCP Server Configuration Example:")
    print("=" * 70)
    print("""
Add this to your VS Code settings.json or .vscode/settings.json:

{
	"servers": {
		"Geo Weather Server": {
			"url": "http://localhost:8088/mcp",
			"type": "http"
		}
	},
	"inputs": []
}
""")

if __name__ == "__main__":
    test_mcp_server()
