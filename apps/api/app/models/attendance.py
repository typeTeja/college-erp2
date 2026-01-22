from datetime import date, time, datetime
from typing import Optional, List
from enum import Enum
import sqlalchemy as sa
from sqlmodel import Field, Relationship, SQLModel

# Enums
class AttendanceStatus(str, Enum):
    PRESENT = "PRESENT"
    ABSENT = "ABSENT"
    LATE = "LATE"
    ON_DUTY = "ON_DUTY"
    
class SessionStatus(str, Enum):
    SCHEDULED = "SCHEDULED"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"

# Models
class AttendanceSession(SQLModel, table=True):
    __tablename__ = "attendance_session"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    subject_id: int = Field(foreign_key="subject.id")
    faculty_id: int = Field(foreign_key="faculty.id")
    program_id: int = Field(foreign_key="program.id")
    program_year_id: int = Field(foreign_key="program_years.id")
    
    semester: int
    semester: int
    section: Optional[str] = Field(default=None, max_length=10) # Made optional
    practical_batch_id: Optional[int] = Field(default=None, foreign_key="practical_batch.id")
    session_date: date
    start_time: time
    end_time: time
    
    status: SessionStatus = Field(default=SessionStatus.SCHEDULED)
    topic_covered: Optional[str] = Field(default=None, sa_column=sa.Column(sa.Text))
    
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now, sa_column_kwargs={"onupdate": datetime.now})

    # Relationships
    subject: Optional["Subject"] = Relationship()
    faculty: Optional["Faculty"] = Relationship()
    # program: Optional["Program"] = Relationship()  # Add if Program model is available
    attendance_records: List["AttendanceRecord"] = Relationship(back_populates="session")


class AttendanceRecord(SQLModel, table=True):
    __tablename__ = "attendance_record"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    session_id: int = Field(foreign_key="attendance_session.id", ondelete="CASCADE")
    student_id: int = Field(foreign_key="student.id")
    
    status: AttendanceStatus
    remarks: Optional[str] = None
    
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now, sa_column_kwargs={"onupdate": datetime.now})
    
    # Relationships
    session: AttendanceSession = Relationship(back_populates="attendance_records")
    student: Optional["Student"] = Relationship()
