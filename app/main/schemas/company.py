from pydantic import BaseModel,ConfigDict,EmailStr
from datetime import datetime
from typing import List, Optional

from app.main.models.companies import CompanyType
from app.main.schemas.adress import AddressSlim
from app.main.schemas.file import FileSlim
from app.main.schemas.owners import OwnerResponse


class CompanyBase(BaseModel):
    name:str
    email:EmailStr
    country_code:str
    phone_number:str
    description:Optional[str]=None
    slogan:str
    address_uuid:str
    logo_uuid:Optional[str]=None
    signature_uuid:Optional[str]=None
    stamp_uuid:Optional[str]=None
    founded_at:datetime
    employee_count:int
    website:Optional[str]=None
    type:CompanyType


class CompanyCreate(CompanyBase):
    pass

class CompanyUpdate(BaseModel):
    uuid:str
    name:Optional[str]=None
    email:Optional[EmailStr]=None
    country_code:Optional[str]=None
    phone_number:Optional[str]=None
    description:Optional[str]=None
    slogan:Optional[str]=None
    address_uuid:Optional[str]=None
    logo_uuid:Optional[str]=None
    signature_uuid:Optional[str]=None
    stamp_uuid:Optional[str]=None
    founded_at:Optional[datetime]=None
    employee_count:Optional[int]=None
    website:Optional[str]=None
    type:Optional[CompanyType]=None


class CompanyResponse(BaseModel):
    uuid:str
    name:str
    email:EmailStr
    country_code:str
    phone_number:str
    full_phone_number:str
    description:Optional[str]=None
    slogan:str
    address:AddressSlim
    logo:Optional[FileSlim]=None
    signature:Optional[FileSlim]=None
    stamp:Optional[FileSlim]=None
    founded_at:datetime
    employee_count:int
    type:str
    status:str
    website:Optional[str]=None
    created_at:datetime
    updated_at:datetime
    model_config = ConfigDict(from_attributes=True)


class CompanyResponseAdmin(BaseModel):
    uuid:str
    name:str
    email:EmailStr
    country_code:str
    phone_number:str
    full_phone_number:str
    description:Optional[str]=None
    slogan:str
    address:AddressSlim
    logo:Optional[FileSlim]=None
    signature:Optional[FileSlim]=None
    stamp:Optional[FileSlim]=None
    owner:OwnerResponse
    founded_at:datetime
    employee_count:int
    type:str
    status:str
    website:Optional[str]=None
    created_at:datetime
    updated_at:datetime
    model_config = ConfigDict(from_attributes=True)
    
class CompanyResponseList(BaseModel):
    total:int
    pages:int
    per_page:int
    current_page :int
    data : List[CompanyResponse]

    model_config = ConfigDict(from_attributes=True)

class CompanyResponseListAdmin(BaseModel):
    total:int
    pages:int
    per_page:int
    current_page :int
    data : List[CompanyResponseAdmin]

    model_config = ConfigDict(from_attributes=True)


class UpdateCompanyStatus(BaseModel):
    uuid:str