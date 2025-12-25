from typing import TYPE_CHECKING, List, Optional
from datetime import date, time
from enum import Enum
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from .semester import Semester
    from .subject import Subject
    from .student import Student

class ExamType(str, Enum):
    MID_TERM = "MID_TERM"
    FINAL = "FINAL"
    INTERNAL = "INTERNAL"
    PRACTICAL = "PRACTICAL"

class ExamStatus(str, Enum):
    DRAFT = "DRAFT"
    PUBLISHED = "PUBLISHED"
    COMPLETED = "COMPLETED"

class Exam(SQLModel, table=True):
    """Represents an exam cycle (e.g., Fall 2024 Mid-Terms)"""
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str  # e.g., "Fall 2024 Mid-Term"
    exam_type: ExamType
    academic_year: str  # e.g., "2024-2025"
    semester_id: int = Field(foreign_key="semester.id")
    start_date: date
    end_date: date
    status: ExamStatus = Field(default=ExamStatus.DRAFT)
    description: Optional[str] = None
    
    # Relationships
    semester: "Semester" = Relationship()
    schedules: List["ExamSchedule"] = Relationship(back_populates="exam")

class ExamSchedule(SQLModel, table=True):
    """Timetable for a specific subject in an exam"""
    __tablename__ = "exam_schedule"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    exam_id: int = Field(foreign_key="exam.id")
    subject_id: int = Field(foreign_key="subject.id")
    exam_date: date
    start_time: time
    end_time: time
    max_marks: int = Field(default=100)
    passing_marks: int = Field(default=40)
    
    # Relationships
    exam: "Exam" = Relationship(back_populates="schedules")
    subject: "Subject" = Relationship()
    results: List["ExamResult"] = Relationship(back_populates="exam_schedule")

class ExamResult(SQLModel, table=True):
    """Marks obtained by a student in a specific exam schedule"""
    __tablename__ = "exam_result"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    exam_schedule_id: int = Field(foreign_key="exam_schedule.id")
    student_id: int = Field(foreign_key="student.id")
    marks_obtained: float
    grade: Optional[str] = None
    remarks: Optional[str] = None
    is_absent: bool = Field(default=False)
    
    # Relationships
    exam_schedule: "ExamSchedule" = Relationship(back_populates="results")
    student: "Student" = Relationship()
