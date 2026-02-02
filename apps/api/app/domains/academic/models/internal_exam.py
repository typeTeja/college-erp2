"""
Internal Exam Models - Internal Assessment Management

Manages internal exams, marks entry, and grade calculation
"""
from typing import TYPE_CHECKING, List, Optional
from datetime import datetime, date, time
from enum import Enum
from sqlmodel import SQLModel, Field, Relationship, Column
from sqlalchemy import Text
from app.shared.enums import ExamType


if TYPE_CHECKING:
    from app.models.student import Student
    from .batch import AcademicBatch, BatchSemester, BatchSubject
    from app.models.user import User


class ExamType(str, Enum):
    """Types of internal exams"""
    MID_TERM = "MID_TERM"
    END_TERM = "END_TERM"
    ASSIGNMENT = "ASSIGNMENT"
    QUIZ = "QUIZ"
    PRACTICAL = "PRACTICAL"
    VIVA = "VIVA"


class ResultStatus(str, Enum):
    """Result status"""
    PASS = "PASS"
    FAIL = "FAIL"
    ABSENT = "ABSENT"
    DETAINED = "DETAINED"


class InternalExam(SQLModel, table=True):
    """Internal exam configuration"""
    __tablename__ = "internal_exam"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    
    # Exam identification
    name: str = Field(max_length=200)  # "Mid Term 1 - 2024"
    exam_code: str = Field(unique=True, index=True, max_length=50)  # "MT1-2024-CSE"
    academic_year: str = Field(index=True)  # "2024-2025"
    
    # Links
    batch_id: int = Field(foreign_key="academic_batches.id", index=True)
    batch_semester_id: int = Field(foreign_key="batch_semesters.id", index=True)
    
    # Exam details
    exam_type: ExamType = Field(default=ExamType.MID_TERM)
    start_date: date
    end_date: date
    
    # Marks configuration
    total_marks: int = Field(default=100, ge=0)
    passing_marks: int = Field(default=40, ge=0)
    weightage: float = Field(default=0.3)  # 30% weightage for final grade
    
    # Instructions
    instructions: Optional[str] = Field(default=None, sa_column=Column(Text))
    
    # Publishing
    is_published: bool = Field(default=False)
    published_at: Optional[datetime] = None
    published_by: Optional[int] = Field(default=None, foreign_key="user.id")
    
    # Status
    is_active: bool = Field(default=True)
    
    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    created_by: Optional[int] = Field(default=None, foreign_key="user.id")
    
    # Relationships
    batch: "AcademicBatch" = Relationship()
    batch_semester: "BatchSemester" = Relationship()
    subjects: List["InternalExamSubject"] = Relationship(
        back_populates="internal_exam",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )


class InternalExamSubject(SQLModel, table=True):
    """Subject configuration for an internal exam"""
    __tablename__ = "internal_exam_subject"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    
    # Links
    internal_exam_id: int = Field(foreign_key="internal_exam.id", index=True)
    batch_subject_id: int = Field(foreign_key="batch_subjects.id", index=True)
    
    # Marks configuration
    max_marks: int = Field(ge=0)
    passing_marks: int = Field(ge=0)
    
    # Exam schedule
    exam_date: date
    exam_time: str  # "10:00 AM"
    duration_minutes: int = Field(default=180)  # 3 hours
    
    # Venue
    room_number: Optional[str] = None
    invigilator_id: Optional[int] = Field(default=None, foreign_key="user.id")
    
    # Status
    is_completed: bool = Field(default=False)
    
    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    internal_exam: "InternalExam" = Relationship(back_populates="subjects")
    batch_subject: "BatchSubject" = Relationship()
    student_marks: List["StudentInternalMarks"] = Relationship(
        back_populates="exam_subject",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )


class StudentInternalMarks(SQLModel, table=True):
    """Individual student marks for an internal exam subject"""
    __tablename__ = "student_internal_marks"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    
    # Links
    student_id: int = Field(foreign_key="student.id", index=True)
    internal_exam_subject_id: int = Field(foreign_key="internal_exam_subject.id", index=True)
    
    # Marks
    marks_obtained: Optional[float] = Field(default=None, ge=0)
    is_absent: bool = Field(default=False)
    
    # Additional details
    remarks: Optional[str] = Field(default=None, sa_column=Column(Text))
    
    # Entry tracking
    entered_by: Optional[int] = Field(default=None, foreign_key="user.id")
    entered_at: Optional[datetime] = None
    
    # Verification
    verified_by: Optional[int] = Field(default=None, foreign_key="user.id")
    verified_at: Optional[datetime] = None
    is_verified: bool = Field(default=False)
    
    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    student: "Student" = Relationship()
    exam_subject: "InternalExamSubject" = Relationship(back_populates="student_marks")


class InternalMarksConsolidated(SQLModel, table=True):
    """Consolidated internal marks for a student in a semester"""
    __tablename__ = "internal_marks_consolidated"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    
    # Links
    student_id: int = Field(foreign_key="student.id", index=True)
    batch_semester_id: int = Field(foreign_key="batch_semesters.id", index=True)
    academic_year: str = Field(index=True)
    
    # Marks summary
    total_max_marks: float = Field(ge=0)
    total_marks_obtained: float = Field(ge=0)
    percentage: float = Field(ge=0, le=100)
    
    # Grading
    grade: Optional[str] = None  # A+, A, B+, B, C, D, F
    gpa: Optional[float] = Field(default=None, ge=0, le=10)
    
    # Performance
    rank: Optional[int] = None
    is_promoted: bool = Field(default=False)
    
    # Result status
    result_status: ResultStatus = Field(default=ResultStatus.PASS)
    
    # Timestamps
    calculated_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    student: "Student" = Relationship()
    batch_semester: "BatchSemester" = Relationship()
