from pydantic import BaseModel
from typing import Optional

# API Response Schemas (separate from DB models)

class StudentBase(BaseModel):
    """Base student schema"""
    admission_number: str
    name: str
    dob: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None

class StudentCreate(StudentBase):
    """Schema for creating a student"""
    program_id: int
    batch_id: int
    program_year_id: int
    batch_semester_id: int
    section_id: Optional[int] = None

class StudentUpdate(BaseModel):
    """Schema for updating a student"""
    name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    section_id: Optional[int] = None
    practical_batch_id: Optional[int] = None

class StudentResponse(StudentBase):
    """Schema for student API response"""
    id: int
    program_name: str = "" # Flattened
    batch_code: Optional[str] = None # Flattened
    
    # IDs
    program_id: int
    batch_id: int
    program_year_id: int
    batch_semester_id: int
    section_id: Optional[int]
    
    class Config:
        from_attributes = True
