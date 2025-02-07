from sqlalchemy.orm import Session
from app.models.user_history import UserHistory
from app.schemas.user_history import UserHistoryCreate

def create_user_history(db: Session, user_history: UserHistoryCreate, user_id: int):
    """
    Crée une nouvelle recherche météo dans la base de données.

    Args:
        db (Session): Session de base de données.
        user_history (UserHistoryCreate): Schéma de création de recherche météo.
        user_id (int): Identifiant de l'utilisateur ayant effectué la recherche.

    Returns:
        UserHistory: La recherche météo créée.
    """
    db_user_history = UserHistory(
        user_id=user_id,
        city=user_history.city,
        latitude=user_history.latitude,
        longitude=user_history.longitude,
        temperature=user_history.temperature
    )
    db.add(db_user_history)
    db.commit()
    db.refresh(db_user_history)
    return db_user_history

def get_user_histories_by_user(db: Session, user_id: int):
    """
    Récupère les recherches météo effectuées par un utilisateur.

    Args:
        db (Session): Session de base de données.
        user_id (int): Identifiant de l'utilisateur.

    Returns:
        List[UserHistory]: Liste des recherches météo de l'utilisateur.
    """
    return db.query(UserHistory).filter(UserHistory.user_id == user_id).all()
