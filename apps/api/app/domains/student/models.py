"""
Student Domain Models

All database models for the student domain including:
- Student core information
- Parent/guardian information
- Enrollment management
- Document management and verification
- ODC (On Duty Certificate) system
- Student portal functionality
"""



# ======================================================================
# Student
# ======================================================================

from typing import TYPE_CHECKING, List, Optional
from enum import Enum
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship, Column, JSON
from sqlalchemy import Text

if TYPE_CHECKING:
    from .enrollment import Enrollment
    from app.models.program import Program
    from .parent import Parent
    from app.domains.academic.models.student_history import StudentSemesterHistory, StudentPromotionLog

from app.schemas.json_fields import StudentDocuments
from app.shared.enums import BloodGroup, CreatedFrom, Gender, ScholarshipCategory, StudentStatus


class Student(SQLModel, table=True):
    """Student information model with comprehensive details"""
    id: Optional[int] = Field(default=None, primary_key=True)
    
    # Basic Information
    admission_number: str = Field(index=True, unique=True)
    name: str
    middle_name: Optional[str] = None
    dob: Optional[str] = None
    
    # Contact Information
    phone: Optional[str] = Field(default=None, index=True)
    email: Optional[str] = Field(default=None, index=True)
    alternate_mobile: Optional[str] = None
    
    # Address Information
    current_address: Optional[str] = Field(default=None, sa_column=Column(Text))
    permanent_address: Optional[str] = Field(default=None, sa_column=Column(Text))
    city: Optional[str] = None
    state: Optional[str] = None
    pincode: Optional[str] = None
    
    # Demographics
    gender: Gender = Field(default=Gender.MALE)
    blood_group: Optional[BloodGroup] = None
    aadhaar_number: Optional[str] = Field(default=None, unique=True, index=True)
    nationality: str = Field(default="Indian")
    religion: Optional[str] = None
    caste_category: Optional[str] = None  # Can also use ScholarshipCategory enum
    
    # Parent Details
    father_name: Optional[str] = None
    father_mobile: Optional[str] = None
    father_email: Optional[str] = None
    father_occupation: Optional[str] = None
    
    mother_name: Optional[str] = None
    mother_mobile: Optional[str] = None
    mother_email: Optional[str] = None
    mother_occupation: Optional[str] = None
    
    # Guardian Details
    guardian_name: Optional[str] = None
    guardian_mobile: Optional[str] = None
    guardian_relation: Optional[str] = None
    
    # Emergency Contact
    emergency_contact_name: Optional[str] = None
    emergency_contact_mobile: Optional[str] = None
    emergency_contact_relation: Optional[str] = None
    
    # Previous Education
    previous_qualification: Optional[str] = None
    previous_institution: Optional[str] = None
    previous_institution_city: Optional[str] = None
    previous_institution_district: Optional[str] = None
    previous_board: Optional[str] = None
    previous_marks: Optional[float] = None
    previous_percentage: Optional[float] = None
    previous_year_of_passing: Optional[int] = None
    
    # Documents (JSON field to store document URLs)
    documents: Optional[StudentDocuments] = Field(default_factory=StudentDocuments, sa_column=Column(JSON))
    # Example: {"photo": "url", "10th_certificate": "url", "12th_certificate": "url"}
    
    # Portal Access
    portal_user_id: Optional[int] = Field(default=None, foreign_key="user.id")
    portal_password_hash: Optional[str] = None
    portal_last_login: Optional[datetime] = None
    
    # Fee Tracking
    fee_structure_id: Optional[int] = Field(default=None, foreign_key="fee_structure.id")
    total_fee: Optional[float] = None
    paid_amount: Optional[float] = Field(default=0.0)
    pending_amount: Optional[float] = None
    
    # Academic Links
    user_id: Optional[int] = Field(default=None, foreign_key="user.id", index=True)
    program_id: int = Field(foreign_key="program.id", index=True)
    
    # Strict Academic Structure (Foreign Keys)
    batch_id: int = Field(foreign_key="academic_batches.id", index=True)
    program_year_id: int = Field(foreign_key="program_years.id", index=True)
    batch_semester_id: int = Field(foreign_key="batch_semesters.id", index=True)
    section_id: Optional[int] = Field(default=None, foreign_key="section.id", index=True)
    practical_batch_id: Optional[int] = Field(default=None, foreign_key="practical_batch.id", index=True)
    
    # Flags relative to admission
    hostel_required: bool = Field(default=False)
    transport_required: bool = Field(default=False)
    scholarship_category: ScholarshipCategory = Field(default=ScholarshipCategory.GENERAL)
    lateral_entry: bool = Field(default=False)
    
    # Status
    status: StudentStatus = Field(default=StudentStatus.IMPORTED_PENDING_VERIFICATION)
    
    # Deactivation Tracking
    deactivated_at: Optional[datetime] = None
    deactivated_by: Optional[int] = Field(default=None, foreign_key="user.id")
    deactivation_reason: Optional[str] = Field(default=None, sa_column=Column(Text))
    
    # Metadata
    created_from: CreatedFrom = Field(default=CreatedFrom.MANUAL)  # manual, admission, bulk_upload
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    program: "Program" = Relationship(back_populates="students")
    enrollments: List["Enrollment"] = Relationship(back_populates="student")
    parent: Optional["Parent"] = Relationship(sa_relationship_kwargs={"uselist": False, "foreign_keys": "Parent.linked_student_id"})
    
    # Academic foundation relationships
    semester_history: List["StudentSemesterHistory"] = Relationship(back_populates="student")
    promotion_logs: List["StudentPromotionLog"] = Relationship(back_populates="student")


# ======================================================================
# Parent
# ======================================================================

from typing import Optional
from sqlmodel import SQLModel, Field

class Parent(SQLModel, table=True):
    """Parent/Guardian information model"""
    id: Optional[int] = Field(default=None, primary_key=True)
    linked_student_id: int = Field(foreign_key="student.id", index=True)
    father_name: str
    father_mobile: str = Field(index=True)
    mother_name: Optional[str] = None
    guardian_mobile: Optional[str] = None


# ======================================================================
# Enrollment
# ======================================================================

from typing import TYPE_CHECKING, Optional
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from .student import Student
    from app.domains.academic.models.batch import BatchSubject
    from app.models.subject import Subject

class Enrollment(SQLModel, table=True):
    """Student-Subject enrollment model"""
    id: Optional[int] = Field(default=None, primary_key=True)
    student_id: int = Field(foreign_key="student.id", index=True)
    subject_id: int = Field(foreign_key="subject.id", index=True)
    academic_year: str  # e.g., "2024-2025"
    grade: Optional[str] = None
    attendance_percentage: Optional[float] = None
    enrolled_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    student: "Student" = Relationship(back_populates="enrollments")
    subject: "Subject" = Relationship(back_populates="enrollments")


# ======================================================================
# Document
# ======================================================================

from typing import TYPE_CHECKING, List, Optional
from datetime import datetime, date
from enum import Enum
from sqlmodel import SQLModel, Field, Relationship, Column
from sqlalchemy import Text, JSON
from app.schemas.json_fields import ChecklistItem

if TYPE_CHECKING:
    from .student import Student
    from app.models import User


class VerificationStatus(str, Enum):
    """Document verification status"""
    PENDING = "PENDING"
    VERIFIED = "VERIFIED"
    REJECTED = "REJECTED"
    EXPIRED = "EXPIRED"


class DocumentCategory(SQLModel, table=True):
    """Document category configuration"""
    __tablename__ = "document_category"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    
    # Category details
    name: str = Field(max_length=200)  # "10th Marksheet", "Aadhar Card"
    code: str = Field(unique=True, index=True, max_length=50)  # "10TH_MARKS"
    description: Optional[str] = Field(default=None, sa_column=Column(Text))
    
    # Requirements
    is_required: bool = Field(default=False)  # Required for admission
    is_mandatory: bool = Field(default=False)  # Must be submitted
    
    # File constraints
    allowed_file_types: List[str] = Field(default=[], sa_column=Column(JSON))  # ["pdf", "jpg", "png"]
    max_file_size: int = Field(default=10485760)  # 10MB in bytes
    max_files: int = Field(default=1)  # Number of files allowed
    
    # Verification
    verification_required: bool = Field(default=True)
    valid_for_days: Optional[int] = None  # Document validity period
    
    # Instructions
    upload_instructions: Optional[str] = Field(default=None, sa_column=Column(Text))
    sample_document_url: Optional[str] = None
    
    # Display
    display_order: int = Field(default=0)
    icon: Optional[str] = None
    
    # Status
    is_active: bool = Field(default=True)
    
    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    documents: List["StudentDocument"] = Relationship(
        back_populates="category",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )


class StudentDocument(SQLModel, table=True):
    """Student uploaded documents"""
    __tablename__ = "student_document"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    
    # Links
    student_id: int = Field(foreign_key="student.id", index=True)
    document_category_id: int = Field(foreign_key="document_category.id", index=True)
    
    # File details
    file_name: str
    file_path: str  # Storage path
    file_size: int  # Bytes
    file_type: str  # pdf, jpg, png
    file_hash: Optional[str] = None  # For duplicate detection
    
    # Upload tracking
    uploaded_at: datetime = Field(default_factory=datetime.utcnow)
    uploaded_by: Optional[int] = Field(default=None, foreign_key="user.id")
    upload_ip: Optional[str] = None
    
    # Verification
    verification_status: VerificationStatus = Field(default=VerificationStatus.PENDING)
    verified_by: Optional[int] = Field(default=None, foreign_key="user.id")
    verified_at: Optional[datetime] = None
    rejection_reason: Optional[str] = Field(default=None, sa_column=Column(Text))
    
    # Validity
    expiry_date: Optional[date] = None
    is_expired: bool = Field(default=False)
    
    # Versioning
    version_number: int = Field(default=1)
    previous_document_id: Optional[int] = Field(default=None, foreign_key="student_document.id")
    is_latest: bool = Field(default=True)
    
    # Metadata
    document_number: Optional[str] = None  # For ID cards, certificates
    issue_date: Optional[date] = None
    issuing_authority: Optional[str] = None
    
    # Notes
    student_remarks: Optional[str] = Field(default=None, sa_column=Column(Text))
    admin_remarks: Optional[str] = Field(default=None, sa_column=Column(Text))
    
    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    student: "Student" = Relationship()
    category: "DocumentCategory" = Relationship(back_populates="documents")
    verifications: List["DocumentVerification"] = Relationship(
        back_populates="document",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )


class DocumentVerification(SQLModel, table=True):
    """Document verification audit trail"""
    __tablename__ = "document_verification"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    
    # Links
    student_document_id: int = Field(foreign_key="student_document.id", index=True)
    
    # Verification details
    verified_by: int = Field(foreign_key="user.id")
    verified_at: datetime = Field(default_factory=datetime.utcnow)
    verification_status: VerificationStatus
    
    # Checklist
    checklist_items: List[ChecklistItem] = Field(default=[], sa_column=Column(JSON))
    # Example: [{"item": "Photo clear", "checked": true}, {"item": "Details match", "checked": true}]
    
    # Remarks
    remarks: Optional[str] = Field(default=None, sa_column=Column(Text))
    rejection_reason: Optional[str] = Field(default=None, sa_column=Column(Text))
    
    # Follow-up
    requires_resubmission: bool = Field(default=False)
    resubmission_deadline: Optional[date] = None
    
    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    document: "StudentDocument" = Relationship(back_populates="verifications")


# ======================================================================
# Odc
# ======================================================================

from typing import TYPE_CHECKING, List, Optional
from datetime import date, datetime
from enum import Enum
from sqlmodel import SQLModel, Field, Relationship
from app.shared.enums import ApplicationStatus, BillingStatus, GenderPreference, ODCStatus, PaymentMethod, PayoutStatus


if TYPE_CHECKING:
    from app.models import User
    from .student import Student


class ODCHotel(SQLModel, table=True):
    """Hotel or Catering Partner for ODC"""
    __tablename__ = "odc_hotel"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    address: str
    contact_person: str
    phone: str
    email: Optional[str] = None
    default_pay_rate: Optional[float] = None  # Default hourly/daily rate
    is_active: bool = Field(default=True)
    
    # Relationships
    requests: List["ODCRequest"] = Relationship(back_populates="hotel")

class ODCRequest(SQLModel, table=True):
    """Specific ODC Event Request"""
    __tablename__ = "odc_request"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    hotel_id: int = Field(foreign_key="odc_hotel.id")
    event_name: str
    event_date: date
    report_time: datetime
    duration_hours: float
    vacancies: int
    gender_preference: GenderPreference = Field(default=GenderPreference.ANY)
    pay_amount: float
    transport_provided: bool = Field(default=False)
    status: ODCStatus = Field(default=ODCStatus.OPEN)
    created_by_id: int = Field(foreign_key="user.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    hotel: ODCHotel = Relationship(back_populates="requests")
    applications: List["StudentODCApplication"] = Relationship(back_populates="request")

    @property
    def hotel_name(self) -> str:
        return self.hotel.name if self.hotel else "Unknown Hotel"

class StudentODCApplication(SQLModel, table=True):
    """Student Application for ODC"""
    __tablename__ = "student_odc_application"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    request_id: int = Field(foreign_key="odc_request.id")
    student_id: int = Field(foreign_key="student.id")
    status: ApplicationStatus = Field(default=ApplicationStatus.APPLIED)
    admin_remarks: Optional[str] = None
    
    # Feedback fields
    student_feedback: Optional[str] = None
    student_rating: Optional[int] = Field(default=None, ge=1, le=5)  # 1-5 stars
    hotel_feedback: Optional[str] = None
    hotel_rating: Optional[int] = Field(default=None, ge=1, le=5)  # 1-5 stars
    
    # Payout fields
    payout_status: PayoutStatus = Field(default=PayoutStatus.PENDING)
    payout_amount: Optional[float] = None
    
    # Timestamps
    applied_at: datetime = Field(default_factory=datetime.utcnow)
    attendance_confirmed_at: Optional[datetime] = None
    
    # Relationships
    request: ODCRequest = Relationship(back_populates="applications")
    payout: Optional["ODCPayout"] = Relationship(back_populates="application")

class ODCBilling(SQLModel, table=True):
    """Billing/Invoice for ODC Event sent to Hotel"""
    __tablename__ = "odc_billing"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    request_id: int = Field(foreign_key="odc_request.id", unique=True)
    invoice_number: str = Field(unique=True, index=True)
    
    # Billing details
    total_students: int  # Number of students who attended
    amount_per_student: float
    total_amount: float
    
    # Status and dates
    status: BillingStatus = Field(default=BillingStatus.DRAFT)
    invoice_date: date
    due_date: Optional[date] = None
    paid_date: Optional[date] = None
    
    # Payment details
    payment_method: Optional[PaymentMethod] = None
    payment_reference: Optional[str] = None
    
    # Metadata
    notes: Optional[str] = None
    created_by_id: int = Field(foreign_key="user.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    request: ODCRequest = Relationship()

class ODCPayout(SQLModel, table=True):
    """Payout to Student for ODC Attendance"""
    __tablename__ = "odc_payout"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    application_id: int = Field(foreign_key="student_odc_application.id", unique=True)
    
    # Payout details
    amount: float
    payment_method: PaymentMethod
    transaction_reference: Optional[str] = None
    
    # Dates
    payout_date: date
    processed_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Metadata
    processed_by_id: int = Field(foreign_key="user.id")
    notes: Optional[str] = None
    
    # Relationships
    application: StudentODCApplication = Relationship(back_populates="payout")


# ======================================================================
# Portal
# ======================================================================

"""
Student Portal Models - Portal Access, Activity & Notifications
"""
from typing import TYPE_CHECKING, List, Optional
from datetime import datetime
from enum import Enum
from sqlmodel import SQLModel, Field, Relationship, Column
from sqlalchemy import Text, JSON

if TYPE_CHECKING:
    from .student import Student
    from app.models import User


class ActivityType(str, Enum):
    """Student activity types"""
    LOGIN = "LOGIN"
    LOGOUT = "LOGOUT"
    PROFILE_UPDATE = "PROFILE_UPDATE"
    DOCUMENT_UPLOAD = "DOCUMENT_UPLOAD"
    FEE_PAYMENT = "FEE_PAYMENT"
    EXAM_REGISTRATION = "EXAM_REGISTRATION"
    HALL_TICKET_DOWNLOAD = "HALL_TICKET_DOWNLOAD"
    RESULT_VIEW = "RESULT_VIEW"


class NotificationPriority(str, Enum):
    """Notification priority levels"""
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    URGENT = "URGENT"


class StudentPortalAccess(SQLModel, table=True):
    """Student portal access and authentication"""
    __tablename__ = "student_portal_access"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    
    # Links
    student_id: int = Field(foreign_key="student.id", unique=True, index=True)
    user_id: Optional[int] = Field(default=None, foreign_key="user.id")
    
    # Access status
    is_active: bool = Field(default=True)
    activation_date: Optional[datetime] = None
    deactivation_date: Optional[datetime] = None
    deactivation_reason: Optional[str] = Field(default=None, sa_column=Column(Text))
    
    # Login tracking
    last_login: Optional[datetime] = None
    last_login_ip: Optional[str] = None
    login_count: int = Field(default=0)
    failed_login_attempts: int = Field(default=0)
    last_failed_login: Optional[datetime] = None
    
    # Security
    password_reset_required: bool = Field(default=False)
    password_reset_token: Optional[str] = None
    password_reset_expires: Optional[datetime] = None
    two_factor_enabled: bool = Field(default=False)
    two_factor_secret: Optional[str] = None
    
    # Session management
    current_session_token: Optional[str] = None
    session_expires_at: Optional[datetime] = None
    
    # Preferences
    email_notifications: bool = Field(default=True)
    sms_notifications: bool = Field(default=False)
    language_preference: str = Field(default="en")
    theme_preference: str = Field(default="light")
    
    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    student: "Student" = Relationship()
    activities: List["StudentActivity"] = Relationship(
        back_populates="student_portal",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )


class StudentActivity(SQLModel, table=True):
    """Student activity log"""
    __tablename__ = "student_activity"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    
    # Links
    student_id: int = Field(foreign_key="student.id", index=True)
    student_portal_access_id: int = Field(foreign_key="student_portal_access.id", index=True)
    
    # Activity details
    activity_type: ActivityType
    activity_description: str
    meta_data: Optional[str] = Field(default=None, sa_column=Column(JSON))
    
    # Request details
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    device_type: Optional[str] = None  # mobile, desktop, tablet
    
    # Status
    is_successful: bool = Field(default=True)
    error_message: Optional[str] = None
    
    # Timestamp
    created_at: datetime = Field(default_factory=datetime.utcnow, index=True)
    
    # Relationships
    student: "Student" = Relationship()
    student_portal: "StudentPortalAccess" = Relationship(back_populates="activities")


class StudentNotification(SQLModel, table=True):
    """Student notifications"""
    __tablename__ = "student_notification"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    
    # Links
    student_id: int = Field(foreign_key="student.id", index=True)
    
    # Notification details
    notification_type: str  # FEE_DUE, EXAM_SCHEDULE, RESULT_PUBLISHED, etc.
    title: str = Field(max_length=200)
    message: str = Field(sa_column=Column(Text))
    link: Optional[str] = None  # Link to relevant page
    
    # Priority
    priority: NotificationPriority = Field(default=NotificationPriority.MEDIUM)
    
    # Read status
    is_read: bool = Field(default=False)
    read_at: Optional[datetime] = None
    
    # Delivery
    sent_via_email: bool = Field(default=False)
    email_sent_at: Optional[datetime] = None
    sent_via_sms: bool = Field(default=False)
    sms_sent_at: Optional[datetime] = None
    
    # Action required
    requires_action: bool = Field(default=False)
    action_completed: bool = Field(default=False)
    action_completed_at: Optional[datetime] = None
    
    # Expiry
    expires_at: Optional[datetime] = None
    is_expired: bool = Field(default=False)
    
    # Metadata
    meta_data: Optional[str] = Field(default=None, sa_column=Column(JSON))
    
    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow, index=True)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    student: "Student" = Relationship()
