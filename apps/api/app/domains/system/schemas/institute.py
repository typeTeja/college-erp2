from typing import Optional
from pydantic import BaseModel

class InstituteInfoBase(BaseModel):
    name: str
    short_code: Optional[str] = None
    address: Optional[str] = None
    contact_email: Optional[str] = None
    contact_phone: Optional[str] = None
    logo_url: Optional[str] = None

class InstituteInfoCreate(InstituteInfoBase):
    pass

class InstituteInfoRead(InstituteInfoBase):
    id: int

    class Config:
        from_attributes = True
