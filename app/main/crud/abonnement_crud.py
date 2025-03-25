from datetime import datetime
import math
from typing import Optional
import uuid
from sqlalchemy.orm import Session

from fastapi import HTTPException,status
from app.main.crud.base import CRUDBase
from app.main.core.i18n import __
from app.main import models, schemas,crud
from sqlalchemy import or_


class CRUDAbonnement(CRUDBase[models.Abonnement,schemas.AbonnemmentCreate,schemas.AbonnementResponseSlim2]):
    
    @classmethod
    def get_by_uuid(cls,db:Session,*,uuid:str):
        return db.query(models.Abonnement).filter(models.Abonnement.uuid==uuid).first()
    

    @classmethod
    def create(cls,db:Session,*,obj_in:schemas.AbonnemmentCreate,added_by:str):
        company = crud.company.get_by_uuid(db,uuid=obj_in.company_uuid)
        if not company:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=__("Company not found"))
        
        type_abonnement = crud.type_abonnement.get_by_uuid(db,uuid=obj_in.type_abonnement_uuid)
        if not type_abonnement:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=__("Type abonnement not found"))
        
         # Vérification de la date d'expiration
        current_date = datetime.utcnow()
        if type_abonnement.end_date < current_date:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=__("Abonnement expiré"))

        new_abonnement = models.Abonnement(
            uuid=str(uuid.uuid4()),
            company_uuid=obj_in.company_uuid,
            type_abonnement_uuid=obj_in.type_abonnement_uuid,
            added_by=added_by
        )
        db.add(new_abonnement)
        db.commit()
        db.refresh(new_abonnement)
        return new_abonnement
    
abonnement = CRUDAbonnement(models.Abonnement)