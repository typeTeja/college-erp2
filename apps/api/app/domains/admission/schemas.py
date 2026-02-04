"""
Admission Domain Schemas

API contract schemas for admission workflow.

**CONTRACT VERSION: v1.0.0**
**STATUS: FROZEN (2026-02-03)**

⚠️ BREAKING CHANGES POLICY:
- Enum additions: Safe (backward compatible)
- New optional fields: Safe
- Required field changes: Requires migration + 6-month deprecation
- Enum removals: 6-month deprecation period
- Field type changes: Major version bump

Any changes to this file require approval and version bump.
"""
from typing import List, Optional, Any, Dict
from datetime import datetime, date
from pydantic import BaseModel, EmailStr, field_validator, Field
from app.shared.enums import (
    ApplicationStatus,
    ApplicationPaymentStatus,
    FeeMode,
    DocumentType,
    DocumentStatus,
    ActivityType,
    TentativeAdmissionStatus,
    Religion,
    CasteCategory,
    ParentRelation,
    EducationLevel,
    EducationBoard,
    ActivityLevel,
    AddressType,
    BloodGroup,
    Gender
)

class ApplicationBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    email: EmailStr
    phone: str = Field(..., pattern=r'^\d{10}$', description="10-digit phone number")
    gender: str = Field(..., pattern=r'^(MALE|FEMALE|OTHER)$')
    program_id: int = Field(..., gt=0)
    state: str = Field(..., min_length=1, max_length=100)
    board: str = Field(..., min_length=1, max_length=100)
    group_of_study: str = Field(..., min_length=1, max_length=50)

class ApplicationCreate(ApplicationBase):
    """Schema for Quick Apply (Stage 1)"""
    fee_mode: FeeMode = FeeMode.ONLINE  # Allow choosing online or offline payment

class ApplicationUpdate(BaseModel):
    """Schema for completing the Full Application (Stage 2)"""
    # Basic Stage 2 fields
    aadhaar_number: Optional[str] = Field(None, pattern=r'^\d{12}$', description="12-digit Aadhaar number")
    father_name: Optional[str] = Field(None, min_length=1, max_length=200)
    father_phone: Optional[str] = Field(None, pattern=r'^\d{10}$', description="10-digit phone number")
    address: Optional[str] = Field(None, min_length=1, max_length=500)
    previous_marks_percentage: Optional[float] = Field(None, ge=0, le=100)
    applied_for_scholarship: Optional[bool] = None
    hostel_required: Optional[bool] = None
    
    # Extended Personal Details
    date_of_birth: Optional[date] = None
    blood_group: Optional[BloodGroup] = None
    nationality: Optional[str] = Field(None, max_length=100)
    religion: Optional[Religion] = None
    caste_category: Optional[CasteCategory] = None
    identification_mark_1: Optional[str] = Field(None, max_length=200)
    identification_mark_2: Optional[str] = Field(None, max_length=200)
    ssc_hall_ticket: Optional[str] = Field(None, max_length=100)
    medium_of_study: Optional[str] = Field(None, max_length=100)
    place_of_birth: Optional[str] = Field(None, max_length=200)
    native_place: Optional[str] = Field(None, max_length=200)
    native_state: Optional[str] = Field(None, max_length=100)
    
    # Extra-Curricular
    extra_curricular_activities: Optional[str] = None
    activity_level: Optional[ActivityLevel] = None
    activity_sponsored_by: Optional[str] = Field(None, max_length=200)
    hobbies: Optional[str] = None
    
    # Declarations
    student_declaration_accepted: Optional[bool] = None
    parent_declaration_accepted: Optional[bool] = None
    declaration_date: Optional[date] = None
    declaration_place: Optional[str] = Field(None, max_length=200)
    
    status: Optional[ApplicationStatus] = None


# ======================================================================
# Nested Data Schemas for Application Details
# ======================================================================

class ApplicationParentCreate(BaseModel):
    """Schema for creating parent/guardian information"""
    relation: ParentRelation
    name: str = Field(..., min_length=1, max_length=200)
    gender: Optional[Gender] = None
    mobile: str = Field(..., pattern=r'^\d{10}$')
    email: Optional[EmailStr] = None
    qualification: Optional[str] = Field(None, max_length=200)
    occupation: Optional[str] = Field(None, max_length=200)
    annual_income: Optional[float] = Field(None, ge=0)
    bank_account_number: Optional[str] = None
    bank_name: Optional[str] = None
    bank_ifsc: Optional[str] = None
    is_primary_contact: bool = False


class ApplicationParentRead(ApplicationParentCreate):
    """Schema for reading parent information"""
    id: int
    application_id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class ApplicationEducationCreate(BaseModel):
    """Schema for creating education history"""
    level: EducationLevel
    institution_name: str = Field(..., min_length=1, max_length=300)
    institution_address: Optional[str] = None
    institution_code: Optional[str] = Field(None, max_length=50)
    board: EducationBoard
    board_other: Optional[str] = Field(None, max_length=200)
    hall_ticket_number: Optional[str] = Field(None, max_length=100)
    year_of_passing: Optional[int] = Field(None, ge=1950, le=2100)
    secured_marks: Optional[float] = Field(None, ge=0)
    total_marks: Optional[float] = Field(None, ge=0)
    percentage: Optional[float] = Field(None, ge=0, le=100)
    cgpa: Optional[float] = Field(None, ge=0, le=10)


class ApplicationEducationRead(ApplicationEducationCreate):
    """Schema for reading education history"""
    id: int
    application_id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class ApplicationAddressCreate(BaseModel):
    """Schema for creating address information"""
    address_type: AddressType
    address_line: str = Field(..., min_length=1)
    village_city: str = Field(..., min_length=1, max_length=200)
    district: Optional[str] = Field(None, max_length=200)
    state: str = Field(..., min_length=1, max_length=100)
    country: str = Field(default="India", max_length=100)
    pincode: str = Field(..., pattern=r'^\d{6}$')
    telephone_residence: Optional[str] = None
    telephone_office: Optional[str] = None


class ApplicationAddressRead(ApplicationAddressCreate):
    """Schema for reading address information"""
    id: int
    application_id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class ApplicationBankDetailsCreate(BaseModel):
    """Schema for creating bank details"""
    account_number: str = Field(..., min_length=1, max_length=50)
    account_holder_name: Optional[str] = Field(None, max_length=200)
    bank_name: str = Field(..., min_length=1, max_length=200)
    branch_name: Optional[str] = Field(None, max_length=200)
    ifsc_code: str = Field(..., pattern=r'^[A-Z]{4}0[A-Z0-9]{6}$')


class ApplicationBankDetailsRead(ApplicationBankDetailsCreate):
    """Schema for reading bank details"""
    id: int
    application_id: int
    is_verified: bool
    verified_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class ApplicationHealthCreate(BaseModel):
    """Schema for creating health/medical fitness information"""
    is_medically_fit: bool
    practitioner_name: Optional[str] = Field(None, max_length=200)
    practitioner_registration_number: Optional[str] = Field(None, max_length=100)
    certificate_date: Optional[date] = None
    certificate_place: Optional[str] = Field(None, max_length=200)


class ApplicationHealthRead(ApplicationHealthCreate):
    """Schema for reading health information"""
    id: int
    application_id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class ApplicationCompleteUpdate(BaseModel):
    """Comprehensive schema for completing full application with nested data"""
    # All fields from ApplicationUpdate
    aadhaar_number: Optional[str] = Field(None, pattern=r'^\d{12}$')
    father_name: Optional[str] = Field(None, max_length=200)
    father_phone: Optional[str] = Field(None, pattern=r'^\d{10}$')
    address: Optional[str] = Field(None, max_length=500)
    previous_marks_percentage: Optional[float] = Field(None, ge=0, le=100)
    applied_for_scholarship: Optional[bool] = None
    hostel_required: Optional[bool] = None
    
    # Extended Personal Details
    date_of_birth: Optional[date] = None
    blood_group: Optional[BloodGroup] = None
    nationality: Optional[str] = Field(None, max_length=100)
    religion: Optional[Religion] = None
    caste_category: Optional[CasteCategory] = None
    identification_mark_1: Optional[str] = Field(None, max_length=200)
    identification_mark_2: Optional[str] = Field(None, max_length=200)
    ssc_hall_ticket: Optional[str] = Field(None, max_length=100)
    medium_of_study: Optional[str] = Field(None, max_length=100)
    place_of_birth: Optional[str] = Field(None, max_length=200)
    native_place: Optional[str] = Field(None, max_length=200)
    native_state: Optional[str] = Field(None, max_length=100)
    
    # Extra-Curricular
    extra_curricular_activities: Optional[str] = None
    activity_level: Optional[ActivityLevel] = None
    activity_sponsored_by: Optional[str] = Field(None, max_length=200)
    hobbies: Optional[str] = None
    
    # Declarations
    student_declaration_accepted: Optional[bool] = None
    parent_declaration_accepted: Optional[bool] = None
    declaration_date: Optional[date] = None
    declaration_place: Optional[str] = Field(None, max_length=200)
    
    # Nested Data
    parents: Optional[List[ApplicationParentCreate]] = []
    education_history: Optional[List[ApplicationEducationCreate]] = []
    addresses: Optional[List[ApplicationAddressCreate]] = []
    bank_details: Optional[ApplicationBankDetailsCreate] = None
    health_info: Optional[ApplicationHealthCreate] = None

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
    payment_status: Optional[str] = "pending"
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
    
    # Extended Personal Details
    date_of_birth: Optional[datetime] = None
    blood_group: Optional[BloodGroup] = None
    nationality: Optional[str] = None
    religion: Optional[Religion] = None
    caste_category: Optional[CasteCategory] = None
    
    # Nested relationships
    parents: List[ApplicationParentRead] = []
    education_history: List[ApplicationEducationRead] = []
    addresses: List[ApplicationAddressRead] = []
    bank_details: Optional[ApplicationBankDetailsRead] = None
    health_info: Optional[ApplicationHealthRead] = None
    
    payments: List[ApplicationPaymentRead] = []
    entrance_exam_score: Optional[EntranceExamScoreRead] = None
    documents: List[DocumentRead] = []
    
    # Soft Delete
    is_deleted: bool
    deleted_at: Optional[datetime] = None

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
    payment_proof_url: Optional[str] = None
    verified: bool = True
    mode: str = "CASH" # CASH, ONLINE
    transaction_id: Optional[str] = None

class PaymentInitiate(BaseModel):
    """Schema for initiating online payment"""
    amount: float
    return_url: str

class PaymentInitiateResponse(BaseModel):
    status: str
    access_key: Optional[str] = None
    payment_url: Optional[str] = None
    error: Optional[str] = None

# Enhanced Admission Workflow Schemas

class QuickApplyCreate(BaseModel):
    """Stage 1: Quick Apply - Minimal fields for lead capture"""
    name: str
    email: EmailStr
    phone: str
    gender: str
    program_id: int
    state: str
    board: str
    group_of_study: str

class QuickApplyResponse(BaseModel):
    """Response after Quick Apply submission"""
    id: int  # Added ID for payment initiation
    application_number: str
    portal_username: Optional[str] = None
    portal_password: Optional[str] = None  # Only sent once
    message: str
    
class ApplicationCompleteUpdate(BaseModel):
    """Stage 2: Complete Application - Full form fields"""
    aadhaar_number: Optional[str] = None
    father_name: Optional[str] = None
    father_phone: Optional[str] = None
    address: Optional[str] = None
    previous_marks_percentage: Optional[float] = None
    applied_for_scholarship: bool = False
    hostel_required: bool = False

class AdmissionSettingsRead(BaseModel):
    """Read admission settings"""
    id: int
    application_fee_enabled: bool
    application_fee_amount: float
    online_payment_enabled: bool
    offline_payment_enabled: bool
    payment_gateway: str
    send_credentials_email: bool
    send_credentials_sms: bool
    auto_create_student_account: bool
    portal_base_url: str
    updated_at: datetime
    
    class Config:
        from_attributes = True

class AdmissionSettingsUpdate(BaseModel):
    """Update admission settings"""
    application_fee_enabled: Optional[bool] = None
    application_fee_amount: Optional[float] = None
    online_payment_enabled: Optional[bool] = None
    offline_payment_enabled: Optional[bool] = None
    send_credentials_email: Optional[bool] = None
    send_credentials_sms: Optional[bool] = None
    auto_create_student_account: Optional[bool] = None
    portal_base_url: Optional[str] = None

class PaymentConfigResponse(BaseModel):
    """Payment configuration for frontend"""
    fee_enabled: bool
    fee_amount: float
    online_enabled: bool
    offline_enabled: bool
    payment_gateway: str

class OfflineApplicationCreate(ApplicationBase):
    """Schema for Full Offline Application Creation (Admin)"""
    # Stage 1 fields inherited from ApplicationBase
    
    # Stage 2 fields (Optional for admin flexibility)
    aadhaar_number: Optional[str] = None
    father_name: Optional[str] = None
    father_phone: Optional[str] = None
    address: Optional[str] = None
    previous_marks_percentage: Optional[float] = None
    applied_for_scholarship: bool = False
    hostel_required: bool = False
    
    # Payment & Status
    fee_mode: FeeMode = FeeMode.OFFLINE
    is_paid: bool = False  # If true, marks as PAID instantly

# --- Tentative Admission Schemas ---

class TentativeAdmissionBase(BaseModel):
    application_id: int
    scholarship_slab: str
    scholarship_amount: float
    base_annual_fee: float
    scholarship_discount: float
    net_annual_fee: float
    tuition_fee: Optional[float] = None
    library_fee: Optional[float] = None
    lab_fee: Optional[float] = None
    uniform_fee: Optional[float] = None
    caution_deposit: Optional[float] = None
    miscellaneous_fee: Optional[float] = None
    number_of_installments: int = 4
    first_installment_amount: float
    valid_until: datetime

class TentativeAdmissionCreate(TentativeAdmissionBase):
    pass

class TentativeAdmissionRead(TentativeAdmissionBase):
    id: int
    status: TentativeAdmissionStatus
    admission_letter_url: Optional[str] = None
    admission_letter_generated: bool
    payment_link: Optional[str] = None
    payment_link_generated: bool
    first_installment_paid: bool
    payment_id: Optional[str] = None
    payment_date: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# --- Entrance Exam Schemas (Migrated from Academic) ---

class EntranceTestConfigBase(BaseModel):
    test_name: str
    test_code: str
    academic_year: str
    program_ids: Optional[List[int]] = None
    test_date: date
    test_time: str
    test_duration_minutes: int = 120
    reporting_time: str = "09:30 AM"
    venue_name: str
    venue_address: str
    venue_instructions: Optional[str] = None
    guidelines: Optional[str] = None
    documents_required: Optional[List[str]] = None
    total_marks: float = 100.0
    subjects: Optional[List[Dict[str, Any]]] = None

class EntranceTestConfigCreate(EntranceTestConfigBase):
    pass

class EntranceTestConfigRead(EntranceTestConfigBase):
    id: int
    is_active: bool
    registration_open: bool
    registration_deadline: Optional[date] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class EntranceExamResultBase(BaseModel):
    admission_id: int
    test_config_id: int
    hall_ticket_number: str
    student_name: str
    program_code: str
    total_max_marks: float
    total_secured_marks: float
    entrance_percentage: float
    previous_percentage: float

class EntranceExamResultCreate(EntranceExamResultBase):
    subject_marks: Optional[List[Dict[str, Any]]] = None
    entrance_weightage: float = 0.5
    previous_weightage: float = 0.5
    omr_sheet_number: Optional[str] = None
    omr_sheet_url: Optional[str] = None

class EntranceExamResultRead(EntranceExamResultBase):
    id: int
    scholarship_slab_id: Optional[int] = None
    subject_marks: Optional[List[Dict[str, Any]]] = None
    entrance_points: float
    previous_points: float
    total_points: float
    average_points: float
    entrance_weightage: float
    previous_weightage: float
    scholarship_amount: Optional[float] = None
    scholarship_percentage: Optional[float] = None
    result_status: str
    remarks: Optional[str] = None
    omr_sheet_number: Optional[str] = None
    omr_sheet_url: Optional[str] = None
    entered_by: Optional[int] = None
    entered_at: Optional[datetime] = None
    verified_by: Optional[int] = None
    verified_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
