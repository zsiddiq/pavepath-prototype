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

# --- Main Function ---
def get_route_and_details(origin, destination):
    """
    Makes a request to the Google Directions API to find a route
    between an origin and a destination, and prints basic details.

    Args:
        origin (str): The starting point of the journey.
        destination (str): The final destination of the journey.
    """
    # Check if the API key was loaded successfully.
    if not API_KEY:
        print("Error: GOOGLE_MAPS_API_KEY not found. Please set it in your .env file.")
        return

    # Define the parameters for the API request.
    # We pass the origin, destination, and our API key.
    params = {
        "origin": origin,
        "destination": destination,
        "key": API_KEY
    }

    try:
        # Make the GET request to the Directions API.
        # `requests.get()` sends the request and returns a response object.
        response = requests.get(BASE_URL, params=params)

        # Raise an exception for bad status codes (e.g., 404, 500).
        response.raise_for_status()

        # Parse the JSON response from the API into a Python dictionary.
        route_data = response.json()

        # Check the status of the response. "OK" means the request was successful.
        if route_data["status"] == "OK":
            # Extract the first route found in the response.
            # The API can return multiple routes, but we'll focus on the first one for now.
            route = route_data["routes"][0]
            
            # Extract the first leg of the route.
            # A "leg" is the journey between a starting point and a destination.
            leg = route["legs"][0]

            # Print some of the key information from the route.
            # `leg["distance"]["text"]` provides the total distance in a human-readable format.
            print(f"Route from {leg['start_address']} to {leg['end_address']}:")
            print(f"Total Distance: {leg['distance']['text']}")
            print(f"Total Duration: {leg['duration']['text']}")
            print("\n")
            print("--- Route Steps ---")
            
            # Iterate through each step of the leg and print the driving instructions.
            # The HTML instructions need to be cleaned up for a cleaner display.
            for step in leg["steps"]:
                # The 'html_instructions' often contains HTML tags. We can remove them
                # or just print the raw text for this initial version.
                print(f"- {step['html_instructions'].replace('<b>', '').replace('</b>', '')}")

        else:
            # If the status is not "OK", something went wrong with the API call.
            # Print the error message provided by the API.
            print(f"Error: API status is '{route_data['status']}'. Message: {route_data.get('error_message', 'No error message provided.')}")

    except requests.exceptions.RequestException as e:
        # Catch any errors that occur during the request (e.g., network issues).
        print(f"A network error occurred: {e}")
    except KeyError:
        # Catch errors if the JSON response structure is unexpected.
        print("Error: Failed to parse the API response. The structure may have changed.")
    except Exception as e:
        # Catch any other unexpected errors.
        print(f"An unexpected error occurred: {e}")

# --- Example Usage ---
# Call our function with a sample origin and destination.
# For testing, you can use any valid addresses or place names.
if __name__ == "__main__":
    origin_address = "Golden Gate Bridge, San Francisco, CA"
    destination_address = "Stinson Beach, CA"
    get_route_and_details(origin_address, destination_address)
