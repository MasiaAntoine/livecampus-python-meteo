from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import config as database
from app.schemas import user_history as schemas
from app.controllers import user_history as crud

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

@router.post("/user_histories/", response_model=schemas.UserHistory)
def create_user_history(user_history: schemas.UserHistoryCreate, user_id: int, db: Session = Depends(get_db)):
    """
    Crée une nouvelle recherche météo pour un utilisateur.

    Args:
        user_history (UserHistoryCreate): Schéma de création de recherche météo.
        user_id (int): Identifiant de l'utilisateur.
        db (Session): Session de base de données.

    Returns:
        UserHistory: La recherche météo créée.
    """
    return crud.create_user_history(db=db, user_history=user_history, user_id=user_id)

@router.get("/user_histories/{user_id}", response_model=list[schemas.UserHistory])
def get_user_histories(user_id: int, db: Session = Depends(get_db)):
    """
    Récupère les recherches météo effectuées par un utilisateur.

    Args:
        user_id (int): Identifiant de l'utilisateur.
        db (Session): Session de base de données.

    Returns:
        List[UserHistory]: Liste des recherches météo de l'utilisateur.
    """
    return crud.get_user_histories_by_user(db=db, user_id=user_id)
