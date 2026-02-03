from typing import TYPE_CHECKING, Optional, List
from datetime import datetime, date, time
from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import Column, Text
from app.shared.enums import SessionStatus, AttendanceStatus

if TYPE_CHECKING:
    from .subject import Subject
    from app.domains.hr.models import Faculty
    from app.domains.student.models import Student

class AttendanceSession(SQLModel, table=True):
    __tablename__ = "attendance_session"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    subject_id: int = Field(foreign_key="subject.id")
    faculty_id: int = Field(foreign_key="faculty.id")
    program_id: int = Field(foreign_key="program.id")
    program_year_id: int = Field(foreign_key="program_years.id")
    
    semester: int
    section: Optional[str] = Field(default=None, max_length=10) # Made optional
    practical_batch_id: Optional[int] = Field(default=None, foreign_key="practical_batch.id")
    session_date: date
    start_time: time
    end_time: time
    
    status: SessionStatus = Field(default=SessionStatus.SCHEDULED)
    topic_covered: Optional[str] = Field(default=None, sa_column=Column(Text))
    
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    subject: Optional["Subject"] = Relationship()
    faculty: Optional["Faculty"] = Relationship()
    # program: Optional["Program"] = Relationship()  # Add if Program model is available
    attendance_records: List["AttendanceRecord"] = Relationship(back_populates="session")


class AttendanceRecord(SQLModel, table=True):
    __tablename__ = "attendance_record"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    session_id: int = Field(foreign_key="attendance_session.id") # ondelete cascade implied by logic but sqlmodel needs strict definition if needed
    student_id: int = Field(foreign_key="student.id")
    
    status: AttendanceStatus
    remarks: Optional[str] = None
    
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    session: AttendanceSession = Relationship(back_populates="attendance_records")
    student: Optional["Student"] = Relationship()
