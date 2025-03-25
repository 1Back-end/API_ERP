import math
from typing import Optional
import uuid

from sqlalchemy import or_
from app.main import models,schemas
from app.main.core.i18n import __
from app.main.core.security import get_password_hash,verify_password,generate_password
from sqlalchemy.orm import Session
from app.main.crud.base import CRUDBase
from app.main.core.mail import notify_admin, send_account_creation_email
from fastapi import HTTPException,status,BackgroundTasks

class  CRUDRenouvellement(CRUDBase[models.Renouvellement,schemas.Renouvellement,schemas.RenouvellementResponse]):
    
    
    @classmethod
    def get_by_name(cls,db:Session,name:str):
        return db.query(models.Renouvellement).filter(models.Renouvellement.name==name,models.Renouvellement.is_deleted==False).first()
    
    @classmethod
    def get_by_uuid(cls,db:Session,uuid:str):
        return db.query(models.Renouvellement).filter(models.Renouvellement.uuid==uuid,models.Renouvellement.is_deleted==False).first()
    
    @classmethod
    def create(cls,db:Session,obj_in:schemas.RenouvellementCreate,added_by_uuid:str):
         
        db_obj = models.TypeAbonnement(
            uuid=str(uuid.uuid4()),
            company_id=obj_in.compagnie_uuid,
            date_renouvellement=obj_in.date_renouvellement,
            date_expiration=obj_in.date_expiration,
            added_by_uuid = added_by_uuid

        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    @classmethod
    def update(cls,db:Session,obj_in:schemas.RenouvellementUpdate,added_by_uuid:str,):
        db_obj = cls.get_by_uuid(db=db,uuid=obj_in.uuid)
        if db_obj is None:
            raise HTTPException(status_code=404,detail=__(key="Renouvellement-not-found"))
        db_obj.company_uuid = obj_in.company_uuid if obj_in.company_uuid else db_obj.company_uuid
        db_obj.start_date = obj_in.start_date if obj_in.start_date else db_obj.start_date
        db_obj.end_date = obj_in.end_date if obj_in.end_date else db_obj.end_date
        db_obj.added_by_uuid = added_by_uuid
        db.flush()
        db.commit()
        db.refresh(db_obj)
        return db_obj
    

    @classmethod
    def delete(cls,db:Session,uuid:str):
        db_obj = cls.get_by_uuid(db=db,uuid=uuid)
        if db_obj is None:
            raise HTTPException(status_code=404,detail=__(key="Renouvellemen-not-found"))
        db_obj.is_deleted = True
        db.flush()
        db.commit()



    @classmethod
    def get_many(
        cls,
        *,
        db: Session,
        page: int = 1,
        per_page: int = 30,
        order: Optional[str] = None,
        order_field: Optional[str] = None,
        keyword: Optional[str] = None
    ):
        if page < 1:
            page = 1

        record_query = db.query(models.Renouvellement).filter(models.Renouvellement.is_deleted == False)

        if keyword:
            record_query = record_query.filter(
                or_(
                    models.Renouvellement.company_uuid .ilike(f"%{keyword}%"),
                )
            )

        if order and order_field and hasattr(models.TypeAbonnement, order_field):
            if order.lower() == "asc":
                record_query = record_query.order_by(getattr(models.Renouvellement , order_field).asc())
            else:
                record_query = record_query.order_by(getattr(models.Renouvellement, order_field).desc())
        total = record_query.count()
        record_query = record_query.offset((page - 1) * per_page).limit(per_page).all()

        return schemas.RenouvellementResponse(
            total=total,
            pages=math.ceil(total / per_page),
            per_page=per_page,
            current_page=page,
            data=record_query
        )
    


      
