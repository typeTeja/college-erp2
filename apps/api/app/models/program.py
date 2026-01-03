from enum import Enum as PyEnum
from typing import TYPE_CHECKING, List, Optional
from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import Column, Text
from datetime import datetime

if TYPE_CHECKING:
    from .program_year import ProgramYear
    from .student import Student
    from .department import Department
    from .fee import FeeStructure

class ProgramType(str, PyEnum):
    UG = "UG"
    PG = "PG"
    DIPLOMA = "DIPLOMA"
    CERTIFICATE = "CERTIFICATE"
    PHD = "PHD"

class ProgramStatus(str, PyEnum):
    DRAFT = "DRAFT"
    ACTIVE = "ACTIVE"
    ARCHIVED = "ARCHIVED"

class Program(SQLModel, table=True):
    """Degree program model (e.g., B.Tech CS, MBA, M.Sc)"""
    id: Optional[int] = Field(default=None, primary_key=True)
    code: str = Field(index=True, unique=True)  # e.g., "BHM"
    short_name: Optional[str] = Field(default=None)  # e.g., "BHM" - Short display name
    name: str  # e.g., "Bachelor of Hotel Management"
    program_type: ProgramType = Field(default=ProgramType.UG)
    status: ProgramStatus = Field(default=ProgramStatus.DRAFT)
    duration_years: int = Field(default=4)
    description: Optional[str] = None
    
    # Academic Structure
    semester_system: bool = Field(default=True)  # True = Semester, False = Year system
    
    # Admission Settings
    rnet_required: bool = Field(default=True)  # Entrance test required
    allow_installments: bool = Field(default=True)  # Allow fee installments
    
    # New Fields
    eligibility_criteria: Optional[str] = Field(default=None, sa_column=Column(Text))
    program_outcomes: Optional[str] = Field(default=None, sa_column=Column(Text))
    total_credits: int = Field(default=0)
    is_active: bool = Field(default=True)
    
    department_id: int = Field(foreign_key="department.id")
    
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow, sa_column_kwargs={"onupdate": datetime.utcnow})
    
    # Relationships
    department: "Department" = Relationship(back_populates="programs")
    years: List["ProgramYear"] = Relationship(back_populates="program", sa_relationship_kwargs={"cascade": "all, delete-orphan"})
    students: List["Student"] = Relationship(back_populates="program")
    fee_structures: List["FeeStructure"] = Relationship(back_populates="program")

    @property
    def department_name(self) -> str:
        return self.department.name if self.department else "Unknown Department"
