from dataclasses import dataclass
from sqlalchemy.sql import func
from datetime import datetime
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql.json import JSONB
from sqlalchemy import Column, ForeignKey, Integer, String, Text, DateTime
from sqlalchemy import event
from app.main.models.db.base_class import Base
from enum import Enum

class UserRoles(str, Enum):
    ADMIN = "admin"
    SUPER_ADMIN = "super_admin"

class UserStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    DELETED = "deleted"
    BLOCKED = "blocked"

class User(Base):
    __tablename__ = "users"

    uuid = Column(String, primary_key=True, unique=True)
    email = Column(String, unique=True, index=True,nulable=False)
    phone_number = Column(String, unique=True, index=True, nullable=False)
    fist_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    password_has = Column(String, nullable=False)
    role = Column(String, nullable=False, default=UserRoles.ADMIN)
    status = Column(String, nullable=False, default=UserStatus.ACTIVE)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())


    def __repr__(self):
        return f"User(uuid={self.uuid}, email={self.email}, phone_number={self.phone_number}, first_name={self.first_name}, last_name={self.last_name}, role={self.role}, status={self.status})"



    