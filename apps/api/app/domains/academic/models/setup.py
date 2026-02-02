from typing import TYPE_CHECKING, List, Optional
from datetime import datetime, date
from decimal import Decimal
from enum import Enum as PyEnum
from sqlmodel import SQLModel, Field, Relationship, Column
from sqlalchemy import DECIMAL
from app.shared.enums import AcademicYearStatus, ExamType, SubjectType


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
    # practical_batches relationship removed as PracticalBatch is now a sibling

class PracticalBatch(SQLModel, table=True):
    """Practical Batch within a semester - independent of sections"""
    __tablename__ = "practical_batch"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str  # e.g., "Batch A1", "Batch B1"
    code: str = Field(index=True)
    
    # Linked to BatchSemester directly (Sibling to Section)
    batch_semester_id: int = Field(foreign_key="batch_semesters.id", index=True)
    
    # Removed: section_id: int = Field(foreign_key="section.id", index=True)
    
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
