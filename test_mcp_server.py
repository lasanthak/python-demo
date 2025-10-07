"""
Test script for MCP server operations
"""

import sys
sys.path.insert(0, '/Users/lkularatne/lkrepos/python-demo')

# Import the underlying functions directly
import mcp_server

def test_operations():
    """Test all three MCP server operations"""

    print("=" * 70)
    print("Testing MCP Server Operations")
    print("=" * 70)

    # Test 1: Get zipcode by coordinates (Austin, TX area)
    print("\n1. Testing get_zipcode_by_coords:")
    print("-" * 70)
    result = mcp_server._get_zipcode_by_coords(30.27, -97.74)
    print(f"   Input: lat=30.27, lon=-97.74")
    print(f"   Result: {result}")

    # Test 2: Get zipcode by coordinates (New York, NY area)
    result = mcp_server._get_zipcode_by_coords(40.71, -74.01)
    print(f"\n   Input: lat=40.71, lon=-74.01")
    print(f"   Result: {result}")

    # Test 3: Get zipcode by city and state
    print("\n\n2. Testing get_zipcode_by_city_state:")
    print("-" * 70)

    test_cities = [
        ("Austin", "TX"),
        ("New York", "NY"),
        ("Los Angeles", "CA"),
        ("Seattle", "WA"),
        ("Denver", "CO"),
        ("Miami", "FL")  # This should fail - not in database
    ]

    for city, state in test_cities:
        result = mcp_server._get_zipcode_by_city_state(city, state)
        print(f"   {city}, {state}: {result}")

    # Test 4: Get temperature by zipcode
    print("\n\n3. Testing get_temperature_by_zipcode:")
    print("-" * 70)

    test_zipcodes = ["78701", "10001", "90001", "98101", "12345"]  # Last one should fail

    for zipcode in test_zipcodes:
        result = mcp_server._get_temperature_by_zipcode(zipcode)
        print(f"   Zip {zipcode}: {result}")

    print("\n" + "=" * 70)
    print("Testing Complete!")
    print("=" * 70)

if __name__ == "__main__":
    test_operations()
