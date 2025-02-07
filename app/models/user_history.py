from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class UserHistory(Base):
    """
    Classe UserHistory représente une recherche météo effectuée par un utilisateur.

    Attributs:
        id (int): Identifiant unique de la recherche.
        user_id (int): Identifiant de l'utilisateur ayant effectué la recherche.
        city (str): Nom de la ville recherchée.
        latitude (float): Latitude de la ville recherchée.
        longitude (float): Longitude de la ville recherchée.
        temperature (float): Température lors de la recherche.
        search_date (datetime): Date et heure de la recherche.
    """
    __tablename__ = "user_histories"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    city = Column(String(100), nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    temperature = Column(Float, nullable=False)
    search_date = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="user_histories")
