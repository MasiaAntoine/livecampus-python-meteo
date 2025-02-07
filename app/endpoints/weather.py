from fastapi import APIRouter, HTTPException, Query
from app.services.open_meteo_api import OpenMeteoAPI
from app.services.nominatim_api import NominatimAPI

router = APIRouter()

@router.get("/weather")
def get_weather(city: str, hourly: str = Query(None), daily: str = Query(None), timezone: str = "auto"):
    try:
        with NominatimAPI() as geo_api:
            coordinates = geo_api.get_coordinates(city)
        with OpenMeteoAPI() as weather_api:
            weather_data = weather_api.get_weather(latitude=coordinates["latitude"], longitude=coordinates["longitude"], hourly=hourly, daily=daily, timezone=timezone)
            return weather_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/current_weather")
def get_current_weather(city: str, timezone: str = "auto"):
    try:
        with NominatimAPI() as geo_api:
            coordinates = geo_api.get_coordinates(city)
        with OpenMeteoAPI() as weather_api:
            current_weather = weather_api.get_current_weather(latitude=coordinates["latitude"], longitude=coordinates["longitude"], timezone=timezone)
            return current_weather
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))