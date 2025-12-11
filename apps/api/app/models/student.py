from typing import TYPE_CHECKING, List, Optional
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from .enrollment import Enrollment
    from .program import Program

class Student(SQLModel, table=True):
    """Student information model"""
    id: Optional[int] = Field(default=None, primary_key=True)
    admission_number: str = Field(index=True, unique=True)
    name: str
    dob: Optional[str] = None
    phone: Optional[str] = Field(default=None, index=True)
    email: Optional[str] = Field(default=None, index=True)
    user_id: Optional[int] = Field(default=None, foreign_key="user.id", index=True)
    program_id: int = Field(foreign_key="program.id", index=True)
    current_year: int = Field(default=1)  # Current year in program (1, 2, 3, 4)
    
    # Relationships
    program: "Program" = Relationship(back_populates="students")
    enrollments: List["Enrollment"] = Relationship(back_populates="student")
