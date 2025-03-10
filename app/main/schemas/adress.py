from pydantic import BaseModel,ConfigDict
from datetime import datetime
from typing import List, Optional


class AddressSlim(BaseModel):
    street:str
    city:str
    state:str
    zipcode:str
    country:str
    model_config = ConfigDict(from_attributes=True)


class AddressBase(BaseModel):
    street:str
    city:str
    state:str
    zipcode:str
    country:str
    apartment_number:str
    additional_information:str

class AddressCreate(AddressBase):
    pass


class AddressUpdate(BaseModel):
    uuid:str
    street:Optional[str]=None
    city:Optional[str]=None
    state:Optional[str]=None
    country:Optional[str]=None
    zipcode:Optional[str]=None
    apartment_number:Optional[str]=None
    additional_information:Optional[str]=None


class AddressResponse(AddressBase):
    uuid:str
    date_added:datetime
    date_modified:datetime
    model_config = ConfigDict(from_attributes=True)


class AddressDelete(BaseModel):
    uuid:str

class AddressDetail(BaseModel):
    uuid:str

class AddressResponseList(BaseModel):
    total : int
    pages:int
    per_page:int
    current_page:int
    data : List[AddressResponse]
    model_config = ConfigDict(from_attributes=True)