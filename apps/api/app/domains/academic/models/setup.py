from typing import TYPE_CHECKING, Optional, List
from datetime import datetime, date
from sqlmodel import SQLModel, Field, Relationship
from app.shared.enums import AcademicYearStatus

if TYPE_CHECKING:
    from .batch import BatchSemester
    from app.domains.hr.models import Faculty

class AcademicYear(SQLModel, table=True):
    """Academic Year Management - Calendar years"""
    __tablename__ = "academic_year"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(unique=True, index=True)  # e.g., "2024-2025"
    start_date: date
    end_date: date
    status: AcademicYearStatus = Field(default=AcademicYearStatus.UPCOMING)
    is_active: bool = Field(default=False) # Renamed or mapped from is_current? using is_current based on legacy if exists but legacy had is_active? Legacy had is_current.
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
    # batch: Optional["AcademicBatch"] = Relationship()

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
