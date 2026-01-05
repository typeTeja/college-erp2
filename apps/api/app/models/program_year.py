from typing import TYPE_CHECKING, List, Optional
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from .program import Program
    from .semester import Semester

class LegacyProgramYear(SQLModel, table=True):
    """
    LEGACY: Year within a program (Year 1, Year 2, etc.)
    
    NOTE: This is the OLD program_year model.
    The NEW academic foundation uses ProgramYear in app.models.academic.batch
    """
    __tablename__ = "program_year"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    program_id: int = Field(foreign_key="program.id", index=True)
    year_number: int  # 1, 2, 3, 4
    name: str  # e.g., "First Year", "Second Year"
    is_active: bool = Field(default=True)
    
    # Relationships
    program: "Program" = Relationship(back_populates="years")
    semesters: List["Semester"] = Relationship(back_populates="program_year", sa_relationship_kwargs={"cascade": "all, delete-orphan"})
