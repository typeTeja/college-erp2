from typing import TYPE_CHECKING, List, Optional
from datetime import datetime
from enum import Enum
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from .program import Program
    from .student import Student
    from .user import User
    from .academic.entrance_exam import EntranceExamResult

class ApplicationStatus(str, Enum):
    PENDING_PAYMENT = "PENDING_PAYMENT"
    PAYMENT_FAILED = "PAYMENT_FAILED"
    PAID = "PAID"
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
    
    status: ApplicationStatus = Field(default=ApplicationStatus.PENDING_PAYMENT, index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Links
    student_id: Optional[int] = Field(default=None, foreign_key="student.id", index=True)
    
    # Relationships
    program: "Program" = Relationship()
    payments: List["ApplicationPayment"] = Relationship(back_populates="application")
    documents: List["ApplicationDocument"] = Relationship(back_populates="application")
    activity_logs: List["ApplicationActivityLog"] = Relationship(back_populates="application")
    entrance_exam_score: Optional["EntranceExamScore"] = Relationship(back_populates="application")
    entrance_result: Optional["EntranceExamResult"] = Relationship(back_populates="admission")

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
