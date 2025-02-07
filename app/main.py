from fastapi import FastAPI
from app.endpoints import user as user_endpoints
from app.endpoints import weather as weather_endpoints
from app.database import config as database
from app.models import user as models

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

app.include_router(user_endpoints.router)
app.include_router(weather_endpoints.router)

def main():
    print("Hello, world!")

if __name__ == "__main__":
    main()