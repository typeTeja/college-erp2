from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, EmailStr
from app.models.admissions import (
    ApplicationStatus, 
    ApplicationPaymentStatus,
    FeeMode,
    DocumentType,
    DocumentStatus,
    ActivityType
)

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
    fee_mode: FeeMode = FeeMode.ONLINE  # Allow choosing online or offline payment

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

class DocumentRead(BaseModel):
    """Schema for reading document information"""
    id: int
    application_id: int
    document_type: DocumentType
    file_url: str
    file_name: str
    file_size: int
    status: DocumentStatus
    rejection_reason: Optional[str] = None
    verified_by: Optional[int] = None
    verified_at: Optional[datetime] = None
    uploaded_at: datetime

    class Config:
        from_attributes = True

class DocumentUpload(BaseModel):
    """Schema for uploading a document"""
    document_type: DocumentType

class DocumentVerify(BaseModel):
    """Schema for verifying a document"""
    status: DocumentStatus
    rejection_reason: Optional[str] = None

class ActivityLogRead(BaseModel):
    """Schema for reading activity log"""
    id: int
    application_id: int
    activity_type: ActivityType
    description: str
    extra_data: Optional[str] = None
    performed_by: Optional[int] = None
    ip_address: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True

class ApplicationRead(ApplicationBase):
    id: int
    application_number: str
    status: ApplicationStatus
    fee_mode: FeeMode
    payment_proof_url: Optional[str] = None
    offline_payment_verified: bool
    offline_payment_verified_by: Optional[int] = None
    offline_payment_verified_at: Optional[datetime] = None
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
    documents: List[DocumentRead] = []

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

class OfflinePaymentVerify(BaseModel):
    """Schema for admin to verify offline payment"""
    payment_proof_url: str
    verified: bool = True

class PaymentInitiate(BaseModel):
    """Schema for initiating online payment"""
    amount: float
    return_url: str
