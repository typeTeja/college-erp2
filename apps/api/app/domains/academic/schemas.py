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
    short_name: Optional[str] = None
    program_type: str  # UG, PG, DIPLOMA, CERTIFICATE
    department_id: int
    duration_years: int
    total_semesters: int
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

class ExamBase(BaseModel):
    name: str
    exam_type: str
    batch_id: int
    semester_no: int
    start_date: date
    end_date: date


class ExamCreate(ExamBase):
    pass


class ExamRead(ExamBase):
    id: int
    status: str
    created_at: datetime
    
    class Config:
        from_attributes = True


# ----------------------------------------------------------------------
# Attendance Schemas
# ----------------------------------------------------------------------

class AttendanceRecordBase(BaseModel):
    student_id: int
    session_id: int
    status: str  # PRESENT, ABSENT, LATE, EXCUSED


class AttendanceRecordCreate(AttendanceRecordBase):
    pass


class AttendanceRecordRead(AttendanceRecordBase):
    id: int
    marked_at: datetime
    
    class Config:
        from_attributes = True
