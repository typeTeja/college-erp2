from typing import TYPE_CHECKING, Optional, List
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship
from app.shared.enums import RegulationStatus, ProgramType, SubjectType, EvaluationType, PromotionRuleType

if TYPE_CHECKING:
    from .program import Program
    from .subject import Subject
    from .batch import AcademicBatch

class Regulation(SQLModel, table=True):
    """
    Regulation (e.g. R18, R20, R22)
    Defines the rules for a set of batches.
    """
    __tablename__ = "regulations"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(unique=True, index=True) # e.g. "R22"
    program_id: int = Field(foreign_key="program.id", index=True)
    program_type: ProgramType = Field(default=ProgramType.UG)
    
    # Global Rules
    total_credits: int
    duration_years: int
    has_credit_based_detention: bool = Field(default=True)
    
    # Passing Criteria
    min_sgpa: float = Field(default=5.0)
    min_cgpa: float = Field(default=5.0)
    
    internal_pass_percentage: float = Field(default=0.0) # Usually 0 or 40%
    external_pass_percentage: float = Field(default=35.0)
    total_pass_percentage: float = Field(default=40.0)
    
    # Locking mechanism
    is_locked: bool = Field(default=False, index=True)
    locked_at: Optional[datetime] = None
    locked_by: Optional[int] = Field(default=None, foreign_key="users.id")
    
    # Optimistic locking
    version: int = Field(default=1)
    
    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    created_by: Optional[int] = Field(default=None, foreign_key="users.id")
    updated_by: Optional[int] = Field(default=None, foreign_key="users.id")
    
    # Relationships
    program: "Program" = Relationship(back_populates="regulations")
    subjects: List["RegulationSubject"] = Relationship(back_populates="regulation")
    semesters: List["RegulationSemester"] = Relationship(back_populates="regulation")
    promotion_rules: List["RegulationPromotionRule"] = Relationship(back_populates="regulation")
    batches: List["AcademicBatch"] = Relationship(back_populates="regulation")

class RegulationSubject(SQLModel, table=True):
    """Subject definition within a specific Regulation"""
    __tablename__ = "regulation_subject"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    regulation_id: int = Field(foreign_key="regulations.id")
    subject_id: int = Field(foreign_key="subject.id")
    
    semester: int = Field(ge=1, le=12)
    credits: float
    
    subject_type: SubjectType = Field(default=SubjectType.THEORY)
    evaluation_type: EvaluationType = Field(default=EvaluationType.THEORY_ONLY)
    
    is_elective: bool = Field(default=False)
    elective_group: Optional[str] = None # For grouping electives
    
    max_marks: int = Field(default=100)
    internal_max: int = Field(default=40)
    external_max: int = Field(default=60)
    
    # Relationships
    regulation: Regulation = Relationship(back_populates="subjects")
    # subject: "Subject" = Relationship()

class RegulationSemester(SQLModel, table=True):
    """Credit constraints per semester"""
    __tablename__ = "regulation_semester"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    regulation_id: int = Field(foreign_key="regulations.id")
    semester: int
    
    total_credits: float
    min_credits: float # Minimum credits required to pass semester
    
    # Relationships
    regulation: Regulation = Relationship(back_populates="semesters")

class RegulationPromotionRule(SQLModel, table=True):
    """Promotion logic (e.g. 1st Year -> 2nd Year requires 50% credits)"""
    __tablename__ = "regulation_promotion_rule"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    regulation_id: int = Field(foreign_key="regulations.id")
    
    from_year: int
    to_year: int
    
    rule_type: PromotionRuleType # CREDIT_PERCENTAGE, CREDIT_COUNT, BACKLOG_COUNT
    min_credits_required: Optional[float] = None
    min_credit_percentage_required: Optional[float] = None
    max_backlogs_allowed: Optional[int] = None
    
    # Relationships
    regulation: Regulation = Relationship(back_populates="promotion_rules")
