from abc import ABC, abstractmethod
import requests


class WeatherAPI(ABC):
    """
    Abstract base class for weather APIs.
    """

    @abstractmethod
    def is_raining_now(self, city: str, country: str) -> bool:
        """
        Check if it is currently raining in the specified city and country.

        Args:
            city (str): The name of the city.
            country (str): The name of the country.

        Returns:
            bool: True if it is currently raining, False otherwise.
        """
        pass


class OpenWeatherAPI(WeatherAPI):
    """
    Implementation of a weather API using OpenWeatherMap.
    """

    def __init__(self, api_key: str):
        """
        Initialize the OpenWeatherAPI with the provided API key.

        Args:
            api_key (str): The API key to access the OpenWeatherAPI.
        """
        self.api_key = api_key

    def _fetch_weather_data(self, city: str, country: str) -> dict:
        """
        Fetch weather data from the OpenWeatherAPI.

        Args:
            city (str): The name of the city.
            country (str): The name of the country.

        Returns:
            dict: Weather data JSON response.
        """

        api_url = f"https://api.openweathermap.org/data/2.5/weather?q={city},{country}&appid={self.api_key}"
        response = requests.get(api_url)
        response.raise_for_status()

        return response.json()

    def is_raining_now(self, city: str, country: str) -> bool:
        """
        Check if it is currently raining in the specified city and country using OpenWeatherAPI.

        Args:
            city (str): The name of the city.
            country (str): The name of the country.

        Returns:
            bool: True if it is currently raining, False otherwise.
        """

        weather_data = self._fetch_weather_data(city, country)
        weather_ids = [str(item.get("id")) for item in weather_data.get("weather", [])]

        # OpenWeatherAPI use codes to indicate the current weather
        # In this case, codes starting with 5xx means it is raining
        # For more information: https://openweathermap.org/weather-conditions
        return any(weather_id.startswith("5") for weather_id in weather_ids)
