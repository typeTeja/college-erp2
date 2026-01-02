from pydantic import BaseModel
from typing import Optional, List

# Program Schemas
from app.models.program import ProgramType, ProgramStatus

class ProgramBase(BaseModel):
    """Base program schema"""
    code: str
    name: str
    program_type: ProgramType = ProgramType.UG
    duration_years: int = 4
    description: Optional[str] = None
    eligibility_criteria: Optional[str] = None
    program_outcomes: Optional[str] = None
    total_credits: int = 0

class ProgramCreate(ProgramBase):
    """Schema for creating a program"""
    department_id: int

class ProgramRead(ProgramBase):
    """Schema for program API response"""
    id: int
    status: ProgramStatus
    department_name: str
    is_active: bool
    
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
