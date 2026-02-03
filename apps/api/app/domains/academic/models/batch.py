from typing import TYPE_CHECKING, Optional, List
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship
from app.shared.enums import BatchStatus, SemesterStatus

if TYPE_CHECKING:
    from .program import Program
    from .regulation import Regulation
    from .setup import AcademicYear, Section, PracticalBatch
    from .subject import Subject
    from .attendance import AttendanceSession
    # from .exam import InternalExam, UniversityExam

class ProgramYear(SQLModel, table=True):
    """Academic Year in context (e.g. 1st Year, 2nd Year)"""
    __tablename__ = "program_years"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str # "First Year"
    year_number: int # 1
    
    # Relationships
    students: List["Student"] = Relationship(back_populates="program_year")

class AcademicBatch(SQLModel, table=True):
    """Cohort of students (e.g. 2024-2028 CSE Batch)"""
    __tablename__ = "academic_batches"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(unique=True, index=True) # "2024-2028 CSE"
    admission_year_id: int = Field(foreign_key="academic_year.id")
    
    # Links
    program_id: int = Field(foreign_key="program.id", index=True)
    regulation_id: int = Field(foreign_key="regulations.id", index=True)
    
    current_year: int = Field(default=1)
    current_semester: int = Field(default=1)
    
    status: BatchStatus = Field(default=BatchStatus.ACTIVE)
    is_active: bool = Field(default=True)
    
    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    created_by: Optional[int] = Field(default=None, foreign_key="users.id")
    
    # Relationships
    program: "Program" = Relationship(back_populates="batches")
    regulation: "Regulation" = Relationship(back_populates="batches")
    semesters: List["BatchSemester"] = Relationship(back_populates="batch")
    students: List["Student"] = Relationship(back_populates="batch")
    
    # internal_exams: List["InternalExam"] = Relationship(back_populates="batch")

class BatchSemester(SQLModel, table=True):
    """Specific semester execution for a batch (e.g., CSE 2024-28 Sem 1)"""
    __tablename__ = "batch_semesters"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    batch_id: int = Field(foreign_key="academic_batches.id", index=True)
    semester_number: int
    academic_year_id: int = Field(foreign_key="academic_year.id") # Calendar year of this sem
    
    start_date: datetime
    end_date: datetime
    
    status: SemesterStatus = Field(default=SemesterStatus.UPCOMING)
    is_current: bool = Field(default=False)
    
    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    batch: AcademicBatch = Relationship(back_populates="semesters")
    subjects: List["BatchSubject"] = Relationship(back_populates="batch_semester")
    sections: List["Section"] = Relationship(back_populates="batch_semester")
    practical_batches: List["PracticalBatch"] = Relationship(back_populates="batch_semester")
    
    # internal_exams: List["InternalExam"] = Relationship(back_populates="batch_semester")
    # university_exam_registrations: List["UniversityExamRegistration"] = Relationship(back_populates="batch_semester")

class BatchSubject(SQLModel, table=True):
    """Subject offered to a batch in a semester (Instance of RegulationSubject)"""
    __tablename__ = "batch_subjects"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    batch_semester_id: int = Field(foreign_key="batch_semesters.id", index=True)
    subject_id: int = Field(foreign_key="subject.id", index=True) # Global Subject
    regulation_subject_id: int = Field(foreign_key="regulation_subject.id") # Points to specific rules
    
    # Faculty Assignment (Course Coordinator)
    faculty_id: Optional[int] = Field(default=None, foreign_key="faculty.id")
    
    is_active: bool = Field(default=True)
    
    # Relationships
    batch_semester: BatchSemester = Relationship(back_populates="subjects")
    # subject: "Subject" = Relationship()
    # regulation_subject: "RegulationSubject" = Relationship()
    # internal_exam_subjects: List["InternalExamSubject"] = Relationship(back_populates="batch_subject")
