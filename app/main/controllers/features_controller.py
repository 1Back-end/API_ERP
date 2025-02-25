from datetime import timedelta, datetime
from typing import Any, List
from fastapi import APIRouter, Depends, Body, HTTPException
from sqlalchemy.orm import Session
from app.main.core.dependencies import get_db, TokenRequired
from app.main import schemas, crud, models
from app.main.core.i18n import __
from app.main.core.config import Config
from app.main.core.dependencies import TokenRequired


router = APIRouter(prefix="/features",tags=["features"])


@router.post("/create",response_model=List[schemas.FeatureResponse])
async def create_feature(
    features_data: schemas.FeatureCreateResquest,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(TokenRequired(roles=["SUPER_ADMIN","ADMIN"]))
):
    added_by_uuid = current_user.uuid

    return crud.features.create(db=db, features_data=features_data,added_by_uuid=added_by_uuid)
    

@router.put("/features",response_model=schemas.FeatureResponse)
async def update_feature(
    obj_in: schemas.FeatureUpdateResquest,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(TokenRequired(roles=["SUPER_ADMIN","ADMIN"]))
):
    added_by_uuid = current_user.uuid
    crud.features.create(db=db,obj_in=obj_in,added_by_uuid=added_by_uuid)
    return {"message": __(key="feature-updated-successfully")}

@router.delete("/delete",response_model=schemas.Msg)
async def delete_feature(
    obj_in: schemas.FeatureDelete,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(TokenRequired(roles=["SUPER_ADMIN","ADMIN"]))
):
    crud.features.delete(db=db, uuid=obj_in.uuid)
    return {"message": __(key="feature-deleted-successfully")}

@router.get("/features/{uuid}",response_model=List[schemas.FeatureResponseSlim1])
async def get_feature(
    type_abonnement_uuid:str,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(TokenRequired(roles=["SUPER_ADMIN","ADMIN"]))
):
    return crud.features.get_features_by_type_abonnement(db=db,type_abonnement_uuid=type_abonnement_uuid)