"""
Batch Models - Academic Batch with Regulation Freezing

CRITICAL RULES:
- Batches bind to ONE regulation permanently
- Regulation data is FROZEN (copied) to batch tables on creation
- Regulation is LOCKED after first batch creation
- ProgramYear is SYSTEM-OWNED and READ-ONLY
"""
from typing import TYPE_CHECKING, List, Optional
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship, Column
from sqlalchemy import Text, UniqueConstraint

if TYPE_CHECKING:
    from ..program import Program
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
    status: str = Field(default="active", max_length=20)  # active, completed, archived
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
    
    program_year: int = Field(ge=1, le=5)
    semester_no: int = Field(ge=1, le=10)
    semester_name: str = Field(max_length=50)
    
    # Credit requirements (frozen from regulation)
    total_credits: int = Field(default=0, ge=0)
    min_credits_to_pass: int = Field(default=0, ge=0)
    
    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    batch: "AcademicBatch" = Relationship(back_populates="semesters")
    program_year: "ProgramYear" = Relationship(back_populates="semesters")
    sections: List["Section"] = Relationship(back_populates="batch_semester")


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


# Update Section model to use batch_semester_id
# This will be in a separate file, but documenting the change here
"""
CRITICAL FIX: Section must link to BatchSemester, not global Semester

class Section(SQLModel, table=True):
    batch_semester_id: int = Field(foreign_key="batch_semesters.id", index=True)
    # NOT: semester_id: int = Field(foreign_key="semester.id")
"""
