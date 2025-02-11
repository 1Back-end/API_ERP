from pydantic import BaseModel,EmailStr,ConfigDict
from typing import Optional
from app.main.models.user import UserRole
from datetime import datetime

class UserBase(BaseModel):
    email:EmailStr
    phone_number:str
    first_name:str
    last_name :str
    password_hash : str
    role:UserRole

class UserCreate(UserBase):
    pass

class UserUpdate(BaseModel):
    uuid:str
    email:Optional[EmailStr]=None
    phone_number:Optional[str]=None
    first_name:Optional[str]=None
    last_name:Optional[str]=None
    role:Optional[UserRole]=None

class UserDelete(BaseModel):
    uuid:str

class UserResponse(UserBase):
    uuid:str
    status:str
    created_at:datetime
    updated_at:str


class UserLogin(BaseModel):
    email:EmailStr
    password:str


class Token(BaseModel):
    access_token: str  # Assurez-vous que ce soit une chaîne de caractères non optionnelle
    token_type: str    # Assurez-vous que ce soit une chaîne de caractères non optionnelle
    model_config = ConfigDict(from_attributes=True)

class UserAuthentification(BaseModel):
    user: UserResponse
    token: Token  # Assurez-vous que ce soit de type `Token`
    model_config = ConfigDict(from_attributes=True)
