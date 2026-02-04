from typing import TYPE_CHECKING, List, Optional
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship
from app.shared.enums import (
    ApplicationPaymentStatus,
    ApplicationStatus,
    FeeMode,
    Religion,
    CasteCategory,
    ActivityLevel,
    BloodGroup
)

if TYPE_CHECKING:
    from app.domains.academic.models import Program
    from app.domains.student.models import Student
    from app.domains.finance.models import ScholarshipSlab
    from .payment import ApplicationPayment
    from .document import ApplicationDocument
    from .activity import ApplicationActivityLog
    from .entrance import EntranceExamScore, EntranceExamResult
    from .tentative import TentativeAdmission, ScholarshipCalculation
    from .application_details import (
        ApplicationParent,
        ApplicationEducation,
        ApplicationAddress,
        ApplicationBankDetails,
        ApplicationHealth
    )

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
    
    # Personal Details (Extended)
    date_of_birth: Optional[datetime] = None
    blood_group: Optional[BloodGroup] = None
    nationality: str = Field(default="Indian", max_length=100)
    religion: Optional[Religion] = None
    caste_category: Optional[CasteCategory] = None
    identification_mark_1: Optional[str] = Field(default=None, max_length=200)
    identification_mark_2: Optional[str] = Field(default=None, max_length=200)
    ssc_hall_ticket: Optional[str] = Field(default=None, max_length=100)
    medium_of_study: Optional[str] = Field(default=None, max_length=100)
    place_of_birth: Optional[str] = Field(default=None, max_length=200)
    native_place: Optional[str] = Field(default=None, max_length=200)
    native_state: Optional[str] = Field(default=None, max_length=100)
    
    # Extra-Curricular
    extra_curricular_activities: Optional[str] = None
    activity_level: Optional[ActivityLevel] = None
    activity_sponsored_by: Optional[str] = Field(default=None, max_length=200)
    hobbies: Optional[str] = None
    
    # Declarations
    student_declaration_accepted: bool = Field(default=False)
    parent_declaration_accepted: bool = Field(default=False)
    declaration_date: Optional[datetime] = None
    declaration_place: Optional[str] = Field(default=None, max_length=200)
    
    # Photo
    photo_url: Optional[str] = None
    
    # Student Portal Access (for progressive application completion)
    portal_user_id: Optional[int] = Field(default=None, foreign_key="users.id", index=True)
    portal_password_hash: Optional[str] = None  # Hashed password for student portal
    portal_first_login: Optional[datetime] = None
    portal_last_login: Optional[datetime] = None
    
    # Application Completion Tracking
    quick_apply_completed_at: Optional[datetime] = None
    full_form_started_at: Optional[datetime] = None
    full_form_completed_at: Optional[datetime] = None
    
    # Payment tracking
    application_fee: float = Field(default=500.0)
    payment_status: ApplicationPaymentStatus = Field(default=ApplicationPaymentStatus.PENDING)
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
    verified_by: Optional[int] = Field(default=None, foreign_key="users.id")
    verification_date: Optional[datetime] = None
    
    # Payment Mode & Offline Payment Tracking
    fee_mode: FeeMode = Field(default=FeeMode.ONLINE)
    payment_proof_url: Optional[str] = None  # For offline payment proof
    offline_payment_verified: bool = Field(default=False)
    offline_payment_verified_by: Optional[int] = Field(default=None, foreign_key="users.id")
    offline_payment_verified_at: Optional[datetime] = None
    
    status: ApplicationStatus = Field(default=ApplicationStatus.QUICK_APPLY_SUBMITTED, index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Soft Delete
    is_deleted: bool = Field(default=False, index=True)
    deleted_at: Optional[datetime] = None
    deleted_by: Optional[int] = Field(default=None, foreign_key="users.id")
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
    
    # New Relationships for Application Details
    parents: List["ApplicationParent"] = Relationship(back_populates="application")
    education_history: List["ApplicationEducation"] = Relationship(back_populates="application")
    addresses: List["ApplicationAddress"] = Relationship(back_populates="application")
    bank_details: Optional["ApplicationBankDetails"] = Relationship(back_populates="application")
    health_info: Optional["ApplicationHealth"] = Relationship(back_populates="application")
