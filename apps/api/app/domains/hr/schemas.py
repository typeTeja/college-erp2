"""
HR Domain Schemas

All Pydantic schemas for the HR domain including:
- Designation management
- Staff management
- Faculty management
"""

from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime, date


# ----------------------------------------------------------------------
# Department Schemas
# ----------------------------------------------------------------------

class DepartmentBase(BaseModel):
    name: str
    code: str
    alias: Optional[str] = None
    is_active: bool = True

class DepartmentRead(DepartmentBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


# ----------------------------------------------------------------------
# Shift Schemas
# ----------------------------------------------------------------------

class ShiftBase(BaseModel):
    name: str
    start_time: str
    end_time: str
    is_active: bool = True

class ShiftRead(ShiftBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


# ----------------------------------------------------------------------
# Designation Schemas
# ----------------------------------------------------------------------

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


class DesignationUpdate(BaseModel):
    name: Optional[str] = None
    code: Optional[str] = None
    level: Optional[int] = None
    department_id: Optional[int] = None
    min_experience_years: Optional[int] = None
    min_qualification: Optional[str] = None
    is_teaching: Optional[bool] = None
    is_active: Optional[bool] = None
    display_order: Optional[int] = None


class DesignationRead(DesignationBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


# ----------------------------------------------------------------------
# Staff Schemas
# ----------------------------------------------------------------------

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


class StaffUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    mobile: Optional[str] = None
    department: Optional[str] = None
    designation: Optional[str] = None
    shift_id: Optional[int] = None
    is_active: Optional[bool] = None


class StaffRead(StaffBase):
    id: int
    user_id: Optional[int] = None
    
    class Config:
        from_attributes = True


# ----------------------------------------------------------------------
# Faculty Schemas
# ----------------------------------------------------------------------

class SubjectShort(BaseModel):
    """Minimal subject info for faculty response"""
    id: int
    code: str
    name: str


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


class FacultyUpdate(BaseModel):
    name: Optional[str] = None
    department: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    qualification: Optional[str] = None
    designation: Optional[str] = None
    max_weekly_hours: Optional[int] = None


class FacultyRead(FacultyBase):
    id: int
    user_id: Optional[int] = None
    subjects: List[SubjectShort] = []
    
    class Config:
        from_attributes = True
