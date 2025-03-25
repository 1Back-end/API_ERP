import enum
from typing import Optional
import uuid
from sqlalchemy.orm import Session
from app.main import models , schemas,crud
from fastapi import HTTPException, Query,status,APIRouter,Depends,BackgroundTasks
from app.main.core.dependencies import TokenRequired, get_db
from app.main.crud.base import CRUDBase
from app.main.core.i18n import __
from app.main.core.dependencies import get_db,OwnersTokenRequired

router = APIRouter(prefix="/company",tags=["company"])

@router.post("/create",response_model=schemas.Msg)
def create_company(
    *,
    db : Session=Depends(get_db),
    obj_in:schemas.CompanyCreate,
    current_user:models.Owner = Depends(OwnersTokenRequired())
):
    exist_name = crud.CRUDCompany.get_by_name(db=db,name=obj_in.name)
    if exist_name:
        raise HTTPException(status_code=409,detail="Name is already exist")
    exist_email = crud.CRUDCompany.get_by_email(db=db,email=obj_in.email)
    if exist_email:
        raise HTTPException(status_code=409,detail="Email is already exist")
    exist_phone_number = crud.CRUDCompany.get_by_phone_number(db=db,phone_number=obj_in.phone_number)
    if exist_phone_number:
        raise HTTPException(status_code=409,detail="Phone number is already exist")
    
    added_by = current_user.uuid
    
    
    crud.company.create(db=db,obj_in=obj_in,added_by=added_by)
    return schemas.Msg(message=__("Company create successfully"))

@router.put("/update",response_model=schemas.Msg)
def update_company(
    *,
    db : Session=Depends(get_db),
    obj_in:schemas.CompanyUpdate,
    current_user : models.User = Depends(TokenRequired(roles=["SUPER_ADMIN"]))
):
    exist_name = crud.CRUDCompany.get_by_name(db=db,name=obj_in.name)
    if exist_name:
        raise HTTPException(status_code=409,detail="Name is already exist")
    exist_email = crud.CRUDCompany.get_by_email(db=db,email=obj_in.email)
    if exist_email:
        raise HTTPException(status_code=409,detail="Email is already exist")
    exist_phone_number = crud.CRUDCompany.get_by_phone_number(db=db,phone_number=obj_in.phone_number)
    if exist_phone_number:
        raise HTTPException(status_code=409,detail="Phone number is already exist")
    
    added_by = current_user.uuid
    crud.company.update_company(db=db,obj_in=obj_in,added_by=added_by)
    return schemas.Msg(message=__("Company updated successfully"))

# @router.put("/delete",response_model=schemas.Msg)
# def delete_company(
#     *,
#     db : Session=Depends(get_db),
#     uuid:str,
#     current_company : models.Company = Depends(TokenRequired(roles=["ADMIN"]))

# ):

# @router.put("/activate",response_model=schemas.Msg)
# def activate_company(
#     *,
#     db : Session=Depends(get_db),
#     uuid:str,
#     current_user : models.User = Depends(TokenRequired(roles=["SUPER_ADMIN","ADMIN"]))

# ):
#     crud.company.activate(db=db,uuid=uuid)
#     return schemas.Msg(message=__(key="company activate successfully"))


# @router.put("/deactivate",response_model=schemas.Msg)
# def deactivate_company(
#     *,
#     db : Session=Depends(get_db),
#     uuid:str,
#     current_user : models.User = Depends(TokenRequired(roles=["SUPER_ADMIN"]))

# ):
#     crud.company.deactivate(db=db,uuid=uuid)
#     return schemas.Msg(message=__(key="company deactivate successfully"))

# router.put("/blocked",response_model=schemas.Msg)
# def blocked_company(
#     *,
#     db : Session=Depends(get_db),
#     uuid:str,
#     current_user : models.User = Depends(TokenRequired(roles=["SUPER_ADMIN"]))

# ):
#     crud.company.blocked(db=db,uuid=uuid)
#     return schemas.Msg(message=__(key="Owner blocked successfully"))
# @router.put("/update",response_model=schemas.CompanyResponse)
# def update_company(
#     *,
#     db : Session=Depends(get_db),
#     uuid:str,
#     obj_in:schemas.CompanyUpdate,
#     current_company : models.Company = Depends(TokenRequired(roles=["ADMIN"]))

# ):
#     return crud.CRUDCompany.update(db=db,uuid=uuid,obj_in=obj_in)



@router.get("/get_company/owners", response_model=None)
def list_companies(
    *,
    db: Session = Depends(get_db),
    page: int =  1,
    per_page: int = 30,
    order:str= Query(None,enum=["ASC","DESC"]),
    order_field: Optional[str] = None,
    keyword: Optional[str] = None,
    status : str = Query(...,enum=[st.value for st in models.CompanyStatus]),
    type : str = Query(...,enum=[st.value for st in models.CompanyType]),
    current_user : models.Owner = Depends(OwnersTokenRequired())
):
    return crud.company.get_many_company_owner(
        db=db,
        page=page,
        per_page=per_page,
        order=order,
        order_field=order_field,
        keyword=keyword,
        status=status,
        type=type,
        owner_uuid=current_user.uuid
    )

@router.put("/update-company-status",response_model=schemas.Msg)
def update_status(
    *,
    db: Session = Depends(get_db),
    obj_in:schemas.UpdateCompanyStatus,
    status : str = Query(...,enum=[st.value for st in models.CompanyStatus]),
    current_user : models.User = Depends(TokenRequired(roles=["SUPER_ADMIN"]))
):
    crud.company.update_status_company(db=db,uuid=obj_in.uuid,status=status)
    return schemas.Msg(message=__("Status update successfully"))


@router.get("/get_company/admin", response_model=None)
def list_companies(
    *,
    db: Session = Depends(get_db),
    page: int =  1,
    per_page: int = 30,
    order:str= Query(None,enum=["ASC","DESC"]),
    order_field: Optional[str] = None,
    keyword: Optional[str] = None,
    status : str = Query(...,enum=[st.value for st in models.CompanyStatus]),
    type : str = Query(...,enum=[st.value for st in models.CompanyType]),
    current_user: models.User = Depends(TokenRequired(roles=["SUPER_ADMIN","ADMIN"]))
):
    return crud.company.get_many_company_admin(
        db=db,
        page=page,
        per_page=per_page,
        order=order,
        order_field=order_field,
        keyword=keyword,
        status=status,
        type=type,
    )