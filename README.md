# LiveCampus Python Météo 🌦️

Cette application tourne sous Docker et est composée de deux conteneurs : un pour l'API et un autre pour l'application Python. L'application permet de récupérer la météo en utilisant l'API.

## URLs des APIs 🌐
- `OPEN_METEO_BASE_URL`: https://api.open-meteo.com/v1
- `NOMINATIM_BASE_URL`: https://nominatim.openstreetmap.org/search

## Fonctionnalités ✨
- Système de compte utilisateur 👤
- Historique des données météorologiques 📈

## Installation 🛠️

1. Créez un fichier `.env` à la racine du projet et ajoutez les variables d'environnement nécessaires comme exemple avec le .envexemple

2. Construisez et démarrez les conteneurs Docker :
    ```bash
    docker-compose up --build
    ```

## Utilisation 🚀

Une fois les conteneurs démarrés, vous pouvez accéder à l'application via l'URL fournie par Docker. Utilisez l'API pour récupérer les données météorologiques et gérer les comptes utilisateurs ainsi que l'historique des données.

## Configuration Postman 📬

Un fichier de configuration Postman (`postman-config.json`) est fourni pour vous permettre d'importer directement toutes les routes de l'API dans Postman. Cela facilite les tests et l'exploration des différentes fonctionnalités de l'API.

## Dépendances 📦

Voici la liste des dépendances utilisées dans ce projet :
- `fastapi==0.109.2`
- `uvicorn==0.27.1`
- `requests==2.32.0`
- `python-dotenv==1.0.1`
- `mysqlclient==2.2.1`
- `sqlalchemy==2.0.25`
- `pydantic==2.6.1`
- `pymysql==1.1.1`
- `pydantic[email]>=2.0.0`
- `passlib[bcrypt]>=1.7.4`
- `pytest==8.3.4`
- `httpx==0.28.1`
- `pytest-asyncio==0.25.3`