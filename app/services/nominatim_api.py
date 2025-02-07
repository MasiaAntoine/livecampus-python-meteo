import os

import requests

class NominatimAPI:
    BASE_URL = os.getenv("NOMINATIM_BASE_URL")

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": "MeteoPython/1.0"})

    def get_coordinates(self, city_name: str):
        params = {
            "q": city_name,
            "format": "json",
            "limit": 1
        }

        try:
            response = self.session.get(self.BASE_URL, params=params)
            response.raise_for_status()
            data = response.json()
            if data:
                location = data[0]
                return {"latitude": float(location["lat"]), "longitude": float(location["lon"])}
            else:
                raise ValueError("City not found")
        except requests.RequestException as e:
            raise requests.RequestException(f"Failed to fetch coordinates: {str(e)}")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.session.close()