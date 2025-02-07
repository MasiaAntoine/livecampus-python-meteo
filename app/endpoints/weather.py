from fastapi import APIRouter, HTTPException, Query, Depends
from sqlalchemy.orm import Session
from app.services.open_meteo_api import OpenMeteoAPI
from app.services.nominatim_api import NominatimAPI
from app.controllers import user_history as crud_user_history
from app.schemas.user_history import UserHistoryCreate
from app.database import config as database

router = APIRouter()

def get_db():
    """
    Génère une session de base de données pour chaque requête.
    """
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/weather")
def get_weather(city: str, user_id: int, hourly: str = Query(None), daily: str = Query(None), timezone: str = "auto", db: Session = Depends(get_db)):
    try:
        with NominatimAPI() as geo_api:
            coordinates = geo_api.get_coordinates(city)
        with OpenMeteoAPI() as weather_api:
            weather_data = weather_api.get_weather(latitude=coordinates["latitude"], longitude=coordinates["longitude"], hourly=hourly, daily=daily, timezone=timezone)
        
        # Sauvegarder l'historique de la recherche
        user_history = UserHistoryCreate(
            city=city,
            latitude=coordinates["latitude"],
            longitude=coordinates["longitude"],
            temperature=weather_data.get("current_weather", {}).get("temperature", 0.0)
        )
        crud_user_history.create_user_history(db=db, user_history=user_history, user_id=user_id)
        
        return weather_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/current_weather")
def get_current_weather(city: str, user_id: int, timezone: str = "auto", db: Session = Depends(get_db)):
    try:
        with NominatimAPI() as geo_api:
            coordinates = geo_api.get_coordinates(city)
        with OpenMeteoAPI() as weather_api:
            current_weather = weather_api.get_current_weather(latitude=coordinates["latitude"], longitude=coordinates["longitude"], timezone=timezone)
        
        # Sauvegarder l'historique de la recherche
        user_history = UserHistoryCreate(
            city=city,
            latitude=coordinates["latitude"],
            longitude=coordinates["longitude"],
            temperature=current_weather.get("temperature", 0.0)
        )
        crud_user_history.create_user_history(db=db, user_history=user_history, user_id=user_id)
        
        return current_weather
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))