from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_user(db: Session, user: UserCreate):
    """
    Crée un nouvel utilisateur dans la base de données.

    Args:
        db (Session): Session de base de données.
        user (UserCreate): Schéma de création d'utilisateur.

    Returns:
        User: L'utilisateur créé.
    """
    hashed_password = pwd_context.hash(user.password)
    db_user = User(
        username=user.username,
        email=user.email,
        password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user(db: Session, user_id: int):
    """
    Récupère un utilisateur par son identifiant.

    Args:
        db (Session): Session de base de données.
        user_id (int): Identifiant de l'utilisateur.

    Returns:
        User: L'utilisateur correspondant à l'identifiant.
    """
    return db.query(User).filter(User.id == user_id).first()

def get_user_by_username(db: Session, username: str):
    """
    Récupère un utilisateur par son nom d'utilisateur.

    Args:
        db (Session): Session de base de données.
        username (str): Nom d'utilisateur.

    Returns:
        User: L'utilisateur correspondant au nom d'utilisateur.
    """
    return db.query(User).filter(User.username == username).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    """
    Récupère une liste d'utilisateurs avec pagination.

    Args:
        db (Session): Session de base de données.
        skip (int): Nombre d'utilisateurs à ignorer.
        limit (int): Nombre maximum d'utilisateurs à retourner.

    Returns:
        List[User]: Liste des utilisateurs.
    """
    return db.query(User).offset(skip).limit(limit).all()

def update_user(db: Session, user_id: int, user: UserUpdate):
    """
    Met à jour un utilisateur existant.

    Args:
        db (Session): Session de base de données.
        user_id (int): Identifiant de l'utilisateur.
        user (UserUpdate): Schéma de mise à jour de l'utilisateur.

    Returns:
        User: L'utilisateur mis à jour.
    """
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user:
        user_data = user.model_dump(exclude_unset=True)
        for key, value in user_data.items():
            setattr(db_user, key, value)
        db.commit()
        db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: int):
    """
    Supprime un utilisateur par son identifiant.

    Args:
        db (Session): Session de base de données.
        user_id (int): Identifiant de l'utilisateur.

    Returns:
        User: L'utilisateur supprimé.
    """
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user:
        db.delete(db_user)
        db.commit()
    return db_user