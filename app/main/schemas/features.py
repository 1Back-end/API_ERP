from typing import List, Optional
from pydantic import BaseModel, ConfigDict
from datetime import datetime
from app.main.schemas.types_abonnement import TypeAbonnementSlim2
from app.main.schemas.user import AddedBy

class Feature(BaseModel):
    name:str
    description:Optional[str]=None
class FeatureCreate(Feature):
    pass

class FeatureDelete(BaseModel):
    uuid:str


class FeatureCreateResquest(BaseModel):
    type_abonnement_uuid:str
    features : List[FeatureCreate]
    model_config = ConfigDict(from_attributes=True)


class FeatureUpdate(BaseModel):
    uuid:str
    name:Optional[str]=None
class FeatureUpdateResquest(BaseModel):
    type_abonnement_uuid:Optional[str]=None
    features : List[FeatureUpdate]=None
    model_config = ConfigDict(from_attributes=True)

class FeatureDelete(BaseModel):
    uuid:str

class FeatureSlim(BaseModel):
    uuid:str
    name:str
class FeatureResponse(FeatureSlim):
    type_abonnement:Optional[TypeAbonnementSlim2]
    added_by:Optional[AddedBy]
    model_config = ConfigDict(from_attributes=True)

class FeatureResponseSlim1(BaseModel):
    uuid:str
    name:str
    is_active:bool
    date_added:datetime
    date_modified:datetime




class TypeAbonnementWithFeatures(BaseModel):
    uuid: str
    name: str
    price: int
    features: List[FeatureResponse]  # Liste des fonctionnalités associées
    added_by: Optional[AddedBy]

    model_config = ConfigDict(from_attributes=True)