from typing import TYPE_CHECKING, Optional
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import Column, Text

if TYPE_CHECKING:
    from app.domains.student.models import Student
    from .batch import BatchSemester
    from .regulation import Regulation

class PromotionEligibility(SQLModel):
    """Schema for checking promotion status (Not a table)"""
    is_eligible: bool
    remarks: list[str] = []
    failed_subjects_count: int = 0
    total_credits_earned: float = 0.0

class StudentSemesterHistory(SQLModel, table=True):
    """Snapshot of a student's status in a past semester"""
    __tablename__ = "student_semester_history"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    student_id: int = Field(foreign_key="student.id", index=True)
    batch_semester_id: int = Field(foreign_key="batch_semesters.id", index=True)
    
    status: str # COMPLETED, DETAINED, DISCONTINUED
    credits_earned: float = Field(default=0.0)
    attendance_percentage: float = Field(default=0.0)
    
    recorded_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    student: "Student" = Relationship()
    batch_semester: "BatchSemester" = Relationship()

class StudentPromotionLog(SQLModel, table=True):
    """Audit log of student promotions"""
    __tablename__ = "student_promotion_log"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    student_id: int = Field(foreign_key="student.id", index=True)
    
    from_semester: int
    to_semester: int
    
    is_promoted: bool
    remarks: Optional[str] = Field(default=None, sa_column=Column(Text))
    
    # Decision maker
    decided_by: int = Field(foreign_key="users.id")
    decided_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    student: "Student" = Relationship()

class StudentRegulationMigration(SQLModel, table=True):
    """Log when a student is moved from one regulation to another (e.g. R18 -> R22)"""
    __tablename__ = "student_regulation_migration"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    student_id: int = Field(foreign_key="student.id", index=True)
    
    from_regulation_id: int = Field(foreign_key="regulations.id")
    to_regulation_id: int = Field(foreign_key="regulations.id")
    
    reason: str = Field(sa_column=Column(Text))
    
    # Approval
    approved_by: int = Field(foreign_key="users.id")
    approved_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    student: "Student" = Relationship()
    # from_regulation: "Regulation" = Relationship()
    # to_regulation: "Regulation" = Relationship()
