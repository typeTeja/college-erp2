from pydantic import BaseModel
from typing import Optional

class FacultyBase(BaseModel):
    name: str
    department: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    qualification: Optional[str] = None
    designation: Optional[str] = None
    max_weekly_hours: int = 20

class FacultyCreate(FacultyBase):
    pass

class FacultyRead(FacultyBase):
    id: int
    user_id: Optional[int] = None
    class Config:
        from_attributes = True
