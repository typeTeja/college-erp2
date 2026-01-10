"""
Master Data Models for Settings Module
Covers: Academic Setup, Fee Configuration, Admission Setup, Infrastructure
"""
from typing import TYPE_CHECKING, List, Optional, Any
from datetime import datetime, date
from decimal import Decimal
from enum import Enum as PyEnum
from sqlmodel import SQLModel, Field, Relationship, Column, JSON
from sqlalchemy import DECIMAL, Text

# ============================================================================
# SECTION 2: Academic Setup
# ============================================================================

class AcademicYearStatus(str, PyEnum):
    UPCOMING = "UPCOMING"
    ACTIVE = "ACTIVE"
    COMPLETED = "COMPLETED"

class AcademicYear(SQLModel, table=True):
    """Academic Year Management - Calendar years"""
    __tablename__ = "academic_year"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(unique=True, index=True)  # e.g., "2024-2025"
    start_date: date
    end_date: date
    status: AcademicYearStatus = Field(default=AcademicYearStatus.UPCOMING)
    is_current: bool = Field(default=False)
    
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)



    updated_at: datetime = Field(default_factory=datetime.utcnow)


class Section(SQLModel, table=True):
    """Section within a batch semester - (e.g., Section A, Section B)"""
    __tablename__ = "section"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str  # e.g., "Section A", "Section B"
    code: str = Field(index=True)  # e.g., "A", "B"
    
    # Linked to BatchSemester
    batch_semester_id: int = Field(foreign_key="batch_semesters.id", index=True)
    # Legacy semester_id removed
    
    batch_id: Optional[int] = Field(default=None, foreign_key="academic_batches.id", index=True)
    
    # Faculty assignment (class teacher/coordinator)
    faculty_id: Optional[int] = Field(default=None, foreign_key="faculty.id", index=True)
    
    max_strength: int = Field(default=40)
    current_strength: int = Field(default=0)
    
    is_active: bool = Field(default=True)
    
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    batch_semester: Optional["BatchSemester"] = Relationship(back_populates="sections")
    practical_batches: List["PracticalBatch"] = Relationship(back_populates="section")


class PracticalBatch(SQLModel, table=True):
    """Practical Batch within a section - smaller groups for lab work"""
    __tablename__ = "practical_batch"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str  # e.g., "P1", "P2"
    code: str = Field(index=True)
    
    section_id: int = Field(foreign_key="section.id", index=True)
    
    max_strength: int = Field(default=20)
    current_strength: int = Field(default=0)
    
    is_active: bool = Field(default=True)
    
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    section: Optional["Section"] = Relationship(back_populates="practical_batches")


class SubjectType(str, PyEnum):
    THEORY = "THEORY"
    PRACTICAL = "PRACTICAL"
    PROJECT = "PROJECT"
    ELECTIVE = "ELECTIVE"
    AUDIT = "AUDIT"

class ExamType(str, PyEnum):
    INTERNAL = "INTERNAL"
    EXTERNAL = "EXTERNAL"
    BOTH = "BOTH"

class SubjectConfig(SQLModel, table=True):
    """Extended Subject Configuration with exam settings"""
    __tablename__ = "subject_config"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    subject_id: int = Field(foreign_key="subject.id", unique=True, index=True)
    
    subject_type: SubjectType = Field(default=SubjectType.THEORY)
    exam_type: ExamType = Field(default=ExamType.BOTH)
    
    # Marks distribution
    internal_max_marks: int = Field(default=30)
    external_max_marks: int = Field(default=70)
    practical_max_marks: int = Field(default=0)
    
    # Pass criteria
    internal_pass_marks: int = Field(default=12)
    external_pass_marks: int = Field(default=28)
    practical_pass_marks: int = Field(default=0)
    
    # Hours per week
    theory_hours: int = Field(default=3)
    practical_hours: int = Field(default=0)
    tutorial_hours: int = Field(default=0)
    
    is_mandatory: bool = Field(default=True)
    has_attendance_requirement: bool = Field(default=True)
    min_attendance_percent: int = Field(default=75)
    
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


# ============================================================================
# SECTION 3: Fee Configuration
# ============================================================================

class FeeHead(SQLModel, table=True):
    """Fee Heads Management - Types of fees (Tuition, Lab, etc.)"""
    __tablename__ = "fee_head"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(unique=True, index=True)  # e.g., "Tuition Fee", "Lab Fee"
    code: str = Field(unique=True, index=True)  # e.g., "TF", "LF"
    description: Optional[str] = None
    
    is_refundable: bool = Field(default=False)
    is_recurring: bool = Field(default=True)  # Collected every year/semester
    is_mandatory: bool = Field(default=True)
    
    display_order: int = Field(default=0)
    is_active: bool = Field(default=True)
    
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class InstallmentPlan(SQLModel, table=True):
    """Installment Plan Management - Payment schedules"""
    __tablename__ = "installment_plan"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(unique=True, index=True)  # e.g., "Quarterly", "Semester-wise"
    code: str = Field(unique=True, index=True)
    description: Optional[str] = None
    
    number_of_installments: int = Field(default=4)
    
    # JSON array of installment details: [{percentage: 25, due_days_from_start: 0}, ...]
    installment_schedule: Any = Field(default=[], sa_column=Column(JSON))
    
    late_fee_per_day: Decimal = Field(default=Decimal("0.00"), sa_column=Column(DECIMAL(10, 2)))
    grace_period_days: int = Field(default=7)
    max_late_fee: Decimal = Field(default=Decimal("500.00"), sa_column=Column(DECIMAL(10, 2)))
    
    is_active: bool = Field(default=True)
    
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class ScholarshipSlab(SQLModel, table=True):
    """Scholarship Slab Management - Merit-based discounts"""
    __tablename__ = "scholarship_slab"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)  # e.g., "Merit Scholarship - Grade A"
    code: str = Field(unique=True, index=True)
    description: Optional[str] = None
    
    # Eligibility criteria
    min_percentage: Decimal = Field(default=Decimal("0.00"), sa_column=Column(DECIMAL(5, 2)))
    max_percentage: Decimal = Field(default=Decimal("100.00"), sa_column=Column(DECIMAL(5, 2)))
    
    # Discount
    discount_type: str = Field(default="PERCENTAGE")  # PERCENTAGE or FIXED
    discount_value: Decimal = Field(sa_column=Column(DECIMAL(10, 2)))
    max_discount_amount: Optional[Decimal] = Field(default=None, sa_column=Column(DECIMAL(10, 2)))
    
    # Applicable to
    applicable_fee_heads: Any = Field(default=[], sa_column=Column(JSON))  # List of fee_head codes
    
    academic_year_id: Optional[int] = Field(default=None, foreign_key="academic_year.id")
    program_id: Optional[int] = Field(default=None, foreign_key="program.id")
    
    is_active: bool = Field(default=True)
    
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


# ============================================================================
# SECTION 4: Admission Setup
# ============================================================================

class Board(SQLModel, table=True):
    """Boards/Universities Master - CBSE, State Boards, etc."""
    __tablename__ = "board"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(unique=True, index=True)  # e.g., "CBSE", "Telangana State Board"
    code: str = Field(unique=True, index=True)  # e.g., "CBSE", "TSBIE"
    full_name: Optional[str] = None
    state: Optional[str] = None
    country: str = Field(default="India")
    
    is_active: bool = Field(default=True)
    display_order: int = Field(default=0)
    
    created_at: datetime = Field(default_factory=datetime.utcnow)


class PreviousQualification(SQLModel, table=True):
    """Previous Qualifications - 10th, 12th, Diploma, etc."""
    __tablename__ = "previous_qualification"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(unique=True, index=True)  # e.g., "10th Standard", "12th Science"
    code: str = Field(unique=True, index=True)  # e.g., "10TH", "12TH_SCI"
    level: int = Field(default=1)  # 1=10th, 2=12th, 3=UG, 4=PG
    
    is_mandatory_for_admission: bool = Field(default=True)
    required_documents: Any = Field(default=[], sa_column=Column(JSON))  # List of required doc types
    
    is_active: bool = Field(default=True)
    display_order: int = Field(default=0)
    
    created_at: datetime = Field(default_factory=datetime.utcnow)


class StudyGroup(SQLModel, table=True):
    """Groups of Study - MPC, BiPC, Commerce, etc."""
    __tablename__ = "study_group"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(unique=True, index=True)  # e.g., "MPC", "BiPC", "Commerce"
    code: str = Field(unique=True, index=True)
    full_name: Optional[str] = None  # e.g., "Mathematics, Physics, Chemistry"
    
    qualification_id: Optional[int] = Field(default=None, foreign_key="previous_qualification.id")
    
    subjects: Any = Field(default=[], sa_column=Column(JSON))  # List of subjects
    
    is_active: bool = Field(default=True)
    display_order: int = Field(default=0)
    
    created_at: datetime = Field(default_factory=datetime.utcnow)


class ReservationCategory(SQLModel, table=True):
    """Reservation Categories - SC, ST, OBC, etc."""
    __tablename__ = "reservation_category"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(unique=True, index=True)  # e.g., "SC", "ST", "OBC"
    code: str = Field(unique=True, index=True)
    full_name: Optional[str] = None  # e.g., "Scheduled Caste"
    
    reservation_percentage: Decimal = Field(default=Decimal("0.00"), sa_column=Column(DECIMAL(5, 2)))
    fee_concession_percentage: Decimal = Field(default=Decimal("0.00"), sa_column=Column(DECIMAL(5, 2)))
    
    requires_certificate: bool = Field(default=True)
    certificate_issuing_authority: Optional[str] = None
    
    is_active: bool = Field(default=True)
    display_order: int = Field(default=0)
    
    created_at: datetime = Field(default_factory=datetime.utcnow)


class LeadSource(SQLModel, table=True):
    """Lead Sources - Marketing channels"""
    __tablename__ = "lead_source"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(unique=True, index=True)  # e.g., "Website", "Social Media", "Campus Visit"
    code: str = Field(unique=True, index=True)
    description: Optional[str] = None
    
    category: str = Field(default="DIGITAL")  # DIGITAL, OFFLINE, REFERRAL, OTHER
    
    is_active: bool = Field(default=True)
    display_order: int = Field(default=0)
    
    created_at: datetime = Field(default_factory=datetime.utcnow)


# ============================================================================
# SECTION 5: Infrastructure
# ============================================================================

class Designation(SQLModel, table=True):
    """Designation Management"""
    __tablename__ = "designation"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(unique=True, index=True)  # e.g., "Professor", "Assistant Professor"
    code: str = Field(unique=True, index=True)
    
    level: int = Field(default=1)  # Hierarchy level
    department_id: Optional[int] = Field(default=None, foreign_key="department.id")
    
    min_experience_years: int = Field(default=0)
    min_qualification: Optional[str] = None
    
    is_teaching: bool = Field(default=True)
    is_active: bool = Field(default=True)
    display_order: int = Field(default=0)
    
    created_at: datetime = Field(default_factory=datetime.utcnow)


class RoomType(str, PyEnum):
    CLASSROOM = "CLASSROOM"
    LAB = "LAB"
    SEMINAR_HALL = "SEMINAR_HALL"
    AUDITORIUM = "AUDITORIUM"
    LIBRARY = "LIBRARY"
    STAFF_ROOM = "STAFF_ROOM"
    OFFICE = "OFFICE"
    OTHER = "OTHER"

class MasterClassroom(SQLModel, table=True):
    """Classroom Management"""
    __tablename__ = "master_classroom"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)  # e.g., "Room 101", "Computer Lab 1"
    code: str = Field(unique=True, index=True)
    
    room_type: RoomType = Field(default=RoomType.CLASSROOM)
    building: Optional[str] = None
    floor: Optional[int] = None
    
    capacity: int = Field(default=40)
    
    has_projector: bool = Field(default=False)
    has_ac: bool = Field(default=False)
    has_smart_board: bool = Field(default=False)
    has_computer: bool = Field(default=False)
    
    department_id: Optional[int] = Field(default=None, foreign_key="department.id")
    
    is_active: bool = Field(default=True)
    
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class PlacementCompany(SQLModel, table=True):
    """Hotels/Companies for Placements"""
    __tablename__ = "placement_company"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)  # e.g., "Taj Hotels", "ITC Hotels"
    code: str = Field(unique=True, index=True)
    
    company_type: str = Field(default="HOTEL")  # HOTEL, RESTAURANT, CRUISE, OTHER
    
    # Contact Information
    contact_person: Optional[str] = None
    contact_email: Optional[str] = None
    contact_phone: Optional[str] = None
    
    address: Optional[str] = Field(default=None, sa_column=Column(Text))
    city: Optional[str] = None
    state: Optional[str] = None
    country: str = Field(default="India")
    
    website: Optional[str] = None
    
    # Partnership details
    is_partner: bool = Field(default=False)
    partnership_start_date: Optional[date] = None
    mou_document_url: Optional[str] = None
    
    # Placement stats
    avg_package_lpa: Optional[Decimal] = Field(default=None, sa_column=Column(DECIMAL(10, 2)))
    students_placed: int = Field(default=0)
    
    is_active: bool = Field(default=True)
    
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


# ============================================================================
# Email/SMS Settings
# ============================================================================

class EmailTemplate(SQLModel, table=True):
    """Email Templates for various notifications"""
    __tablename__ = "email_template"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(unique=True, index=True)  # e.g., "welcome_email", "fee_reminder"
    subject: str
    body: str = Field(sa_column=Column(Text))
    
    template_type: str = Field(default="TRANSACTIONAL")  # TRANSACTIONAL, PROMOTIONAL
    
    variables: Any = Field(default=[], sa_column=Column(JSON))  # List of available variables
    
    is_active: bool = Field(default=True)
    
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class SMSTemplate(SQLModel, table=True):
    """SMS Templates for various notifications"""
    __tablename__ = "sms_template"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(unique=True, index=True)
    content: str = Field(sa_column=Column(Text))
    
    dlt_template_id: Optional[str] = None  # DLT registered template ID (India specific)
    sender_id: Optional[str] = None  # e.g., "RCHMCT"
    
    template_type: str = Field(default="TRANSACTIONAL")
    
    variables: Any = Field(default=[], sa_column=Column(JSON))
    
    is_active: bool = Field(default=True)
    
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
