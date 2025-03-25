import enum
from typing import Optional
import uuid
from sqlalchemy.orm import Session
from app.main import models , schemas,crud
from fastapi import HTTPException, Query,status,APIRouter,Depends,BackgroundTasks
from app.main.core.dependencies import TokenRequired, get_db
from app.main.crud.base import CRUDBase
from app.main.core.i18n import __
from app.main.core.dependencies import get_db,TokenRequired

router = APIRouter(prefix="/type_abonnements",tags=["type_abonnements"])

@router.post("/create",response_model=schemas.TypeAbonnementResponse)
def create_type_abonnements(
    *,
    db: Session = Depends(get_db),
    obj_in:schemas.TypeAbonnementCreate,
    current_user : models.User = Depends(TokenRequired(roles=["SUPER_ADMIN"]))
):
    added_by_uuid = current_user.uuid
    return crud.type_abonnement.create(db=db,obj_in=obj_in,added_by_uuid=added_by_uuid)


@router.put("/update",response_model=schemas.TypeAbonnementResponse)
def update_type_abonnements(
    *,
    db: Session = Depends(get_db),
    obj_in:schemas.TypeAbonnementUpdate,
    current_user : models.User = Depends(TokenRequired(roles=["SUPER_ADMIN"]))
):
    added_by_uuid = current_user.uuid
    return crud.type_abonnement.update(db=db,obj_in=obj_in,added_by_uuid=added_by_uuid)


@router.delete("/delete",response_model=schemas.Msg)
def delete_type_abonnements(
    *,
    db: Session = Depends(get_db),
    uuid:str,
    current_user : models.User = Depends(TokenRequired(roles=["SUPER_ADMIN"]))
):
    crud.type_abonnement.delete(db=db,uuid=uuid)
    return {"message":__("type-abonnement-deleted")}

@router.get("/get_all_type_abonnements", response_model=None)
def list_type_abonnnements(
    *,
    db: Session = Depends(get_db),
    page: int =  1,
    per_page: int = 30,
    order:str= Query(None,enum=["ASC","DESC"]),
    order_field: Optional[str] = None,
    keyword: Optional[str] = None,
):
    return crud.type_abonnement.get_many(
        db=db,
        page=page,
        per_page=per_page,
        order=order,
        order_field=order_field,
        keyword=keyword,
    )
