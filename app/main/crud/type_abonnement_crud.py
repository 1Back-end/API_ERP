import math
import bcrypt
from fastapi import HTTPException
from sqlalchemy import or_
import re
from typing import List, Optional, Union
import uuid
from app.main.core.i18n import __
from sqlalchemy.orm import Session
from app.main.crud.base import CRUDBase
from app.main import models,schemas


class CRUDTypeAbonnement(CRUDBase[models.TypeAbonnement,schemas.TypeAbonnementCreate,schemas.TypeAbonnementUpdate]):
    
    @classmethod
    def get_by_uuid(cls,db:Session,*,uuid:str):
        return db.query(models.TypeAbonnement).filter(models.TypeAbonnement.uuid == uuid,models.TypeAbonnement.is_deleted==False).first()
    
    @classmethod
    def get_by_name(cls,db:Session,*,name:str):
        return db.query(models.TypeAbonnement).filter(models.TypeAbonnement.name == name,models.TypeAbonnement.is_deleted==False).first()
    
    @classmethod
    def get_by_list(cls,db:Session):
        return db.query(models.TypeAbonnement).filter(models.TypeAbonnement.is_deleted==False).all()
    
    @classmethod
    def create(cls,db:Session,*,obj_in:schemas.TypeAbonnementCreate,added_by_uuid:str):
        new_typeabonnement = models.TypeAbonnement(
            uuid=str(uuid.uuid4()),
            name = obj_in.name,
            price = obj_in.price,
            added_by_uuid=added_by_uuid
        )
        db.add(new_typeabonnement)
        db.commit()
        db.refresh(new_typeabonnement)
        return new_typeabonnement
    
    @classmethod
    def update(cls,db:Session,*,obj_in:schemas.TypeAbonnementUpdate,added_by_uuid:str):
        type_abonnement = cls.get_by_uuid(db=db,uuid=obj_in.uuid)
        if type_abonnement is not None:
            raise HTTPException(status_code=404,detail=__("type-abonnement-not-found"))
        
        type_abonnement.name = obj_in.name if obj_in.name else type_abonnement.name
        type_abonnement.price = obj_in.price if obj_in.price else type_abonnement.price
        db.flush()
        db.commit()
        db.refresh(type_abonnement)
        return type_abonnement
    
    @classmethod
    def delete(cls,db:Session,*,uuid:str):
        type_abonnement = cls.get_by_uuid(db=db,uuid=uuid)
        if type_abonnement is not None:
            raise HTTPException(status_code=404,detail=__("type-abonnement-not-found"))
        type_abonnement.is_deleted = True
        db.commit()

type_abonnement = CRUDTypeAbonnement(models.TypeAbonnement)


