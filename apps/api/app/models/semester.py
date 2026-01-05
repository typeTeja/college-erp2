from typing import TYPE_CHECKING, List, Optional
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from .program_year import LegacyProgramYear
    from .subject import Subject

class Semester(SQLModel, table=True):
    """Semester within a program year"""
    id: Optional[int] = Field(default=None, primary_key=True)
    program_year_id: int = Field(foreign_key="program_year.id", index=True)
    semester_number: int  # 1 or 2 (for each year)
    name: str  # e.g., "Semester 1", "Semester 2"
    
    # Configuration
    is_internship: bool = Field(default=False)
    is_project_semester: bool = Field(default=False)
    start_month: Optional[int] = Field(default=None)  # 1-12
    end_month: Optional[int] = Field(default=None)  # 1-12
    
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    
    # Relationships
    program_year: "LegacyProgramYear" = Relationship(back_populates="semesters")
    subjects: List["Subject"] = Relationship(back_populates="semester")
