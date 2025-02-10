from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import timedelta
from app.database import config as database
from app.schemas import user as schemas
from app.controllers import user as crud
from app.utils import create_access_token

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_db():
    """
    Génère une session de base de données pour chaque requête.
    """
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """
    Crée un nouvel utilisateur.

    Args:
        user (UserCreate): Schéma de création d'utilisateur.
        db (Session): Session de base de données.

    Returns:
        User: L'utilisateur créé.
    """
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return crud.create_user(db=db, user=user)

@router.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    """
    Récupère un utilisateur par son identifiant.

    Args:
        user_id (int): Identifiant de l'utilisateur.
        db (Session): Session de base de données.

    Returns:
        User: L'utilisateur correspondant à l'identifiant.
    """
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.get("/users/", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """
    Récupère une liste d'utilisateurs avec pagination.

    Args:
        skip (int): Nombre d'utilisateurs à ignorer.
        limit (int): Nombre maximum d'utilisateurs à retourner.
        db (Session): Session de base de données.

    Returns:
        List[User]: Liste des utilisateurs.
    """
    users = crud.get_users(db, skip=skip, limit=limit)
    return users

@router.put("/users/{user_id}", response_model=schemas.User)
def update_user(user_id: int, user: schemas.UserUpdate, db: Session = Depends(get_db)):
    """
    Met à jour un utilisateur existant.

    Args:
        user_id (int): Identifiant de l'utilisateur.
        user (UserUpdate): Schéma de mise à jour de l'utilisateur.
        db (Session): Session de base de données.

    Returns:
        User: L'utilisateur mis à jour.
    """
    db_user = crud.update_user(db, user_id=user_id, user=user)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.delete("/users/{user_id}", response_model=schemas.User)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    """
    Supprime un utilisateur par son identifiant.

    Args:
        user_id (int): Identifiant de l'utilisateur.
        db (Session): Session de base de données.

    Returns:
        User: L'utilisateur supprimé.
    """
    db_user = crud.delete_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.post("/token", response_model=schemas.Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    Connexion de l'utilisateur et génération du token.

    Args:
        form_data (OAuth2PasswordRequestForm): Formulaire de connexion.
        db (Session): Session de base de données.

    Returns:
        Token: Le token d'accès.
    """
    user = crud.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=400,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    # save token in database
    crud.save_user_token(db, user.id, access_token)
    return {"access_token": access_token, "token_type": "bearer"}