from dataclasses import dataclass   
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Text, Table, Boolean,types,event, Enum
from datetime import datetime, date
from sqlalchemy.orm import relationship
from .db.base_class import Base
from sqlalchemy.dialects.postgresql import ENUM

class Ownerstatus(str,Enum):
    ACTIVED = "ACTIVED"
    UNACTIVED = "UNACTIVED"
    DELETED = "DELETED"
    BLOCKED= "BLOCKED"

class Owner(Base):
    """
     database model for storing Owner related details
    """
    __tablename__ = 'owners'

    uuid: str = Column(String, primary_key=True, unique=True, index=True)

    email: str = Column(String, nullable=False, default="", index=True)
    firstname: str = Column(String, nullable=False, default="")
    lastname: str = Column(String, nullable=False, default="")
    country_code: str = Column(String(5), nullable=False, default="", index=True)
    phone_number: str = Column(String(20), nullable=False, default="", index=True)
    full_phone_number: str = Column(String(25), nullable=False, default="", index=True)

    added_by_uuid: str = Column(String, ForeignKey('users.uuid'), nullable=True)
    added_by = relationship("User", foreign_keys=[added_by_uuid], uselist=False)

    avatar_uuid: str = Column(String, ForeignKey('storages.uuid'), nullable=True)
    avatar = relationship("Storage", foreign_keys=[avatar_uuid], uselist=False)
    
    # membership_uuid:str = Column(String, ForeignKey('memberships.uuid',ondelete = "CASCADE",onupdate= "CASCADE"), nullable=False )

    password_hash: str = Column(String(100), nullable=True, default="")
    # status = Column(types.Enum(UserStatusType), index=True, nullable=False, default=UserStatusType.UNACTIVED)
    status = Column(String,nullable=False,default=Ownerstatus.ACTIVED)
    is_new_user: bool = Column(Boolean, nullable=True, default=False)
    otp: str = Column(String(5), nullable=True, default="")
    otp_expired_at: datetime = Column(DateTime, nullable=True, default=None)
    otp_password: str = Column(String(5), nullable=True, default="")
    otp_password_expired_at: datetime = Column(DateTime, nullable=True, default=None)


    date_added: datetime = Column(DateTime, nullable=False, default=datetime.now())
    date_modified: datetime = Column(DateTime, nullable=False, default=datetime.now())

    def __repr__(self):
        return '<Owner: uuid: {} email: {}>'.format(self.uuid, self.email)


@event.listens_for(Owner, 'before_insert')
def update_created_modified_on_create_listener(mapper, connection, target):
    """ Event listener that runs before a record is updated, and sets the creation/modified field accordingly."""
    target.date_added = datetime.now()
    target.date_modified = datetime.now()


@event.listens_for(Owner, 'before_update')
def update_modified_on_update_listener(mapper, connection, target):
    """ Event listener that runs before a record is updated, and sets the modified field accordingly."""
    target.date_modified = datetime.now()


class OwnerActionValidation(Base):
    __tablename__ = 'owner_action_validations'

    uuid: str = Column(String, primary_key=True)

    user_uuid: str = Column(String, ForeignKey('owners.uuid'), nullable=True)
    code: str = Column(String, unique=False, nullable=True)
    expired_date: any = Column(DateTime, default=datetime.now())
    value: str = Column(String, default="", nullable=True)

    date_added: any = Column(DateTime, nullable=False, default=datetime.now())


@event.listens_for(OwnerActionValidation, 'before_insert')
def update_created_modified_on_create_listener(mapper, connection, target):
    """ Event listener that runs before a record is updated, and sets the creation/modified field accordingly."""
    target.date_added = datetime.now()
