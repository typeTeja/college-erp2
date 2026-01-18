from pydantic import BaseModel, EmailStr
from typing import Optional, Dict
from datetime import datetime

# API Response Schemas (separate from DB models)

class StudentBase(BaseModel):
    """Base student schema"""
    admission_number: str
    name: str
    middle_name: Optional[str] = None
    dob: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    alternate_mobile: Optional[str] = None

class StudentCreate(StudentBase):
    """Schema for creating a student"""
    # Required academic links
    program_id: int
    batch_id: int
    program_year_id: int
    batch_semester_id: int
    section_id: Optional[int] = None
    practical_batch_id: Optional[int] = None
    
    # Optional demographics
    gender: Optional[str] = None
    blood_group: Optional[str] = None
    nationality: Optional[str] = "Indian"
    religion: Optional[str] = None
    caste_category: Optional[str] = None
    
    # Optional address
    current_address: Optional[str] = None
    permanent_address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    pincode: Optional[str] = None
    
    # Optional parent details
    father_name: Optional[str] = None
    father_mobile: Optional[str] = None
    father_email: Optional[str] = None
    father_occupation: Optional[str] = None
    mother_name: Optional[str] = None
    mother_mobile: Optional[str] = None
    mother_email: Optional[str] = None
    mother_occupation: Optional[str] = None
    
    # Optional guardian details
    guardian_name: Optional[str] = None
    guardian_mobile: Optional[str] = None
    guardian_relation: Optional[str] = None
    
    # Optional emergency contact
    emergency_contact_name: Optional[str] = None
    emergency_contact_mobile: Optional[str] = None
    emergency_contact_relation: Optional[str] = None
    
    # Optional previous education
    previous_qualification: Optional[str] = None
    previous_institution: Optional[str] = None
    previous_institution_city: Optional[str] = None
    previous_institution_district: Optional[str] = None
    previous_board: Optional[str] = None
    previous_marks: Optional[float] = None
    previous_percentage: Optional[float] = None
    previous_year_of_passing: Optional[int] = None
    
    # Optional flags
    hostel_required: Optional[bool] = False
    transport_required: Optional[bool] = False
    lateral_entry: Optional[bool] = False

class StudentUpdate(BaseModel):
    """Schema for updating a student"""
    # Basic info
    name: Optional[str] = None
    middle_name: Optional[str] = None
    dob: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    alternate_mobile: Optional[str] = None
    
    # Address
    current_address: Optional[str] = None
    permanent_address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    pincode: Optional[str] = None
    
    # Demographics
    gender: Optional[str] = None
    blood_group: Optional[str] = None
    nationality: Optional[str] = None
    religion: Optional[str] = None
    caste_category: Optional[str] = None
    
    # Parent details
    father_name: Optional[str] = None
    father_mobile: Optional[str] = None
    father_email: Optional[str] = None
    father_occupation: Optional[str] = None
    mother_name: Optional[str] = None
    mother_mobile: Optional[str] = None
    mother_email: Optional[str] = None
    mother_occupation: Optional[str] = None
    
    # Guardian details
    guardian_name: Optional[str] = None
    guardian_mobile: Optional[str] = None
    guardian_relation: Optional[str] = None
    
    # Emergency contact
    emergency_contact_name: Optional[str] = None
    emergency_contact_mobile: Optional[str] = None
    emergency_contact_relation: Optional[str] = None
    
    # Previous education
    previous_qualification: Optional[str] = None
    previous_institution: Optional[str] = None
    previous_institution_city: Optional[str] = None
    previous_institution_district: Optional[str] = None
    previous_board: Optional[str] = None
    previous_marks: Optional[float] = None
    previous_percentage: Optional[float] = None
    previous_year_of_passing: Optional[int] = None
    
    # Academic updates
    section_id: Optional[int] = None
    practical_batch_id: Optional[int] = None
    
    # Flags
    hostel_required: Optional[bool] = None
    transport_required: Optional[bool] = None
    status: Optional[str] = None

class StudentResponse(StudentBase):
    """Schema for student API response"""
    id: int
    
    # Demographics
    gender: Optional[str] = None
    blood_group: Optional[str] = None
    aadhaar_number: Optional[str] = None
    nationality: Optional[str] = None
    religion: Optional[str] = None
    caste_category: Optional[str] = None
    
    # Address
    current_address: Optional[str] = None
    permanent_address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    pincode: Optional[str] = None
    
    # Parent details
    father_name: Optional[str] = None
    father_mobile: Optional[str] = None
    father_email: Optional[str] = None
    father_occupation: Optional[str] = None
    mother_name: Optional[str] = None
    mother_mobile: Optional[str] = None
    mother_email: Optional[str] = None
    mother_occupation: Optional[str] = None
    
    # Guardian details
    guardian_name: Optional[str] = None
    guardian_mobile: Optional[str] = None
    guardian_relation: Optional[str] = None
    
    # Emergency contact
    emergency_contact_name: Optional[str] = None
    emergency_contact_mobile: Optional[str] = None
    emergency_contact_relation: Optional[str] = None
    
    # Previous education
    previous_qualification: Optional[str] = None
    previous_institution: Optional[str] = None
    previous_institution_city: Optional[str] = None
    previous_institution_district: Optional[str] = None
    previous_board: Optional[str] = None
    previous_marks: Optional[float] = None
    previous_percentage: Optional[float] = None
    previous_year_of_passing: Optional[int] = None
    
    # Documents
    documents: Optional[Dict[str, str]] = None
    
    # Portal access
    portal_user_id: Optional[int] = None
    portal_last_login: Optional[datetime] = None
    
    # Fee tracking
    fee_structure_id: Optional[int] = None
    total_fee: Optional[float] = None
    paid_amount: Optional[float] = None
    pending_amount: Optional[float] = None
    
    # Academic IDs
    program_id: int
    batch_id: int
    program_year_id: int
    batch_semester_id: int
    section_id: Optional[int] = None
    practical_batch_id: Optional[int] = None
    
    # Flattened fields
    program_name: str = ""
    batch_code: Optional[str] = None
    
    # Flags
    hostel_required: bool = False
    transport_required: bool = False
    scholarship_category: Optional[str] = None
    lateral_entry: bool = False
    
    # Status
    status: str
    
    # Deactivation
    deactivated_at: Optional[datetime] = None
    deactivated_by: Optional[int] = None
    deactivation_reason: Optional[str] = None
    
    # Metadata
    created_from: str = "manual"
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True
