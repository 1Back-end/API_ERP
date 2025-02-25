from sqlalchemy import Column, ForeignKey, Integer, DateTime, func,String
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid
from .db.base_class import Base

class Abonnement(Base):
    __tablename__ = "abonnements"

    uuid = Column(String, primary_key=True, index=True)
    start_date = Column(DateTime, default=func.now(), nullable=False)  # Date de début
    end_date = Column(DateTime, nullable=False)  # Date de fin
    date_added = Column(DateTime, server_default=func.now())  # Date d'ajout
    company_uuid = Column(String,ForeignKey('companies.uuid'), nullable=False)
    company = relationship("Company",foreign_keys=[company_uuid])
    added_by = Column(String, ForeignKey("owners.uuid"), nullable=False)  # Référence au propriétaire
    owner = relationship("Owner", foreign_keys=[added_by])
    type_abonnement_uuid = Column(String, ForeignKey("types_abonnement.uuid"), nullable=False)  # Type d'abonnement auquel cette fonctionnalité appartient
    type_abonnement = relationship("TypeAbonnement",foreign_keys=[type_abonnement_uuid])

    date_modified = Column(DateTime, server_default=func.now(), onupdate=func.now())  # Date de mise à jour