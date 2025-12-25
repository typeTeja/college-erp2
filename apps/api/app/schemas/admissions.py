from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, EmailStr
from app.models.admissions import ApplicationStatus, ApplicationPaymentStatus

class ApplicationBase(BaseModel):
    name: str
    email: EmailStr
    phone: str
    gender: str
    program_id: int
    state: str
    board: str
    group_of_study: str

class ApplicationCreate(ApplicationBase):
    """Schema for Quick Apply (Stage 1)"""
    pass

class ApplicationUpdate(BaseModel):
    """Schema for completing the Full Application (Stage 2)"""
    aadhaar_number: Optional[str] = None
    father_name: Optional[str] = None
    father_phone: Optional[str] = None
    address: Optional[str] = None
    previous_marks_percentage: Optional[float] = None
    applied_for_scholarship: Optional[bool] = None
    hostel_required: Optional[bool] = None
    status: Optional[ApplicationStatus] = None

class ApplicationPaymentRead(BaseModel):
    id: int
    transaction_id: str
    amount: float
    status: ApplicationPaymentStatus
    payment_method: Optional[str] = None
    paid_at: Optional[datetime] = None
    created_at: datetime

    class Config:
        from_attributes = True

class EntranceExamScoreRead(BaseModel):
    id: int
    marks_obtained: float
    total_marks: float
    exam_date: datetime

    class Config:
        from_attributes = True

class ApplicationRead(ApplicationBase):
    id: int
    application_number: str
    status: ApplicationStatus
    created_at: datetime
    updated_at: datetime
    
    # Extra fields for full view
    aadhaar_number: Optional[str] = None
    father_name: Optional[str] = None
    father_phone: Optional[str] = None
    address: Optional[str] = None
    previous_marks_percentage: Optional[float] = None
    applied_for_scholarship: bool
    hostel_required: bool
    
    payments: List[ApplicationPaymentRead] = []
    entrance_exam_score: Optional[EntranceExamScoreRead] = None

    class Config:
        from_attributes = True

class EntranceExamScoreCreate(BaseModel):
    application_id: int
    marks_obtained: float
    total_marks: float = 100.0
    exam_date: Optional[datetime] = None

class ProgramShort(BaseModel):
    id: int
    name: str

class ApplicationRecentRead(BaseModel):
    id: int
    fullName: str
    email: str
    status: ApplicationStatus
    createdAt: datetime
    course: ProgramShort

    class Config:
        from_attributes = True
