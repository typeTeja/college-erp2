from typing import TYPE_CHECKING, Optional
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from app.domains.student.models import Student
    from .setup import Section, PracticalBatch

class StudentSectionAssignment(SQLModel, table=True):
    """Assigning student to a section for a semester"""
    __tablename__ = "student_section_assignment"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    student_id: int = Field(foreign_key="student.id", index=True)
    section_id: int = Field(foreign_key="section.id", index=True)
    
    assignment_type: str = Field(default="AUTO", max_length=20)  # AUTO, MANUAL, RULE_BASED
    assigned_at: datetime = Field(default_factory=datetime.utcnow)
    assigned_by: Optional[int] = Field(default=None, foreign_key="users.id")
    is_active: bool = Field(default=True)
    
    # Relationships
    student: "Student" = Relationship()
    section: "Section" = Relationship()

class StudentPracticalBatchAllocation(SQLModel, table=True):
    """Assigning student to specific practical batch (e.g. Lab Batch A1)"""
    __tablename__ = "student_practical_batch_allocation"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    student_id: int = Field(foreign_key="student.id", index=True)
    practical_batch_id: int = Field(foreign_key="practical_batch.id", index=True)
    
    assignment_type: str = Field(default="AUTO", max_length=20)  # AUTO, MANUAL
    assigned_at: datetime = Field(default_factory=datetime.utcnow)
    assigned_by: Optional[int] = Field(default=None, foreign_key="users.id")
    is_active: bool = Field(default=True)
    
    # Relationships
    student: "Student" = Relationship()
    practical_batch: "PracticalBatch" = Relationship()

# Deprecated or Alias? 'StudentLabAssignment' was not seen in full read but implied.
# Using 'StudentPracticalBatchAllocation' as primary.
