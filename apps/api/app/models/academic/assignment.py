"""
Student Assignment Models
Tracks student assignments to sections and lab groups
"""
from typing import TYPE_CHECKING, Optional
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from app.models.student import Student
    from app.models.master_data import Section, PracticalBatch
    from app.models.academic.batch import AcademicBatch
    from app.models.user import User


class StudentSectionAssignment(SQLModel, table=True):
    """
    Assigns students to sections within a batch/semester
    
    Business Rules:
    - One student can only be in one section per semester
    - Cannot exceed section capacity
    - Assignment can be AUTO, MANUAL, or RULE_BASED
    """
    __tablename__ = "student_section_assignment"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    student_id: int = Field(foreign_key="student.id", index=True)
    section_id: int = Field(foreign_key="section.id", index=True)
    batch_id: int = Field(foreign_key="academic_batches.id", index=True)
    semester_no: int = Field(ge=1, le=10)
    
    assignment_type: str = Field(default="AUTO", max_length=20)  # AUTO, MANUAL, RULE_BASED
    assigned_at: datetime = Field(default_factory=datetime.utcnow)
    assigned_by: Optional[int] = Field(default=None, foreign_key="user.id")
    is_active: bool = Field(default=True)
    
    # Relationships
    student: "Student" = Relationship()
    section: "Section" = Relationship()
    batch: "AcademicBatch" = Relationship()
    assigner: Optional["User"] = Relationship()


class StudentLabAssignment(SQLModel, table=True):
    """
    Assigns students to lab groups within a section
    
    Business Rules:
    - One student can only be in one lab group per practical batch
    - Cannot exceed lab capacity
    - Must be assigned to section first
    """
    __tablename__ = "student_lab_assignment"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    student_id: int = Field(foreign_key="student.id", index=True)
    practical_batch_id: int = Field(foreign_key="practical_batch.id", index=True)
    section_id: int = Field(foreign_key="section.id", index=True)
    
    assignment_type: str = Field(default="AUTO", max_length=20)  # AUTO, MANUAL
    assigned_at: datetime = Field(default_factory=datetime.utcnow)
    assigned_by: Optional[int] = Field(default=None, foreign_key="user.id")
    is_active: bool = Field(default=True)
    
    # Relationships
    student: "Student" = Relationship()
    practical_batch: "PracticalBatch" = Relationship()
    section: "Section" = Relationship()
    assigner: Optional["User"] = Relationship()
