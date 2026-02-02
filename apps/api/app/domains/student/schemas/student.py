from typing import List, Optional
from datetime import datetime, date
from pydantic import BaseModel, Field
from app.shared.enums import BloodGroup, Gender, StudentStatus


class StudentBase(BaseModel):
    name: str
    middle_name: Optional[str] = None
    dob: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    gender: Gender = Gender.MALE
    blood_group: Optional[BloodGroup] = None
    aadhaar_number: Optional[str] = None
    nationality: str = "Indian"
    
    # Academic Links
    program_id: int
    batch_id: int
    program_year_id: int
    batch_semester_id: int
    section_id: Optional[int] = None

class StudentCreate(StudentBase):
    admission_number: str

class StudentUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    status: Optional[StudentStatus] = None

class StudentResponse(StudentBase):
    id: int
    admission_number: str
    status: StudentStatus
    program_name: Optional[str] = None
    batch_code: Optional[str] = None
    
    class Config:
        from_attributes = True
