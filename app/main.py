from fastapi import FastAPI
from app.database import engine
from app.models import user as models
from app.endpoints import user as user_endpoints

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(user_endpoints.router)

def main():
    print("Hello, world!")

if __name__ == "__main__":
    main()