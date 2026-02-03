from typing import TYPE_CHECKING, List, Optional
from datetime import datetime, date, time
from enum import Enum
from sqlmodel import SQLModel, Field, Relationship, Column
from sqlalchemy import Text, JSON
from app.shared.enums import ExamStatus, ExamType, ExamResultStatus

if TYPE_CHECKING:
    from .batch import BatchSemester, BatchSubject, AcademicBatch
    from .subject import Subject
    from app.domains.student.models import Student
    from app.domains.hr.models import Faculty

# ======================================================================
# General / Shared Exam Models
# ======================================================================

class Exam(SQLModel, table=True):
    """Represents an exam cycle (e.g., Fall 2024 Mid-Terms)"""
    __tablename__ = "exam"
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str  # e.g., "Fall 2024 Mid-Term"
    exam_type: ExamType
    academic_year: str  # e.g., "2024-2025"
    
    # Updated to link to BatchSemester
    batch_semester_id: int = Field(foreign_key="batch_semesters.id")
    
    start_date: date
    end_date: date
    status: ExamStatus = Field(default=ExamStatus.DRAFT)
    description: Optional[str] = None
    
    # Relationships
    batch_semester: "BatchSemester" = Relationship()
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

# ======================================================================
# Internal Exam
# ======================================================================

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
    published_by: Optional[int] = Field(default=None, foreign_key="users.id")
    
    # Status
    is_active: bool = Field(default=True)
    
    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    created_by: Optional[int] = Field(default=None, foreign_key="users.id")
    
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
    invigilator_id: Optional[int] = Field(default=None, foreign_key="users.id")
    
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
    entered_by: Optional[int] = Field(default=None, foreign_key="users.id")
    entered_at: Optional[datetime] = None
    
    # Verification
    verified_by: Optional[int] = Field(default=None, foreign_key="users.id")
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

# ======================================================================
# University Exam
# ======================================================================

class UniversityExam(SQLModel, table=True):
    """University exam configuration"""
    __tablename__ = "university_exam"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    
    # Exam identification
    exam_name: str = Field(max_length=200)  # "End Semester Exam - May 2024"
    exam_code: str = Field(unique=True, index=True, max_length=50)
    academic_year: str = Field(index=True)
    semester: int = Field(ge=1, le=8)  # 1-8
    
    # Registration period
    registration_start: date
    registration_end: date
    late_registration_end: Optional[date] = None
    
    # Exam period
    exam_start_date: date
    exam_end_date: date
    
    # Fees
    exam_fee: float = Field(ge=0)
    late_fee: float = Field(default=0.0, ge=0)
    
    # Eligibility criteria
    min_attendance_percentage: float = Field(default=75.0, ge=0, le=100)
    allow_detained_students: bool = Field(default=False)
    
    # Instructions
    instructions: Optional[str] = Field(default=None, sa_column=Column(Text))
    
    # Status
    is_active: bool = Field(default=True)
    is_registration_open: bool = Field(default=True)
    
    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    created_by: Optional[int] = Field(default=None, foreign_key="users.id")
    
    # Relationships
    registrations: List["UniversityExamRegistration"] = Relationship(
        back_populates="university_exam",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )
    results: List["UniversityExamResult"] = Relationship(
        back_populates="university_exam",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )

class UniversityExamRegistration(SQLModel, table=True):
    """Student registration for university exam"""
    __tablename__ = "university_exam_registration"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    
    # Links
    student_id: int = Field(foreign_key="student.id", index=True)
    university_exam_id: int = Field(foreign_key="university_exam.id", index=True)
    batch_semester_id: int = Field(foreign_key="batch_semesters.id", index=True)
    
    # Registration details
    registration_number: str = Field(unique=True, index=True)
    registration_date: date = Field(default_factory=date.today)
    is_late_registration: bool = Field(default=False)
    
    # Subjects registered (JSON array of subject IDs)
    subjects_registered: str = Field(sa_column=Column(JSON))
    # Example: [{"subject_id": 1, "subject_code": "CS101", "subject_name": "Programming"}]
    
    # Fee details
    exam_fee: float
    late_fee: float = Field(default=0.0)
    total_fee: float
    fee_paid: bool = Field(default=False)
    payment_id: Optional[str] = None
    payment_date: Optional[date] = None
    
    # Eligibility
    is_eligible: bool = Field(default=True)
    eligibility_remarks: Optional[str] = Field(default=None, sa_column=Column(Text))
    attendance_percentage: Optional[float] = None
    
    # Hall ticket
    hall_ticket_number: Optional[str] = None
    hall_ticket_generated: bool = Field(default=False)
    hall_ticket_url: Optional[str] = None
    
    # Status
    is_cancelled: bool = Field(default=False)
    cancelled_at: Optional[datetime] = None
    cancellation_reason: Optional[str] = Field(default=None, sa_column=Column(Text))
    
    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    student: "Student" = Relationship()
    university_exam: "UniversityExam" = Relationship(back_populates="registrations")
    batch_semester: "BatchSemester" = Relationship()

class UniversityExamResult(SQLModel, table=True):
    """University exam results for individual subjects"""
    __tablename__ = "university_exam_result"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    
    # Links
    student_id: int = Field(foreign_key="student.id", index=True)
    university_exam_id: int = Field(foreign_key="university_exam.id", index=True)
    batch_subject_id: int = Field(foreign_key="batch_subjects.id", index=True)
    
    # Marks
    theory_max_marks: Optional[float] = None
    theory_marks: Optional[float] = None
    practical_max_marks: Optional[float] = None
    practical_marks: Optional[float] = None
    internal_max_marks: Optional[float] = None
    internal_marks: Optional[float] = None
    
    # Total
    total_max_marks: float
    total_marks: float
    percentage: float = Field(ge=0, le=100)
    
    # Grading
    grade: Optional[str] = None  # O, A+, A, B+, B, C, D, F
    grade_points: Optional[float] = None  # 10, 9, 8, 7, 6, 5, 4, 0
    credits: int = Field(ge=0)
    credits_earned: int = Field(ge=0)
    
    # Result
    result_status: ExamResultStatus = Field(default=ExamResultStatus.PASS)
    
    # Remarks
    remarks: Optional[str] = Field(default=None, sa_column=Column(Text))
    
    # Import tracking
    imported_at: Optional[datetime] = None
    imported_by: Optional[int] = Field(default=None, foreign_key="users.id")
    
    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    student: "Student" = Relationship()
    university_exam: "UniversityExam" = Relationship(back_populates="results")
    batch_subject: "BatchSubject" = Relationship()

class SemesterResult(SQLModel, table=True):
    """Consolidated semester results with SGPA/CGPA"""
    __tablename__ = "semester_result"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    
    # Links
    student_id: int = Field(foreign_key="student.id", index=True)
    batch_semester_id: int = Field(foreign_key="batch_semesters.id", index=True)
    academic_year: str = Field(index=True)
    semester: int = Field(ge=1, le=8)
    
    # Credits
    total_credits: int = Field(ge=0)
    credits_earned: int = Field(ge=0)
    credits_failed: int = Field(default=0, ge=0)
    
    # GPA
    sgpa: Optional[float] = Field(default=None, ge=0, le=10)  # Semester GPA
    cgpa: Optional[float] = Field(default=None, ge=0, le=10)  # Cumulative GPA
    
    # Performance
    total_marks: float
    marks_obtained: float
    percentage: float = Field(ge=0, le=100)
    
    # Rank
    rank: Optional[int] = None
    
    # Result
    result_status: ExamResultStatus = Field(default=ExamResultStatus.PASS)
    is_promoted: bool = Field(default=False)
    
    # Backlog subjects (JSON array)
    backlog_subjects: Optional[str] = Field(default=None, sa_column=Column(JSON))
    # Example: [{"subject_id": 1, "subject_code": "CS101", "attempt": 2}]
    
    # Remarks
    remarks: Optional[str] = Field(default=None, sa_column=Column(Text))
    
    # Calculation
    calculated_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    student: "Student" = Relationship()
    batch_semester: "BatchSemester" = Relationship()
