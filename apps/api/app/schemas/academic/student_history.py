"""
Student History Pydantic Schemas
"""
from typing import Optional
from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, Field


# ============================================================================
# Student Semester History Schemas
# ============================================================================

class StudentSemesterHistoryBase(BaseModel):
    """Base semester history fields"""
    student_id: int = Field(..., gt=0)
    batch_id: int = Field(..., gt=0)
    academic_year_id: int = Field(..., gt=0)
    regulation_id: int = Field(..., gt=0)
    
    program_year: int = Field(..., ge=1, le=5)
    semester_no: int = Field(..., ge=1, le=10)
    
    total_credits: int = Field(default=0, ge=0)
    earned_credits: int = Field(default=0, ge=0)
    failed_credits: int = Field(default=0, ge=0)
    
    status: str = Field(..., max_length=20)  # PROMOTED, DETAINED, REPEAT, READMISSION


class StudentSemesterHistoryCreate(StudentSemesterHistoryBase):
    """Create semester history"""
    pass


class StudentSemesterHistoryUpdate(BaseModel):
    """
    Update semester history
    
    NOTE: Only credits and status should be updatable
    """
    total_credits: Optional[int] = Field(None, ge=0)
    earned_credits: Optional[int] = Field(None, ge=0)
    failed_credits: Optional[int] = Field(None, ge=0)
    status: Optional[str] = Field(None, max_length=20)


class StudentSemesterHistoryRead(StudentSemesterHistoryBase):
    """Read semester history"""
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# ============================================================================
# Student Promotion Log Schemas
# ============================================================================

class StudentPromotionLogBase(BaseModel):
    """Base promotion log fields"""
    student_id: int = Field(..., gt=0)
    batch_id: int = Field(..., gt=0)
    regulation_id: int = Field(..., gt=0)
    
    from_year: int = Field(..., ge=1, le=5)
    to_year: int = Field(..., ge=1, le=5)
    from_semester: int = Field(..., ge=1, le=10)
    to_semester: int = Field(..., ge=1, le=10)
    
    status: str = Field(..., max_length=20)
    reason: str
    
    year_total_credits: int = Field(default=0, ge=0)
    year_earned_credits: int = Field(default=0, ge=0)
    year_failed_credits: int = Field(default=0, ge=0)
    year_percentage: Optional[Decimal] = None


class StudentPromotionLogCreate(StudentPromotionLogBase):
    """Create promotion log"""
    decided_by: int = Field(..., gt=0)


class StudentPromotionLogRead(StudentPromotionLogBase):
    """Read promotion log"""
    id: int
    decided_by: int
    decided_at: datetime
    
    class Config:
        from_attributes = True


# ============================================================================
# Promotion Request/Response Schemas
# ============================================================================

class PromotionEligibilityResponse(BaseModel):
    """Response for promotion eligibility check"""
    eligible: bool
    message: str
    year_total_credits: int
    year_earned_credits: int
    year_failed_credits: int
    year_percentage: Decimal


class PromoteStudentRequest(BaseModel):
    """Request to promote a student"""
    student_id: int = Field(..., gt=0)
    force: bool = Field(default=False, description="Force promotion even if not eligible")


class PromoteStudentResponse(BaseModel):
    """Response after promoting a student"""
    success: bool
    message: str
    from_year: int
    to_year: int
    from_semester: int
    to_semester: int
    year_percentage: Decimal


# ============================================================================
# Student Regulation Migration Schemas
# ============================================================================

class StudentRegulationMigrationBase(BaseModel):
    """Base regulation migration fields"""
    student_id: int = Field(..., gt=0)
    from_regulation_id: int = Field(..., gt=0)
    to_regulation_id: int = Field(..., gt=0)
    reason: str


class StudentRegulationMigrationCreate(StudentRegulationMigrationBase):
    """Create regulation migration"""
    approved_by: int = Field(..., gt=0)


class StudentRegulationMigrationRead(StudentRegulationMigrationBase):
    """Read regulation migration"""
    id: int
    migration_date: datetime
    approved_by: int
    approved_at: datetime
    
    class Config:
        from_attributes = True
