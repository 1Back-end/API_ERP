from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional

from app.main.schemas.user import UserBase

class RenouvellementBase(BaseModel):
    company_uuid:str
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None

class RenouvellementCreate(RenouvellementBase):
    pass  # ✅ Ajout de "pass" pour éviter une erreur de syntaxe

class RenouvellementUpdate(RenouvellementBase):
    uuid:str  # ✅ Ajout de l'attribut "uuid" pour la mise à jour
    company_uuid:str
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None


class RenouvellementResponse(BaseModel):
    uuid:str
    company_uuid:str
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    added_by:UserBase
    date_added:datetime
    date_modified:datetime
    model_config = ConfigDict(from_attributes=True)
