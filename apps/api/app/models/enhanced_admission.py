"""
Enhanced Admission Models - RCMS Features

Additional models for comprehensive admission workflow
"""
from typing import TYPE_CHECKING, List, Optional
from datetime import datetime, date
from enum import Enum
from sqlmodel import SQLModel, Field, Relationship, Column
from sqlalchemy import JSON, Text

if TYPE_CHECKING:
    from .admissions import Application
    from .user import User


class TentativeAdmissionStatus(str, Enum):
    """Tentative admission status"""
    PENDING_PAYMENT = "PENDING_PAYMENT"
    PAYMENT_RECEIVED = "PAYMENT_RECEIVED"
    EXPIRED = "EXPIRED"


class EntranceTestConfig(SQLModel, table=True):
    """Entrance test configuration"""
    __tablename__ = "entrance_test_config"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    
    # Test Details
    test_name: str  # "Regency National Entrance Test 2024-25"
    academic_year: str  # "2024-25"
    
    # Schedule
    test_date: date = Field(index=True)
    test_time: str  # "10:00 AM"
    test_duration_minutes: int = Field(default=120)
    reporting_time: Optional[str] = None  # "09:30 AM"
    
    # Venue
    venue_name: str
    venue_address: str = Field(sa_column=Column(Text))
    venue_instructions: Optional[str] = Field(default=None, sa_column=Column(Text))
    
    # Guidelines
    guidelines: Optional[str] = Field(default=None, sa_column=Column(Text))
    documents_required: Optional[str] = Field(default=None, sa_column=Column(JSON))
    # Example: ["Hall Ticket", "Photo ID", "Pen/Pencil"]
    
    # Exam Details
    total_marks: float = Field(default=100.0)
    subjects: Optional[str] = Field(default=None, sa_column=Column(JSON))
    # Example: [{"name": "English", "marks": 25}, {"name": "GK", "marks": 25}]
    
    # Status
    is_active: bool = Field(default=True)
    registration_open: bool = Field(default=True)
    registration_deadline: Optional[date] = None
    
    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class TentativeAdmission(SQLModel, table=True):
    """Tentative admission with fee structure"""
    __tablename__ = "tentative_admission"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    
    # Links
    application_id: int = Field(foreign_key="application.id", index=True)
    
    # Scholarship Details
    scholarship_slab: str  # A, B, C, D
    scholarship_amount: float
    
    # Fee Structure
    base_annual_fee: float
    scholarship_discount: float
    net_annual_fee: float
    
    # Fee Breakdown
    tuition_fee: Optional[float] = None
    library_fee: Optional[float] = None
    lab_fee: Optional[float] = None
    uniform_fee: Optional[float] = None
    caution_deposit: Optional[float] = None
    miscellaneous_fee: Optional[float] = None
    
    # Payment Plan
    number_of_installments: int = Field(default=4)
    first_installment_amount: float
    
    # Admission Letter
    admission_letter_url: Optional[str] = None
    admission_letter_generated: bool = Field(default=False)
    
    # Payment Link
    payment_link: Optional[str] = None
    payment_link_generated: bool = Field(default=False)
    
    # First Installment Payment
    first_installment_paid: bool = Field(default=False)
    payment_id: Optional[str] = None
    payment_date: Optional[datetime] = None
    
    # Validity
    valid_until: date
    
    # Status
    status: TentativeAdmissionStatus = Field(
        default=TentativeAdmissionStatus.PENDING_PAYMENT,
        index=True
    )
    
    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    application: "Application" = Relationship()


class ScholarshipCalculation(SQLModel, table=True):
    """Scholarship calculation based on merit"""
    __tablename__ = "scholarship_calculation"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    
    # Links
    application_id: int = Field(foreign_key="application.id", unique=True, index=True)
    
    # Student Info
    student_name: str
    course: str
    
    # Previous Academic Performance
    previous_percentage: Optional[float] = None
    previous_score: float = Field(default=0.0)  # Converted to points
    
    # Entrance Exam Performance
    entrance_percentage: Optional[float] = None
    entrance_score: float = Field(default=0.0)  # Converted to points
    
    # Weighted Average
    previous_weightage: float = Field(default=0.5)  # 50%
    entrance_weightage: float = Field(default=0.5)  # 50%
    final_merit_score: float = Field(default=0.0)
    
    # Scholarship Slab Determination
    scholarship_slab: Optional[str] = None  # A, B, C, D
    scholarship_percentage: float = Field(default=0.0)
    scholarship_amount: float = Field(default=0.0)
    
    # Annual Fee
    base_annual_fee: float = Field(default=0.0)
    final_annual_fee: float = Field(default=0.0)  # After scholarship
    
    # Status
    is_calculated: bool = Field(default=False)
    calculated_by: Optional[int] = Field(default=None, foreign_key="user.id")
    calculation_date: Optional[datetime] = None
    
    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    application: "Application" = Relationship()
