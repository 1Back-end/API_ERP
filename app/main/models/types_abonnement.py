from dataclasses import dataclass   
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Text, Table, Boolean, func,types,event, Enum
from datetime import datetime, date
from sqlalchemy.orm import relationship
from .db.base_class import Base
from sqlalchemy.dialects.postgresql import ENUM


class TypeAbonnement(Base):
    __tablename__ = "types_abonnement"

    uuid = Column(String, primary_key=True, index=True)  
    name = Column(String, nullable=False, unique=True)  # Nom de l'abonnement
    price = Column(Integer, nullable=False)  # Prix en FCFA
    added_by_uuid: str = Column(String, ForeignKey('users.uuid'), nullable=True)
    added_by = relationship("User", foreign_keys=[added_by_uuid], uselist=False)
    is_deleted = Column(Boolean, default=False)  # Est-ce que la fonctionnalité est active
    date_added = Column(DateTime, server_default=func.now())  
    date_modified = Column(DateTime, server_default=func.now(), onupdate=func.now())  
    # Relation avec Feature
    features = relationship("Feature", back_populates="type_abonnement", cascade="all, delete-orphan")