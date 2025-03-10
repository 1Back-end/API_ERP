from datetime import datetime, timedelta
import enum
from typing import Optional
import uuid
from sqlalchemy.orm import Session
from app.main import models , schemas,crud
from fastapi import HTTPException, Query,status,APIRouter,Depends
from app.main.core.config import Config
from app.main.core.dependencies import get_db,TokenRequired
from app.main.core.security import create_access_token,generate_code,is_valid_password,get_password_hash
from app.main.crud.base import CRUDBase
from app.main.core.i18n import __
from app.main.core.mail import send_start_reset_password

router = APIRouter(prefix="/users",tags=["users"])

@router.post("/administrator",response_model=schemas.UserResponse,status_code=201)
def create_administrator(
    *,
    db : Session=Depends(get_db),
    obj_in:schemas.UserCreate,
    current_user : models.User = Depends(TokenRequired(roles=["SUPER_ADMIN"]))
):
    exist_email = crud.user.get_by_email(db=db,email=obj_in.email)
    if exist_email:
        raise HTTPException(status_code=409,detail=__(key="this-email-is-already-exist"))
    exist_phone_number = crud.user.get_by_phone_number(db=db,phone_number=obj_in.phone_number)
    if exist_phone_number:
        raise HTTPException(status_code=409,detail=__(key="this-phone-number-is-already-exist"))
    return crud.user.create(db=db,obj_in=obj_in)


@router.put("/delete",response_model=schemas.Msg)
def delete_users(
    *,
    db : Session=Depends(get_db),
    uuid:str,
    current_user : models.User = Depends(TokenRequired(roles=["SUPER_ADMIN"]))

):
    crud.user.delete(db=db,uuid=uuid)
    return schemas.Msg(message=__(key="User delete successfully"))




@router.put("/activate",response_model=schemas.Msg)
def activate_users(
    *,
    db : Session=Depends(get_db),
    uuid:str,
    current_user : models.User = Depends(TokenRequired(roles=["SUPER_ADMIN"]))

):
    crud.user.activate(db=db,uuid=uuid)
    return schemas.Msg(message=__(key="User activate successfully"))



@router.put("/blocked",response_model=schemas.Msg)
def blocked_users(
    *,
    db : Session=Depends(get_db),
    uuid:str,
    current_user : models.User = Depends(TokenRequired(roles=["SUPER_ADMIN"]))

):
    crud.user.blocked(db=db,uuid=uuid)
    return schemas.Msg(message=__(key="User blocked successfully"))




@router.put("/deactivate",response_model=schemas.Msg)
def deactivate_users(
    *,
    db : Session=Depends(get_db),
    uuid:str,
    current_user : models.User = Depends(TokenRequired(roles=["SUPER_ADMIN"]))

):
    crud.user.deactivate(db=db,uuid=uuid)
    return schemas.Msg(message=__(key="User deactivate successfully"))




