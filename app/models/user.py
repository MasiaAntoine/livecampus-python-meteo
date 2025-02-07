from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class User(Base):
    """
    Classe User représente un utilisateur dans la base de données.

    Attributs:
        id (int): Identifiant unique de l'utilisateur.
        username (str): Nom d'utilisateur unique.
        email (str): Adresse email unique.
        password (str): Mot de passe de l'utilisateur.
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True)
    email = Column(String(100), unique=True, index=True)
    password = Column(String(100))