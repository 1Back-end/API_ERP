from typing import Optional
from pydantic import BaseModel, ConfigDict
from datetime import datetime
from app.main.schemas.types_abonnement import TypeAbonnementSlim1
from app.main.schemas.user import AddedBy

class Feature(BaseModel):
    name:str
    description:Optional[str]=None
    type_abonnement_uuid:str

class FeatureCreate(Feature):
    pass

class FeatureDelete(BaseModel):
    uuid:str

class FeatureUpdate(BaseModel):
    name :Optional[str]=None
    description:Optional[str]=None
    type_abonnement_uuid:Optional[str]=None

class FeatureResponse(BaseModel):
    name :Optional[str]=None
    description:Optional[str]=None
    type_abonnement:Optional[TypeAbonnementSlim1]
    added_by:Optional[AddedBy]
    model_config = ConfigDict(from_attributes=True)
