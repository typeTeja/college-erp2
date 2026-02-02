from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class StudentDocuments(BaseModel):
    """Schema for Student.documents JSON field"""
    photo: Optional[str] = None
    aadhaar_card: Optional[str] = None
    tenth_marksheet: Optional[str] = None
    twelfth_marksheet: Optional[str] = None
    transfer_certificate: Optional[str] = None
    migration_certificate: Optional[str] = None
    caste_certificate: Optional[str] = None
    income_certificate: Optional[str] = None
    other_documents: Dict[str, str] = Field(default_factory=dict)

class InstallmentDetail(BaseModel):
    """Schema for individual installment in InstallmentPlan"""
    installment_no: int
    percentage: float
    due_days_from_start: int
    description: Optional[str] = None

class EntranceTestSubject(BaseModel):
    """Schema for subjects in EntranceTestConfig"""
    name: str
    marks: float
    description: Optional[str] = None

class SubjectMarksEntry(BaseModel):
    """Schema for subject-wise marks in EntranceExamResult"""
    subject: str
    max: float
    secured: float

class ChecklistItem(BaseModel):
    """Schema for individual checklist item in DocumentVerification"""
    item: str
    checked: bool = False
    remarks: Optional[str] = None
