from pydantic import BaseModel,EmailStr,ConfigDict
from typing import List, Optional
from app.main.models.user import UserRole
from datetime import datetime
from app.main.schemas.file import FileSlim1
from app.main.schemas.user import UserBase


class TypeAbonnementBase(BaseModel):
    name:str
    price : int
    currency : str
    start_date:datetime
    end_date:datetime


class TypeAbonnementCreate(TypeAbonnementBase):
    pass

class TypeAbonnementUpdate(BaseModel):
    uuid:str
    name:Optional[str]=None
    price:Optional[int]=None
    currency:Optional[str]=None
    start_date:Optional[datetime]=None
    end_date:Optional[datetime]=None

class TypeAbonnementResponse(BaseModel):
    uuid:str
    name:str
    full_price:str
    start_date:datetime
    end_date:datetime
    added_by:UserBase
    date_added:datetime
    date_modified:datetime
    model_config = ConfigDict(from_attributes=True)

class TypeAbonnementResponseList(BaseModel):
    total:int
    pages:int
    per_page:int
    current_page :int
    data : List[TypeAbonnementResponse]

    model_config = ConfigDict(from_attributes=True)

