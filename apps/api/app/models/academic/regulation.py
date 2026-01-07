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
    from ..program import Program
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
    
    # Passing marks criteria
    min_internal_pass: int = Field(default=12, ge=0)
    min_external_pass: int = Field(default=28, ge=0)
    min_total_pass: int = Field(default=40, ge=0)
    
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
