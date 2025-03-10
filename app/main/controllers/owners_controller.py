import enum
from typing import Optional
import uuid
from sqlalchemy.orm import Session
from app.main import models , schemas,crud
from fastapi import HTTPException, Query,status,APIRouter,Depends,BackgroundTasks
from app.main.core.dependencies import get_db
from app.main.crud.base import CRUDBase
from app.main.core.i18n import __
from app.main.core.dependencies import get_db,TokenRequired

router = APIRouter(prefix="/owners",tags=["owners"])


@router.post("/create",response_model=schemas.Msg)
def create_owners(
    *,
    db : Session=Depends(get_db),
    obj_in:schemas.OwnerCreate,
    background_tasks:BackgroundTasks
):
    exist_email = crud.owners.get_by_email(db=db,email=obj_in.email)
    if exist_email:
        raise HTTPException(status_code=409,detail="Email is already exist")
    exist_phone_number = crud.owners.get_by_phone_number(db=db,phone_number=obj_in.phone_number)
    if exist_phone_number:
        raise HTTPException(status_code=409,detail="Phone number is already exist")
    
    if obj_in.avatar_uuid:
        avatar = crud.storage_crud.get_file_by_uuid(db=db,file_uuid=obj_in.avatar_uuid)
        if not avatar:
            raise HTTPException(status_code=404,detail="Avatar not found")
        
    crud.owners.create(db=db,obj_in=obj_in,background_tasks=background_tasks)
    return schemas.Msg(message="Your account created succesfully")





@router.put("/update-owner-status",response_model=schemas.Msg)
def update_status(
    *,
    db: Session = Depends(get_db),
    obj_in:schemas.UpdateOwnerStatus,
    status : str = Query(...,enum=["ACTIVED","UNACTIVED","DELETED","BLOCKED"]),
    current_user : models.User = Depends(TokenRequired(roles=["SUPER_ADMIN"]))
):
    crud.owners.update_status_owner(db=db,uuid=obj_in.uuid,status=status)
    return schemas.Msg(message=__("Status update successfully"))






# @router.put("/delete",response_model=schemas.Msg)
# def delete_owners(
#     *,
#     db : Session=Depends(get_db),
#     uuid:str,
#     current_user : models.User = Depends(TokenRequired(roles=["SUPER_ADMIN"]))

# ):
#     crud.owners.delete(db=db,uuid=uuid)
#     return schemas.Msg(message=__(key="Owner delete successfully"))





# @router.put("/activate",response_model=schemas.Msg)
# def activate_owners(
#     *,
#     db : Session=Depends(get_db),
#     uuid:str,
#     current_user : models.User = Depends(TokenRequired(roles=["SUPER_ADMIN"]))

# ):
#     crud.owners.activate(db=db,uuid=uuid)
#     return schemas.Msg(message=__(key="Owner activate successfully"))




# @router.put("/blocked",response_model=schemas.Msg)
# def blocked_owners(
#     *,
#     db : Session=Depends(get_db),
#     uuid:str,
#     current_user : models.User = Depends(TokenRequired(roles=["SUPER_ADMIN"]))

# ):
#     crud.owners.blocked(db=db,uuid=uuid)
#     return schemas.Msg(message=__(key="Owner blocked successfully"))





# @router.put("/deactivate",response_model=schemas.Msg)
# def deactivate_owners(
#     *,
#     db : Session=Depends(get_db),
#     uuid:str,
#     current_user : models.User = Depends(TokenRequired(roles=["SUPER_ADMIN"]))

# ):
#     crud.owners.deactivate(db=db,uuid=uuid)
#     return schemas.Msg(message=__(key="Owner deactivate successfully"))













