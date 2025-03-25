
from typing import List, Optional
from pydantic import BaseModel, ConfigDict
from datetime import datetime
from app.main.schemas.company import CompanyResponseAdmin, CompanyResponseSlim1
from app.main.schemas.feature import TypeAbonnementWithFeaturesSlim
from app.main.schemas.file import FileSlim1
from app.main.schemas.owners import OwnerResponse
from app.main.schemas.type_abonnement import TypeAbonnementResponse
from app.main.schemas.user import UserBase

class AbonnementBase(BaseModel):
    company_uuid:str
    type_abonnement_uuid:str


class AbonnemmentCreate(AbonnementBase):
    pass

class AbonnementResponseSlim1(BaseModel):
    type_abonnement:TypeAbonnementWithFeaturesSlim
    date_added:datetime
    date_modified:datetime
    model_config = ConfigDict(from_attributes=True)


class AbonnementResponseSlim2(BaseModel):
    company:CompanyResponseSlim1
    owner:OwnerResponse
    type_abonnement:TypeAbonnementResponse
    date_added:datetime
    date_modified:datetime
    model_config = ConfigDict(from_attributes=True)