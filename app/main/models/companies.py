from dataclasses import dataclass
from sqlalchemy.sql import func
from datetime import datetime
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql.json import JSONB
from sqlalchemy import Column, ForeignKey, Integer, String, Text, DateTime
from sqlalchemy import event
from app.main.models.db.base_class import Base
from enum import Enum

class CompanyStatus(str,Enum):
    ACTIVE = "ACTIVE",
    INACTIVE = "INACTIVE",
    CLOSED = "CLOSED"

class CompanyType(str,Enum):
    PERSONNAL = "PERSONNAL",
    SARL = "SARL"
    SA = "SA"
    SAS = "SAS"
    ONG = "ONG"

class Company(Base):
    __tablename__ = "companies"

    uuid = Column(String, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, index=True, unique=True)
    phone = Column(String, index=True, unique=True)
    adress_uuid = Column(String, ForeignKey("addresses.uuid"), nullable=False)
    address = relationship("Address",foreign_keys=[adress_uuid])
    description = Column(Text, nullable=True)
    slogan = Column(String, nullable=True)

    logo_uuid = Column(String, ForeignKey("storages.uuid"), nullable=True)
    logo = relationship("Storage",foreign_keys=[logo_uuid])

    signature_uuid = Column(String, ForeignKey("storages.uuid"), nullable=True)
    signature = relationship("Storage",foreign_keys=[signature_uuid])

    stamp_uuid = Column(String, ForeignKey("storages.uuid"), nullable=True)
    stamp = relationship("Storage",foreign_keys=[stamp_uuid])

    founded = Column(DateTime, nullable=True,default=datetime.now())
    employees_count = Column(Integer, nullable=True)
    type = Column(String, nullable=True,default=CompanyType.PERSONNAL)
    status = Column(String, nullable=True,default=CompanyStatus.INACTIVE)
    added_by = Column(String, ForeignKey("owners.uuid"), nullable=False)
    owner = relationship("Owner",foreign_keys=[added_by])
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())


    def __repr__(self):
        return f"Company(uuid={self.uuid}, name={self.name}"

