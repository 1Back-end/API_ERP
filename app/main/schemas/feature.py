
from typing import List, Optional
from pydantic import BaseModel, ConfigDict
from datetime import datetime
from app.main.schemas.file import FileSlim1
from app.main.schemas.type_abonnement import TypeAbonnementResponse
from app.main.schemas.user import UserBase


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
    description:Optional[str]=None

class FeatureUpdateResquest(BaseModel):
    type_abonnement_uuid:Optional[str]=None
    features : List[FeatureUpdate]=None
    model_config = ConfigDict(from_attributes=True)



class FeatureSlim(BaseModel):
    uuid:str
    name:str
    description:Optional[str]=None
    # type_abonnement:Optional[TypeAbonnementResponse]=None
    # added_by:Optional[UserBase]
    is_active:bool
    date_added:datetime
    date_modified:datetime
    model_config = ConfigDict(from_attributes=True)

class TypeAbonnementWithFeatures(BaseModel):
    uuid: str
    name: str
    price: int
    features: List[FeatureSlim]  # Liste des fonctionnalités associées
    added_by: Optional[UserBase]

    model_config = ConfigDict(from_attributes=True)

class TypeAbonnementWithFeaturesSlim(BaseModel):
    uuid:str
    name:str
    full_price:str
    start_date:datetime
    end_date:datetime
    features: List[FeatureSlim]  # Liste des fonctionnalités associées
    model_config = ConfigDict(from_attributes=True)

class FeaturesResponseList(BaseModel):
    total:int
    pages:int
    per_page:int
    current_page :int
    data : List[FeatureSlim]

    model_config = ConfigDict(from_attributes=True)

