from datetime import date, time, datetime
from typing import Optional, List
from pydantic import BaseModel
from .student import StudentResponse as StudentRead  # Aliased to match usage
from .subject import SubjectRead
from .faculty import FacultyRead
from app.domains.academic.models import AttendanceStatus, SessionStatus

# Shared properties
class AttendanceSessionBase(BaseModel):
    subject_id: int
    faculty_id: int
    program_id: int
    program_year_id: int
    semester: int
    section: str
    session_date: date
    start_time: time
    end_time: time
    topic_covered: Optional[str] = None
    status: SessionStatus = SessionStatus.SCHEDULED

class AttendanceSessionCreate(AttendanceSessionBase):
    pass

class AttendanceSessionRead(AttendanceSessionBase):
    id: int
    created_at: datetime
    updated_at: datetime
    subject: Optional[SubjectRead] = None
    faculty: Optional[FacultyRead] = None

class AttendanceSessionUpdate(BaseModel):
    topic_covered: Optional[str] = None
    status: Optional[SessionStatus] = None

# Attendance Record Schemas
class AttendanceRecordBase(BaseModel):
    student_id: int
    status: AttendanceStatus
    remarks: Optional[str] = None

class AttendanceRecordCreate(AttendanceRecordBase):
    pass

class AttendanceRecordRead(AttendanceRecordBase):
    id: int
    session_id: int
    student: Optional[StudentRead] = None

# Bulk Operations
class BulkAttendanceCreate(BaseModel):
    session_id: int
    records: List[AttendanceRecordCreate]

class AttendanceStats(BaseModel):
    total_classes: int
    present: int
    absent: int
    late: int
    on_duty: int
    attendance_percentage: float
