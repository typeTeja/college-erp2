from typing import TYPE_CHECKING, List, Optional
from datetime import datetime, date
from enum import Enum
from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import Column, JSON, Text

if TYPE_CHECKING:
    from app.models.program import Program
    from app.models.student import Student
    from app.models.user import User
    from app.domains.finance.models import ScholarshipSlab
    from ....schemas.json_fields import EntranceTestSubject, SubjectMarksEntry

class ApplicationStatus(str, Enum):
    # Legacy Statuses (DB Support)
    APPLIED = "APPLIED"
    
    # Enhanced Workflow Statuses
    QUICK_APPLY_SUBMITTED = "QUICK_APPLY_SUBMITTED"  # Stage 1 complete, account created
    LOGGED_IN = "LOGGED_IN"  # Student logged in but form incomplete
    FORM_IN_PROGRESS = "FORM_IN_PROGRESS"  # Student started full form
    
    # Payment Statuses
    PENDING_PAYMENT = "PENDING_PAYMENT"
    PAYMENT_FAILED = "PAYMENT_FAILED"
    PAID = "PAID"
    
    # Application Processing Statuses
    FORM_COMPLETED = "FORM_COMPLETED"
    UNDER_REVIEW = "UNDER_REVIEW"
    APPROVED = "APPROVED"
    ADMITTED = "ADMITTED"
    REJECTED = "REJECTED"
    WITHDRAWN = "WITHDRAWN"

class ApplicationPaymentStatus(str, Enum):
    PENDING = "PENDING"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"

class FeeMode(str, Enum):
    """Payment mode for application fee"""
    ONLINE = "ONLINE"
    OFFLINE = "OFFLINE"

class DocumentType(str, Enum):
    """Types of documents that can be uploaded"""
    PHOTO = "PHOTO"
    AADHAAR = "AADHAAR"
    TENTH_MARKSHEET = "TENTH_MARKSHEET"
    TWELFTH_MARKSHEET = "TWELFTH_MARKSHEET"
    MIGRATION_CERTIFICATE = "MIGRATION_CERTIFICATE"
    TRANSFER_CERTIFICATE = "TRANSFER_CERTIFICATE"
    CASTE_CERTIFICATE = "CASTE_CERTIFICATE"
    INCOME_CERTIFICATE = "INCOME_CERTIFICATE"
    OTHER = "OTHER"

class DocumentStatus(str, Enum):
    """Document verification status"""
    UPLOADED = "UPLOADED"
    VERIFIED = "VERIFIED"
    REJECTED = "REJECTED"

class ActivityType(str, Enum):
    """Types of activities that can be logged"""
    APPLICATION_CREATED = "APPLICATION_CREATED"
    PAYMENT_INITIATED = "PAYMENT_INITIATED"
    PAYMENT_SUCCESS = "PAYMENT_SUCCESS"
    PAYMENT_FAILED = "PAYMENT_FAILED"
    OFFLINE_PAYMENT_VERIFIED = "OFFLINE_PAYMENT_VERIFIED"
    FORM_COMPLETED = "FORM_COMPLETED"
    DOCUMENT_UPLOADED = "DOCUMENT_UPLOADED"
    DOCUMENT_VERIFIED = "DOCUMENT_VERIFIED"
    DOCUMENT_REJECTED = "DOCUMENT_REJECTED"
    STATUS_CHANGED = "STATUS_CHANGED"
    ADMISSION_CONFIRMED = "ADMISSION_CONFIRMED"
    ADMISSION_REJECTED = "ADMISSION_REJECTED"
    APPLICATION_DELETED = "APPLICATION_DELETED"
    APPLICATION_RESTORED = "APPLICATION_RESTORED"
    TEST_DATA_CLEANUP = "TEST_DATA_CLEANUP"

class TentativeAdmissionStatus(str, Enum):
    """Tentative admission status"""
    PENDING_PAYMENT = "PENDING_PAYMENT"
    PAYMENT_RECEIVED = "PAYMENT_RECEIVED"
    EXPIRED = "EXPIRED"

class Application(SQLModel, table=True):
    """Student admission application model"""
    id: Optional[int] = Field(default=None, primary_key=True)
    application_number: str = Field(index=True, unique=True, nullable=False)
    
    # Stage 1: Quick Apply Fields
    name: str
    email: str = Field(index=True)
    phone: str = Field(index=True)
    gender: str
    program_id: int = Field(foreign_key="program.id", index=True)
    state: str
    board: str
    group_of_study: str # MPC, BiPC, etc.
    
    # Stage 2: Full Form Fields
    aadhaar_number: Optional[str] = Field(default=None, index=True)
    father_name: Optional[str] = None
    father_phone: Optional[str] = None
    address: Optional[str] = None
    previous_marks_percentage: Optional[float] = None
    applied_for_scholarship: bool = Field(default=False)
    hostel_required: bool = Field(default=False)
    
    # Photo
    photo_url: Optional[str] = None
    
    # Student Portal Access (for progressive application completion)
    portal_user_id: Optional[int] = Field(default=None, foreign_key="user.id", index=True)
    portal_password_hash: Optional[str] = None  # Hashed password for student portal
    portal_first_login: Optional[datetime] = None
    portal_last_login: Optional[datetime] = None
    
    # Application Completion Tracking
    quick_apply_completed_at: Optional[datetime] = None
    full_form_started_at: Optional[datetime] = None
    full_form_completed_at: Optional[datetime] = None
    
    # Payment tracking
    application_fee: float = Field(default=500.0)
    payment_status: str = Field(default="pending")  # pending, paid, failed
    payment_id: Optional[str] = None
    payment_date: Optional[datetime] = None
    
    # Hall Ticket
    hall_ticket_number: Optional[str] = Field(default=None, unique=True, index=True)
    hall_ticket_generated: bool = Field(default=False)
    hall_ticket_generated_date: Optional[datetime] = None
    hall_ticket_url: Optional[str] = None
    
    # Entrance Exam (link to EntranceExamResult)
    entrance_marks: Optional[float] = None  # Denormalized for quick access
    entrance_percentage: Optional[float] = None
    
    # Scholarship
    scholarship_slab_id: Optional[int] = Field(default=None, foreign_key="scholarship_slab.id")
    scholarship_amount: Optional[float] = None
    scholarship_percentage: Optional[float] = None
    
    # Offer Letter
    offer_letter_url: Optional[str] = None
    offer_letter_generated: bool = Field(default=False)
    offer_letter_generated_date: Optional[datetime] = None
    
    # Confirmation
    first_installment_paid: bool = Field(default=False)
    first_installment_amount: Optional[float] = None
    first_installment_payment_id: Optional[str] = None
    first_installment_payment_date: Optional[datetime] = None
    
    admission_number: Optional[str] = Field(default=None, unique=True, index=True)
    admission_date: Optional[datetime] = None
    
    # Document tracking (JSON)
    documents_submitted: Optional[str] = None  # JSON: {"10th": {"uploaded": true, "verified": false}}
    affidavits_submitted: Optional[str] = None  # JSON: {"anti_ragging": {"uploaded": true}}
    original_documents: Optional[str] = None  # JSON: [{"name": "10th Cert", "number": "123"}]
    
    documents_verified: bool = Field(default=False)
    verified_by: Optional[int] = Field(default=None, foreign_key="user.id")
    verification_date: Optional[datetime] = None
    
    # Payment Mode & Offline Payment Tracking
    fee_mode: FeeMode = Field(default=FeeMode.ONLINE)
    payment_proof_url: Optional[str] = None  # For offline payment proof
    offline_payment_verified: bool = Field(default=False)
    offline_payment_verified_by: Optional[int] = Field(default=None, foreign_key="user.id")
    offline_payment_verified_at: Optional[datetime] = None
    
    status: ApplicationStatus = Field(default=ApplicationStatus.QUICK_APPLY_SUBMITTED, index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Soft Delete
    is_deleted: bool = Field(default=False, index=True)
    deleted_at: Optional[datetime] = None
    deleted_by: Optional[int] = Field(default=None, foreign_key="user.id")
    delete_reason: Optional[str] = None
    
    # Links
    student_id: Optional[int] = Field(default=None, foreign_key="student.id", index=True)
    
    # Relationships
    program: "Program" = Relationship()
    payments: List["ApplicationPayment"] = Relationship(back_populates="application")
    documents: List["ApplicationDocument"] = Relationship(back_populates="application")
    activity_logs: List["ApplicationActivityLog"] = Relationship(back_populates="application")
    entrance_exam_score: Optional["EntranceExamScore"] = Relationship(back_populates="application")
    entrance_result: Optional["EntranceExamResult"] = Relationship(back_populates="admission")
    tentative_admissions: List["TentativeAdmission"] = Relationship(back_populates="application")
    scholarship_calculation: Optional["ScholarshipCalculation"] = Relationship(back_populates="application")

class ApplicationPayment(SQLModel, table=True):
    """Tracks application fee payments via Easebuzz or other gateways"""
    id: Optional[int] = Field(default=None, primary_key=True)
    application_id: int = Field(foreign_key="application.id", index=True)
    transaction_id: str = Field(unique=True, index=True)
    amount: float
    status: ApplicationPaymentStatus = Field(default=ApplicationPaymentStatus.PENDING)
    payment_method: Optional[str] = None # Easebuzz, Card, UPI
    paid_at: Optional[datetime] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    application: Application = Relationship(back_populates="payments")

class EntranceExamScore(SQLModel, table=True):
    """Manual entrance exam marks entry linked to application for scholarship calculation"""
    id: Optional[int] = Field(default=None, primary_key=True)
    application_id: int = Field(foreign_key="application.id", unique=True, index=True)
    marks_obtained: float
    total_marks: float = Field(default=100.0)
    exam_date: datetime = Field(default_factory=datetime.utcnow)
    verified_by: Optional[int] = Field(default=None, foreign_key="user.id")
    
    # Relationships
    application: Application = Relationship(back_populates="entrance_exam_score")

class ApplicationDocument(SQLModel, table=True):
    """Documents uploaded by applicants for verification"""
    id: Optional[int] = Field(default=None, primary_key=True)
    application_id: int = Field(foreign_key="application.id", index=True)
    document_type: DocumentType
    file_url: str
    file_name: str
    file_size: int  # in bytes
    status: DocumentStatus = Field(default=DocumentStatus.UPLOADED)
    rejection_reason: Optional[str] = None
    verified_by: Optional[int] = Field(default=None, foreign_key="user.id")
    verified_at: Optional[datetime] = None
    uploaded_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    application: Application = Relationship(back_populates="documents")

class ApplicationActivityLog(SQLModel, table=True):
    """Activity log for tracking all changes to an application"""
    id: Optional[int] = Field(default=None, primary_key=True)
    application_id: int = Field(foreign_key="application.id", index=True)
    activity_type: ActivityType
    description: str
    extra_data: Optional[str] = None  # JSON string for additional data (renamed from metadata to avoid SQLAlchemy conflict)
    performed_by: Optional[int] = Field(default=None, foreign_key="user.id")
    ip_address: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    application: Application = Relationship(back_populates="activity_logs")


class AdmissionSettings(SQLModel, table=True):
    """Global admission settings for configuring application workflow"""
    __tablename__ = "admission_settings"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    
    # Application Fee Configuration
    application_fee_enabled: bool = Field(default=True)
    application_fee_amount: float = Field(default=500.0)
    
    # Payment Method Configuration
    online_payment_enabled: bool = Field(default=True)
    offline_payment_enabled: bool = Field(default=True)
    
    # Payment Gateway Settings
    payment_gateway: str = Field(default="easebuzz")  # easebuzz, razorpay, etc.
    payment_gateway_key: Optional[str] = None  # API key for payment gateway
    payment_gateway_secret: Optional[str] = None  # API secret for payment gateway
    
    # Email/SMS Configuration
    send_credentials_email: bool = Field(default=True)
    send_credentials_sms: bool = Field(default=False)  # Default false until SMS gateway configured
    sms_gateway: Optional[str] = None  # twilio, aws_sns, etc.
    sms_gateway_key: Optional[str] = None
    sms_gateway_secret: Optional[str] = None
    
    # Auto-account Creation
    auto_create_student_account: bool = Field(default=True)
    
    # Portal Configuration
    portal_base_url: str = Field(default="https://portal.college.edu")
    
    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    updated_by: Optional[int] = Field(default=None, foreign_key="user.id")

class TentativeAdmission(SQLModel, table=True):
    """Tentative admission with fee structure"""
    __tablename__ = "tentative_admission"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    application_id: int = Field(foreign_key="application.id", index=True)
    
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
    
    number_of_installments: int = Field(default=4)
    first_installment_amount: float
    
    admission_letter_url: Optional[str] = None
    admission_letter_generated: bool = Field(default=False)
    payment_link: Optional[str] = None
    payment_link_generated: bool = Field(default=False)
    
    first_installment_paid: bool = Field(default=False)
    payment_id: Optional[str] = None
    payment_date: Optional[datetime] = None
    valid_until: datetime # Changed from date to datetime for consistency
    
    status: TentativeAdmissionStatus = Field(
        default=TentativeAdmissionStatus.PENDING_PAYMENT,
        index=True
    )
    
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    application: "Application" = Relationship(back_populates="tentative_admissions")

class ScholarshipCalculation(SQLModel, table=True):
    """Scholarship calculation based on merit"""
    __tablename__ = "scholarship_calculation"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    application_id: int = Field(foreign_key="application.id", unique=True, index=True)
    
    student_name: str
    course: str
    
    previous_percentage: Optional[float] = None
    previous_score: float = Field(default=0.0)
    entrance_percentage: Optional[float] = None
    entrance_score: float = Field(default=0.0)
    
    previous_weightage: float = Field(default=0.5)
    entrance_weightage: float = Field(default=0.5)
    final_merit_score: float = Field(default=0.0)
    
    scholarship_slab: Optional[str] = None
    scholarship_percentage: float = Field(default=0.0)
    scholarship_amount: float = Field(default=0.0)
    
    base_annual_fee: float = Field(default=0.0)
    final_annual_fee: float = Field(default=0.0)
    
    is_calculated: bool = Field(default=False)
    calculated_by: Optional[int] = Field(default=None, foreign_key="user.id")
    calculation_date: Optional[datetime] = None
    
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    application: "Application" = Relationship(back_populates="scholarship_calculation")

class EntranceTestConfig(SQLModel, table=True):
    """Configuration for entrance exams (RNET)"""
    __tablename__ = "entrance_test_config"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    test_name: str = Field(max_length=200)
    test_code: str = Field(unique=True, index=True, max_length=50)
    academic_year: str = Field(index=True)
    
    program_ids: List[int] = Field(default=[], sa_column=Column(JSON))
    
    test_date: date
    test_time: str
    test_duration_minutes: int = Field(default=120)
    reporting_time: str = Field(default="09:30 AM")
    
    venue_name: str
    venue_address: str = Field(sa_column=Column(Text))
    venue_instructions: Optional[str] = Field(default=None, sa_column=Column(Text))
    
    guidelines: Optional[str] = Field(default=None, sa_column=Column(Text))
    documents_required: List[str] = Field(default=[], sa_column=Column(JSON))
    
    total_marks: float = Field(default=100.0)
    subjects: List["EntranceTestSubject"] = Field(default=[], sa_column=Column(JSON))
    
    is_active: bool = Field(default=True)
    registration_open: bool = Field(default=True)
    registration_deadline: Optional[date] = None
    
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    created_by: Optional[int] = Field(default=None, foreign_key="user.id")
    
    results: List["EntranceExamResult"] = Relationship(back_populates="test_config")

class EntranceExamResult(SQLModel, table=True):
    """Entrance exam results and scholarship calculation"""
    __tablename__ = "entrance_exam_result"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    admission_id: int = Field(foreign_key="application.id", index=True)
    test_config_id: int = Field(foreign_key="entrance_test_config.id", index=True)
    scholarship_slab_id: Optional[int] = Field(default=None, foreign_key="scholarship_slab.id", index=True)
    
    hall_ticket_number: str = Field(unique=True, index=True)
    student_name: str
    program_code: str = Field(index=True)
    
    total_max_marks: float
    total_secured_marks: float
    entrance_percentage: float = Field(ge=0, le=100)
    
    subject_marks: List["SubjectMarksEntry"] = Field(default=[], sa_column=Column(JSON))
    
    previous_percentage: float = Field(ge=0, le=100)
    
    entrance_points: float = Field(ge=0, le=100)
    previous_points: float = Field(ge=0, le=100)
    total_points: float = Field(ge=0, le=100)
    average_points: float = Field(ge=0, le=100)
    
    entrance_weightage: float = Field(default=0.5)
    previous_weightage: float = Field(default=0.5)
    
    scholarship_amount: Optional[float] = None
    scholarship_percentage: Optional[float] = None
    
    result_status: str = Field(default="pending")
    remarks: Optional[str] = Field(default=None, sa_column=Column(Text))
    
    omr_sheet_number: Optional[str] = None
    omr_sheet_url: Optional[str] = None
    
    entered_by: Optional[int] = Field(default=None, foreign_key="user.id")
    entered_at: Optional[datetime] = None
    verified_by: Optional[int] = Field(default=None, foreign_key="user.id")
    verified_at: Optional[datetime] = None
    
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    admission: "Application" = Relationship(back_populates="entrance_result")
    test_config: "EntranceTestConfig" = Relationship(back_populates="results")
    scholarship_slab: Optional["ScholarshipSlab"] = Relationship(back_populates="results")
