from dataclasses import dataclass   
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Text, Table, Boolean, func,types,event, Enum
from datetime import datetime, date
from sqlalchemy.orm import relationship
from .db.base_class import Base
from sqlalchemy.dialects.postgresql import ENUM

class Feature(Base):
    __tablename__ = "features"

    uuid = Column(String, primary_key=True)
    name = Column(String(100), nullable=False)  # Nom de la fonctionnalité
    description = Column(String, nullable=True)  # Description de la fonctionnalité
    type_abonnement_uuid = Column(String, ForeignKey("types_abonnement.uuid"), nullable=False)  # Type d'abonnement auquel cette fonctionnalité appartient
    type_abonnement = relationship("TypeAbonnement",foreign_keys=[type_abonnement_uuid])
    added_by_uuid: str = Column(String, ForeignKey('users.uuid'), nullable=True)
    added_by = relationship("User", foreign_keys=[added_by_uuid], uselist=False)
    is_active = Column(Boolean, default=True)  # Est-ce que la fonctionnalité est active
    is_deleted = Column(Boolean, default=True)  # Est-ce que la fonctionnalité est active
    date_added = Column(DateTime, server_default=func.now())  
    date_modified = Column(DateTime, server_default=func.now(), onupdate=func.now())  

