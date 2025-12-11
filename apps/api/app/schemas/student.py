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
    current_year: int = 1

class StudentUpdate(BaseModel):
    """Schema for updating a student"""
    name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    current_year: Optional[int] = None

class StudentResponse(StudentBase):
    """Schema for student API response"""
    id: int
    program_name: str  # Flattened for frontend
    current_year: int
    
    class Config:
        from_attributes = True
