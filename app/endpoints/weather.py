from fastapi import APIRouter, HTTPException, Query
from app.services.open_meteo_api import OpenMeteoAPI

router = APIRouter()

@router.get("/weather")
def get_weather(latitude: float, longitude: float, hourly: str = Query(None), daily: str = Query(None), timezone: str = "auto"):
    try:
        with OpenMeteoAPI() as api:
            weather_data = api.get_weather(latitude=latitude, longitude=longitude, hourly=hourly, daily=daily, timezone=timezone)
            return weather_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/current_weather")
def get_current_weather(latitude: float, longitude: float, timezone: str = "auto"):
    try:
        with OpenMeteoAPI() as api:
            current_weather = api.get_current_weather(latitude=latitude, longitude=longitude, timezone=timezone)
            return current_weather
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))