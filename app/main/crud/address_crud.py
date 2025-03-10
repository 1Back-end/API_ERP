import math
from typing import Optional
import uuid
from sqlalchemy.orm import Session

from fastapi import HTTPException,status
from app.main.crud.base import CRUDBase
from app.main.core.i18n import __
from app.main import models, schemas
from sqlalchemy import or_

class CRUDAddresss(CRUDBase[models.Address,schemas.AddressCreate,schemas.AddressUpdate]):

    @classmethod
    def get_by_uuid(cls,db:Session,*,uuid:str):
        return db.query(models.Address).filter(models.Address.uuid==uuid).first()
    
    @classmethod
    def create(cls,db:Session,*,obj_in:schemas.AddressCreate):
        new_address = models.Address(
            uuid=str(uuid.uuid4()),
            street=obj_in.street,
            city=obj_in.city,
            state=obj_in.state,
            zipcode=obj_in.zipcode,
            country=obj_in.country,
            apartment_number=obj_in.apartment_number,
            additional_information=obj_in.additional_information
        )
        db.add(new_address)
        db.commit()
        db.refresh(new_address)
        return new_address
    
    @classmethod
    def update(cls,db:Session,*,obj_in:schemas.AddressUpdate):
        address = cls.get_by_uuid(db=db,uuid=obj_in.uuid)
        if address is None:
            raise HTTPException(status_code=404,detail=__(key="address-not-found"))
        address.street = obj_in.street if obj_in.street else address.street
        address.city = obj_in.street if obj_in.city else address.city
        address.state = obj_in.state if obj_in.state else address.state
        address.zipcode = obj_in.zipcode if obj_in.zipcode else address.zipcode
        address.country = obj_in.country if obj_in.country else address.country
        address.apartment_number = obj_in.apartment_number if obj_in.apartment_number else address.apartment_number
        address.additional_information = obj_in.additional_information if obj_in.additional_information else address.additional_information
        db.flush()
        db.commit()
        db.refresh(address)
        return address
    
    @classmethod
    def get_many(
        cls,
        *,
        db:Session,
        page : int = 1,
        per_page: int = 30,
        order : Optional[str]=None,
        order_filed : Optional[str]=None,
        keyword : Optional[str]=None

    ):
        if page < 1:
            page = 1

        record_query = db.query(models.Address)

        if keyword:
            record_query = record_query.filter(
                or_(
                    models.Address.additional_information.ilike(f"%{keyword}%"),
                    models.Address.country.ilike(f"%{keyword}%"),
                    models.Address.apartment_number.ilike(f"%{keyword}%"),
                )
            )
        if order and order_filed and hasattr(models.Address,order_filed):
            if order.lower() == "asc":
                record_query = record_query.order_by(getattr(models.Address,order_filed).asc())
            else:
                record_query = record_query.order_by(getattr(models.Address,order_filed).desc())
        total = record_query.count()

        record_query = record_query.offset((page-1) * per_page).limit(per_page).all()

        return schemas.AddressResponseList(
            total=total,
            pages = math.ceil(total/per_page),
            per_page=per_page,
            current_page=page,
            data=record_query
        )

    
    



address = CRUDAddresss(models.Address)