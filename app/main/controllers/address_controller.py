import enum
from typing import Optional
import uuid
from sqlalchemy.orm import Session
from app.main import models , schemas,crud
from fastapi import HTTPException, Query,status,APIRouter,Depends
from app.main.core.dependencies import get_db
from app.main.crud.base import CRUDBase
from app.main.core.i18n import __

router = APIRouter(prefix="/address",tags=["Address"])

@router.post("",response_model=schemas.AddressResponse,status_code=status.HTTP_201_CREATED)
def create_address(
    *,
    db : Session=Depends(get_db),
    obj_in:schemas.AddressCreate
):
    return crud.address.create(db=db,obj_in=obj_in)


@router.get("/{uuid}",response_model=schemas.AddressResponse,status_code=status.HTTP_202_ACCEPTED)
def get_address_by_uuid(
    *,
    db : Session=Depends(get_db),
    uuid:str

):
    return crud.address.get_by_uuid(db=db,uuid=uuid)

@router.put("",response_model=schemas.AddressResponse,status_code=status.HTTP_202_ACCEPTED)
def update_address(
    *,
    db : Session=Depends(get_db),
    obj_in:schemas.AddressUpdate

):
    return crud.address.update(db=db,obj_in=obj_in)


@router.get("",response_model=None)
def get_by_pagination(
    *,
    db : Session=Depends(get_db),
    page : int = 1,
    per_page: int = 30,
    order : str= Query("desc",enum=["asc","desc"]),
    order_filed : str="date_added",
    keyword : Optional[str]=None
):
    return crud.address.get_many(
        db=db,
        page = page,
        per_page=per_page,
        order=order,
        order_filed=order_filed,
        keyword=keyword
    )