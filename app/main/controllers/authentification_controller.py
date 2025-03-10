from datetime import datetime, timedelta
import enum
from typing import Optional
import uuid
from sqlalchemy.orm import Session
from app.main import models , schemas,crud
from fastapi import HTTPException, Query,status,APIRouter,Depends
from app.main.core.config import Config
from app.main.core.dependencies import OwnersTokenRequired, get_db,TokenRequired
from app.main.core.security import create_access_token,generate_code,is_valid_password,get_password_hash
from app.main.crud.base import CRUDBase
from app.main.core.i18n import __
from app.main.core.mail import send_start_reset_password
from app.main.models import db

router = APIRouter(prefix="/authentification",tags=["authentification"])



@router.post("/login/administrator",response_model=schemas.UserAuthentification)
def login(
    obj_in:schemas.UserLogin,
    db:Session=Depends(get_db)
):
    user=crud.user.authenticate(
        db=db,email=obj_in.email,password=obj_in.password

    )
    if not user:
        raise HTTPException(status_code=404,detail="user not found")
    if user.status in [models.UserStatus.BLOCKED,models.UserStatus.DELETED]:
        raise HTTPException(status_code=400,detail="failed to login")
    if user.status != models.UserStatus.ACTIVE:
        raise HTTPException(status_code=402,detail="user not activate")
    
    access_token_expires = timedelta(minutes=Config.ACCESS_TOKEN_EXPIRE_MINUTES)
    return{
        "user" : user,
        "token" : {
            "access_token" : create_access_token(
                user.uuid,expires_delta=access_token_expires
            ),
           "token_type" : "bearer" 
        }
    }

@router.post("/start-reset-password/administrator",response_model=schemas.Msg)
def start_reset_password(
    obj_in:schemas.ResetPasswordOption1Step1,
    db:Session=Depends(get_db)  
):
    user = crud.user.get_by_email(db=db,email=obj_in.email)
    if not user:
        raise HTTPException(status_code=404,detail="user not found")
    code = generate_code(length=12)
    code = str(code[0:5])
    # code = "0000"
    print(f"Code generate",code)
    user.otp_password = code
    user.otp_password_expiry = datetime.now() + timedelta(minutes=20)
    db.commit()
    db.refresh(user)
    send_start_reset_password(email_to=obj_in.email, name=f"{user.first_name} {user.last_name}", code=code)
    return schemas.Msg(message="reset password started succesfully")


@router.post("/check-otp-password/administrator",response_model=schemas.Msg)
def check_otp_password(
    obj_in:schemas.ResetPasswordOption2Step2,
    db:Session=Depends(get_db) 
):
    user = crud.user.get_by_email(db=db,email=obj_in.email)
    if not user:
        raise HTTPException(status_code=404,detail="user not found")
    if user.otp_password != obj_in.otp:
        raise HTTPException(status_code=400,detail="otp invalid")
    if user.otp_password_expiry < datetime.now():
        raise HTTPException(status_code=400,detail="otp expired")
    return schemas.Msg(message="otp valid")

@router.post("/reset-password/administrator",response_model=schemas.Msg)
def reset_password(
    obj_in:schemas.ResetPasswordOption3Step3,
    db:Session=Depends(get_db) 

):
    user = crud.user.get_by_email(db=db,email=obj_in.email)
    if not user:
        raise HTTPException(status_code=404,detail="user not found")
    if user.otp_password != obj_in.otp:
        raise HTTPException(status_code=400,detail="otp invalid")
    if user.otp_password_expiry < datetime.now():
        raise HTTPException(status_code=400,detail="otp expired")
    if not is_valid_password(password=obj_in.new_password):
        raise HTTPException(status_code=400,detail="Invalid password")
    user.password_hash = get_password_hash(password=obj_in.new_password)
    user.otp_password=None
    user.otp_password_expiry=None
    db.commit()
    db.refresh(user)
    return schemas.Msg(message="password reset successfully")
    
    

@router.post("/profile/administrator",response_model=schemas.UserProfile)
def get_current_user(
    current_user : any = Depends(TokenRequired())

):
    return current_user






























@router.post("/login/owners",response_model=schemas.OwnerAuthentification)
def login(
    obj_in:schemas.OwnerLogin,
    db:Session=Depends(get_db)
):
    owner=crud.owners.authenticate(
        db=db,email=obj_in.email,password=obj_in.password

    )
    if not owner:
        raise HTTPException(status_code=404,detail="user not found")
    if owner.status in [models.Ownerstatus.BLOCKED,models.Ownerstatus.DELETED]:
        raise HTTPException(status_code=400,detail="failed to login")
    if owner.status != models.Ownerstatus.ACTIVED:
        raise HTTPException(status_code=402,detail="user not activate")
    
    access_token_expires = timedelta(minutes=Config.ACCESS_TOKEN_EXPIRE_MINUTES)
    return{
        "owner" : owner,
        "token" : {
            "access_token" : create_access_token(
                owner.uuid,expires_delta=access_token_expires
            ),
           "token_type" : "bearer" 
        }
    }

@router.post("/start-reset-password/owners",response_model=schemas.Msg)
def start_reset_password(
    obj_in:schemas.ResetPasswordOption1Step1,
    db:Session=Depends(get_db)  
):
    owner = crud.owners.get_by_email(db=db,email=obj_in.email)
    if not owner:
        raise HTTPException(status_code=404,detail="user not found")
    code = generate_code(length=12)
    code = str(code[0:5])
    # code = "0000"
    print(f"Code generate",code)
    owner.otp_password = code
    owner.otp_password_expired_at = datetime.now() + timedelta(minutes=20)
    db.commit()
    db.refresh(owner)
    send_start_reset_password(email_to=obj_in.email, name=f"{owner.first_name} {owner.last_name}", code=code)
    return schemas.Msg(message="reset password started succesfully")


@router.post("/check-otp-password/owners",response_model=schemas.Msg)
def check_otp_password(
    obj_in:schemas.ResetPasswordOption2Step2,
    db:Session=Depends(get_db) 
):
    owner = crud.owners.get_by_email(db=db,email=obj_in.email)
    if not owner:
        raise HTTPException(status_code=404,detail="user not found")
    if owner.otp_password != obj_in.otp:
        raise HTTPException(status_code=400,detail="otp invalid")
    if owner.otp_password_expired_at < datetime.now():
        raise HTTPException(status_code=400,detail="otp expired")
    return schemas.Msg(message="otp valid")

@router.post("/reset-password/owners",response_model=schemas.Msg)
def reset_password(
    obj_in:schemas.ResetPasswordOption3Step3,
    db:Session=Depends(get_db) 

):
    owner = crud.owners.get_by_email(db=db,email=obj_in.email)
    if not owner:
        raise HTTPException(status_code=404,detail="user not found")
    if owner.otp_password != obj_in.otp:
        raise HTTPException(status_code=400,detail="otp invalid")
    if owner.otp_password_expired_at < datetime.now():
        raise HTTPException(status_code=400,detail="otp expired")
    if not is_valid_password(password=obj_in.new_password):
        raise HTTPException(status_code=400,detail="Invalid password")
    owner.password_hash = get_password_hash(password=obj_in.new_password)
    owner.otp_password=None
    owner.otp_password_expired_at=None
    db.commit()
    db.refresh(owner)
    return schemas.Msg(message="password reset successfully")
    
    

@router.post("/profile/owners",response_model=schemas.OwnerProfile)
def get_current_user(
    current_user : any = Depends(OwnersTokenRequired())

):
    return current_user




@router.post("/login/owners",response_model=schemas.OwnerAuthentification)
def login(
    obj_in:schemas.OwnerLogin,
    db:Session=Depends(get_db)
):
    owner=crud.owners.authenticate(
        db=db,email=obj_in.email,password=obj_in.password

    )
    if not owner:
        raise HTTPException(status_code=404,detail="user not found")
    if owner.status in [models.Ownerstatus.BLOCKED,models.Ownerstatus.DELETED]:
        raise HTTPException(status_code=400,detail="failed to login")
    if owner.status != models.Ownerstatus.ACTIVED:
        raise HTTPException(status_code=402,detail="user not activate")
    
    access_token_expires = timedelta(minutes=Config.ACCESS_TOKEN_EXPIRE_MINUTES)
    return{
        "owner" : owner,
        "token" : {
            "access_token" : create_access_token(
                owner.uuid,expires_delta=access_token_expires
            ),
           "token_type" : "bearer" 
        }
    }

@router.post("/start-reset-password/owners",response_model=schemas.Msg)
def start_reset_password(
    obj_in:schemas.ResetPasswordOption1Step1,
    db:Session=Depends(get_db)  
):
    owner = crud.owners.get_by_email(db=db,email=obj_in.email)
    if not owner:
        raise HTTPException(status_code=404,detail="user not found")
    code = generate_code(length=12)
    code = str(code[0:5])
    # code = "0000"
    print(f"Code generate",code)
    owner.otp_password = code
    owner.otp_password_expired_at = datetime.now() + timedelta(minutes=20)
    db.commit()
    db.refresh(owner)
    send_start_reset_password(email_to=obj_in.email, name=f"{owner.first_name} {owner.last_name}", code=code)
    return schemas.Msg(message="reset password started succesfully")


@router.post("/check-otp-password/owners",response_model=schemas.Msg)
def check_otp_password(
    obj_in:schemas.ResetPasswordOption2Step2,
    db:Session=Depends(get_db) 
):
    owner = crud.owners.get_by_email(db=db,email=obj_in.email)
    if not owner:
        raise HTTPException(status_code=404,detail="user not found")
    if owner.otp_password != obj_in.otp:
        raise HTTPException(status_code=400,detail="otp invalid")
    if owner.otp_password_expired_at < datetime.now():
        raise HTTPException(status_code=400,detail="otp expired")
    return schemas.Msg(message="otp valid")

@router.post("/reset-password/owners",response_model=schemas.Msg)
def reset_password(
    obj_in:schemas.ResetPasswordOption3Step3,
    db:Session=Depends(get_db) 

):
    owner = crud.owners.get_by_email(db=db,email=obj_in.email)
    if not owner:
        raise HTTPException(status_code=404,detail="user not found")
    if owner.otp_password != obj_in.otp:
        raise HTTPException(status_code=400,detail="otp invalid")
    if owner.otp_password_expired_at < datetime.now():
        raise HTTPException(status_code=400,detail="otp expired")
    if not is_valid_password(password=obj_in.new_password):
        raise HTTPException(status_code=400,detail="Invalid password")
    owner.password_hash = get_password_hash(password=obj_in.new_password)
    owner.otp_password=None
    owner.otp_password_expired_at=None
    db.commit()
    db.refresh(owner)
    return schemas.Msg(message="password reset successfully")
    
    

@router.post("/profile/owners",response_model=schemas.OwnerProfile)
def get_current_user(
    current_user : any = Depends(OwnersTokenRequired())

):
    return current_user







