from typing import Optional
from pydantic import BaseModel, ConfigDict, EmailStr
from datetime import datetime
from app.main.schemas import UserAuthentication, File, DataList
from app.main.schemas.address import AddressSlim
from app.main.schemas.user import AddedBy
from app.main.models.companies import CompanyStatus,CompanyType
from app.main.schemas.file import FileSlim1

class CompanyBase(BaseModel):
    name:str
    email:str
    phone:str
    description:str
    slogan:str
    address_uuid:str
    logo_uuid:Optional[str]=None
    signature_uuid:Optional[str]=None
    stamp_uuid:Optional[str]=None
    founded_at:datetime
    employee_count:int
    type:CompanyType
    model_config = ConfigDict(from_attributes=True)

class CompanyCreate(CompanyBase):
    pass


class CompanyUpdate(BaseModel):
    uuid:Optional[str]=None
    name:Optional[str]=None
    email:Optional[str]=None
    phone:Optional[str]=None
    description:Optional[str]=None
    slogan:Optional[str]=None
    address:Optional[str]=None
    logo_uuid:Optional[str]=None
    signature_uuid:Optional[str]=None
    stamp_uuid:Optional[str]=None
    founded_at:Optional[datetime]=None
    employee_count:Optional[int]=None
    type:Optional[CompanyType]=None
    model_config = ConfigDict(from_attributes=True)

class CompanyDelete(BaseModel):
    uuid:str

class CompanyResponse(BaseModel):
    uuid:Optional[str]=None
    name:Optional[str]=None
    email:Optional[str]=None
    phone:Optional[str]=None
    description:Optional[str]=None
    slogan:Optional[str]=None
    address:Optional[AddressSlim]=None
    logo:Optional[FileSlim1]=None
    signature:Optional[FileSlim1]=None
    stamp:Optional[FileSlim1]=None
    owner:Optional[AddedBy]=None
    founded_at:Optional[datetime]=None
    employee_count:Optional[int]=None
    type:Optional[CompanyType]=None
    model_config = ConfigDict(from_attributes=True)


class CompanyResponseList(BaseModel):
    total: int
    pages: int
    per_page: int
    current_page:int
    data: list[CompanyResponse]

    model_config = ConfigDict(from_attributes=True)