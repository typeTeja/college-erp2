from pydantic import BaseModel
from typing import Optional, List

# Program Schemas

class ProgramBase(BaseModel):
    """Base program schema"""
    code: str
    name: str
    duration_years: int = 4
    description: Optional[str] = None

class ProgramCreate(ProgramBase):
    """Schema for creating a program"""
    department_id: int

class ProgramResponse(ProgramBase):
    """Schema for program API response"""
    id: int
    department_name: str
    
    class Config:
        from_attributes = True

# Subject Schemas

class SubjectBase(BaseModel):
    """Base subject schema"""
    code: str
    name: str
    credits: int = 3
    description: Optional[str] = None

class SubjectCreate(SubjectBase):
    """Schema for creating a subject"""
    semester_id: int
    faculty_id: Optional[int] = None

class SubjectResponse(SubjectBase):
    """Schema for subject API response"""
    id: int
    semester_name: str
    faculty_name: Optional[str] = None
    
    class Config:
        from_attributes = True
