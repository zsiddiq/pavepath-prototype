# pavepath/main.py

# A critical first step: Always import the necessary libraries.
# `requests` will be used to make HTTP requests to the Google Maps API.
# `os` will be used to interact with the operating system, specifically to get our API key.
# `dotenv` helps us load environment variables from a .env file securely.
import requests
import os
from dotenv import load_dotenv

# Load environment variables from the .env file.
# This makes sure our API key is not hardcoded in the script.
load_dotenv()

# --- Configuration ---
# Get the Google Maps API key from the environment variables.
# The `os.getenv()` method retrieves the value of the environment variable.
# We'll expect the .env file to contain a line like: GOOGLE_MAPS_API_KEY="your_api_key_here"
API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")

# Define the base URL for the Google Directions API.
# This is the endpoint we will send our requests to.
BASE_URL = "https://maps.googleapis.com/maps/api/directions/json"

# A list of keywords we'll use to search for unpaved roads.
# We'll check the route instructions for these phrases.
UNPAVED_KEYWORDS = ["unpaved", "dirt road", "gravel road", "fire road", "dirt track"]


# --- Core Logic Function ---
def check_for_dirt_roads(route_steps):
    """
    Checks a list of route steps for keywords that might indicate
    the presence of an unpaved road.

    Args:
        route_steps (list): A list of step dictionaries from the Directions API response.

    Returns:
        bool: True if a keyword is found, False otherwise.
    """
    # Iterate through each step in the route.
    for step in route_steps:
        # Get the HTML instructions and convert to lowercase for case-insensitive matching.
        instructions = step["html_instructions"].lower()
        
        # Check if any of our keywords are present in the instructions.
        for keyword in UNPAVED_KEYWORDS:
            if keyword in instructions:
                # If a keyword is found, we can immediately return True.
                return True
                
    # If the loop completes without finding any keywords, no dirt roads were detected.
    return False


# --- Main Function ---
def get_route_and_details(origin, destination):
    """
    Makes a request to the Google Directions API, and checks if the route
    includes any likely dirt roads.

    Args:
        origin (str): The starting point of the journey.
        destination (str): The final destination of the journey.
    """
    # Check if the API key was loaded successfully.
    if not API_KEY:
        print("Error: GOOGLE_MAPS_API_KEY not found. Please set it in your .env file.")
        return

    # Define the parameters for the API request.
    params = {
        "origin": origin,
        "destination": destination,
        "key": API_KEY,
        "alternatives": "true" # Request alternative routes for a future step
    }

    try:
        # Make the GET request to the Directions API.
        response = requests.get(BASE_URL, params=params)

        # Raise an exception for bad status codes.
        response.raise_for_status()

        # Parse the JSON response.
        route_data = response.json()

        if route_data["status"] == "OK":
            # Extract the first route found in the response.
            route = route_data["routes"][0]
            leg = route["legs"][0]

            print(f"Route from {leg['start_address']} to {leg['end_address']}:")
            print(f"Total Distance: {leg['distance']['text']}")
            print(f"Total Duration: {leg['duration']['text']}")
            print("\n")
            print("--- Route Steps ---")
            
            # Check for dirt roads using our new function.
            has_dirt_roads = check_for_dirt_roads(leg["steps"])
            
            # If dirt roads are detected, display an alert.
            if has_dirt_roads:
                print("🚨  ALERT! Your route may include unpaved or dirt roads.  🚨")
                print("---------------------------------------------------------------")
            
            # Iterate through each step and print the instructions.
            for step in leg["steps"]:
                print(f"- {step['html_instructions'].replace('<b>', '').replace('</b>', '')}")

        else:
            # If the status is not "OK", print the API error message.
            print(f"Error: API status is '{route_data['status']}'. Message: {route_data.get('error_message', 'No error message provided.')}")

    except requests.exceptions.RequestException as e:
        print(f"A network error occurred: {e}")
    except KeyError:
        print("Error: Failed to parse the API response. The structure may have changed.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


# --- Example Usage ---
if __name__ == "__main__":
    # Test with a route that likely contains an unpaved road.
    origin_address = "29402 Pacific Coast Hwy, Malibu, CA"
    destination_address = "Mishe Mokwa Trailhead, CA"
    get_route_and_details(origin_address, destination_address)

