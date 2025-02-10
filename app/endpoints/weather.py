from fastapi import APIRouter, HTTPException, Query, Depends, Request
from sqlalchemy.orm import Session
from app.services.open_meteo_api import OpenMeteoAPI
from app.services.nominatim_api import NominatimAPI
from app.controllers import user_history as crud_user_history
from app.schemas.user_history import UserHistoryCreate
from app.database import config as database
from app.controllers import user as crud_user
from typing import Optional

router = APIRouter()

WEATHER_CODES = {
    0: "un ciel parfaitement dégagé",
    1: "un ciel majoritairement dégagé",
    2: "quelques nuages dans le ciel",
    3: "un ciel entièrement couvert",
    45: "du brouillard",
    48: "du brouillard givrant",
    51: "une légère bruine",
    53: "de la bruine modérée",
    55: "une forte bruine",
    56: "de la bruine verglaçante légère",
    57: "de la bruine verglaçante dense",
    61: "une légère pluie",
    63: "de la pluie modérée",
    65: "de fortes précipitations",
    66: "de la pluie verglaçante légère",
    67: "de la pluie verglaçante forte",
    71: "de légères chutes de neige",
    73: "des chutes de neige modérées",
    75: "d'importantes chutes de neige",
    77: "des grains de neige",
    80: "de légères averses",
    81: "des averses modérées",
    82: "de violentes averses",
    85: "de légères averses de neige",
    86: "de fortes averses de neige",
    95: "un orage",
    96: "un orage avec légère grêle",
    99: "un orage violent avec forte grêle"
}

def get_db():
    """
    Génère une session de base de données pour chaque requête.
    """
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

def format_temperature(temp: float) -> str:
    """
    Formate la température pour l'affichage.
    """
    return f"{temp:.1f}°C"

def get_weather_description(weather_code: int) -> str:
    """
    Retourne la description en français du code météo.
    """
    return WEATHER_CODES.get(weather_code, "des conditions météorologiques particulières")

def get_user_from_auth(request: Request, db: Session) -> tuple[Optional[int], bool]:
    """
    Récupère l'utilisateur à partir du token d'authentification.
    Retourne (user_id, should_be_logged)
    """
    authorization = request.headers.get("Authorization")
    if not authorization:
        return None, False

    try:
        token = authorization.split(" ")[1]
        user = crud_user.get_user_by_token(db, token)
        return user.id, True
    except (IndexError, AttributeError):
        return None, False

def format_daily_message(weather_data: dict, city: str) -> str:
    """
    Formate un message détaillé pour les prévisions météorologiques.
    Utilise les données horaires et journalières pour créer un message complet.
    """
    # Récupération des données horaires
    hourly = weather_data.get("hourly", {})
    hourly_temps = hourly.get("temperature_2m", [])
    current_hour_index = 0  # Première heure disponible

    # Températures actuelles et prochaines heures
    current_temp = format_temperature(hourly_temps[current_hour_index])
    next_hours_temps = hourly_temps[current_hour_index:current_hour_index + 6]  # Prochaines 6 heures
    min_next_hours = format_temperature(min(next_hours_temps))
    max_next_hours = format_temperature(max(next_hours_temps))

    # Données journalières
    daily = weather_data.get("daily", {})
    daily_max_temps = daily.get("temperature_2m_max", [])
    today_max = format_temperature(daily_max_temps[0]) if daily_max_temps else "N/A"

    # Construction du message
    message = f"À {city}, il fait actuellement {current_temp}"

    # Ajout de la tendance pour les prochaines heures
    if min_next_hours != max_next_hours:
        message += f". Dans les 6 prochaines heures, les températures oscilleront entre {min_next_hours} et {max_next_hours}"
    else:
        message += f". La température restera stable autour de {min_next_hours} pour les prochaines heures"

    # Ajout du maximum journalier
    message += f". Le maximum attendu aujourd'hui est de {today_max}"

    # Ajout des prévisions pour les prochains jours si disponibles
    if len(daily_max_temps) > 1:
        tomorrow_max = format_temperature(daily_max_temps[1])
        message += f". Demain, la température maximale sera de {tomorrow_max}"

    return message

@router.get("/weather")
def get_weather(
        request: Request,
        city: str,
        db: Session = Depends(get_db),
        hourly: str = Query("temperature_2m"),  # Par défaut, on demande au moins la température
        daily: str = Query("temperature_2m_max"),  # Par défaut, on demande au moins le maximum
        timezone: str = "auto"
):
    try:
        user_id, should_be_logged = get_user_from_auth(request, db)

        with NominatimAPI() as geo_api:
            coordinates = geo_api.get_coordinates(city)

        with OpenMeteoAPI() as weather_api:
            weather_data = weather_api.get_weather(
                latitude=coordinates["latitude"],
                longitude=coordinates["longitude"],
                hourly=hourly,
                daily=daily,
                timezone=timezone
            )

        if should_be_logged:
            # Utiliser la première température horaire comme température actuelle
            current_temp = weather_data.get("hourly", {}).get("temperature_2m", [0.0])[0]
            user_history = UserHistoryCreate(
                city=city,
                latitude=coordinates["latitude"],
                longitude=coordinates["longitude"],
                temperature=current_temp
            )
            crud_user_history.create_user_history(db=db, user_history=user_history, user_id=user_id)

        return {
            "message": format_daily_message(weather_data, city),
            "data": weather_data
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/current_weather")
def get_current_weather(
        request: Request,
        city: str,
        db: Session = Depends(get_db),
        timezone: str = "auto"
):
    try:
        user_id, should_be_logged = get_user_from_auth(request, db)

        with NominatimAPI() as geo_api:
            coordinates = geo_api.get_coordinates(city)

        with OpenMeteoAPI() as weather_api:
            current_weather = weather_api.get_current_weather(
                latitude=coordinates["latitude"],
                longitude=coordinates["longitude"],
                timezone=timezone
            )

        temp = format_temperature(current_weather.get("temperature", 0.0))
        weather_desc = get_weather_description(current_weather.get("weathercode", -1))

        if should_be_logged:
            user_history = UserHistoryCreate(
                city=city,
                latitude=coordinates["latitude"],
                longitude=coordinates["longitude"],
                temperature=current_weather.get("temperature", 0.0)
            )
            crud_user_history.create_user_history(db=db, user_history=user_history, user_id=user_id)

        return {
            "message": f"À {city}, il fait actuellement {temp} avec {weather_desc}.",
            "data": current_weather
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))