from typing import Optional
from datetime import date
from pydantic import BaseModel

class StaffBase(BaseModel):
    name: str
    email: str
    mobile: str
    department: Optional[str] = None
    designation: str
    join_date: date
    shift_id: Optional[int] = None
    is_active: bool = True

class StaffCreate(StaffBase):
    pass

class StaffRead(StaffBase):
    id: int
    user_id: Optional[int] = None

class StaffUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    mobile: Optional[str] = None
    department: Optional[str] = None
    designation: Optional[str] = None
    shift_id: Optional[int] = None
    is_active: Optional[bool] = None
