import math
from typing import Optional
import uuid
from sqlalchemy.orm import Session

from fastapi import HTTPException,status
from app.main.core.security import verify_password
from app.main.crud.base import CRUDBase
from app.main.core.i18n import __
from app.main import models, schemas,crud
from sqlalchemy import or_
import math


class CRUDCompany(CRUDBase[models.Company,schemas.CompanyCreate,schemas.CompanyUpdate]):


    @classmethod
    def get_by_uuid(cls,db:Session,*,uuid:str):
        return db.query(models.Company).filter(models.Company.uuid==uuid,models.Company.is_deleted==False).first()
    
    @classmethod
    def get_by_name(cls,db:Session,*,name:str):
        return db.query(models.Company).filter(models.Company.name==name,models.Company.is_deleted==False).first()
    
    @classmethod
    def get_by_email(cls,db:Session,*,email:str):
        return db.query(models.Company).filter(models.Company.email==email,models.Company.is_deleted==False).first()
    
    @classmethod
    def get_by_phone_number(cls,db:Session,*,phone_number:str):
        return db.query(models.Company).filter(models.Company.phone_number==phone_number,models.Company.is_deleted==False).first()
    

    @classmethod
    def create(cls,db:Session,*,obj_in:schemas.CompanyCreate,added_by:str):
        address = crud.address.get_by_uuid(db=db,uuid=obj_in.address_uuid)
        if not address:
            raise HTTPException(status_code=404,detail=__(key="address-not-found"))
        if obj_in.logo_uuid:
            logo = crud.storage_crud.get_file_by_uuid(db=db,file_uuid=obj_in.logo_uuid)
            if not logo:
                raise HTTPException(status_code=404,detail=__(key="logo-not-found"))
        if obj_in.signature_uuid:
            signature = crud.storage_crud.get_file_by_uuid(db=db,file_uuid=obj_in.signature_uuid)
            if not signature:
                raise HTTPException(status_code=404,detail=__(key="signature-not-found"))
        if obj_in.stamp_uuid:
            stamp = crud.storage_crud.get_file_by_uuid(db=db,file_uuid=obj_in.stamp_uuid)
            if not stamp:
                raise HTTPException(status_code=404,detail=__(key="stamp-not-found"))
            
        comapny = models.Company(
            uuid=str(uuid.uuid4()),
            name=obj_in.name,
            email=obj_in.email,
            country_code=obj_in.country_code,
            phone_number=obj_in.phone_number,
            full_phone_number = f"{obj_in.country_code}{obj_in.phone_number}",
            description=obj_in.description,
            slogan=obj_in.slogan,
            address_uuid=obj_in.address_uuid,
            logo_uuid=obj_in.logo_uuid if obj_in.logo_uuid else None,
            signature_uuid=obj_in.signature_uuid if obj_in.signature_uuid else None,
            stamp_uuid=obj_in.stamp_uuid if obj_in.stamp_uuid else None,
            founded_at=obj_in.founded_at,
            employee_count=obj_in.employee_count,
            website=obj_in.website,
            added_by=added_by,
            type=obj_in.type
        )
        db.add(comapny)
        db.commit()
        db.refresh(comapny)
        return comapny
    
    @classmethod
    def delete(cls,db:Session,uuid:str):
         company = cls.get_by_uuid(db=db,uuid=uuid)
         if not company :
              raise HTTPException(status_code=404,detail="company not found")
         company.status=models.CompanyStatus.DELETED
         db.commit()

    @classmethod
    def activate(cls,db:Session,uuid:str,):
         company=cls.get_by_uuid(db=db,uuid=uuid)
         if not company:
              raise HTTPException(status_code=404,detail="company not found")
         company.status=models.CompanyStatus.ACTIVED
         db.commit()

    @classmethod
    def blocked(cls,db:Session,uuid:str):
         company = cls.get_by_uuid(db=db,uuid=uuid)
         if not company:
              raise HTTPException(status_code=404,detail="company not found")
         company.status=models.CompanyStatus.BLOCKED
         db.commit()


    @classmethod
    def update_company(cls, db: Session, obj_in:schemas.CompanyUpdate,added_by:str):
        address = crud.address.get_by_uuid(db=db,uuid=obj_in.address_uuid)
        if not address:
            raise HTTPException(status_code=404,detail=__(key="address-not-found"))
        if obj_in.logo_uuid:
            logo = crud.storage_crud.get_file_by_uuid(db=db,file_uuid=obj_in.logo_uuid)
            if not logo:
                raise HTTPException(status_code=404,detail=__(key="logo-not-found"))
        if obj_in.signature_uuid:
            signature = crud.storage_crud.get_file_by_uuid(db=db,file_uuid=obj_in.signature_uuid)
            if not signature:
                raise HTTPException(status_code=404,detail=__(key="signature-not-found"))
        if obj_in.stamp_uuid:
            stamp = crud.storage_crud.get_file_by_uuid(db=db,file_uuid=obj_in.stamp_uuid)
            if not stamp:
                raise HTTPException(status_code=404,detail=__(key="stamp-not-found"))
        company = cls.get_by_uuid(db=db, uuid=obj_in.uuid)
        if not company:
            raise HTTPException(status_code=404, detail="Company not found")
        company.name = obj_in.name if obj_in.name else company.name
        company.email = obj_in.email if obj_in.email else company.email
        company.country_code = obj_in.country_code if obj_in.country_code else company.country_code
        company.phone_number = obj_in.phone_number if obj_in.phone_number else company.phone_number
        company.description = obj_in.description if obj_in.description else company.description
        company.slogan = obj_in.slogan if obj_in.slogan else obj_in.slogan
        company.address_uuid =  obj_in.address_uuid if obj_in.address_uuid else company.address_uuid 
        company.logo_uuid = obj_in.logo_uuid  if obj_in.logo_uuid else company.logo_uuid 
        company.signature_uuid = obj_in.signature_uuid if obj_in.signature_uuid else company.signature_uuid
        company.stamp_uuid = obj_in.stamp_uuid if obj_in.stamp_uuid else company.stamp_uuid
        company.founded_at = obj_in.founded_at if obj_in.founded_at else company.founded_at
        company.employee_count = obj_in.employee_count if obj_in.employee_count else company.employee_count
        company.website = obj_in.website if obj_in.website else company.website
        company.type = obj_in.type if obj_in.type else company.type
        db.flush()
        db.commit()
        db.refresh(company)
        return company
        
        
    
    

    @classmethod
    def get_many_company_owner(
        cls, 
        *,
        db: Session,
        page: int = 1,
        per_page: int = 30,
        order: Optional[str] = None,
        order_field: Optional[str] = None,
        keyword: Optional[str] = None,
        status : Optional[str]=None,
        type : Optional[str]=None,
        owner_uuid : Optional[str]=None
    ):
        if page < 1:
            page = 1

        record_query = db.query(models.Company).filter(models.Company.is_deleted == False,models.Company.added_by==owner_uuid)

        if keyword:
            record_query = record_query.filter(
                or_(
                    models.Company.name.ilike(f"%{keyword}%"),
                    models.Company.email.ilike(f"%{keyword}%"),
                    models.Company.phone_number.ilike(f"%{keyword}%"),
                    models.Company.description.ilike(f"%{keyword}%"),
                    models.Company.slogan.ilike(f"%{keyword}%"),
                )
            )

        if order and order_field and hasattr(models.Company, order_field):
            if order.lower() == "asc":
                record_query = record_query.order_by(getattr(models.Company, order_field).asc())
            else:
                record_query = record_query.order_by(getattr(models.Company, order_field).desc())

        if status:
            record_query = record_query.filter(models.Company.status==status)

        if type:
            record_query = record_query.filter(models.Company.type==type)

        total = record_query.count()
        record_query = record_query.offset((page - 1) * per_page).limit(per_page).all()

        return schemas.CompanyResponseList(
            total=total,
            pages=math.ceil(total / per_page),
            per_page=per_page,
            current_page=page,
            data=record_query
        )
    

    @classmethod
    def get_many_company_admin(
        cls, 
        *,
        db: Session,
        page: int = 1,
        per_page: int = 30,
        order: Optional[str] = None,
        order_field: Optional[str] = None,
        keyword: Optional[str] = None,
        status : Optional[str]=None,
        type : Optional[str]=None,
    ):
        if page < 1:
            page = 1

        record_query = db.query(models.Company).filter(models.Company.is_deleted == False)

        if keyword:
            record_query = record_query.filter(
                or_(
                    models.Company.name.ilike(f"%{keyword}%"),
                    models.Company.email.ilike(f"%{keyword}%"),
                    models.Company.phone_number.ilike(f"%{keyword}%"),
                    models.Company.description.ilike(f"%{keyword}%"),
                    models.Company.slogan.ilike(f"%{keyword}%"),
                )
            )

        if order and order_field and hasattr(models.Company, order_field):
            if order.lower() == "asc":
                record_query = record_query.order_by(getattr(models.Company, order_field).asc())
            else:
                record_query = record_query.order_by(getattr(models.Company, order_field).desc())

        if status:
            record_query = record_query.filter(models.Company.status==status)

        if type:
            record_query = record_query.filter(models.Company.type==type)

        total = record_query.count()
        record_query = record_query.offset((page - 1) * per_page).limit(per_page).all()

        return schemas.CompanyResponseListAdmin(
            total=total,
            pages=math.ceil(total / per_page),
            per_page=per_page,
            current_page=page,
            data=record_query
        )
    
     
     # Code pour faire la modification des statuts en utilisant une seule fontion en passant en paramètre le uuid de l'entreprise et le status qui sera selectionné
    @classmethod
    def update_status_company(cls,db:Session,uuid:str,status:str):
        company = cls.get_by_uuid(db=db,uuid=uuid)
        if not company:
            raise HTTPException(status_code=404,detail="Company not found")
        company.status = status
        db.commit()





company = CRUDCompany(models.Company)


    

    
    

