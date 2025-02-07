import os
from typing import Dict, Optional, Union

import requests

class OpenMeteoAPI:
    BASE_URL = os.getenv("OPEN_METEO_BASE_URL")

    def __init__(self):
        self.session = requests.Session()

    def get_weather(self,
                    latitude: float,
                    longitude: float,
                    hourly: Optional[str] = None,
                    daily: Optional[str] = None,
                    timezone: str = "auto") -> Dict[str, Union[str, float, dict]]:

        params = {
            "latitude": latitude,
            "longitude": longitude,
            "timezone": timezone
        }

        if hourly:
            params["hourly"] = hourly
        if daily:
            params["daily"] = daily

        try:
            response = self.session.get(f"{self.BASE_URL}/forecast", params=params)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            raise requests.RequestException(f"Failed to fetch weather data: {str(e)}")

    def get_current_weather(self,
                            latitude: float,
                            longitude: float,
                            timezone: str = "auto") -> Dict[str, Union[str, float]]:

        params = {
            "latitude": latitude,
            "longitude": longitude,
            "timezone": timezone,
            "current_weather": True
        }

        try:
            response = self.session.get(f"{self.BASE_URL}/forecast", params=params)
            response.raise_for_status()
            return response.json().get("current_weather", {})
        except requests.RequestException as e:
            raise requests.RequestException(f"Failed to fetch current weather: {str(e)}")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.session.close()