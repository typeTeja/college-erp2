"""
Hall Ticket Schemas - API Request/Response Models
"""
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime, date


# ============================================================================
# Hall Ticket Config Schemas
# ============================================================================

class HallTicketConfigBase(BaseModel):
    """Base schema for hall ticket config"""
    exam_name: str
    exam_code: str
    academic_year: str
    exam_date: date
    exam_start_time: str
    exam_end_time: str
    reporting_time: str = "09:30 AM"
    venue_name: str
    venue_address: str
    venue_map_url: Optional[str] = None
    instructions: str
    documents_required: Optional[List[str]] = None
    prohibited_items: Optional[List[str]] = None
    template_url: Optional[str] = None
    logo_url: Optional[str] = None
    header_text: Optional[str] = None
    footer_text: Optional[str] = None
    include_photo: bool = True
    include_signature: bool = False
    include_qr_code: bool = True
    include_barcode: bool = False


class HallTicketConfigCreate(HallTicketConfigBase):
    """Schema for creating hall ticket config"""
    pass


class HallTicketConfigUpdate(BaseModel):
    """Schema for updating hall ticket config"""
    exam_name: Optional[str] = None
    exam_date: Optional[date] = None
    venue_name: Optional[str] = None
    venue_address: Optional[str] = None
    instructions: Optional[str] = None
    is_active: Optional[bool] = None


class HallTicketConfigResponse(HallTicketConfigBase):
    """Schema for hall ticket config response"""
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# ============================================================================
# Hall Ticket Schemas
# ============================================================================

class HallTicketResponse(BaseModel):
    """Schema for hall ticket response"""
    id: int
    student_id: int
    hall_ticket_config_id: int
    hall_ticket_number: str
    student_name: str
    admission_number: str
    program_name: str
    year: int
    semester: int
    photo_url: Optional[str] = None
    signature_url: Optional[str] = None
    pdf_url: Optional[str] = None
    qr_code_url: Optional[str] = None
    barcode_url: Optional[str] = None
    status: str
    download_count: int
    first_downloaded_at: Optional[datetime] = None
    last_downloaded_at: Optional[datetime] = None
    generated_at: datetime
    created_at: datetime
    
    class Config:
        from_attributes = True


# ============================================================================
# Generation Schemas
# ============================================================================

class HallTicketGenerateRequest(BaseModel):
    """Request to generate hall ticket"""
    student_id: int
    config_id: int
    force: bool = False


class BulkHallTicketGenerateRequest(BaseModel):
    """Request for bulk hall ticket generation"""
    config_id: int
    student_ids: List[int]
    force: bool = False


class BulkGenerationResponse(BaseModel):
    """Response for bulk generation"""
    success: List[dict]
    failed: List[dict]
    total_success: int
    total_failed: int


# ============================================================================
# Eligibility Schemas
# ============================================================================

class EligibilityCheckResponse(BaseModel):
    """Response for eligibility check"""
    student_id: int
    is_eligible: bool
    issues: List[dict]


# ============================================================================
# Action Schemas
# ============================================================================

class CancelHallTicketRequest(BaseModel):
    """Request to cancel hall ticket"""
    reason: str


class ReissueHallTicketRequest(BaseModel):
    """Request to reissue hall ticket"""
    reason: str


# ============================================================================
# Discipline Block Schemas
# ============================================================================

class DisciplineBlockCreate(BaseModel):
    """Schema for creating discipline block"""
    student_id: int
    block_reason: str  # FEE_DUES, ATTENDANCE_SHORTAGE, DISCIPLINARY_ACTION, etc.
    block_description: str


class DisciplineBlockResponse(BaseModel):
    """Schema for discipline block response"""
    id: int
    student_id: int
    block_reason: str
    block_description: str
    block_date: date
    unblock_date: Optional[date] = None
    is_active: bool
    blocked_by: int
    unblocked_by: Optional[int] = None
    unblocked_at: Optional[datetime] = None
    unblock_remarks: Optional[str] = None
    created_at: datetime
    
    class Config:
        from_attributes = True


class UnblockStudentRequest(BaseModel):
    """Request to unblock student"""
    remarks: str
