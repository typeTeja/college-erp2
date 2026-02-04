"""
Academic Domain Schemas

Pydantic schemas for the academic domain.
Note: This is a simplified version. Full schemas can be added as needed.
"""

from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime, date


# ----------------------------------------------------------------------
# Program Schemas
# ----------------------------------------------------------------------

class ProgramBase(BaseModel):
    code: str
    name: str
    alias: Optional[str] = None
    program_type: str  # UG, PG, DIPLOMA, CERTIFICATE
    department_id: Optional[int] = None
    duration_years: int
    number_of_semesters: int
    status: str = "ACTIVE"  # ACTIVE, INACTIVE, ARCHIVED

class ProgramCreate(ProgramBase):
    pass

class ProgramRead(ProgramBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


# ----------------------------------------------------------------------
# Academic Year Schemas
# ----------------------------------------------------------------------

class AcademicYearBase(BaseModel):
    year: str
    start_date: date
    end_date: date
    is_current: bool = False


class AcademicYearCreate(AcademicYearBase):
    pass


class AcademicYearRead(AcademicYearBase):
    id: int
    
    class Config:
        from_attributes = True


# ----------------------------------------------------------------------
# Batch Schemas
# ----------------------------------------------------------------------

class BatchBase(BaseModel):
    batch_code: str
    batch_name: str
    program_id: int
    regulation_id: int
    joining_year: int
    start_year: int
    end_year: int


class BatchCreate(BatchBase):
    pass


class BatchRead(BatchBase):
    id: int
    current_year: int
    total_students: int
    status: str
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


# ----------------------------------------------------------------------
# Regulation Schemas
# ----------------------------------------------------------------------

class RegulationBase(BaseModel):
    regulation_code: str
    regulation_name: str
    program_id: int
    effective_from: date


class RegulationCreate(RegulationBase):
    pass


class RegulationRead(RegulationBase):
    id: int
    is_locked: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


# ----------------------------------------------------------------------
# Section Schemas
# ----------------------------------------------------------------------

class SectionBase(BaseModel):
    name: str
    batch_id: int
    semester_no: int
    capacity: int = 60


class SectionCreate(SectionBase):
    pass


class SectionRead(SectionBase):
    id: int
    current_strength: int
    
    class Config:
        from_attributes = True


# ----------------------------------------------------------------------
# Exam Schemas
# ----------------------------------------------------------------------

from app.shared.enums import ExamType, ExamStatus, ExamResultStatus

class ExamBase(BaseModel):
    name: str
    exam_type: ExamType
    academic_year: str
    batch_semester_id: int
    start_date: date
    end_date: date
    description: Optional[str] = None

class ExamCreate(ExamBase):
    pass

class ExamRead(ExamBase):
    id: int
    status: ExamStatus
    
    class Config:
        from_attributes = True

class InternalExamBase(BaseModel):
    name: str
    exam_code: str
    academic_year: str
    batch_id: int
    batch_semester_id: int
    exam_type: ExamType = ExamType.MID_TERM
    start_date: date
    end_date: date
    total_marks: int = 100
    passing_marks: int = 40
    weightage: float = 0.3

class InternalExamCreate(InternalExamBase):
    pass

class InternalExamRead(InternalExamBase):
    id: int
    is_published: bool
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

class StudentInternalMarksBase(BaseModel):
    student_id: int
    internal_exam_subject_id: int
    marks_obtained: Optional[float] = None
    is_absent: bool = False
    remarks: Optional[str] = None

class StudentInternalMarksCreate(StudentInternalMarksBase):
    pass

class StudentInternalMarksRead(StudentInternalMarksBase):
    id: int
    is_verified: bool
    
    class Config:
        from_attributes = True


# ----------------------------------------------------------------------
# Attendance Schemas
# ----------------------------------------------------------------------

from app.shared.enums import SessionStatus, AttendanceStatus

class AttendanceSessionBase(BaseModel):
    subject_id: int
    faculty_id: int
    program_id: int
    program_year_id: int
    semester: int
    section: Optional[str] = None
    practical_batch_id: Optional[int] = None
    session_date: date
    start_time: str # Format "HH:MM"
    end_time: str # Format "HH:MM"
    status: SessionStatus = SessionStatus.SCHEDULED

class AttendanceSessionCreate(AttendanceSessionBase):
    pass

class AttendanceSessionRead(AttendanceSessionBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class AttendanceRecordBase(BaseModel):
    student_id: int
    session_id: int
    status: AttendanceStatus
    remarks: Optional[str] = None

class AttendanceRecordCreate(AttendanceRecordBase):
    pass

class AttendanceRecordRead(AttendanceRecordBase):
    id: int
    
    class Config:
        from_attributes = True

class BulkAttendanceMark(BaseModel):
    session_id: int
    attendance_data: List[AttendanceRecordCreate]

# ----------------------------------------------------------------------
# Timetable Schemas
# ----------------------------------------------------------------------

from app.shared.enums import DayOfWeek, SlotType

class TimetableSlotBase(BaseModel):
    day_of_week: DayOfWeek
    start_time: str
    end_time: str
    slot_type: SlotType = SlotType.THEORY
    batch_semester_id: int
    subject_id: Optional[int] = None
    faculty_id: Optional[int] = None
    room_id: Optional[int] = None
    section: Optional[str] = None

class TimetableSlotCreate(TimetableSlotBase):
    pass

class TimetableSlotRead(TimetableSlotBase):
    id: int
    
    class Config:
        from_attributes = True
