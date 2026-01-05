"""
Regulation Pydantic Schemas
"""
from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, Field, field_validator


# ============================================================================
# Regulation Schemas
# ============================================================================

class RegulationBase(BaseModel):
    """Base regulation fields"""
    regulation_code: str = Field(..., max_length=20, description="Unique regulation code (e.g., R26)")
    regulation_name: str = Field(..., max_length=100)
    program_id: int = Field(..., gt=0)
    
    promotion_model: str = Field(default="CREDIT_BASED", max_length=50)
    year1_to_year2_min_percentage: int = Field(default=50, ge=0, le=100)
    year2_to_year3_min_year2_percentage: int = Field(default=50, ge=0, le=100)
    year3_to_graduation_min_percentage: int = Field(default=100, ge=0, le=100)
    
    min_internal_pass: int = Field(default=12, ge=0)
    min_external_pass: int = Field(default=28, ge=0)
    min_total_pass: int = Field(default=40, ge=0)
    
    is_active: bool = Field(default=True)


class RegulationCreate(RegulationBase):
    """Create regulation"""
    pass


class RegulationUpdate(BaseModel):
    """
    Update regulation
    NOTE: Cannot update if is_locked = True
    """
    regulation_name: Optional[str] = Field(None, max_length=100)
    
    year1_to_year2_min_percentage: Optional[int] = Field(None, ge=0, le=100)
    year2_to_year3_min_year2_percentage: Optional[int] = Field(None, ge=0, le=100)
    year3_to_graduation_min_percentage: Optional[int] = Field(None, ge=0, le=100)
    
    min_internal_pass: Optional[int] = Field(None, ge=0)
    min_external_pass: Optional[int] = Field(None, ge=0)
    min_total_pass: Optional[int] = Field(None, ge=0)
    
    is_active: Optional[bool] = None


class RegulationRead(RegulationBase):
    """Read regulation with metadata"""
    id: int
    is_locked: bool
    locked_at: Optional[datetime] = None
    locked_by: Optional[int] = None
    version: int
    created_at: datetime
    updated_at: datetime
    created_by: Optional[int] = None
    updated_by: Optional[int] = None
    
    class Config:
        from_attributes = True


# ============================================================================
# Regulation Subject Schemas
# ============================================================================

class RegulationSubjectBase(BaseModel):
    """Base subject fields"""
    subject_code: str = Field(..., max_length=20)
    subject_name: str = Field(..., max_length=200)
    short_name: str = Field(..., max_length=50)
    
    subject_type: str = Field(..., max_length=20, description="THEORY, PRACTICAL, INTERNSHIP, PROJECT")
    
    program_year: int = Field(..., ge=1, le=5)
    semester_no: int = Field(..., ge=1, le=10)
    
    internal_max: int = Field(..., ge=0)
    external_max: int = Field(..., ge=0)
    total_max: int = Field(..., ge=0)
    passing_percentage: int = Field(default=40, ge=0, le=100)
    
    evaluation_type: str = Field(..., max_length=30, description="EXAM, CONTINUOUS, ATTENDANCE_ONLY, CERTIFICATION")
    has_exam: bool = Field(default=True)
    has_assignments: bool = Field(default=True)
    hours_per_session: int = Field(default=1, ge=0)
    
    credits: int = Field(..., ge=0)
    is_active: bool = Field(default=True)
    is_elective: bool = Field(default=False)
    
    @field_validator('total_max')
    @classmethod
    def validate_total_marks(cls, v, info):
        """Validate total_max = internal_max + external_max"""
        internal = info.data.get('internal_max', 0)
        external = info.data.get('external_max', 0)
        if v != internal + external:
            raise ValueError(f'total_max must equal internal_max + external_max ({internal} + {external} = {internal + external})')
        return v


class RegulationSubjectCreate(RegulationSubjectBase):
    """Create subject"""
    regulation_id: int = Field(..., gt=0)


class RegulationSubjectUpdate(BaseModel):
    """Update subject (only if regulation not locked)"""
    subject_name: Optional[str] = Field(None, max_length=200)
    short_name: Optional[str] = Field(None, max_length=50)
    
    internal_max: Optional[int] = Field(None, ge=0)
    external_max: Optional[int] = Field(None, ge=0)
    total_max: Optional[int] = Field(None, ge=0)
    passing_percentage: Optional[int] = Field(None, ge=0, le=100)
    
    has_exam: Optional[bool] = None
    has_assignments: Optional[bool] = None
    hours_per_session: Optional[int] = Field(None, ge=0)
    
    credits: Optional[int] = Field(None, ge=0)
    is_active: Optional[bool] = None
    is_elective: Optional[bool] = None


class RegulationSubjectRead(RegulationSubjectBase):
    """Read subject"""
    id: int
    regulation_id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# ============================================================================
# Regulation Semester Schemas
# ============================================================================

class RegulationSemesterBase(BaseModel):
    """Base semester fields"""
    program_year: int = Field(..., ge=1, le=5)
    semester_no: int = Field(..., ge=1, le=10)
    semester_name: str = Field(..., max_length=50)
    total_credits: int = Field(default=0, ge=0)
    min_credits_to_pass: int = Field(default=0, ge=0)


class RegulationSemesterCreate(RegulationSemesterBase):
    """Create semester"""
    regulation_id: int = Field(..., gt=0)


class RegulationSemesterRead(RegulationSemesterBase):
    """Read semester"""
    id: int
    regulation_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


# ============================================================================
# Regulation Promotion Rule Schemas
# ============================================================================

class RegulationPromotionRuleBase(BaseModel):
    """Base promotion rule fields"""
    from_year: int = Field(..., ge=1, le=5)
    to_year: int = Field(..., ge=1, le=5)
    min_prev_year_percentage: int = Field(default=0, ge=0, le=100)
    min_current_year_percentage: int = Field(default=50, ge=0, le=100)
    additional_rules: Optional[str] = None


class RegulationPromotionRuleCreate(RegulationPromotionRuleBase):
    """Create promotion rule"""
    regulation_id: int = Field(..., gt=0)


class RegulationPromotionRuleRead(RegulationPromotionRuleBase):
    """Read promotion rule"""
    id: int
    regulation_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


# ============================================================================
# Composite Schemas
# ============================================================================

class RegulationWithDetails(RegulationRead):
    """Regulation with all related data"""
    subjects: List[RegulationSubjectRead] = []
    semesters: List[RegulationSemesterRead] = []
    promotion_rules: List[RegulationPromotionRuleRead] = []
    
    class Config:
        from_attributes = True
