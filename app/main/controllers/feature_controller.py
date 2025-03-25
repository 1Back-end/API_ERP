
from datetime import timedelta, datetime
from typing import Any, List, Optional
from fastapi import APIRouter, Depends, Body, HTTPException, Query
from sqlalchemy.orm import Session
from app.main.core.dependencies import get_db, TokenRequired
from app.main import schemas, crud, models
from app.main.core.i18n import __
from app.main.core.config import Config
from app.main.core.dependencies import TokenRequired


router = APIRouter(prefix="/features",tags=["features"])


@router.post("/create",response_model=List[schemas.FeatureSlim])
async def create_feature(
    features_data: schemas.FeatureCreateResquest,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(TokenRequired(roles=["SUPER_ADMIN","ADMIN"]))
):
    added_by_uuid = current_user.uuid

    return crud.features.create(db=db, features_data=features_data,added_by_uuid=added_by_uuid)
    

@router.put("/features",response_model=schemas.FeatureSlim)
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

@router.get("/features/{uuid}",response_model=List[schemas.FeatureSlim])
async def get_feature(
    type_abonnement_uuid:str,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(TokenRequired(roles=["SUPER_ADMIN","ADMIN"]))
):
    return crud.features.get_features_by_type_abonnement(db=db,type_abonnement_uuid=type_abonnement_uuid)

@router.get("/get_all_features", response_model=None)
def list_features(
    *,
    db: Session = Depends(get_db),
    page: int =  1,
    per_page: int = 30,
    order:str= Query(None,enum=["ASC","DESC"]),
    order_field: Optional[str] = None,
    keyword: Optional[str] = None,
):
    return crud.features.get_many(
        db=db,
        page=page,
        per_page=per_page,
        order=order,
        order_field=order_field,
        keyword=keyword,
    )
