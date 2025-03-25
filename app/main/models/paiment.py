from dataclasses import dataclass   
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Text, Table, Boolean, types, event, Enum
from datetime import datetime, date
from sqlalchemy.orm import relationship
from .db.base_class import Base
from sqlalchemy.dialects.postgresql import ENUM
from enum import Enum
from sqlalchemy import Float

class PaymentStatus(str, Enum.Enum):
    PENDING = "PENDING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"

@dataclass
class Payment(Base):
    __tablename__ = "payments"

    id: int = Column(Integer, primary_key=True, index=True)
    uuid: str = Column(String, unique=True, index=True, nullable=False)
    amount: float = Column(Float, nullable=False)
    currency: str = Column(String, nullable=False)
    status: PaymentStatus = Column(ENUM(PaymentStatus), default=PaymentStatus.PENDING, nullable=False)
    created_at: datetime = Column(DateTime, default=datetime.utcnow)