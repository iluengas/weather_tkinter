import requests
import time
from scripts.config import API_KEY
from scripts.valid_cities import add_valid_city


class CityNotFoundError(Exception):
    pass


# Create a dictionary to store cached weather data
weather_cache = {}

# Define the expiration time for the cached weather data (in seconds)
CACHE_EXPIRATION_TIME = 3600  # 1 hour


def make_weather_api_request(city_name):
    """
    Makes a request to the weather API and returns the response data.

    Args:
        city_name (str): Name of the city to fetch weather data for.

    Returns:
        requests.Response: Response object containing the weather data.
    """

    url = f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&units=imperial&APPID={API_KEY}"
    response = requests.get(url)
    return response


def handle_weather_response(response, city_name):
    """
    Checks for exceptions in response and returns weather data

    Args:
    response (response): The response object
    city_name (str): The name of the city

    Returns:
    weather, description, temp, humidity, pressure, wind_speed, timezone

    """
    try:
        response.raise_for_status()
        weather_json = response.json()

        if weather_json['cod'] == '404':
            raise CityNotFoundError(f"City weather not found: {city_name}")

        weather = weather_json['weather'][0]['main']
        description = weather_json['weather'][0]['description']
        temp = round(weather_json['main']['temp'])
        humidity = weather_json['main']['humidity']
        pressure = weather_json['main']['pressure']
        wind_speed = weather_json['wind']['speed']
        timezone = weather_json['timezone']  # Get the timezone information

        return weather, description, temp, humidity, pressure, wind_speed, timezone

    except requests.exceptions.RequestException as e:
        print(f"An error occurred while fetching weather data: {e}")

    except CityNotFoundError as e:
        print(e)

    return None


def is_weather_data_expired(city_name):
    """
    Checks if the weather data for a city in the cache has expired.

    Args:
        city_name (str): Name of the city.

    Returns:
        bool: True if the weather data has expired, False otherwise.
    """
    if city_name in weather_cache:
        cached_time = weather_cache[city_name]['time']
        current_time = time.time()
        return (current_time - cached_time) > CACHE_EXPIRATION_TIME
    return True


def get_weather(city_name):
    """
    Returns the weather and temperature for a given city.

    - Makes an API request to retrieve weather data if not available in the cache or expired.
    - Handles the API response.
    - Adds the valid city to the list of valid cities.
    - Implements caching to avoid unnecessary API calls.

    Args:
        city_name (str): Name of the city.

    Returns:
        dict: A dictionary containing the weather and temperature information, or an empty dictionary if data retrieval fails.
    """
    # Convert city_name to lowercase for case-insensitive matching
    city_name = city_name.lower()
    # Check if weather data for the city is already cached and not expired
    if not is_weather_data_expired(city_name) and city_name in weather_cache:
        return {
            'weather': weather_cache[city_name]['weather'],
            'description': weather_cache[city_name]['description'],
            'temperature': weather_cache[city_name]['temperature'],
            'humidity': weather_cache[city_name]['humidity'],
            'pressure': weather_cache[city_name]['pressure'],
            'wind_speed': weather_cache[city_name]['wind_speed'],
            # Add the timezone to the returned data
            'timezone': weather_cache[city_name]['timezone']
        }

    response = make_weather_api_request(city_name)
    result = handle_weather_response(response, city_name)

    if result is not None:
        weather, description, temp, humidity, pressure, wind_speed, timezone = result
        add_valid_city(city_name)

        # Cache the weather data with current timestamp
        weather_cache[city_name] = {
            'weather': weather,
            'description': description,
            'temperature': temp,
            'humidity': humidity,
            'pressure': pressure,
            'wind_speed': wind_speed,
            'timezone': timezone,  # Save the timezone in the cache
            'time': time.time()
        }

        return {
            'weather': weather,
            'description': description,
            'temperature': temp,
            'humidity': humidity,
            'pressure': pressure,
            'wind_speed': wind_speed,
            'timezone': timezone  # Include the timezone in the returned data
        }

    return {}
