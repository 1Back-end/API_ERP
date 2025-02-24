from datetime import timedelta, datetime
from typing import Any, List
from fastapi import APIRouter, Depends, Body, HTTPException
from sqlalchemy.orm import Session
from app.main.core.dependencies import get_db, TokenRequired
from app.main import schemas, crud, models
from app.main.core.i18n import __
from app.main.core.config import Config
from app.main.core.dependencies import TokenRequired

router = APIRouter(prefix="/type_abonnement", tags=["type_abonnement"])


@router.post("/create",response_model=schemas.TypeAbonnementResponse)
def create_type_abonnement(
    *,
    db: Session = Depends(get_db),
    obj_in : schemas.TypeAbonnementCreate,
    current_user: models.User = Depends(TokenRequired(roles=["SUPER_ADMIN","ADMIN"]))
):
    exist_name = crud.type_abonnement.get_by_name(db=db,name=obj_in.name)
    if not exist_name:
        raise HTTPException(status_code=409,detail=__(key="this-type-abonnement-is-already-exist"))
    added_by_uuid = current_user.uuid
    return crud.type_abonnement.create(db=db,obj_in=obj_in,added_by_uuid=added_by_uuid)

@router.put("/update",response_model=schemas.TypeAbonnementUpdate)
def update_type_abonnement(
    *,
    db: Session = Depends(get_db),
    obj_in : schemas.TypeAbonnementCreate,
    current_user: models.User = Depends(TokenRequired(roles=["SUPER_ADMIN","ADMIN"]))
):
    added_by_uuid = current_user.uuid
    return crud.type_abonnement.update(db=db,obj_in=obj_in,added_by_uuid=added_by_uuid)

@router.delete("/delete",response_model=schemas.Msg)
def delete_type_abonnement(
    *,
    db: Session = Depends(get_db),
    obj_in : schemas.TypeAbonnementDelete,
    current_user: models.User = Depends(TokenRequired(roles=["SUPER_ADMIN","ADMIN"]))
):
    return crud.type_abonnement.create(db=db,uuid=obj_in.uuid)

@router.get("/get_all",response_model=List[schemas.TypeAbonnementSlim1])
def get_all(
    *,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(TokenRequired(roles=["SUPER_ADMIN","ADMIN"]))
):
    return crud.type_abonnement.get_by_list(db=db)

@router.get("/{uuid}/get_by_uuid",response_model=schemas.TypeAbonnementSlim1)
def get(
    *,
    uuid:str,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(TokenRequired(roles=["SUPER_ADMIN","ADMIN"]))

):
    return crud.type_abonnement.get_by_uuid(db=db,uuid=uuid)
