from typing import TYPE_CHECKING, List, Optional
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from .semester import Semester
    from .faculty import Faculty
    from .enrollment import Enrollment

class Subject(SQLModel, table=True):
    """Individual subject/course taught in a semester"""
    id: Optional[int] = Field(default=None, primary_key=True)
    code: str = Field(index=True, unique=True)  # e.g., "CS101"
    name: str  # e.g., "Data Structures"
    credits: int = Field(default=3)
    description: Optional[str] = None
    semester_id: int = Field(foreign_key="semester.id", index=True)
    faculty_id: Optional[int] = Field(default=None, foreign_key="faculty.id")
    
    # Relationships
    semester: "Semester" = Relationship(back_populates="subjects")
    faculty: Optional["Faculty"] = Relationship(back_populates="subjects")
    enrollments: List["Enrollment"] = Relationship(back_populates="subject")
