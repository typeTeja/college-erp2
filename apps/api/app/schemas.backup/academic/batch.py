"""
Batch Pydantic Schemas
"""
from typing import Optional, List
from datetime import datetime, date
from pydantic import BaseModel, Field, field_validator
from app.schemas.master_data import SectionRead, PracticalBatchRead


# ============================================================================
# Academic Batch Schemas
# ============================================================================

class AcademicBatchBase(BaseModel):
    """Base batch fields"""
    program_id: int = Field(..., gt=0)
    regulation_id: int = Field(..., gt=0)
    joining_year: int = Field(..., ge=2000, le=2100)
    total_students: int = Field(default=0, ge=0)


class AcademicBatchCreate(AcademicBatchBase):
    """
    Create academic batch
    
    Auto-generates:
    - batch_code (e.g., "2024-2027")
    - batch_name (e.g., "Batch 2024-2027")
    - start_year = joining_year
    - end_year = joining_year + program.duration_years
    - Program years (1st, 2nd, 3rd)
    - Semesters (2 per year)
    - Frozen subjects from regulation
    """
    pass


class AcademicBatchUpdate(BaseModel):
    """
    Update batch
    
    NOTE: Cannot update if students are admitted
    Only status and total_students can be updated
    """
    total_students: Optional[int] = Field(None, ge=0)
    status: Optional[str] = Field(None, max_length=20)
    is_active: Optional[bool] = None


class AcademicBatchRead(AcademicBatchBase):
    """Read batch"""
    id: int
    batch_code: str
    batch_name: str
    start_year: int
    end_year: int
    current_year: int
    status: str
    is_active: bool
    created_at: datetime
    updated_at: datetime
    created_by: Optional[int] = None
    
    class Config:
        from_attributes = True


# ============================================================================
# Program Year Schemas (READ-ONLY)
# ============================================================================

class ProgramYearRead(BaseModel):
    """
    Read program year
    
    NOTE: This is READ-ONLY, no Create/Update schemas
    """
    id: int
    batch_id: int
    year_no: int
    year_name: str
    created_at: datetime
    
    class Config:
        from_attributes = True


# ============================================================================
# Batch Semester Schemas
# ============================================================================

class BatchSemesterRead(BaseModel):
    """Read batch semester (frozen from regulation)"""
    id: int
    batch_id: int
    program_year_id: int
    year_no: int
    semester_no: int
    semester_name: str
    total_credits: int
    min_credits_to_pass: int
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    is_active: bool
    sections: List[SectionRead] = []
    practical_batches: List[PracticalBatchRead] = []
    created_at: datetime
    
    class Config:
        from_attributes = True


class BatchSemesterUpdate(BaseModel):
    """Update semester dates"""
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    is_active: Optional[bool] = None


# ============================================================================
# Batch Subject Schemas
# ============================================================================

class BatchSubjectRead(BaseModel):
    """Read batch subject (frozen from regulation)"""
    id: int
    batch_id: int
    subject_code: str
    subject_name: str
    short_name: str
    subject_type: str
    program_year: int
    semester_no: int
    internal_max: int
    external_max: int
    total_max: int
    passing_percentage: int
    evaluation_type: str
    has_exam: bool
    has_assignments: bool
    hours_per_session: int
    credits: int
    is_active: bool
    is_elective: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


# ============================================================================
# Composite Schemas
# ============================================================================

class AcademicBatchWithDetails(AcademicBatchRead):
    """Batch with all related data"""
    program_years: List[ProgramYearRead] = []
    semesters: List[BatchSemesterRead] = []
    subjects: List[BatchSubjectRead] = []
    
    class Config:
        from_attributes = True


class ProgramYearWithSemesters(ProgramYearRead):
    """Program year with semesters"""
    semesters: List[BatchSemesterRead] = []
    
    class Config:
        from_attributes = True
