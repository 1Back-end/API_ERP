# from dataclasses import dataclass   
# from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Text, Table, Boolean, func, types, event, Enum
# from datetime import datetime, date, timedelta
# from sqlalchemy.orm import relationship
# from .db.base_class import Base
# from sqlalchemy.dialects.postgresql import ENUM
# from enum import Enum
# from sqlalchemy import Float


# class Renouvellement(Base):
#     __tablename__ = "renouvellements"

# uuid= Column(Integer, primary_key=True, index=True)
# company_id = Column(Integer, ForeignKey("company.id"), nullable=False)
# start_date = Column(DateTime, default=datetime.utcnow)
# end_date = Column(DateTime, default=lambda: datetime.utcnow() + timedelta(days=365))


# added_by_uuid: str = Column(String, ForeignKey('users.uuid'), nullable=True)
# added_by = relationship("User", foreign_keys=[added_by_uuid], uselist=False)
# is_deleted = Column(Boolean, default=False)  # Est-ce que la fonctionnalité est active
# date_added = Column(DateTime, server_default=func.now())  
# date_modified = Column(DateTime, server_default=func.now(), onupdate=func.now())  

# company = relationship("Company", back_populates="renouvellements")
