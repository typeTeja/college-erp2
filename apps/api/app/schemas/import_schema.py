from typing import Optional, List
from enum import Enum
from pydantic import BaseModel, EmailStr, Field, validator
from datetime import date
from app.models.student import Gender, BloodGroup, ScholarshipCategory
from app.shared.enums import BloodGroup, Gender, ImportRowStatus, ScholarshipCategory


class StudentImportRow(BaseModel):
    # Basic Info - Strict Admission Number, everything else optional/defaulted
    admission_number: str
    name: Optional[str] = "Unknown Student"
    gender: Optional[Gender] = Gender.MALE
    dob: Optional[date] = None
    mobile: Optional[str] = Field(None, min_length=10, max_length=15)
    email: Optional[EmailStr] = None
    aadhaar: Optional[str] = None
    blood_group: Optional[BloodGroup] = None
    
    # Academic Info
    course_code: Optional[str] = "BTECH-CS" # Default fallback
    academic_year: Optional[int] = 1
    semester: Optional[int] = 1
    section: Optional[str] = "A"
    batch: Optional[str] = "2024-2028"
    
    # Parent Info
    father_name: Optional[str] = "Unknown"
    father_mobile: Optional[str] = "9999999999"
    mother_name: Optional[str] = None
    guardian_mobile: Optional[str] = None
    
    # Flags
    hostel_required: Optional[str] = "NO"
    transport_required: Optional[str] = "NO"
    scholarship_category: Optional[ScholarshipCategory] = ScholarshipCategory.GENERAL
    lateral_entry: Optional[str] = "NO"
    
    @validator('admission_number')
    def validate_admission_number(cls, v):
        if not v.isdigit():
            raise ValueError('Admission Number must be numeric only')
        return v

    @validator('mobile', 'father_mobile')
    def validate_mobile(cls, v):
        if v and (not v.isdigit() or len(v) != 10):
            # For weak validation mode, we can accept bad mobiles or set dummy? 
            # User wants optional, so if bad, maybe just ignore or raise error?
            # User said: "make all Fields are opional for temporary"
            # I will allow None, but if provided, it should effectively be len=10 check or just relaxed?
            # "except admition number" implies others are truly optional.
            pass 
        return v
    
    @validator('hostel_required', 'transport_required', 'lateral_entry')
    def validate_yes_no(cls, v):
        if v and v.upper() not in ['YES', 'NO']:
            return "NO" # Default to NO if invalid
        return v.upper() if v else "NO"

class ImportErrorDetail(BaseModel):
    field: str
    message: str

class ImportPreviewRow(BaseModel):
    row_number: int
    data: StudentImportRow
    status: ImportRowStatus
    errors: List[ImportErrorDetail] = []

class ImportPreviewResponse(BaseModel):
    total_rows: int
    valid_count: int
    invalid_count: int
    duplicate_count: int
    rows: List[ImportPreviewRow]

class ImportExecuteRequest(BaseModel):
    file_token: str # Token referencing uploaded temporary file
