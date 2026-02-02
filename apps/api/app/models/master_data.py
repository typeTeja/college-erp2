"""
Backward Compatibility Stub for Master Data Models
Phase 1 Refactor (2026-02-01)
"""
from app.domains.academic.models import AcademicYear, Section, PracticalBatch, SubjectConfig
from app.models.finance.fee_config import FeeHead, InstallmentPlan, ScholarshipSlab
from .settings.registration import (
    Board, PreviousQualification, StudyGroup, 
    ReservationCategory, LeadSource
)
from app.domains.hr.models import Designation
from app.domains.campus.infrastructure.models import MasterClassroom
from .placement.company import PlacementCompany
from .settings.notifications import EmailTemplate, SMSTemplate
from .enums import AcademicYearStatus, SubjectType, ExamType, RoomType
