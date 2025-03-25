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




router = APIRouter(prefix="/renouvellements",tags=["renouvellements"])

@router.post("/create",response_model=schemas.RenouvellementResponse)
def create_renouvellement(
    *,
    db: Session = Depends(get_db),
    obj_in:schemas.RenouvellementCreate,
    current_user : models.User = Depends(TokenRequired(roles=["SUPER_ADMIN,ADMIN"]))
):
    added_by_uuid = current_user.uuid
    return crud.renouvellement.create(db=db,obj_in=obj_in,added_by_uuid=added_by_uuid)


@router.put("/update",response_model=schemas.RenouvellementResponse)
def update_type_abonnements(
    *,
    db: Session = Depends(get_db),
    obj_in:schemas.RenouvellementUpdate,
    current_user : models.User = Depends(TokenRequired(roles=["SUPER_ADMIN,ADMIN"]))
):
    added_by_uuid = current_user.uuid
    return crud.renouvellement.update(db=db,obj_in=obj_in,added_by_uuid=added_by_uuid)


@router.delete("/delete",response_model=schemas.Msg)
def delete_type_abonnements(
    *,
    db: Session = Depends(get_db),
    uuid:str,
    current_user : models.User = Depends(TokenRequired(roles=["SUPER_ADMIN,ADMIN"]))
):
    crud.renouvellement.delete(db=db,uuid=uuid)
    return {"message":__("renouvellement-deleted")}

