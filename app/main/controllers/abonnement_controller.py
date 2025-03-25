import enum
from typing import Optional
import uuid
from sqlalchemy.orm import Session
from app.main import models , schemas,crud
from fastapi import HTTPException, Query,status,APIRouter,Depends,BackgroundTasks
from app.main.core.dependencies import get_db
from app.main.crud.base import CRUDBase
from app.main.core.i18n import __
from app.main.core.dependencies import get_db,OwnersTokenRequired


router = APIRouter(prefix="/abonnement",tags=["abonnement"])


@router.post("/subsciption",response_model=schemas.AbonnementResponseSlim1)
def create_abonnement(
    *,
    db : Session=Depends(get_db),
    obj_in:schemas.AbonnemmentCreate,
    current_user:models.Owner = Depends(OwnersTokenRequired())
):
    return crud.abonnement.create(db=db,obj_in=obj_in,added_by=current_user.uuid)
