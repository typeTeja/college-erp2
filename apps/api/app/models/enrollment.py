from typing import TYPE_CHECKING, Optional
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from .student import Student
    from .subject import Subject

class Enrollment(SQLModel, table=True):
    """Student-Subject enrollment model"""
    id: Optional[int] = Field(default=None, primary_key=True)
    student_id: int = Field(foreign_key="student.id", index=True)
    subject_id: int = Field(foreign_key="subject.id", index=True)
    academic_year: str  # e.g., "2024-2025"
    grade: Optional[str] = None
    attendance_percentage: Optional[float] = None
    enrolled_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    student: "Student" = Relationship(back_populates="enrollments")
    subject: "Subject" = Relationship(back_populates="enrollments")
