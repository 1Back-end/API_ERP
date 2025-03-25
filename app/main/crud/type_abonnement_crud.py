import math
from typing import Optional
import uuid
from sqlalchemy.orm import Session
from fastapi import HTTPException,status
from app.main.crud.base import CRUDBase
from app.main.core.i18n import __
from app.main import models, schemas
from sqlalchemy import or_



class CRUDTypeAbonnement(CRUDBase[models.TypeAbonnement,schemas.TypeAbonnementCreate,schemas.TypeAbonnementUpdate]):

    @classmethod
    def get_by_name(cls,db:Session,name:str):
        return db.query(models.TypeAbonnement).filter(models.TypeAbonnement.name==name,models.TypeAbonnement.is_deleted==False).first()
    
    @classmethod
    def get_by_uuid(cls,db:Session,uuid:str):
        return db.query(models.TypeAbonnement).filter(models.TypeAbonnement.uuid==uuid,models.TypeAbonnement.is_deleted==False).first()
    
    @classmethod
    def create(cls,db:Session,obj_in:schemas.TypeAbonnementCreate,added_by_uuid:str):

        db_obj = models.TypeAbonnement(
            uuid=str(uuid.uuid4()),
            name=obj_in.name,
            currency=obj_in.currency,
            price = obj_in.price,
            full_price = f"{obj_in.price} {obj_in.currency}",
            start_date = obj_in.start_date,
            end_date = obj_in.end_date,
            added_by_uuid = added_by_uuid
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    

    @classmethod
    def update(cls,db:Session,obj_in:schemas.TypeAbonnementUpdate,added_by_uuid:str):
        db_obj = cls.get_by_uuid(db=db,uuid=obj_in.uuid)
        if db_obj is None:
            raise HTTPException(status_code=404,detail=__(key="type-abonnement-not-found"))
        db_obj.name = obj_in.name if obj_in.name else db_obj.name
        db_obj.currency = obj_in.currency if obj_in.currency else db_obj.currency
        db_obj.price = obj_in.price if obj_in.price else db_obj.price
        db_obj.full_price = f"{db_obj.price} {db_obj.currency}",
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
            raise HTTPException(status_code=404,detail=__(key="type-abonnement-not-found"))
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

            record_query = db.query(models.TypeAbonnement).filter(models.TypeAbonnement.is_deleted == False)

            if keyword:
                record_query = record_query.filter(
                    or_(
                        models.TypeAbonnement.name.ilike(f"%{keyword}%"),
                        models.TypeAbonnement.currency.ilike(f"%{keyword}%"),
                    )
                )

            if order and order_field and hasattr(models.TypeAbonnement, order_field):
                if order.lower() == "asc":
                    record_query = record_query.order_by(getattr(models.TypeAbonnement, order_field).asc())
                else:
                    record_query = record_query.order_by(getattr(models.TypeAbonnement, order_field).desc())
            total = record_query.count()
            record_query = record_query.offset((page - 1) * per_page).limit(per_page).all()

            return schemas.TypeAbonnementResponseList(
                total=total,
                pages=math.ceil(total / per_page),
                per_page=per_page,
                current_page=page,
                data=record_query
            )




        




        


type_abonnement = CRUDTypeAbonnement(models.TypeAbonnement)