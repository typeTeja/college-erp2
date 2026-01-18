"""
Entrance Exam Schemas - API Request/Response Models
"""
from pydantic import BaseModel
from typing import Optional, List, Dict
from datetime import datetime, date


# ============================================================================
# Entrance Test Config Schemas
# ============================================================================

class EntranceTestConfigBase(BaseModel):
    """Base schema for entrance test configuration"""
    test_name: str
    test_code: str
    academic_year: str
    program_ids: Optional[List[int]] = None
    test_date: date
    test_time: str
    test_duration_minutes: int = 120
    reporting_time: str = "09:30 AM"
    venue_name: str
    venue_address: str
    venue_instructions: Optional[str] = None
    guidelines: Optional[str] = None
    documents_required: Optional[List[str]] = None
    total_marks: float = 100.0
    subjects: Optional[List[Dict[str, any]]] = None


class EntranceTestConfigCreate(EntranceTestConfigBase):
    """Schema for creating entrance test config"""
    pass


class EntranceTestConfigUpdate(BaseModel):
    """Schema for updating entrance test config"""
    test_name: Optional[str] = None
    test_date: Optional[date] = None
    test_time: Optional[str] = None
    venue_name: Optional[str] = None
    venue_address: Optional[str] = None
    venue_instructions: Optional[str] = None
    guidelines: Optional[str] = None
    is_active: Optional[bool] = None
    registration_open: Optional[bool] = None
    registration_deadline: Optional[date] = None


class EntranceTestConfigResponse(EntranceTestConfigBase):
    """Schema for entrance test config response"""
    id: int
    is_active: bool
    registration_open: bool
    registration_deadline: Optional[date] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# ============================================================================
# Scholarship Slab Schemas
# ============================================================================

class ScholarshipSlabBase(BaseModel):
    """Base schema for scholarship slab"""
    slab_name: str
    slab_code: str
    min_points: float
    max_points: float
    scholarship_percentage: float
    description: Optional[str] = None
    program_ids: Optional[List[int]] = None
    academic_year: str


class ScholarshipSlabCreate(ScholarshipSlabBase):
    """Schema for creating scholarship slab"""
    pass


class ScholarshipSlabUpdate(BaseModel):
    """Schema for updating scholarship slab"""
    slab_name: Optional[str] = None
    min_points: Optional[float] = None
    max_points: Optional[float] = None
    scholarship_percentage: Optional[float] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None


class ScholarshipSlabResponse(ScholarshipSlabBase):
    """Schema for scholarship slab response"""
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# ============================================================================
# Entrance Exam Result Schemas
# ============================================================================

class EntranceExamResultBase(BaseModel):
    """Base schema for entrance exam result"""
    admission_id: int
    test_config_id: int
    hall_ticket_number: str
    student_name: str
    program_code: str
    total_max_marks: float
    total_secured_marks: float
    entrance_percentage: float
    previous_percentage: float


class EntranceExamResultCreate(EntranceExamResultBase):
    """Schema for creating entrance exam result"""
    subject_marks: Optional[List[Dict[str, any]]] = None
    entrance_weightage: float = 0.5
    previous_weightage: float = 0.5
    omr_sheet_number: Optional[str] = None
    omr_sheet_url: Optional[str] = None


class EntranceExamResultUpdate(BaseModel):
    """Schema for updating entrance exam result"""
    total_secured_marks: Optional[float] = None
    entrance_percentage: Optional[float] = None
    subject_marks: Optional[List[Dict[str, any]]] = None
    scholarship_slab_id: Optional[int] = None
    result_status: Optional[str] = None
    remarks: Optional[str] = None


class EntranceExamResultResponse(EntranceExamResultBase):
    """Schema for entrance exam result response"""
    id: int
    scholarship_slab_id: Optional[int] = None
    subject_marks: Optional[List[Dict[str, any]]] = None
    entrance_points: float
    previous_points: float
    total_points: float
    average_points: float
    entrance_weightage: float
    previous_weightage: float
    scholarship_amount: Optional[float] = None
    scholarship_percentage: Optional[float] = None
    result_status: str
    remarks: Optional[str] = None
    omr_sheet_number: Optional[str] = None
    omr_sheet_url: Optional[str] = None
    entered_by: Optional[int] = None
    entered_at: Optional[datetime] = None
    verified_by: Optional[int] = None
    verified_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# ============================================================================
# Bulk Operations
# ============================================================================

class BulkResultEntry(BaseModel):
    """Schema for bulk result entry"""
    hall_ticket_number: str
    total_secured_marks: float
    subject_marks: Optional[List[Dict[str, any]]] = None


class BulkResultUpload(BaseModel):
    """Schema for bulk result upload"""
    test_config_id: int
    results: List[BulkResultEntry]


# ============================================================================
# Scholarship Calculation
# ============================================================================

class ScholarshipCalculationRequest(BaseModel):
    """Request to calculate scholarship for a result"""
    result_id: int
    force_recalculate: bool = False


class ScholarshipCalculationResponse(BaseModel):
    """Response with scholarship calculation details"""
    result_id: int
    entrance_points: float
    previous_points: float
    total_points: float
    average_points: float
    scholarship_slab_id: Optional[int] = None
    scholarship_slab_name: Optional[str] = None
    scholarship_percentage: float
    scholarship_amount: float
    base_fee: float
    final_fee: float
