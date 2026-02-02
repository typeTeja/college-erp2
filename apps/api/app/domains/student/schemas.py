"""
Student Domain Schemas

Pydantic schemas for the student domain.
Note: This is a simplified version. Full schemas can be added as needed.
"""

from pydantic import BaseModel
from typing import Optional
from datetime import datetime, date


# ----------------------------------------------------------------------
# Student Schemas
# ----------------------------------------------------------------------

class StudentBase(BaseModel):
    admission_number: str
    first_name: str
    last_name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    date_of_birth: date
    gender: str


class StudentCreate(StudentBase):
    pass


class StudentRead(StudentBase):
    id: int
    batch_id: Optional[int] = None
    status: str
    created_at: datetime
    
    class Config:
        from_attributes = True


# ----------------------------------------------------------------------
# Parent Schemas
# ----------------------------------------------------------------------

class ParentBase(BaseModel):
    name: str
    relationship: str
    phone: str
    email: Optional[str] = None


class ParentCreate(ParentBase):
    student_id: int


class ParentRead(ParentBase):
    id: int
    student_id: int
    
    class Config:
        from_attributes = True


# ----------------------------------------------------------------------
# Enrollment Schemas
# ----------------------------------------------------------------------

class EnrollmentBase(BaseModel):
    student_id: int
    batch_id: int
    semester_no: int
    enrollment_date: date


class EnrollmentCreate(EnrollmentBase):
    pass


class EnrollmentRead(EnrollmentBase):
    id: int
    status: str
    
    class Config:
        from_attributes = True


# ----------------------------------------------------------------------
# Document Schemas
# ----------------------------------------------------------------------

class DocumentBase(BaseModel):
    student_id: int
    category: str
    file_url: str


class DocumentCreate(DocumentBase):
    pass


class DocumentRead(DocumentBase):
    id: int
    verification_status: str
    uploaded_at: datetime
    
    class Config:
        from_attributes = True
