"""
MCP Server for Zip Code and Weather Operations
Provides three operations:
1. get_zipcode_by_coords: Return zip code for a given lon & lat
2. get_zipcode_by_city_state: Return zip code for a given city and state
3. get_temperature_by_zipcode: Current temperature in Fahrenheit for a given zip code
"""

from fastmcp import FastMCP
import requests
from typing import Optional
import math

# Initialize FastMCP server
mcp = FastMCP("Geo Weather Server", port=8088, stateless_http=True)

# Hardcoded geo data for major US cities
GEO_DATA = [
    {"city": "Austin", "state": "TX", "zipcode": "78701", "lat": 30.2672, "lon": -97.7431},
    {"city": "New York", "state": "NY", "zipcode": "10001", "lat": 40.7128, "lon": -74.0060},
    {"city": "Los Angeles", "state": "CA", "zipcode": "90001", "lat": 34.0522, "lon": -118.2437},
    {"city": "Chicago", "state": "IL", "zipcode": "60601", "lat": 41.8781, "lon": -87.6298},
    {"city": "Houston", "state": "TX", "zipcode": "77001", "lat": 29.7604, "lon": -95.3698},
    {"city": "Phoenix", "state": "AZ", "zipcode": "85001", "lat": 33.4484, "lon": -112.0740},
    {"city": "Philadelphia", "state": "PA", "zipcode": "19101", "lat": 39.9526, "lon": -75.1652},
    {"city": "San Antonio", "state": "TX", "zipcode": "78201", "lat": 29.4241, "lon": -98.4936},
    {"city": "San Diego", "state": "CA", "zipcode": "92101", "lat": 32.7157, "lon": -117.1611},
    {"city": "Dallas", "state": "TX", "zipcode": "75201", "lat": 32.7767, "lon": -96.7970},
    {"city": "Jacksonville", "state": "FL", "zipcode": "32099", "lat": 30.3322, "lon": -81.6557},
    {"city": "Fort Worth", "state": "TX", "zipcode": "76101", "lat": 32.7555, "lon": -97.3308},
    {"city": "San Jose", "state": "CA", "zipcode": "95101", "lat": 37.3382, "lon": -121.8863},
    {"city": "Charlotte", "state": "NC", "zipcode": "28201", "lat": 35.2271, "lon": -80.8431},
    {"city": "Columbus", "state": "OH", "zipcode": "43201", "lat": 39.9612, "lon": -82.9988},
    {"city": "Indianapolis", "state": "IN", "zipcode": "46201", "lat": 39.7684, "lon": -86.1581},
    {"city": "San Francisco", "state": "CA", "zipcode": "94101", "lat": 37.7749, "lon": -122.4194},
    {"city": "Seattle", "state": "WA", "zipcode": "98101", "lat": 47.6062, "lon": -122.3321},
    {"city": "Denver", "state": "CO", "zipcode": "80201", "lat": 39.7392, "lon": -104.9903},
    {"city": "Oklahoma City", "state": "OK", "zipcode": "73101", "lat": 35.4676, "lon": -97.5164},
]


def calculate_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Calculate the distance between two points using the Haversine formula.
    Returns distance in kilometers.
    """
    # Convert to radians
    lat1_rad = math.radians(lat1)
    lat2_rad = math.radians(lat2)
    lon1_rad = math.radians(lon1)
    lon2_rad = math.radians(lon2)

    # Haversine formula
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad
    a = math.sin(dlat/2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))

    # Earth's radius in kilometers
    r = 6371
    return c * r


def _get_zipcode_by_coords(lat: float, lon: float) -> str:
    """Core implementation for getting zipcode by coordinates"""
    if not GEO_DATA:
        return "Error: No geo data available"

    # Find the closest city
    closest_city = None
    min_distance = float('inf')

    for city_data in GEO_DATA:
        distance = calculate_distance(lat, lon, city_data["lat"], city_data["lon"])
        if distance < min_distance:
            min_distance = distance
            closest_city = city_data

    if closest_city:
        return f"Zip code: {closest_city['zipcode']} ({closest_city['city']}, {closest_city['state']}) - Distance: {min_distance:.2f} km"

    return "Error: Could not find nearest city"


@mcp.tool()
def get_zipcode_by_coords(lat: float, lon: float) -> str:
    """
    Return zip code for a given latitude and longitude.
    Finds the closest city in the database.

    Args:
        lat: Latitude coordinate
        lon: Longitude coordinate

    Returns:
        Zip code of the nearest city
    """
    return _get_zipcode_by_coords(lat, lon)


def _get_zipcode_by_city_state(city: str, state: str) -> str:
    """Core implementation for getting zipcode by city and state"""
    # Normalize inputs for comparison
    city_normalized = city.strip().lower()
    state_normalized = state.strip().upper()

    for city_data in GEO_DATA:
        if (city_data["city"].lower() == city_normalized and
            city_data["state"].upper() == state_normalized):
            return f"Zip code for {city_data['city']}, {city_data['state']}: {city_data['zipcode']}"

    return f"Error: City '{city}' in state '{state}' not found in database"


@mcp.tool()
def get_zipcode_by_city_state(city: str, state: str) -> str:
    """
    Return zip code for a given city and state.

    Args:
        city: City name (e.g., "Austin")
        state: State abbreviation (e.g., "TX")

    Returns:
        Zip code for the specified city and state
    """
    return _get_zipcode_by_city_state(city, state)


def _get_temperature_by_zipcode(zipcode: str) -> str:
    """Core implementation for getting temperature by zipcode"""
    # Find the city data for this zip code
    city_data = None
    for data in GEO_DATA:
        if data["zipcode"] == zipcode:
            city_data = data
            break

    if not city_data:
        return f"Error: Zip code '{zipcode}' not found in database"

    try:
        # Use Open-Meteo API (no API key required)
        url = f"https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": city_data["lat"],
            "longitude": city_data["lon"],
            "current_weather": "true",
            "temperature_unit": "fahrenheit"
        }

        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()

        data = response.json()
        current_weather = data.get("current_weather", {})
        temperature = current_weather.get("temperature")

        if temperature is not None:
            return (f"Current temperature in {city_data['city']}, {city_data['state']} "
                   f"(Zip: {zipcode}): {temperature}°F")
        else:
            return "Error: Temperature data not available"

    except requests.exceptions.RequestException as e:
        return f"Error fetching weather data: {str(e)}"
    except Exception as e:
        return f"Error: {str(e)}"


@mcp.tool()
def get_temperature_by_zipcode(zipcode: str) -> str:
    """
    Get current temperature in Fahrenheit for a given zip code.
    Uses the Open-Meteo API with coordinates from our database.

    Args:
        zipcode: Zip code (e.g., "78701")

    Returns:
        Current temperature in Fahrenheit
    """
    return _get_temperature_by_zipcode(zipcode)


if __name__ == "__main__":
    # Run the MCP server in HTTP mode
    mcp.run(transport="sse")
