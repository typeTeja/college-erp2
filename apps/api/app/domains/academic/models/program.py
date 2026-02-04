from typing import TYPE_CHECKING, List, Optional
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship
from app.shared.enums import ProgramType, ProgramStatus

if TYPE_CHECKING:
    from .batch import AcademicBatch
    from .regulation import Regulation
    from app.domains.student.models import Student
    from app.domains.finance.models.fee_management import FeeStructure

class Program(SQLModel, table=True):
    """
    Academic Program (e.g., B.Tech CSE, MBA, B.Sc Physics)
    Root entity for academic structure.
    """
    __tablename__ = "program"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    
    # Identification
    name: str = Field(unique=True, index=True, max_length=100) # e.g. "B.Tech Computer Science"
    code: str = Field(unique=True, index=True, max_length=20)   # e.g. "BTECH-CSE"
    alias: Optional[str] = Field(default=None, max_length=20)   # e.g. "CSE"
    
    # Details
    program_type: ProgramType = Field(default=ProgramType.UG)
    # department_id: Optional[int] = None # Department model missing
    
    # Duration
    duration_years: int = Field(default=4, ge=1, le=6)
    number_of_semesters: int = Field(default=8, ge=1, le=12)
    
    # Status
    status: ProgramStatus = Field(default=ProgramStatus.ACTIVE)
    is_active: bool = Field(default=True)
    
    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    batches: List["AcademicBatch"] = Relationship(back_populates="program")
    regulations: List["Regulation"] = Relationship(back_populates="program")
    students: List["Student"] = Relationship(back_populates="program")
    fee_structures: List["FeeStructure"] = Relationship(back_populates="program")
