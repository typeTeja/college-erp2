"""
Schemas for Settings Master Data Module
"""
from typing import List, Optional, Any
from datetime import datetime, date
from decimal import Decimal
from pydantic import BaseModel, Field

# ============================================================================
# Academic Year Schemas
# ============================================================================

class AcademicYearBase(BaseModel):
    name: str
    start_date: date
    end_date: date
    status: str = "UPCOMING"
    is_current: bool = False

class AcademicYearCreate(AcademicYearBase):
    pass

class AcademicYearUpdate(BaseModel):
    name: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    status: Optional[str] = None
    is_current: Optional[bool] = None

class AcademicYearRead(AcademicYearBase):
    id: int
    created_at: datetime
    updated_at: datetime

# ============================================================================
# Academic Batch Schemas
# ============================================================================

class AcademicBatchBase(BaseModel):
    name: str
    code: str
    program_id: int
    academic_year_id: int
    admission_year: int
    graduation_year: int
    max_strength: int = 60
    is_active: bool = True

class AcademicBatchCreate(AcademicBatchBase):
    pass

class AcademicBatchUpdate(BaseModel):
    name: Optional[str] = None
    max_strength: Optional[int] = None
    is_active: Optional[bool] = None

class AcademicBatchRead(AcademicBatchBase):
    id: int
    current_strength: int
    created_at: datetime
    updated_at: datetime

# ============================================================================
# Section Schemas
# ============================================================================

class SectionBase(BaseModel):
    name: str
    code: str
    batch_semester_id: int
    batch_id: Optional[int] = None
    max_strength: int = 40
    is_active: bool = True

class SectionCreate(SectionBase):
    pass

class SectionUpdate(BaseModel):
    name: Optional[str] = None
    max_strength: Optional[int] = None
    is_active: Optional[bool] = None

class SectionRead(SectionBase):
    id: int
    current_strength: int
    created_at: datetime

# ============================================================================
# Practical Batch Schemas
# ============================================================================

class PracticalBatchBase(BaseModel):
    name: str
    code: str
    batch_semester_id: int
    max_strength: int = 40
    is_active: bool = True

class PracticalBatchCreate(PracticalBatchBase):
    pass

class PracticalBatchUpdate(BaseModel):
    name: Optional[str] = None
    max_strength: Optional[int] = None
    is_active: Optional[bool] = None

class PracticalBatchRead(PracticalBatchBase):
    id: int
    current_strength: int
    created_at: datetime

# ============================================================================
# Subject Config Schemas
# ============================================================================

class SubjectConfigBase(BaseModel):
    subject_id: int
    subject_type: str = "THEORY"
    exam_type: str = "BOTH"
    internal_max_marks: int = 30
    external_max_marks: int = 70
    practical_max_marks: int = 0
    internal_pass_marks: int = 12
    external_pass_marks: int = 28
    practical_pass_marks: int = 0
    theory_hours: int = 3
    practical_hours: int = 0
    tutorial_hours: int = 0
    is_mandatory: bool = True
    has_attendance_requirement: bool = True
    min_attendance_percent: int = 75

class SubjectConfigCreate(SubjectConfigBase):
    pass

class SubjectConfigUpdate(BaseModel):
    subject_type: Optional[str] = None
    exam_type: Optional[str] = None
    internal_max_marks: Optional[int] = None
    external_max_marks: Optional[int] = None
    practical_max_marks: Optional[int] = None
    internal_pass_marks: Optional[int] = None
    external_pass_marks: Optional[int] = None
    practical_pass_marks: Optional[int] = None
    theory_hours: Optional[int] = None
    practical_hours: Optional[int] = None
    tutorial_hours: Optional[int] = None
    is_mandatory: Optional[bool] = None
    has_attendance_requirement: Optional[bool] = None
    min_attendance_percent: Optional[int] = None

class SubjectConfigRead(SubjectConfigBase):
    id: int
    created_at: datetime
    updated_at: datetime

# ============================================================================
# Fee Head Schemas
# ============================================================================

class FeeHeadBase(BaseModel):
    name: str
    code: str
    description: Optional[str] = None
    is_refundable: bool = False
    is_recurring: bool = True
    is_mandatory: bool = True
    display_order: int = 0
    is_active: bool = True

class FeeHeadCreate(FeeHeadBase):
    pass

class FeeHeadUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    is_refundable: Optional[bool] = None
    is_recurring: Optional[bool] = None
    is_mandatory: Optional[bool] = None
    display_order: Optional[int] = None
    is_active: Optional[bool] = None

class FeeHeadRead(FeeHeadBase):
    id: int
    created_at: datetime
    updated_at: datetime

# ============================================================================
# Installment Plan Schemas
# ============================================================================

class InstallmentPlanBase(BaseModel):
    name: str
    code: str
    description: Optional[str] = None
    number_of_installments: int = 4
    installment_schedule: List[dict] = []
    late_fee_per_day: Decimal = Decimal("0.00")
    grace_period_days: int = 7
    max_late_fee: Decimal = Decimal("500.00")
    is_active: bool = True

class InstallmentPlanCreate(InstallmentPlanBase):
    pass

class InstallmentPlanUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    number_of_installments: Optional[int] = None
    installment_schedule: Optional[List[dict]] = None
    late_fee_per_day: Optional[Decimal] = None
    grace_period_days: Optional[int] = None
    max_late_fee: Optional[Decimal] = None
    is_active: Optional[bool] = None

class InstallmentPlanRead(InstallmentPlanBase):
    id: int
    created_at: datetime
    updated_at: datetime

# ============================================================================
# Scholarship Slab Schemas
# ============================================================================

class ScholarshipSlabBase(BaseModel):
    name: str
    code: str
    description: Optional[str] = None
    min_percentage: Decimal = Decimal("0.00")
    max_percentage: Decimal = Decimal("100.00")
    discount_type: str = "PERCENTAGE"
    discount_value: Decimal
    max_discount_amount: Optional[Decimal] = None
    applicable_fee_heads: List[int] = []  # Changed from List[str] to List[int]
    academic_year_id: Optional[int] = None
    program_id: Optional[int] = None
    is_active: bool = True

class ScholarshipSlabCreate(ScholarshipSlabBase):
    pass

class ScholarshipSlabUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    min_percentage: Optional[Decimal] = None
    max_percentage: Optional[Decimal] = None
    discount_type: Optional[str] = None
    discount_value: Optional[Decimal] = None
    max_discount_amount: Optional[Decimal] = None
    applicable_fee_heads: Optional[List[int]] = None  # Changed from List[str] to List[int]
    is_active: Optional[bool] = None

class ScholarshipSlabRead(ScholarshipSlabBase):
    id: int
    created_at: datetime
    updated_at: datetime

# ============================================================================
# Board Schemas
# ============================================================================

class BoardBase(BaseModel):
    name: str
    code: str
    full_name: Optional[str] = None
    state: Optional[str] = None
    country: str = "India"
    is_active: bool = True
    display_order: int = 0

class BoardCreate(BoardBase):
    pass

class BoardUpdate(BaseModel):
    name: Optional[str] = None
    full_name: Optional[str] = None
    state: Optional[str] = None
    is_active: Optional[bool] = None
    display_order: Optional[int] = None

class BoardRead(BoardBase):
    id: int
    created_at: datetime

# ============================================================================
# Previous Qualification Schemas
# ============================================================================

class PreviousQualificationBase(BaseModel):
    name: str
    code: str
    level: int = 1
    is_mandatory_for_admission: bool = True
    required_documents: List[str] = []
    is_active: bool = True
    display_order: int = 0

class PreviousQualificationCreate(PreviousQualificationBase):
    pass

class PreviousQualificationUpdate(BaseModel):
    name: Optional[str] = None
    level: Optional[int] = None
    is_mandatory_for_admission: Optional[bool] = None
    required_documents: Optional[List[str]] = None
    is_active: Optional[bool] = None
    display_order: Optional[int] = None

class PreviousQualificationRead(PreviousQualificationBase):
    id: int
    created_at: datetime

# ============================================================================
# Study Group Schemas
# ============================================================================

class StudyGroupBase(BaseModel):
    name: str
    code: str
    full_name: Optional[str] = None
    qualification_id: Optional[int] = None
    subjects: List[str] = []
    is_active: bool = True
    display_order: int = 0

class StudyGroupCreate(StudyGroupBase):
    pass

class StudyGroupUpdate(BaseModel):
    name: Optional[str] = None
    full_name: Optional[str] = None
    subjects: Optional[List[str]] = None
    is_active: Optional[bool] = None
    display_order: Optional[int] = None

class StudyGroupRead(StudyGroupBase):
    id: int
    created_at: datetime

# ============================================================================
# Reservation Category Schemas
# ============================================================================

class ReservationCategoryBase(BaseModel):
    name: str
    code: str
    full_name: Optional[str] = None
    reservation_percentage: Decimal = Decimal("0.00")
    fee_concession_percentage: Decimal = Decimal("0.00")
    requires_certificate: bool = True
    certificate_issuing_authority: Optional[str] = None
    is_active: bool = True
    display_order: int = 0

class ReservationCategoryCreate(ReservationCategoryBase):
    pass

class ReservationCategoryUpdate(BaseModel):
    name: Optional[str] = None
    full_name: Optional[str] = None
    reservation_percentage: Optional[Decimal] = None
    fee_concession_percentage: Optional[Decimal] = None
    requires_certificate: Optional[bool] = None
    certificate_issuing_authority: Optional[str] = None
    is_active: Optional[bool] = None
    display_order: Optional[int] = None

class ReservationCategoryRead(ReservationCategoryBase):
    id: int
    created_at: datetime

# ============================================================================
# Lead Source Schemas
# ============================================================================

class LeadSourceBase(BaseModel):
    name: str
    code: str
    description: Optional[str] = None
    category: str = "DIGITAL"
    is_active: bool = True
    display_order: int = 0

class LeadSourceCreate(LeadSourceBase):
    pass

class LeadSourceUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    is_active: Optional[bool] = None
    display_order: Optional[int] = None

class LeadSourceRead(LeadSourceBase):
    id: int
    created_at: datetime

# ============================================================================
# Designation Schemas
# ============================================================================

class DesignationBase(BaseModel):
    name: str
    code: str
    level: int = 1
    department_id: Optional[int] = None
    min_experience_years: int = 0
    min_qualification: Optional[str] = None
    is_teaching: bool = True
    is_active: bool = True
    display_order: int = 0

class DesignationCreate(DesignationBase):
    pass

class DesignationUpdate(BaseModel):
    name: Optional[str] = None
    level: Optional[int] = None
    min_experience_years: Optional[int] = None
    min_qualification: Optional[str] = None
    is_teaching: Optional[bool] = None
    is_active: Optional[bool] = None
    display_order: Optional[int] = None

class DesignationRead(DesignationBase):
    id: int
    created_at: datetime

# ============================================================================
# Classroom Schemas
# ============================================================================

class ClassroomBase(BaseModel):
    name: str
    code: str
    room_type: str = "CLASSROOM"
    building: Optional[str] = None
    floor: Optional[int] = None
    capacity: int = 40
    has_projector: bool = False
    has_ac: bool = False
    has_smart_board: bool = False
    has_computer: bool = False
    department_id: Optional[int] = None
    is_active: bool = True

class ClassroomCreate(ClassroomBase):
    pass

class ClassroomUpdate(BaseModel):
    name: Optional[str] = None
    room_type: Optional[str] = None
    building: Optional[str] = None
    floor: Optional[int] = None
    capacity: Optional[int] = None
    has_projector: Optional[bool] = None
    has_ac: Optional[bool] = None
    has_smart_board: Optional[bool] = None
    has_computer: Optional[bool] = None
    is_active: Optional[bool] = None

class ClassroomRead(ClassroomBase):
    id: int
    created_at: datetime
    updated_at: datetime

# ============================================================================
# Placement Company Schemas
# ============================================================================

class PlacementCompanyBase(BaseModel):
    name: str
    code: str
    company_type: str = "HOTEL"
    contact_person: Optional[str] = None
    contact_email: Optional[str] = None
    contact_phone: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: str = "India"
    website: Optional[str] = None
    is_partner: bool = False
    partnership_start_date: Optional[date] = None
    mou_document_url: Optional[str] = None
    avg_package_lpa: Optional[Decimal] = None
    is_active: bool = True

class PlacementCompanyCreate(PlacementCompanyBase):
    pass

class PlacementCompanyUpdate(BaseModel):
    name: Optional[str] = None
    company_type: Optional[str] = None
    contact_person: Optional[str] = None
    contact_email: Optional[str] = None
    contact_phone: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    website: Optional[str] = None
    is_partner: Optional[bool] = None
    partnership_start_date: Optional[date] = None
    mou_document_url: Optional[str] = None
    avg_package_lpa: Optional[Decimal] = None
    is_active: Optional[bool] = None

class PlacementCompanyRead(PlacementCompanyBase):
    id: int
    students_placed: int
    created_at: datetime
    updated_at: datetime

# ============================================================================
# Email Template Schemas
# ============================================================================

class EmailTemplateBase(BaseModel):
    name: str
    subject: str
    body: str
    template_type: str = "TRANSACTIONAL"
    variables: List[str] = []
    is_active: bool = True

class EmailTemplateCreate(EmailTemplateBase):
    pass

class EmailTemplateUpdate(BaseModel):
    subject: Optional[str] = None
    body: Optional[str] = None
    template_type: Optional[str] = None
    variables: Optional[List[str]] = None
    is_active: Optional[bool] = None

class EmailTemplateRead(EmailTemplateBase):
    id: int
    created_at: datetime
    updated_at: datetime

# ============================================================================
# SMS Template Schemas
# ============================================================================

class SMSTemplateBase(BaseModel):
    name: str
    content: str
    dlt_template_id: Optional[str] = None
    sender_id: Optional[str] = None
    template_type: str = "TRANSACTIONAL"
    variables: List[str] = []
    is_active: bool = True

class SMSTemplateCreate(SMSTemplateBase):
    pass

class SMSTemplateUpdate(BaseModel):
    content: Optional[str] = None
    dlt_template_id: Optional[str] = None
    sender_id: Optional[str] = None
    template_type: Optional[str] = None
    variables: Optional[List[str]] = None
    is_active: Optional[bool] = None

class SMSTemplateRead(SMSTemplateBase):
    id: int
    created_at: datetime
    updated_at: datetime

# ============================================================================
# Department Schemas
# ============================================================================

class DepartmentBase(BaseModel):
    name: str = Field(..., max_length=100)
    code: str = Field(..., max_length=20)
    description: Optional[str] = None
    head_of_department_id: Optional[int] = None
    is_active: bool = True

class DepartmentCreate(DepartmentBase):
    pass

class DepartmentUpdate(BaseModel):
    name: Optional[str] = None
    code: Optional[str] = None
    description: Optional[str] = None
    head_of_department_id: Optional[int] = None
    is_active: Optional[bool] = None

class DepartmentRead(DepartmentBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
