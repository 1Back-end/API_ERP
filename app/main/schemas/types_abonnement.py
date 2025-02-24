from typing import Optional
from pydantic import BaseModel, ConfigDict, EmailStr
from datetime import datetime
from app.main.schemas.user import AddedBy

class TypeAbonnementBase(BaseModel):
    name:str
    price:float

class TypeAbonnementCreate(TypeAbonnementBase):
    pass

class TypeAbonnementUpdate(BaseModel):
    uuid:str
    name : Optional[str]=None
    price : Optional[float]=None

class TypeAbonnementDelete(BaseModel):
    uuid:str

class TypeAbonnementResponse(BaseModel):
    uuid:str
    name:str
    price : float
    date_added:datetime
    date_modified:datetime
    added_by:Optional[AddedBy]
    model_config = ConfigDict(from_attributes=True)

class TypeAbonnementSlim1(BaseModel):
    uuid:str
    name:str
    price : float
    date_added:datetime
    date_modified:datetime
    model_config = ConfigDict(from_attributes=True)

