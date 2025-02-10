from dataclasses import dataclass
from xmlrpc.client import Boolean
from sqlalchemy.sql import func
from datetime import datetime
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql.json import JSONB
from sqlalchemy import Column, ForeignKey, Integer, String, Text, DateTime
from sqlalchemy import event
from app.main.models.db.base_class import Base
from enum import Enum
from sqlalchemy.orm import relationship


class Owner(Base):
     __tablename__ = "owners"

     uuid = Column(String, primary_key=True, unique=True)
     first_name = Column(String, nullable=True)
     last_name = Column(String, nullable=True)
     email = Column(String, unique=True, index=True, nullable=False)
     phone_number = Column(String, unique=True, index=True, nullable=False)
     adress_uuid = Column(String, ForeignKey("addresses.uuid"), nullable=False)
     address = relationship("Address",foreign_keys=[adress_uuid])
     password_has = Column(String, nullable=False)
     is_active = Column(Boolean, default=False)
     is_deleted = Column(Boolean, default=False)
     created_at = Column(DateTime, server_default=func.now())
     updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

     def __repr__(self):
        return f"Owner(uuid={self.uuid}, first_name={self.first_name}, last_name={self.last_name}, email={self.email}, phone_number={self.phone_number}, address={self.address}, password_has={self.password_has}, is_active={self.is_active}, is_deleted={self.is_deleted})"
        