from typing import TYPE_CHECKING, Optional
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship
from app.shared.enums import TentativeAdmissionStatus

if TYPE_CHECKING:
    from .application import Application

class TentativeAdmission(SQLModel, table=True):
    """Tentative admission with fee structure"""
    __tablename__ = "tentative_admission"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    application_id: int = Field(foreign_key="application.id", index=True)
    
    scholarship_slab: str 
    scholarship_amount: float
    base_annual_fee: float
    scholarship_discount: float
    net_annual_fee: float
    
    tuition_fee: Optional[float] = None
    library_fee: Optional[float] = None
    lab_fee: Optional[float] = None
    uniform_fee: Optional[float] = None
    caution_deposit: Optional[float] = None
    miscellaneous_fee: Optional[float] = None
    
    number_of_installments: int = Field(default=4)
    first_installment_amount: float
    
    admission_letter_url: Optional[str] = None
    admission_letter_generated: bool = Field(default=False)
    payment_link: Optional[str] = None
    payment_link_generated: bool = Field(default=False)
    
    first_installment_paid: bool = Field(default=False)
    payment_id: Optional[str] = None
    payment_date: Optional[datetime] = None
    valid_until: datetime # Changed from date to datetime for consistency
    
    status: TentativeAdmissionStatus = Field(
        default=TentativeAdmissionStatus.PENDING_PAYMENT,
        index=True
    )
    
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    application: "Application" = Relationship(back_populates="tentative_admissions")

class ScholarshipCalculation(SQLModel, table=True):
    """Scholarship calculation based on merit"""
    __tablename__ = "scholarship_calculation"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    application_id: int = Field(foreign_key="application.id", unique=True, index=True)
    
    student_name: str
    course: str
    
    previous_percentage: Optional[float] = None
    previous_score: float = Field(default=0.0)
    entrance_percentage: Optional[float] = None
    entrance_score: float = Field(default=0.0)
    
    previous_weightage: float = Field(default=0.5)
    entrance_weightage: float = Field(default=0.5)
    final_merit_score: float = Field(default=0.0)
    
    scholarship_slab: Optional[str] = None
    scholarship_percentage: float = Field(default=0.0)
    scholarship_amount: float = Field(default=0.0)
    
    base_annual_fee: float = Field(default=0.0)
    final_annual_fee: float = Field(default=0.0)
    
    is_calculated: bool = Field(default=False)
    calculated_by: Optional[int] = Field(default=None, foreign_key="users.id")
    calculation_date: Optional[datetime] = None
    
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    application: "Application" = Relationship(back_populates="scholarship_calculation")
