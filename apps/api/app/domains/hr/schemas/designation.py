from typing import Optional
from datetime import datetime
from pydantic import BaseModel

class DesignationBase(BaseModel):
    name: str
    code: str
    level: int = 1
    department_id: Optional[int] = None
    min_experience_years: int = 0
    min_qualification: Optional[str] = None
    is_teaching: bool = True
    is_active: bool = True
    display_order: int = 0

class DesignationCreate(DesignationBase):
    pass

class DesignationRead(DesignationBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
