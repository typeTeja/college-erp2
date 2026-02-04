from typing import TYPE_CHECKING, Optional, List
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship
from app.shared.enums import SubjectType, EvaluationType

if TYPE_CHECKING:
    from .batch import BatchSemester
    from app.domains.hr.models import Faculty
    from app.domains.student.models import Enrollment

class Subject(SQLModel, table=True):
    """
    Academic Subject (Global Definition)
    e.g. "Engineering Physics", "Data Structures"
    """
    __tablename__ = "subject"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    code: str = Field(unique=True, index=True)
    description: Optional[str] = None
    
    # Relationships
    faculty_id: Optional[int] = Field(default=None, foreign_key="faculty.id")
    faculty: Optional["Faculty"] = Relationship(back_populates="subjects")
    
    enrollments: List["Enrollment"] = Relationship(back_populates="subject")
    
    # Metadata
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class SubjectConfig(SQLModel, table=True):
    """Extended Subject Configuration with exam settings"""
    __tablename__ = "subject_config"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    subject_id: int = Field(foreign_key="subject.id", unique=True, index=True)
    
    # Evaluation Config
    has_theory: bool = Field(default=True)
    has_practical: bool = Field(default=False)
    
    theory_credits: float = Field(default=3.0)
    practical_credits: float = Field(default=0.0)
    
    # Marks Distribution
    internal_marks: int = Field(default=40)
    external_marks: int = Field(default=60)
    
    created_at: datetime = Field(default_factory=datetime.utcnow)
