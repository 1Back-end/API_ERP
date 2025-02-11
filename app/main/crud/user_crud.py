import uuid
from app.main import models,schemas
from app.main.core.security import get_password_hash,verify_password
from sqlalchemy.orm import Session
from app.main.crud.base import CRUDBase

class CRUDUser(CRUDBase[models.User,schemas.UserCreate,schemas.UserUpdate]):


    @classmethod
    def get_by_email(cls,db:Session,*,email:str):
        return db.query(models.User).filter(models.User.email==email,
                                            models.User.status.notin_([models.UserStatus.DELETED,models.UserStatus.INACTIVE,models.UserStatus.BLOCKED])).first()
    
    @classmethod
    def get_by_phone_number(cls,db:Session,*,phone_number:str):
         return db.query(models.User).filter(models.User.phone_number==phone_number,
                                             models.User.status.notin_([models.UserStatus.DELETED,models.UserStatus.INACTIVE,models.UserStatus.BLOCKED])).first()
    

    @classmethod
    def get_by_uuid(cls,db:Session,*,uuid:str):
         return db.query(models.User).filter(models.User.uuid==uuid,
                                             models.User.status.notin_([models.UserStatus.DELETED,models.UserStatus.INACTIVE,models.UserStatus.BLOCKED])).first()
    

    @classmethod
    def create(cls,db:Session,*,obj_in:schemas.UserCreate):
         hashed_password = get_password_hash(obj_in.password_hash)
         new_user = models.User(
              uuid=str(uuid.uuid4()),
              email=obj_in.email,
              phone_number=obj_in.phone_number,
              first_name=obj_in.first_name,
              last_name=obj_in.last_name,
              password_hash=hashed_password

         )
         db.add(new_user)
         db.commit()
         db.refresh(new_user)
         return new_user
    
    @classmethod
    def update(cls,db:Session,*,obj_in:schemas.UserUpdate):
         user = cls.get_by_uuid(db=db,uuid=obj_in.uuid)
    
    




