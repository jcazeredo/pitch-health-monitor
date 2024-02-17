from abc import ABC, abstractmethod
import requests

class WeatherAPI(ABC):   
    @abstractmethod
    def is_raining_now(self, lat: float, lon: float) -> bool:
        pass

class OpenWeatherAPI(WeatherAPI):
    def __init__(self, api_key: str):
        self.api_key = api_key
    
    def _fetch_weather_data(self, lat: float, lon: float) -> dict:
        api_url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={self.api_key}"
        response = requests.get(api_url)
        response.raise_for_status()
        return response.json()
    
    def is_raining_now(self, lat: float, lon: float) -> bool:
        weather_data = self._fetch_weather_data(lat, lon)
        weather_ids = [str(item.get("id")) for item in weather_data.get("weather", [])]
        return any(weather_id.startswith("5") for weather_id in weather_ids)
