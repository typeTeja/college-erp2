from typing import TYPE_CHECKING, List, Optional
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from .program_year import ProgramYear
    from .student import Student
    from .department import Department
    from .fee import FeeStructure

class Program(SQLModel, table=True):
    """Degree program model (e.g., B.Tech CS, MBA, M.Sc)"""
    id: Optional[int] = Field(default=None, primary_key=True)
    code: str = Field(index=True, unique=True)  # e.g., "BTECH-CS"
    name: str  # e.g., "Bachelor of Technology - Computer Science"
    duration_years: int = Field(default=4)
    description: Optional[str] = None
    department_id: int = Field(foreign_key="department.id")
    
    # Relationships
    department: "Department" = Relationship(back_populates="programs")
    years: List["ProgramYear"] = Relationship(back_populates="program")
    students: List["Student"] = Relationship(back_populates="program")
    fee_structures: List["FeeStructure"] = Relationship(back_populates="program")
