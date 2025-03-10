import uuid
from app.main import models,schemas
from app.main.core.security import get_password_hash,verify_password,generate_password
from sqlalchemy.orm import Session
from app.main.crud.base import CRUDBase
from app.main.core.mail import notify_admin, send_account_creation_email
from fastapi import HTTPException,status,BackgroundTasks

class CRUDOwner(CRUDBase[models.Owner,schemas.OwnerCreate,schemas.OwnerResponse]):

    @classmethod
    def get_by_uuid(cls,db:Session,uuid:str):
         return db.query(models.Owner).filter(models.Owner.uuid==uuid).first()
    
    @classmethod
    def get_by_email(cls,db:Session,email:str):
         return db.query(models.Owner).filter(models.Owner.email==email).first()
    
    @classmethod
    def get_by_phone_number(cls,db:Session,phone_number:str):
         return db.query(models.Owner).filter(models.Owner.phone_number==phone_number).first()
    

    @classmethod
    def create(cls, db: Session, obj_in: schemas.OwnerCreate, background_tasks: BackgroundTasks):
        new_owner = models.Owner(
            uuid=str(uuid.uuid4()),
            email=obj_in.email,
            country_code=obj_in.country_code,
            phone_number=obj_in.phone_number,
            first_name=obj_in.first_name,
            last_name=obj_in.last_name,
            password_hash=get_password_hash(obj_in.password_hash),
            full_phone_number=f"{obj_in.country_code}{obj_in.phone_number}",
            avatar_uuid = obj_in.avatar_uuid if obj_in.avatar_uuid else None
        )
        db.add(new_owner)
        db.commit()
        db.refresh(new_owner)

        # Récupérer les administrateurs actifs et envoyer une notification
        admins = db.query(models.User).filter(models.User.status == models.UserStatus.ACTIVE).all()
        for admin in admins:
            background_tasks.add_task(
                notify_admin, email_to=admin.email, name=f"{new_owner.first_name} {new_owner.last_name}", full_phone_number=f"{new_owner.country_code}{new_owner.phone_number}"
            )

        return new_owner
    


    classmethod
    def authenticate(cls,db:Session,email:str,password:str):
         owners = cls.get_by_email(db=db,email=email)
         if not owners:
             return None
         if not verify_password(password,owners.password_hash):
             return None
         return owners
    

#     @classmethod
#     def delete(cls,db:Session,uuid:str):
#          owners = cls.get_by_uuid(db=db,uuid=uuid)
#          if not owners :
#               raise HTTPException(status_code=404,detail="owner not found")
#          owners.status=models.Ownerstatus.DELETED
#          db.commit()
    
    
    
#     @classmethod
#     def blocked(cls,db:Session,uuid:str):
#          owners = cls.get_by_uuid(db=db,uuid=uuid)
#          if not owners :
#               raise HTTPException(status_code=404,detail="owners not found")
#          owners.status=models.Ownerstatus.BLOCKED
#          db.commit()




#     @classmethod
#     def activate(cls,db:Session,uuid:str,):
#          owners=cls.get_by_uuid(db=db,uuid=uuid)
#          if not owners:
#               raise HTTPException(status_code=404,detail="owner not found")
#          owners.status=models.Ownerstatus.ACTIVED
#          db.commit()




    
#     @classmethod
#     def deactivate(cls,db:Session,uuid:str,):
#          owners=cls.get_by_uuid(db=db,uuid=uuid)
#          if not owners:
#               raise HTTPException(status_code=404,detail="owner not found")
#          owners.status=models.Ownerstatus.UNACTIVED
#          db.commit()



    @classmethod
    def update_status_owner(cls,db:Session,uuid:str,status:str):
        owners = cls.get_by_uuid(db=db,uuid=uuid)
        if not owners:
            raise HTTPException(status_code=404,detail="Owner not found")
     
        owners.status = status
        db.commit()



owners = CRUDOwner(models.Owner)
