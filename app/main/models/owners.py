from dataclasses import dataclass   
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Text, Table, Boolean,types,event, Enum
from datetime import datetime, date
from sqlalchemy.orm import relationship
from .db.base_class import Base
from sqlalchemy.dialects.postgresql import ENUM


class Owner(Base):
    """
     database model for storing Owner related details
    """
    __tablename__ = 'owners'

    uuid = Column(String,primary_key=True,index=True)
    first_name = Column(String,nullable=False)
    last_name = Column(String,nullable=False)
    email = Column(String, nullable=False, unique=True)
    phone_number = Column(String, nullable=False, unique=True)
    address_uuid = Column(String, ForeignKey('addresses.uuid'), nullable=True)
    address = relationship("Address",foreign_keys=[address_uuid])
    password_hash = Column(String, nullable=False)
    is_active = Column(Boolean,default=False)
    is_deleted = Column(Boolean,default=False)


    def __repr__(self):
        return f"Owner(uuid='{self.uuid}', first_name='{self.first_name}'"
    


     