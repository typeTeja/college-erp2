"""
Academic Domain Models

All database models for the academic domain including:
- Academic setup (years, sections, practical batches)
- Regulations and program structure
- Academic batches and semesters
- Student assignments and allocations
- Attendance tracking
- Timetable management
- Exam management (internal, university, hall tickets)
- Student academic history
"""



# ======================================================================
# Setup
# ======================================================================

from typing import TYPE_CHECKING, List, Optional
from datetime import datetime, date
from decimal import Decimal
from enum import Enum as PyEnum
from sqlmodel import SQLModel, Field, Relationship, Column
from sqlalchemy import DECIMAL
from app.shared.enums import AcademicYearStatus, ExamType, SubjectType, BatchStatus


if TYPE_CHECKING:
    from app.domains.admission.models import EntranceExamResult
    from .batch import BatchSemester


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

class Section(SQLModel, table=True):
    """Section within a batch semester - (e.g., Section A, Section B)"""
    __tablename__ = "section"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str  # e.g., "Section A", "Section B"
    code: str = Field(index=True)  # e.g., "A", "B"
    
    # Linked to BatchSemester
    batch_semester_id: int = Field(foreign_key="batch_semesters.id", index=True)
    
    batch_id: Optional[int] = Field(default=None, foreign_key="academic_batches.id", index=True)
    
    # Faculty assignment (class teacher/coordinator)
    faculty_id: Optional[int] = Field(default=None, foreign_key="faculty.id", index=True)
    
    max_strength: int = Field(default=40)
    current_strength: int = Field(default=0)
    
    is_active: bool = Field(default=True)
    
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    batch_semester: Optional["BatchSemester"] = Relationship(back_populates="sections")

class PracticalBatch(SQLModel, table=True):
    """Practical Batch within a semester - independent of sections"""
    __tablename__ = "practical_batch"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str  # e.g., "Batch A1", "Batch B1"
    code: str = Field(index=True)
    
    # Linked to BatchSemester directly (Sibling to Section)
    batch_semester_id: int = Field(foreign_key="batch_semesters.id", index=True)
    
    max_strength: int = Field(default=20)
    current_strength: int = Field(default=0)
    
    is_active: bool = Field(default=True)
    
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    batch_semester: Optional["BatchSemester"] = Relationship(back_populates="practical_batches")


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


# ======================================================================
# Regulation
# ======================================================================

"""
Regulation Models - Academic Rules Engine

CRITICAL RULES:
- Regulations are LOCKED after first batch creation
- Locked regulations CANNOT be modified or deleted
- All academic rules frozen to batches on creation
"""
from typing import TYPE_CHECKING, List, Optional
from datetime import datetime
from decimal import Decimal
from sqlmodel import SQLModel, Field, Relationship, Column
from sqlalchemy import DECIMAL, Text, UniqueConstraint

if TYPE_CHECKING:
    from app.models.program import Program
    from .batch import AcademicBatch


class Regulation(SQLModel, table=True):
    """
    Academic Regulation - Defines rules for a program cohort
    
    LOCKING RULES:
    - is_locked = False: Can be edited/deleted
    - is_locked = True: IMMUTABLE (after batch creation)
    - version: Optimistic locking for concurrent updates
    """
    __tablename__ = "regulations"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    regulation_code: str = Field(unique=True, index=True, max_length=20)  # "R26", "R24"
    regulation_name: str = Field(max_length=100)
    program_id: int = Field(foreign_key="program.id", index=True)
    
    # Promotion Model
    promotion_model: str = Field(default="CREDIT_BASED", max_length=50)
    
    # Year-wise promotion percentages
    year1_to_year2_min_percentage: int = Field(default=50, ge=0, le=100)
    year2_to_year3_min_year2_percentage: int = Field(default=50, ge=0, le=100)
    year3_to_graduation_min_percentage: int = Field(default=100, ge=0, le=100)
    
    # Passing marks criteria (Global/Fallback)
    min_internal_pass: int = Field(default=12, ge=0)
    min_external_pass: int = Field(default=28, ge=0)
    min_total_pass: int = Field(default=40, ge=0)

    # Theory Evaluation Config
    theory_max_marks: int = Field(default=100, ge=0)
    theory_internal_max: int = Field(default=60, ge=0)
    theory_external_max: int = Field(default=40, ge=0)
    theory_pass_percentage: int = Field(default=40, ge=0, le=100)

    # Practical Evaluation Config
    practical_max_marks: int = Field(default=100, ge=0)
    practical_internal_max: int = Field(default=40, ge=0)
    practical_external_max: int = Field(default=60, ge=0)
    practical_pass_percentage: int = Field(default=50, ge=0, le=100)
    
    # Locking mechanism
    is_locked: bool = Field(default=False, index=True)
    locked_at: Optional[datetime] = None
    locked_by: Optional[int] = Field(default=None, foreign_key="user.id")
    
    # Optimistic locking
    version: int = Field(default=1)
    
    # Status
    is_active: bool = Field(default=True, index=True)
    
    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    created_by: Optional[int] = Field(default=None, foreign_key="user.id")
    updated_by: Optional[int] = Field(default=None, foreign_key="user.id")
    
    # Relationships
    program: "Program" = Relationship() # back_populates="regulations" removed to avoid circular mapper issue
    subjects: List["RegulationSubject"] = Relationship(
        back_populates="regulation",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )
    semesters: List["RegulationSemester"] = Relationship(
        back_populates="regulation",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )
    promotion_rules: List["RegulationPromotionRule"] = Relationship(
        back_populates="regulation",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )
    batches: List["AcademicBatch"] = Relationship(back_populates="regulation")  # NEW


class RegulationSubject(SQLModel, table=True):
    """
    Subject definition within a regulation
    Frozen to batches on creation
    """
    __tablename__ = "regulation_subjects"
    __table_args__ = (
        UniqueConstraint('regulation_id', 'subject_code', name='uq_regulation_subject'),
    )
    
    id: Optional[int] = Field(default=None, primary_key=True)
    regulation_id: int = Field(foreign_key="regulations.id", index=True)
    
    # Subject identification
    subject_code: str = Field(max_length=20, index=True)
    subject_name: str = Field(max_length=200)
    short_name: str = Field(max_length=50)
    
    # Subject type
    subject_type: str = Field(max_length=20)  # THEORY, PRACTICAL, INTERNSHIP, PROJECT
    
    # Semester placement
    program_year: int = Field(ge=1, le=5)
    semester_no: int = Field(ge=1, le=10)
    
    # Marks structure
    internal_max: int = Field(ge=0)
    external_max: int = Field(ge=0)
    total_max: int = Field(ge=0)
    passing_percentage: int = Field(default=40, ge=0, le=100)
    
    # Evaluation configuration
    evaluation_type: str = Field(max_length=30)  # EXAM, CONTINUOUS, ATTENDANCE_ONLY, CERTIFICATION
    has_exam: bool = Field(default=True)
    has_assignments: bool = Field(default=True)
    hours_per_session: int = Field(default=1, ge=0)
    
    # Credits
    credits: int = Field(ge=0)
    
    # Status
    is_active: bool = Field(default=True)
    is_elective: bool = Field(default=False)
    
    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    regulation: "Regulation" = Relationship(back_populates="subjects")


class RegulationSemester(SQLModel, table=True):
    """
    Semester structure within a regulation
    Defines credit requirements per semester
    """
    __tablename__ = "regulation_semesters"
    __table_args__ = (
        UniqueConstraint('regulation_id', 'semester_no', name='uq_regulation_semester'),
    )
    
    id: Optional[int] = Field(default=None, primary_key=True)
    regulation_id: int = Field(foreign_key="regulations.id", index=True)
    
    program_year: int = Field(ge=1, le=5)
    semester_no: int = Field(ge=1, le=10)
    semester_name: str = Field(max_length=50)  # "Semester 1", "Semester 2"
    
    # Credit requirements
    total_credits: int = Field(default=0, ge=0)
    min_credits_to_pass: int = Field(default=0, ge=0)
    
    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    regulation: "Regulation" = Relationship(back_populates="semesters")


class RegulationPromotionRule(SQLModel, table=True):
    """
    Promotion rules for year-to-year progression
    """
    __tablename__ = "regulation_promotion_rules"
    __table_args__ = (
        UniqueConstraint('regulation_id', 'from_year', 'to_year', name='uq_regulation_promotion'),
    )
    
    id: Optional[int] = Field(default=None, primary_key=True)
    regulation_id: int = Field(foreign_key="regulations.id", index=True)
    
    from_year: int = Field(ge=1, le=5)
    to_year: int = Field(ge=1, le=5)
    
    # Previous year requirement
    min_prev_year_percentage: int = Field(default=0, ge=0, le=100)
    
    # Current year requirement
    min_current_year_percentage: int = Field(default=50, ge=0, le=100)
    
    # Additional rules (JSON)
    additional_rules: Optional[str] = Field(default=None, sa_column=Column(Text))
    
    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    regulation: "Regulation" = Relationship(back_populates="promotion_rules")


# ======================================================================
# Batch
# ======================================================================

"""
Batch Models - Academic Batch with Regulation Freezing

CRITICAL RULES:
- Batches bind to ONE regulation permanently
- Regulation data is FROZEN (copied) to batch tables on creation
- Regulation is LOCKED after first batch creation
- ProgramYear is SYSTEM-OWNED and READ-ONLY
"""
from typing import TYPE_CHECKING, List, Optional
from datetime import datetime, date
from sqlmodel import SQLModel, Field, Relationship, Column
from sqlalchemy import Text, UniqueConstraint

if TYPE_CHECKING:
    from app.models.program import Program
    from .regulation import Regulation


class ProgramYear(SQLModel, table=True):
    """
    SYSTEM-OWNED MODEL - READ-ONLY
    
    Auto-generated during batch creation ONLY
    - NO UPDATE API endpoint allowed
    - NO DELETE API endpoint allowed
    - Used only for reads (dashboards, hierarchy)
    
    Represents academic years within a batch (1st Year, 2nd Year, etc.)
    """
    __tablename__ = "program_years"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    batch_id: int = Field(foreign_key="academic_batches.id", index=True)
    year_no: int = Field(ge=1, le=5)  # 1, 2, 3, etc.
    year_name: str = Field(max_length=50)  # "1st Year", "2nd Year"
    
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    batch: "AcademicBatch" = Relationship(back_populates="program_years")
    semesters: List["BatchSemester"] = Relationship(back_populates="program_year")


class AcademicBatch(SQLModel, table=True):
    """
    Academic Batch - Binds students to a regulation
    
    CRITICAL: Once created, regulation data is frozen to this batch
    """
    __tablename__ = "academic_batches"
    __table_args__ = (
        UniqueConstraint('program_id', 'joining_year', name='uq_batch_program_year'),
    )
    
    id: Optional[int] = Field(default=None, primary_key=True)
    
    # Batch identification
    batch_code: str = Field(unique=True, index=True, max_length=50)  # "2024-2027"
    batch_name: str = Field(max_length=100)  # "Batch 2024-2027"
    
    # Links
    program_id: int = Field(foreign_key="program.id", index=True)
    regulation_id: int = Field(foreign_key="regulations.id", index=True)
    
    # Academic years
    joining_year: int  # 2024
    start_year: int  # 2024
    end_year: int  # 2027
    
    # Current status
    current_year: int = Field(default=1, ge=1)
    total_students: int = Field(default=0, ge=0)
    
    # Status
    status: BatchStatus = Field(default=BatchStatus.ACTIVE)
    is_active: bool = Field(default=True)
    
    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    created_by: Optional[int] = Field(default=None, foreign_key="user.id")
    
    # Relationships
    program: "Program" = Relationship(back_populates="batches")
    regulation: "Regulation" = Relationship(back_populates="batches")
    program_years: List["ProgramYear"] = Relationship(
        back_populates="batch",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )
    subjects: List["BatchSubject"] = Relationship(
        back_populates="batch",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )
    semesters: List["BatchSemester"] = Relationship(
        back_populates="batch",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )


class BatchSemester(SQLModel, table=True):
    """
    Frozen semester structure for a batch
    Copied from RegulationSemester on batch creation
    """
    __tablename__ = "batch_semesters"
    __table_args__ = (
        UniqueConstraint('batch_id', 'semester_no', name='uq_batch_semester'),
    )
    
    id: Optional[int] = Field(default=None, primary_key=True)
    batch_id: int = Field(foreign_key="academic_batches.id", index=True)
    program_year_id: int = Field(foreign_key="program_years.id", index=True)
    
    year_no: int = Field(ge=1, le=5) # Renamed from program_year to avoid conflict with relationship
    semester_no: int = Field(ge=1, le=10)
    semester_name: str = Field(max_length=50)
    
    # Credit requirements (frozen from regulation)
    total_credits: int = Field(default=0, ge=0)
    min_credits_to_pass: int = Field(default=0, ge=0)
    
    # Semester Dates (For Auto-Promotion)
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    is_active: bool = Field(default=False)
    
    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    batch: "AcademicBatch" = Relationship(back_populates="semesters")
    program_year: "ProgramYear" = Relationship(back_populates="semesters")
    sections: List["Section"] = Relationship(back_populates="batch_semester")
    practical_batches: List["PracticalBatch"] = Relationship(back_populates="batch_semester")


class BatchSubject(SQLModel, table=True):
    """
    Frozen subject definition for a batch
    Copied from RegulationSubject on batch creation
    
    IMMUTABLE after batch creation
    """
    __tablename__ = "batch_subjects"
    __table_args__ = (
        UniqueConstraint('batch_id', 'subject_code', name='uq_batch_subject'),
    )
    
    id: Optional[int] = Field(default=None, primary_key=True)
    batch_id: int = Field(foreign_key="academic_batches.id", index=True)
    
    # Subject identification (frozen)
    subject_code: str = Field(max_length=20, index=True)
    subject_name: str = Field(max_length=200)
    short_name: str = Field(max_length=50)
    
    # Subject type (frozen)
    subject_type: str = Field(max_length=20)
    
    # Semester placement (frozen)
    program_year: int = Field(ge=1, le=5)
    semester_no: int = Field(ge=1, le=10)
    
    # Marks structure (frozen)
    internal_max: int = Field(ge=0)
    external_max: int = Field(ge=0)
    total_max: int = Field(ge=0)
    passing_percentage: int = Field(default=40, ge=0, le=100)
    
    # Evaluation configuration (frozen)
    evaluation_type: str = Field(max_length=30)
    has_exam: bool = Field(default=True)
    has_assignments: bool = Field(default=True)
    hours_per_session: int = Field(default=1, ge=0)
    
    # Credits (frozen)
    credits: int = Field(ge=0)
    
    # Status
    is_active: bool = Field(default=True)
    is_elective: bool = Field(default=False)
    
    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    batch: "AcademicBatch" = Relationship(back_populates="subjects")


# ======================================================================
# Assignment
# ======================================================================

"""
Student Assignment Models
Tracks student assignments to sections and lab groups
"""
from typing import TYPE_CHECKING, Optional
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from app.models.student import Student
    from .setup import Section, PracticalBatch
    from .batch import AcademicBatch
    from app.models import User


class StudentSectionAssignment(SQLModel, table=True):
    """
    Assigns students to sections within a batch/semester
    
    Business Rules:
    - One student can only be in one section per semester
    - Cannot exceed section capacity
    - Assignment can be AUTO, MANUAL, or RULE_BASED
    """
    __tablename__ = "student_section_assignment"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    student_id: int = Field(foreign_key="student.id", index=True)
    section_id: int = Field(foreign_key="section.id", index=True)
    batch_id: int = Field(foreign_key="academic_batches.id", index=True)
    semester_no: int = Field(ge=1, le=10)
    
    assignment_type: str = Field(default="AUTO", max_length=20)  # AUTO, MANUAL, RULE_BASED
    assigned_at: datetime = Field(default_factory=datetime.utcnow)
    assigned_by: Optional[int] = Field(default=None, foreign_key="user.id")
    is_active: bool = Field(default=True)
    
    # Relationships
    student: "Student" = Relationship()
    section: "Section" = Relationship()
    batch: "AcademicBatch" = Relationship()
    assigner: Optional["User"] = Relationship()


class StudentLabAssignment(SQLModel, table=True):
    """
    Assigns students to lab groups within a section
    
    Business Rules:
    - One student can only be in one lab group per practical batch
    - Cannot exceed lab capacity
    - Must be assigned to section first
    """
    __tablename__ = "student_lab_assignment"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    student_id: int = Field(foreign_key="student.id", index=True)
    practical_batch_id: int = Field(foreign_key="practical_batch.id", index=True)
    section_id: int = Field(foreign_key="section.id", index=True)
    
    assignment_type: str = Field(default="AUTO", max_length=20)  # AUTO, MANUAL
    assigned_at: datetime = Field(default_factory=datetime.utcnow)
    assigned_by: Optional[int] = Field(default=None, foreign_key="user.id")
    is_active: bool = Field(default=True)
    
    # Relationships
    student: "Student" = Relationship()
    practical_batch: "PracticalBatch" = Relationship()
    section: "Section" = Relationship()
    assigner: Optional["User"] = Relationship()


# ======================================================================
# Allocation
# ======================================================================

from typing import Optional
from sqlmodel import SQLModel, Field, UniqueConstraint
from datetime import datetime

class StudentPracticalBatchAllocation(SQLModel, table=True):
    """
    Allocates a student to a specific Practical Batch for a specific Subject.
    
    RULES:
    1. A student can only be in ONE practical batch per subject per semester.
    2. Capacity limit of the Practical Batch must be checked before creating allocation.
    """
    __tablename__ = "student_practical_batch_allocation"
    __table_args__ = (
        UniqueConstraint('student_id', 'subject_id', 'batch_semester_id', name='uq_student_subject_allocation'),
    )
    
    id: Optional[int] = Field(default=None, primary_key=True)
    
    student_id: int = Field(foreign_key="student.id", index=True)
    practical_batch_id: int = Field(foreign_key="practical_batch.id", index=True)
    batch_semester_id: int = Field(foreign_key="batch_semesters.id", index=True)
    subject_id: int = Field(foreign_key="subject.id", index=True)
    
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)


# ======================================================================
# Student History
# ======================================================================

"""
Student History Models - Academic Progression Tracking

CRITICAL CORRECTIONS APPLIED:
1. StudentCreditTracker REMOVED (merged into StudentSemesterHistory)
2. Single source of truth for semester progression
3. Promotion transaction order: History → Logs → Student → Commit
"""
from typing import TYPE_CHECKING, Optional
from datetime import datetime
from decimal import Decimal, ROUND_HALF_UP
from sqlmodel import SQLModel, Field, Relationship, Column
from sqlalchemy import DECIMAL, Text, UniqueConstraint

if TYPE_CHECKING:
    from app.models.student import Student
    from .batch import AcademicBatch
    from .regulation import Regulation


class StudentSemesterHistory(SQLModel, table=True):
    """
    SINGLE SOURCE OF TRUTH for student academic progression
    
    Combines:
    - Semester history (academic timeline)
    - Credit tracking (earned/failed credits)
    
    CRITICAL: This is the ONLY table for credit tracking
    StudentCreditTracker has been REMOVED
    """
    __tablename__ = "student_semester_history"
    __table_args__ = (
        UniqueConstraint('student_id', 'academic_year_id', 'semester_no', name='uq_student_semester'),
    )
    
    id: Optional[int] = Field(default=None, primary_key=True)
    
    # Student links
    student_id: int = Field(foreign_key="student.id", index=True)
    batch_id: int = Field(foreign_key="academic_batches.id", index=True)
    academic_year_id: int = Field(foreign_key="academic_year.id", index=True)
    regulation_id: int = Field(foreign_key="regulations.id", index=True)
    
    # Semester identification
    program_year: int = Field(ge=1, le=5)  # 1, 2, 3
    semester_no: int = Field(ge=1, le=10)  # 1-6 typically
    
    # CREDIT TRACKING (merged from StudentCreditTracker)
    total_credits: int = Field(default=0, ge=0)
    earned_credits: int = Field(default=0, ge=0)
    failed_credits: int = Field(default=0, ge=0)
    
    # Status
    status: str = Field(max_length=20)  # PROMOTED, DETAINED, REPEAT, READMISSION
    
    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    student: "Student" = Relationship(back_populates="semester_history")
    batch: "AcademicBatch" = Relationship()
    regulation: "Regulation" = Relationship()
    
    @property
    def credit_percentage(self) -> Decimal:
        """
        Calculate credit percentage with precision
        Uses Decimal to avoid floating-point errors
        """
        if self.total_credits == 0:
            return Decimal('0.00')
        
        pct = (Decimal(str(self.earned_credits)) / Decimal(str(self.total_credits))) * 100
        return pct.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    
    @property
    def is_passed(self) -> bool:
        """Check if student passed this semester"""
        return self.status == "PROMOTED"


class StudentPromotionLog(SQLModel, table=True):
    """
    Log of all promotion/detention decisions
    
    CRITICAL: This is written BEFORE student record is updated
    Ensures audit trail exists even if transaction fails
    """
    __tablename__ = "student_promotion_logs"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    
    student_id: int = Field(foreign_key="student.id", index=True)
    batch_id: int = Field(foreign_key="academic_batches.id", index=True)
    regulation_id: int = Field(foreign_key="regulations.id", index=True)
    
    # Promotion details
    from_year: int = Field(ge=1, le=5)
    to_year: int = Field(ge=1, le=5)
    from_semester: int = Field(ge=1, le=10)
    to_semester: int = Field(ge=1, le=10)
    
    # Decision
    status: str = Field(max_length=20)  # PROMOTED, DETAINED, REPEAT
    reason: str = Field(sa_column=Column(Text))
    
    # Credits summary
    year_total_credits: int = Field(default=0, ge=0)
    year_earned_credits: int = Field(default=0, ge=0)
    year_failed_credits: int = Field(default=0, ge=0)
    year_percentage: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(DECIMAL(5, 2))
    )
    
    # Decision maker
    decided_by: int = Field(foreign_key="user.id")
    decided_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    student: "Student" = Relationship(back_populates="promotion_logs")
    batch: "AcademicBatch" = Relationship()
    regulation: "Regulation" = Relationship()


class StudentRegulationMigration(SQLModel, table=True):
    """
    Track regulation changes for students
    
    Rare but important: When a student switches regulations
    (e.g., university changes regulation mid-course)
    """
    __tablename__ = "student_regulation_migrations"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    
    student_id: int = Field(foreign_key="student.id", index=True)
    
    # Migration details
    from_regulation_id: int = Field(foreign_key="regulations.id")
    to_regulation_id: int = Field(foreign_key="regulations.id")
    
    migration_date: datetime = Field(default_factory=datetime.utcnow)
    reason: str = Field(sa_column=Column(Text))
    
    # Approval
    approved_by: int = Field(foreign_key="user.id")
    approved_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    student: "Student" = Relationship()


# ============================================================================
# Promotion Eligibility Check (Business Logic)
# ============================================================================

class PromotionEligibility:
    """
    Check if student is eligible for promotion
    
    Based on regulation rules and credit requirements
    """
    
    @staticmethod
    def check_year_promotion(
        student_id: int,
        current_year: int,
        regulation,
        session
    ) -> dict:
        """
        Check if student can be promoted to next year
        
        Returns:
        {
            "eligible": bool,
            "message": str,
            "year_total_credits": int,
            "year_earned_credits": int,
            "year_failed_credits": int,
            "year_percentage": Decimal
        }
        """
        from sqlmodel import select, func
        
        # Get all semesters for current year
        start_semester = (current_year - 1) * 2 + 1
        end_semester = current_year * 2
        
        # Get semester history for current year
        history_records = session.exec(
            select(StudentSemesterHistory)
            .where(StudentSemesterHistory.student_id == student_id)
            .where(StudentSemesterHistory.program_year == current_year)
            .where(StudentSemesterHistory.semester_no.between(start_semester, end_semester))
        ).all()
        
        if not history_records:
            return {
                "eligible": False,
                "message": "No semester history found for current year",
                "year_total_credits": 0,
                "year_earned_credits": 0,
                "year_failed_credits": 0,
                "year_percentage": Decimal('0.00')
            }
        
        # Calculate year totals
        year_total_credits = sum(h.total_credits for h in history_records)
        year_earned_credits = sum(h.earned_credits for h in history_records)
        year_failed_credits = sum(h.failed_credits for h in history_records)
        
        # Calculate percentage
        if year_total_credits == 0:
            year_percentage = Decimal('0.00')
        else:
            year_percentage = (
                Decimal(str(year_earned_credits)) / Decimal(str(year_total_credits))
            ) * 100
            year_percentage = year_percentage.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        
        # Get promotion rule
        if current_year == 1:
            min_percentage = regulation.year1_to_year2_min_percentage
        elif current_year == 2:
            min_percentage = regulation.year2_to_year3_min_year2_percentage
        else:
            min_percentage = regulation.year3_to_graduation_min_percentage
        
        # Check eligibility
        eligible = year_percentage >= min_percentage
        
        if eligible:
            message = f"Eligible for promotion. Earned {year_percentage}% (required: {min_percentage}%)"
        else:
            message = f"Not eligible. Earned {year_percentage}% (required: {min_percentage}%)"
        
        return {
            "eligible": eligible,
            "message": message,
            "year_total_credits": year_total_credits,
            "year_earned_credits": year_earned_credits,
            "year_failed_credits": year_failed_credits,
            "year_percentage": year_percentage
        }


# ======================================================================
# Attendance
# ======================================================================

from datetime import date, time, datetime
from typing import Optional, List
from enum import Enum
import sqlalchemy as sa
from sqlmodel import Field, Relationship, SQLModel
from app.shared.enums import AttendanceStatus, SessionStatus


# Enums
    

# Models
class AttendanceSession(SQLModel, table=True):
    __tablename__ = "attendance_session"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    subject_id: int = Field(foreign_key="subject.id")
    faculty_id: int = Field(foreign_key="faculty.id")
    program_id: int = Field(foreign_key="program.id")
    program_year_id: int = Field(foreign_key="program_years.id")
    
    semester: int
    section: Optional[str] = Field(default=None, max_length=10) # Made optional
    practical_batch_id: Optional[int] = Field(default=None, foreign_key="practical_batch.id")
    session_date: date
    start_time: time
    end_time: time
    
    status: SessionStatus = Field(default=SessionStatus.SCHEDULED)
    topic_covered: Optional[str] = Field(default=None, sa_column=sa.Column(sa.Text))
    
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now, sa_column_kwargs={"onupdate": datetime.now})

    # Relationships
    subject: Optional["Subject"] = Relationship()
    faculty: Optional["Faculty"] = Relationship()
    # program: Optional["Program"] = Relationship()  # Add if Program model is available
    attendance_records: List["AttendanceRecord"] = Relationship(back_populates="session")


class AttendanceRecord(SQLModel, table=True):
    __tablename__ = "attendance_record"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    session_id: int = Field(foreign_key="attendance_session.id", ondelete="CASCADE")
    student_id: int = Field(foreign_key="student.id")
    
    status: AttendanceStatus
    remarks: Optional[str] = None
    
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now, sa_column_kwargs={"onupdate": datetime.now})
    
    # Relationships
    session: AttendanceSession = Relationship(back_populates="attendance_records")
    student: Optional["Student"] = Relationship()


# ======================================================================
# Timetable
# ======================================================================

from enum import Enum
from typing import Optional, List, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship
from datetime import date, time
from app.shared.enums import AdjustmentStatus, DayOfWeek, SlotType


if TYPE_CHECKING:
    from ...models.faculty import Faculty
    from ...models.subject import Subject
    from .batch import BatchSemester


# --- Master Data ---

class TimeSlot(SQLModel, table=True):
    """Defines a period (e.g., 09:00 - 10:00)"""
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str  # e.g., "Period 1", "Morning Break"
    start_time: time
    end_time: time
    type: SlotType = Field(default=SlotType.THEORY)
    is_active: bool = Field(default=True)

class Classroom(SQLModel, table=True):
    """Physical rooms/labs"""
    id: Optional[int] = Field(default=None, primary_key=True)
    room_number: str = Field(index=True, unique=True)
    capacity: int
    type: str = Field(default="LECTURE") # LECTURE, LAB, SEMINAR_HALL
    is_active: bool = Field(default=True)

# --- Timetable Structure ---

class TimetableTemplate(SQLModel, table=True):
    """Named templates for schedule structures (e.g. 'Regular 9-4', 'Half Day')"""
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(unique=True)
    description: Optional[str] = None

class ClassSchedule(SQLModel, table=True):
    """The actual Timetable entries"""
    __tablename__ = "timetable_entry"

    id: Optional[int] = Field(default=None, primary_key=True)
    academic_year_id: int
    batch_semester_id: int = Field(foreign_key="batch_semesters.id")
    section_id: Optional[int] = None # Link to Section model
    practical_batch_id: Optional[int] = Field(default=None, foreign_key="practical_batch.id")
    
    day_of_week: DayOfWeek
    period_id: int = Field(foreign_key="timeslot.id")
    subject_id: Optional[int] = Field(default=None, foreign_key="subject.id")
    faculty_id: Optional[int] = Field(default=None, foreign_key="faculty.id")
    room_id: Optional[int] = Field(default=None, foreign_key="classroom.id")
    
    # Relationships
    period: Optional[TimeSlot] = Relationship()
    # subject: Optional["Subject"] = Relationship()
    # faculty: Optional["Faculty"] = Relationship()
    # room: Optional[Classroom] = Relationship()

class ClassAdjustment(SQLModel, table=True):
    """Substitution/Adjustment Ledger"""
    id: Optional[int] = Field(default=None, primary_key=True)
    timetable_entry_id: int = Field(foreign_key="timetable_entry.id")
    date: date
    
    original_faculty_id: int = Field(foreign_key="faculty.id")
    substitute_faculty_id: Optional[int] = Field(default=None, foreign_key="faculty.id")
    
    status: AdjustmentStatus = Field(default=AdjustmentStatus.REQUESTED)
    reason: Optional[str] = None
    
    created_at: date = Field(default_factory=date.today)


# ======================================================================
# Exam
# ======================================================================

from typing import TYPE_CHECKING, List, Optional
from datetime import date, time
from enum import Enum
from sqlmodel import SQLModel, Field, Relationship
from app.shared.enums import ExamStatus, ExamType


if TYPE_CHECKING:
    from .batch import BatchSemester
    from ...models.subject import Subject
    from ...models.student import Student


class Exam(SQLModel, table=True):
    """Represents an exam cycle (e.g., Fall 2024 Mid-Terms)"""
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str  # e.g., "Fall 2024 Mid-Term"
    exam_type: ExamType
    academic_year: str  # e.g., "2024-2025"
    
    # Updated to link to BatchSemester
    batch_semester_id: int = Field(foreign_key="batch_semesters.id")
    
    start_date: date
    end_date: date
    status: ExamStatus = Field(default=ExamStatus.DRAFT)
    description: Optional[str] = None
    
    # Relationships
    batch_semester: "BatchSemester" = Relationship()
    schedules: List["ExamSchedule"] = Relationship(back_populates="exam")

class ExamSchedule(SQLModel, table=True):
    """Timetable for a specific subject in an exam"""
    __tablename__ = "exam_schedule"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    exam_id: int = Field(foreign_key="exam.id")
    subject_id: int = Field(foreign_key="subject.id")
    exam_date: date
    start_time: time
    end_time: time
    max_marks: int = Field(default=100)
    passing_marks: int = Field(default=40)
    
    # Relationships
    exam: "Exam" = Relationship(back_populates="schedules")
    subject: "Subject" = Relationship()
    results: List["ExamResult"] = Relationship(back_populates="exam_schedule")

class ExamResult(SQLModel, table=True):
    """Marks obtained by a student in a specific exam schedule"""
    __tablename__ = "exam_result"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    exam_schedule_id: int = Field(foreign_key="exam_schedule.id")
    student_id: int = Field(foreign_key="student.id")
    marks_obtained: float
    grade: Optional[str] = None
    remarks: Optional[str] = None
    is_absent: bool = Field(default=False)
    
    # Relationships
    exam_schedule: "ExamSchedule" = Relationship(back_populates="results")
    student: "Student" = Relationship()


# ======================================================================
# Internal Exam
# ======================================================================

"""
Internal Exam Models - Internal Assessment Management

Manages internal exams, marks entry, and grade calculation
"""
from typing import TYPE_CHECKING, List, Optional
from datetime import datetime, date, time
from enum import Enum
from sqlmodel import SQLModel, Field, Relationship, Column
from sqlalchemy import Text
from app.shared.enums import ExamType


if TYPE_CHECKING:
    from app.models.student import Student
    from .batch import AcademicBatch, BatchSemester, BatchSubject
    from app.models import User


class ExamType(str, Enum):
    """Types of internal exams"""
    MID_TERM = "MID_TERM"
    END_TERM = "END_TERM"
    ASSIGNMENT = "ASSIGNMENT"
    QUIZ = "QUIZ"
    PRACTICAL = "PRACTICAL"
    VIVA = "VIVA"


class ResultStatus(str, Enum):
    """Result status"""
    PASS = "PASS"
    FAIL = "FAIL"
    ABSENT = "ABSENT"
    DETAINED = "DETAINED"


class InternalExam(SQLModel, table=True):
    """Internal exam configuration"""
    __tablename__ = "internal_exam"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    
    # Exam identification
    name: str = Field(max_length=200)  # "Mid Term 1 - 2024"
    exam_code: str = Field(unique=True, index=True, max_length=50)  # "MT1-2024-CSE"
    academic_year: str = Field(index=True)  # "2024-2025"
    
    # Links
    batch_id: int = Field(foreign_key="academic_batches.id", index=True)
    batch_semester_id: int = Field(foreign_key="batch_semesters.id", index=True)
    
    # Exam details
    exam_type: ExamType = Field(default=ExamType.MID_TERM)
    start_date: date
    end_date: date
    
    # Marks configuration
    total_marks: int = Field(default=100, ge=0)
    passing_marks: int = Field(default=40, ge=0)
    weightage: float = Field(default=0.3)  # 30% weightage for final grade
    
    # Instructions
    instructions: Optional[str] = Field(default=None, sa_column=Column(Text))
    
    # Publishing
    is_published: bool = Field(default=False)
    published_at: Optional[datetime] = None
    published_by: Optional[int] = Field(default=None, foreign_key="user.id")
    
    # Status
    is_active: bool = Field(default=True)
    
    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    created_by: Optional[int] = Field(default=None, foreign_key="user.id")
    
    # Relationships
    batch: "AcademicBatch" = Relationship()
    batch_semester: "BatchSemester" = Relationship()
    subjects: List["InternalExamSubject"] = Relationship(
        back_populates="internal_exam",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )


class InternalExamSubject(SQLModel, table=True):
    """Subject configuration for an internal exam"""
    __tablename__ = "internal_exam_subject"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    
    # Links
    internal_exam_id: int = Field(foreign_key="internal_exam.id", index=True)
    batch_subject_id: int = Field(foreign_key="batch_subjects.id", index=True)
    
    # Marks configuration
    max_marks: int = Field(ge=0)
    passing_marks: int = Field(ge=0)
    
    # Exam schedule
    exam_date: date
    exam_time: str  # "10:00 AM"
    duration_minutes: int = Field(default=180)  # 3 hours
    
    # Venue
    room_number: Optional[str] = None
    invigilator_id: Optional[int] = Field(default=None, foreign_key="user.id")
    
    # Status
    is_completed: bool = Field(default=False)
    
    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    internal_exam: "InternalExam" = Relationship(back_populates="subjects")
    batch_subject: "BatchSubject" = Relationship()
    student_marks: List["StudentInternalMarks"] = Relationship(
        back_populates="exam_subject",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )


class StudentInternalMarks(SQLModel, table=True):
    """Individual student marks for an internal exam subject"""
    __tablename__ = "student_internal_marks"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    
    # Links
    student_id: int = Field(foreign_key="student.id", index=True)
    internal_exam_subject_id: int = Field(foreign_key="internal_exam_subject.id", index=True)
    
    # Marks
    marks_obtained: Optional[float] = Field(default=None, ge=0)
    is_absent: bool = Field(default=False)
    
    # Additional details
    remarks: Optional[str] = Field(default=None, sa_column=Column(Text))
    
    # Entry tracking
    entered_by: Optional[int] = Field(default=None, foreign_key="user.id")
    entered_at: Optional[datetime] = None
    
    # Verification
    verified_by: Optional[int] = Field(default=None, foreign_key="user.id")
    verified_at: Optional[datetime] = None
    is_verified: bool = Field(default=False)
    
    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    student: "Student" = Relationship()
    exam_subject: "InternalExamSubject" = Relationship(back_populates="student_marks")


class InternalMarksConsolidated(SQLModel, table=True):
    """Consolidated internal marks for a student in a semester"""
    __tablename__ = "internal_marks_consolidated"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    
    # Links
    student_id: int = Field(foreign_key="student.id", index=True)
    batch_semester_id: int = Field(foreign_key="batch_semesters.id", index=True)
    academic_year: str = Field(index=True)
    
    # Marks summary
    total_max_marks: float = Field(ge=0)
    total_marks_obtained: float = Field(ge=0)
    percentage: float = Field(ge=0, le=100)
    
    # Grading
    grade: Optional[str] = None  # A+, A, B+, B, C, D, F
    gpa: Optional[float] = Field(default=None, ge=0, le=10)
    
    # Performance
    rank: Optional[int] = None
    is_promoted: bool = Field(default=False)
    
    # Result status
    result_status: ResultStatus = Field(default=ResultStatus.PASS)
    
    # Timestamps
    calculated_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    student: "Student" = Relationship()
    batch_semester: "BatchSemester" = Relationship()


# ======================================================================
# University Exam
# ======================================================================

"""
University Exam Models - University Exam Registration & Results

Manages university exam registration, eligibility, and result management
"""
from typing import TYPE_CHECKING, List, Optional
from datetime import datetime, date
from enum import Enum
from sqlmodel import SQLModel, Field, Relationship, Column
from sqlalchemy import Text, JSON

if TYPE_CHECKING:
    from app.models.student import Student
    from .batch import BatchSemester, BatchSubject
    from app.models import User


class ExamResultStatus(str, Enum):
    """University exam result status"""
    PASS = "PASS"
    FAIL = "FAIL"
    ABSENT = "ABSENT"
    DETAINED = "DETAINED"
    WITHHELD = "WITHHELD"


class UniversityExam(SQLModel, table=True):
    """University exam configuration"""
    __tablename__ = "university_exam"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    
    # Exam identification
    exam_name: str = Field(max_length=200)  # "End Semester Exam - May 2024"
    exam_code: str = Field(unique=True, index=True, max_length=50)
    academic_year: str = Field(index=True)
    semester: int = Field(ge=1, le=8)  # 1-8
    
    # Registration period
    registration_start: date
    registration_end: date
    late_registration_end: Optional[date] = None
    
    # Exam period
    exam_start_date: date
    exam_end_date: date
    
    # Fees
    exam_fee: float = Field(ge=0)
    late_fee: float = Field(default=0.0, ge=0)
    
    # Eligibility criteria
    min_attendance_percentage: float = Field(default=75.0, ge=0, le=100)
    allow_detained_students: bool = Field(default=False)
    
    # Instructions
    instructions: Optional[str] = Field(default=None, sa_column=Column(Text))
    
    # Status
    is_active: bool = Field(default=True)
    is_registration_open: bool = Field(default=True)
    
    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    created_by: Optional[int] = Field(default=None, foreign_key="user.id")
    
    # Relationships
    registrations: List["UniversityExamRegistration"] = Relationship(
        back_populates="university_exam",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )
    results: List["UniversityExamResult"] = Relationship(
        back_populates="university_exam",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )


class UniversityExamRegistration(SQLModel, table=True):
    """Student registration for university exam"""
    __tablename__ = "university_exam_registration"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    
    # Links
    student_id: int = Field(foreign_key="student.id", index=True)
    university_exam_id: int = Field(foreign_key="university_exam.id", index=True)
    batch_semester_id: int = Field(foreign_key="batch_semesters.id", index=True)
    
    # Registration details
    registration_number: str = Field(unique=True, index=True)
    registration_date: date = Field(default_factory=date.today)
    is_late_registration: bool = Field(default=False)
    
    # Subjects registered (JSON array of subject IDs)
    subjects_registered: str = Field(sa_column=Column(JSON))
    # Example: [{"subject_id": 1, "subject_code": "CS101", "subject_name": "Programming"}]
    
    # Fee details
    exam_fee: float
    late_fee: float = Field(default=0.0)
    total_fee: float
    fee_paid: bool = Field(default=False)
    payment_id: Optional[str] = None
    payment_date: Optional[date] = None
    
    # Eligibility
    is_eligible: bool = Field(default=True)
    eligibility_remarks: Optional[str] = Field(default=None, sa_column=Column(Text))
    attendance_percentage: Optional[float] = None
    
    # Hall ticket
    hall_ticket_number: Optional[str] = None
    hall_ticket_generated: bool = Field(default=False)
    hall_ticket_url: Optional[str] = None
    
    # Status
    is_cancelled: bool = Field(default=False)
    cancelled_at: Optional[datetime] = None
    cancellation_reason: Optional[str] = Field(default=None, sa_column=Column(Text))
    
    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    student: "Student" = Relationship()
    university_exam: "UniversityExam" = Relationship(back_populates="registrations")
    batch_semester: "BatchSemester" = Relationship()


class UniversityExamResult(SQLModel, table=True):
    """University exam results for individual subjects"""
    __tablename__ = "university_exam_result"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    
    # Links
    student_id: int = Field(foreign_key="student.id", index=True)
    university_exam_id: int = Field(foreign_key="university_exam.id", index=True)
    batch_subject_id: int = Field(foreign_key="batch_subjects.id", index=True)
    
    # Marks
    theory_max_marks: Optional[float] = None
    theory_marks: Optional[float] = None
    practical_max_marks: Optional[float] = None
    practical_marks: Optional[float] = None
    internal_max_marks: Optional[float] = None
    internal_marks: Optional[float] = None
    
    # Total
    total_max_marks: float
    total_marks: float
    percentage: float = Field(ge=0, le=100)
    
    # Grading
    grade: Optional[str] = None  # O, A+, A, B+, B, C, D, F
    grade_points: Optional[float] = None  # 10, 9, 8, 7, 6, 5, 4, 0
    credits: int = Field(ge=0)
    credits_earned: int = Field(ge=0)
    
    # Result
    result_status: ExamResultStatus = Field(default=ExamResultStatus.PASS)
    
    # Remarks
    remarks: Optional[str] = Field(default=None, sa_column=Column(Text))
    
    # Import tracking
    imported_at: Optional[datetime] = None
    imported_by: Optional[int] = Field(default=None, foreign_key="user.id")
    
    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    student: "Student" = Relationship()
    university_exam: "UniversityExam" = Relationship(back_populates="results")
    batch_subject: "BatchSubject" = Relationship()


class SemesterResult(SQLModel, table=True):
    """Consolidated semester results with SGPA/CGPA"""
    __tablename__ = "semester_result"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    
    # Links
    student_id: int = Field(foreign_key="student.id", index=True)
    batch_semester_id: int = Field(foreign_key="batch_semesters.id", index=True)
    academic_year: str = Field(index=True)
    semester: int = Field(ge=1, le=8)
    
    # Credits
    total_credits: int = Field(ge=0)
    credits_earned: int = Field(ge=0)
    credits_failed: int = Field(default=0, ge=0)
    
    # GPA
    sgpa: Optional[float] = Field(default=None, ge=0, le=10)  # Semester GPA
    cgpa: Optional[float] = Field(default=None, ge=0, le=10)  # Cumulative GPA
    
    # Performance
    total_marks: float
    marks_obtained: float
    percentage: float = Field(ge=0, le=100)
    
    # Rank
    rank: Optional[int] = None
    
    # Result
    result_status: ExamResultStatus = Field(default=ExamResultStatus.PASS)
    is_promoted: bool = Field(default=False)
    
    # Backlog subjects (JSON array)
    backlog_subjects: Optional[str] = Field(default=None, sa_column=Column(JSON))
    # Example: [{"subject_id": 1, "subject_code": "CS101", "attempt": 2}]
    
    # Remarks
    remarks: Optional[str] = Field(default=None, sa_column=Column(Text))
    
    # Calculation
    calculated_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    student: "Student" = Relationship()
    batch_semester: "BatchSemester" = Relationship()


# ======================================================================
# Hall Ticket
# ======================================================================

"""
Hall Ticket Models - Hall Ticket Generation & Management

Manages hall ticket configuration, generation, and discipline blocks
"""
from typing import TYPE_CHECKING, List, Optional
from datetime import datetime, date
from enum import Enum
from sqlmodel import SQLModel, Field, Relationship, Column
from sqlalchemy import Text

if TYPE_CHECKING:
    from app.models.student import Student
    from app.models import User


class HallTicketStatus(str, Enum):
    """Hall ticket status"""
    GENERATED = "GENERATED"
    DOWNLOADED = "DOWNLOADED"
    CANCELLED = "CANCELLED"
    REISSUED = "REISSUED"


class BlockReason(str, Enum):
    """Reasons for discipline block"""
    FEE_DUES = "FEE_DUES"
    ATTENDANCE_SHORTAGE = "ATTENDANCE_SHORTAGE"
    DISCIPLINARY_ACTION = "DISCIPLINARY_ACTION"
    DOCUMENT_PENDING = "DOCUMENT_PENDING"
    OTHER = "OTHER"


class HallTicketConfig(SQLModel, table=True):
    """Configuration for hall ticket generation"""
    __tablename__ = "hall_ticket_config"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    
    # Exam identification
    exam_name: str = Field(max_length=200)  # "RNET 2024", "University End Sem 2024"
    exam_code: str = Field(unique=True, index=True, max_length=50)
    academic_year: str = Field(index=True)
    
    # Exam schedule
    exam_date: date
    exam_start_time: str  # "10:00 AM"
    exam_end_time: str  # "01:00 PM"
    reporting_time: str = Field(default="09:30 AM")
    
    # Venue details
    venue_name: str
    venue_address: str = Field(sa_column=Column(Text))
    venue_map_url: Optional[str] = None
    
    # Instructions
    instructions: str = Field(sa_column=Column(Text))
    documents_required: Optional[str] = None  # JSON array
    prohibited_items: Optional[str] = None  # JSON array
    
    # Branding
    template_url: Optional[str] = None  # Path to custom template
    logo_url: Optional[str] = None
    header_text: Optional[str] = None
    footer_text: Optional[str] = None
    
    # Settings
    include_photo: bool = Field(default=True)
    include_signature: bool = Field(default=False)
    include_qr_code: bool = Field(default=True)
    include_barcode: bool = Field(default=False)
    
    # Status
    is_active: bool = Field(default=True)
    
    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    created_by: Optional[int] = Field(default=None, foreign_key="user.id")
    
    # Relationships
    hall_tickets: List["HallTicket"] = Relationship(
        back_populates="config",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )


class HallTicket(SQLModel, table=True):
    """Individual hall ticket for a student"""
    __tablename__ = "hall_ticket"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    
    # Links
    student_id: int = Field(foreign_key="student.id", index=True)
    hall_ticket_config_id: int = Field(foreign_key="hall_ticket_config.id", index=True)
    
    # Hall ticket details
    hall_ticket_number: str = Field(unique=True, index=True)  # "HT-2024-001234"
    
    # Student details (denormalized for quick access)
    student_name: str
    admission_number: str
    program_name: str
    year: int
    semester: int
    
    # Media
    photo_url: Optional[str] = None
    signature_url: Optional[str] = None
    
    # Generated files
    pdf_url: Optional[str] = None
    qr_code_url: Optional[str] = None
    barcode_url: Optional[str] = None
    
    # Status
    status: HallTicketStatus = Field(default=HallTicketStatus.GENERATED)
    
    # Download tracking
    download_count: int = Field(default=0)
    first_downloaded_at: Optional[datetime] = None
    last_downloaded_at: Optional[datetime] = None
    
    # Generation tracking
    generated_at: datetime = Field(default_factory=datetime.utcnow)
    generated_by: Optional[int] = Field(default=None, foreign_key="user.id")
    
    # Cancellation/Reissue
    cancelled_at: Optional[datetime] = None
    cancelled_by: Optional[int] = Field(default=None, foreign_key="user.id")
    cancellation_reason: Optional[str] = Field(default=None, sa_column=Column(Text))
    
    reissued_at: Optional[datetime] = None
    reissued_by: Optional[int] = Field(default=None, foreign_key="user.id")
    reissue_reason: Optional[str] = Field(default=None, sa_column=Column(Text))
    
    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    student: "Student" = Relationship()
    config: "HallTicketConfig" = Relationship(back_populates="hall_tickets")


class DisciplineBlock(SQLModel, table=True):
    """Discipline block preventing hall ticket generation"""
    __tablename__ = "discipline_block"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    
    # Links
    student_id: int = Field(foreign_key="student.id", index=True)
    
    # Block details
    block_reason: BlockReason
    block_description: str = Field(sa_column=Column(Text))
    
    # Block period
    block_date: date = Field(default_factory=date.today)
    unblock_date: Optional[date] = None
    
    # Status
    is_active: bool = Field(default=True)
    
    # Actions
    blocked_by: int = Field(foreign_key="user.id")
    unblocked_by: Optional[int] = Field(default=None, foreign_key="user.id")
    unblocked_at: Optional[datetime] = None
    unblock_remarks: Optional[str] = Field(default=None, sa_column=Column(Text))
    
    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    student: "Student" = Relationship()


# ======================================================================
# Entrance Exam
# ======================================================================

from app.domains.admission.models import (
    EntranceTestConfig,
    EntranceExamResult
)
# Stub for backward compatibility
