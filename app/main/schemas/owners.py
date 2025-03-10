from pydantic import BaseModel,EmailStr,ConfigDict
from typing import Optional
from app.main.models.user import UserRole
from datetime import datetime

from app.main.schemas.file import FileSlim1


class OwnerBase(BaseModel):
    email:EmailStr
    country_code:str
    phone_number:str
    first_name:str
    last_name :str
    password_hash:str
    avatar_uuid:Optional[str]=None


class OwnerCreate(OwnerBase):
    pass

class OwnerResponse(BaseModel):
    uuid:str
    email:EmailStr
    country_code:str
    phone_number:str
    first_name:str
    last_name:str
    status:str
    avatar:Optional[FileSlim1]=None
    date_added:datetime
    date_modified:datetime
    model_config = ConfigDict(from_attributes=True)

    

class OwnerDetails(BaseModel):
    uuid:str

class OwnerDelete(BaseModel):
    uuid:str


class OwnerProfile(BaseModel):
    uuid:str
    email:EmailStr
    country_code:str
    phone_number:str
    first_name:str
    last_name:str
    model_config = ConfigDict(from_attributes=True)



class Token(BaseModel):
    access_token: str  # Assurez-vous que ce soit une chaîne de caractères non optionnelle
    token_type: str    # Assurez-vous que ce soit une chaîne de caractères non optionnelle
    model_config = ConfigDict(from_attributes=True)



class OwnerLogin(BaseModel):
    email:EmailStr
    password:str

class OwnerAuthentification(BaseModel):
    owner: OwnerProfile
    token: Token  # Assurez-vous que ce soit de type `Token`
    model_config = ConfigDict(from_attributes=True)

class ResetPasswordOption1Step1(BaseModel):
    email:EmailStr

class ResetPasswordOption2Step2(BaseModel):
    email:EmailStr
    otp:str
    
class ResetPasswordOption3Step3(BaseModel):
    email:EmailStr
    otp:str
    new_password:str


class UpdateOwnerStatus(BaseModel):
    uuid:str