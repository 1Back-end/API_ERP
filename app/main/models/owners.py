from dataclasses import dataclass
from sqlalchemy.sql import func
from datetime import datetime
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql.json import JSONB
from sqlalchemy import Column, ForeignKey, Integer, String, Text, DateTime
from sqlalchemy import event
from app.main.models.db.base_class import Base
from enum import Enum


class Owner(Base):
     __tablename__ = "owners"

     uuid = Column(String, primary_key=True, unique=True)
     first_name = Column(String, nullable=True)
     last_name = Column(String, nullable=True)
     email = Column(String, unique=True, index=True, nullable=False)
     phone_number = Column(String, unique=True, index=True, nullable=False)
     address = Column(String, nullable=True)
     city = Column(String, nullable=True)