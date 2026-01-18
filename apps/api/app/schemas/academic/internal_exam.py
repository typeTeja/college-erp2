"""
Internal Exam Schemas - API Request/Response Models
"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime, date


# ============================================================================
# Internal Exam Schemas
# ============================================================================

class InternalExamBase(BaseModel):
    """Base schema for internal exam"""
    name: str
    exam_code: str
    academic_year: str
    batch_id: int
    batch_semester_id: int
    exam_type: str  # MID_TERM, END_TERM, ASSIGNMENT, QUIZ, PRACTICAL, VIVA
    start_date: date
    end_date: date
    total_marks: int = 100
    passing_marks: int = 40
    weightage: float = 0.3
    instructions: Optional[str] = None


class InternalExamCreate(InternalExamBase):
    """Schema for creating internal exam"""
    pass


class InternalExamResponse(InternalExamBase):
    """Schema for internal exam response"""
    id: int
    is_published: bool
    published_at: Optional[datetime] = None
    published_by: Optional[int] = None
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# ============================================================================
# Internal Exam Subject Schemas
# ============================================================================

class InternalExamSubjectBase(BaseModel):
    """Base schema for exam subject"""
    batch_subject_id: int
    max_marks: int
    passing_marks: int
    exam_date: date
    exam_time: str
    duration_minutes: int = 180
    room_number: Optional[str] = None
    invigilator_id: Optional[int] = None


class InternalExamSubjectCreate(InternalExamSubjectBase):
    """Schema for creating exam subject"""
    pass


class InternalExamSubjectResponse(InternalExamSubjectBase):
    """Schema for exam subject response"""
    id: int
    internal_exam_id: int
    is_completed: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


class BulkSubjectCreate(BaseModel):
    """Schema for bulk subject creation"""
    subjects: List[InternalExamSubjectCreate]


# ============================================================================
# Marks Entry Schemas
# ============================================================================

class StudentInternalMarksBase(BaseModel):
    """Base schema for student marks"""
    student_id: int
    internal_exam_subject_id: int
    marks_obtained: Optional[float] = None
    is_absent: bool = False
    remarks: Optional[str] = None


class StudentInternalMarksCreate(StudentInternalMarksBase):
    """Schema for creating student marks"""
    pass


class StudentInternalMarksResponse(StudentInternalMarksBase):
    """Schema for student marks response"""
    id: int
    entered_by: Optional[int] = None
    entered_at: Optional[datetime] = None
    verified_by: Optional[int] = None
    verified_at: Optional[datetime] = None
    is_verified: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class BulkMarksEntry(BaseModel):
    """Schema for bulk marks entry"""
    marks: List[StudentInternalMarksCreate]


class MarksVerification(BaseModel):
    """Schema for marks verification"""
    marks_ids: List[int]


# ============================================================================
# Consolidated Results Schemas
# ============================================================================

class InternalMarksConsolidatedResponse(BaseModel):
    """Schema for consolidated marks response"""
    id: int
    student_id: int
    batch_semester_id: int
    academic_year: str
    total_max_marks: float
    total_marks_obtained: float
    percentage: float
    grade: Optional[str] = None
    gpa: Optional[float] = None
    rank: Optional[int] = None
    is_promoted: bool
    result_status: str
    calculated_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# ============================================================================
# Statistics Schemas
# ============================================================================

class ExamStatistics(BaseModel):
    """Exam statistics response"""
    exam_id: int
    exam_name: str
    total_students: int
    present_students: int
    absent_students: int
    average_marks: float
    attendance_percentage: float


class StudentResultSummary(BaseModel):
    """Student result summary"""
    student_id: int
    student_name: str
    admission_number: str
    results: List[InternalMarksConsolidatedResponse]
    overall_gpa: float
    overall_percentage: float


# ============================================================================
# Publish Results Schema
# ============================================================================

class PublishResultsRequest(BaseModel):
    """Request to publish exam results"""
    exam_id: int
    notify_students: bool = False
