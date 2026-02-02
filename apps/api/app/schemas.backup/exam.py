from typing import List, Optional
from datetime import date, time
from pydantic import BaseModel
from app.shared.enums import ExamStatus, ExamType


# --- Exam Schemas ---

class ExamBase(BaseModel):
    name: str
    exam_type: ExamType
    academic_year: str
    semester_id: int
    start_date: date
    end_date: date
    description: Optional[str] = None
    status: ExamStatus = ExamStatus.DRAFT

class ExamCreate(ExamBase):
    pass

class ExamUpdate(BaseModel):
    name: Optional[str] = None
    exam_type: Optional[ExamType] = None
    academic_year: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    description: Optional[str] = None
    status: Optional[ExamStatus] = None

class ExamRead(ExamBase):
    id: int

# --- Exam Schedule Schemas ---

class ExamScheduleBase(BaseModel):
    exam_id: int
    subject_id: int
    exam_date: date
    start_time: time
    end_time: time
    max_marks: int = 100
    passing_marks: int = 40

class ExamScheduleCreate(ExamScheduleBase):
    pass

class ExamScheduleUpdate(BaseModel):
    exam_date: Optional[date] = None
    start_time: Optional[time] = None
    end_time: Optional[time] = None
    max_marks: Optional[int] = None
    # passing_marks: Optional[int] = None

class ExamScheduleRead(ExamScheduleBase):
    id: int
    subject_name: Optional[str] = None # Enriched from relationship

# --- Exam Result Schemas ---

class ExamResultBase(BaseModel):
    exam_schedule_id: int
    student_id: int
    marks_obtained: float
    grade: Optional[str] = None
    remarks: Optional[str] = None
    is_absent: bool = False

class ExamResultCreate(ExamResultBase):
    pass

class BulkMarksEntry(BaseModel):
    exam_schedule_id: int
    records: List[ExamResultCreate]

class ExamResultRead(ExamResultBase):
    id: int
    student_name: Optional[str] = None # Enriched
    subject_name: Optional[str] = None # Enriched
    exam_name: Optional[str] = None # Enriched
