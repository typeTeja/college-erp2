from typing import Optional
from sqlmodel import SQLModel, Field, UniqueConstraint
from datetime import datetime

class StudentPracticalBatchAllocation(SQLModel, table=True):
    """
    Allocates a student to a specific Practical Batch for a specific Subject.
    
    RULES:
    1. A student can only be in ONE practical batch per subject per semester.
    2. Capacity limit of the Practical Batch must be checked before creating allocation.
    """
    __tablename__ = "student_practical_batch_allocation"
    __table_args__ = (
        UniqueConstraint('student_id', 'subject_id', 'batch_semester_id', name='uq_student_subject_allocation'),
    )
    
    id: Optional[int] = Field(default=None, primary_key=True)
    
    student_id: int = Field(foreign_key="student.id", index=True)
    practical_batch_id: int = Field(foreign_key="practical_batch.id", index=True)
    batch_semester_id: int = Field(foreign_key="batch_semesters.id", index=True)
    subject_id: int = Field(foreign_key="subject.id", index=True)
    
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
