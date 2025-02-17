from datetime import timedelta, datetime
from typing import Any
from fastapi import APIRouter, Depends, Body, HTTPException
from sqlalchemy.orm import Session
from app.main.core.dependencies import get_db, TokenRequired
from app.main import schemas, crud, models
from app.main.core.i18n import __
from app.main.core.security import create_access_token, get_password_hash
from app.main.core.config import Config
from app.main.core.dependencies import TokenRequired

router = APIRouter(prefix="", tags=["users"])


@router.post("/login",  response_model=schemas.UserAuthentication)
async def login(
        country_code: str = Body(...),
        phone_number: str = Body(...),
        password: str = Body(...),
        db: Session = Depends(get_db),
) -> Any:
    """
    Sign in with phone number and password
    """
    user = crud.user.authenticate(
        db, phone_number=f"{country_code}{phone_number}", password=password
    )
    if not user:
        raise HTTPException(status_code=400, detail=__(key="auth-login-failed"))

    if user.status in [models.UserStatus.BLOCKED, models.UserStatus.DELETED]:
        raise HTTPException(status_code=400, detail=__(key="auth-login-failed"))

    if user.status != models.UserStatus.ACTIVED:
        raise HTTPException(status_code=402, detail=__(key="user-not-activated"))

    access_token_expires = timedelta(minutes=Config.ACCESS_TOKEN_EXPIRE_MINUTES)

    return {
        "user": user,
        "token": {
            "access_token": create_access_token(
                user.uuid, expires_delta=access_token_expires
            ),
            "token_type": "bearer",
        }
    }


@router.post("/register",response_model=schemas.Msg)
def register(
    *,
    db: Session = Depends(get_db),
    obj_in:schemas.UserCreate,
    current_user: models.User = Depends(TokenRequired(roles=["SUPER_ADMIN"]))
):
    exist_phone = crud.user.get_by_phone_number(db=db, phone_number=f"{obj_in.country_code}{obj_in.phone_number}")
    if exist_phone:
        raise HTTPException(status_code=409, detail=__(key="phone_number-already-used"))

    exist_email = crud.user.get_by_email(db=db, email=obj_in.email)
    if exist_email:
        raise HTTPException(status_code=409, detail=__(key="email-already-used"))
    crud.user.create(
        db, obj_in=obj_in
    )
    return schemas.Msg(message=__(key="user-created-successfully"))

@router.post("/start-reset-password", response_model=schemas.Msg)
def start_reset_password(
        country_code: str = Body(...),
        phone_number: str = Body(...),
        db: Session = Depends(get_db),

) -> schemas.Msg:
    """
    Start reset password with phone number
    """
    user = crud.user.get_by_phone_number(db=db, phone_number=f"{country_code}{phone_number}")
    if not user:
        raise HTTPException(status_code=404, detail=__(key="user-not-found"))

    user.otp_password = "00000"
    user.otp_password_expired_at = datetime.now() + timedelta(minutes=20)
    db.commit()
    db.refresh(user)

    return schemas.Msg(message=__(key="reset-password-started"))

@router.post("/check-otp-password", summary="Check OTP password", response_model=schemas.Msg)
def check_otp_password(
        country_code: str = Body(...),
        phone_number: str = Body(...),
        otp: str = Body(...),
        db: Session = Depends(get_db),
) -> schemas.Msg:
    """
    Check OTP password
    """
    user = crud.user.get_by_phone_number(db=db, phone_number=f"{country_code}{phone_number}")
    if not user:
        raise HTTPException(status_code=404, detail=__(key="user-not-found"))

    if user.otp_password != otp:
        raise HTTPException(status_code=400, detail=__(key="otp-invalid"))

    if user.otp_password_expired_at < datetime.now():
        raise HTTPException(status_code=400, detail=__(key="otp-expired"))

    return schemas.Msg(message=__(key="otp-valid"))

@router.post("/reset-password", summary="Reset password", response_model=schemas.Msg)
def reset_password(
        country_code: str = Body(...),
        phone_number: str = Body(...),
        otp: str = Body(...),
        password: str = Body(...),
        db: Session = Depends(get_db),
) -> schemas.Msg:
    """
    Reset password
    """
    user = crud.user.get_by_phone_number(db=db, phone_number=f"{country_code}{phone_number}")
    if not user:
        raise HTTPException(status_code=404, detail=__("user-not-found"))

    if user.otp_password != otp:
        raise HTTPException(status_code=400, detail=__("otp-invalid"))

    if user.otp_password_expired_at < datetime.now():
        raise HTTPException(status_code=400, detail=__("otp-expired"))

    user.password_hash = get_password_hash(password=password)
    user.otp_password = None
    user.otp_password_expired_at = None
    db.commit()
    db.refresh(user)

    return schemas.Msg(message=__(key="password-reset-successfully"))


@router.get("/me", summary="Get current user", response_model=schemas.UserDetail)
def get_current_user(
        current_user: models.User = Depends(TokenRequired()),
        db: Session = Depends(get_db),
) -> models.User:
    """
    Get current user
    """
    return current_user

@router.put("/actived/{uuid}", response_model=schemas.Msg)
def actived(
    uuid: str,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(TokenRequired(roles=["SUPER_ADMIN"]))
):
    # Appel de la fonction d'activation par UUID
    crud.user.actived_account(db=db, uuid=uuid)
    return schemas.Msg(message=__(key="user-account-activated-successfully"))


@router.put("/deactived/{uuid}", response_model=schemas.Msg)
def deactived(
    uuid: str,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(TokenRequired(roles=["SUPER_ADMIN"]))
):
    # Appel de la fonction d'activation par UUID
    crud.user.deactived_account(db=db, uuid=uuid)
    return schemas.Msg(message=__(key="user-account-deactivated-successfully"))

@router.put("/blocked/{uuid}", response_model=schemas.Msg)
def blocked(
    uuid: str,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(TokenRequired(roles=["SUPER_ADMIN"]))
):
    # Appel de la fonction d'activation par UUID
    crud.user.blocked_account(db=db, uuid=uuid)
    return schemas.Msg(message=__(key="user-account-blocked-successfully"))
    
@router.put("/deleted/{uuid}", response_model=schemas.Msg)
def delete(
    uuid: str,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(TokenRequired(roles=["SUPER_ADMIN"]))
):
    # Appel de la fonction d'activation par UUID
    crud.user.deleted_account(db=db, uuid=uuid)
    return schemas.Msg(message=__(key="user-account-deleted-successfully"))