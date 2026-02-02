from typing import TYPE_CHECKING, List, Optional
from datetime import date, datetime
from enum import Enum
from sqlmodel import SQLModel, Field, Relationship
from app.shared.enums import ApplicationStatus, BillingStatus, GenderPreference, ODCStatus, PaymentMethod, PayoutStatus


if TYPE_CHECKING:
    from app.models.user import User
    from .student import Student


class ODCHotel(SQLModel, table=True):
    """Hotel or Catering Partner for ODC"""
    __tablename__ = "odc_hotel"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    address: str
    contact_person: str
    phone: str
    email: Optional[str] = None
    default_pay_rate: Optional[float] = None  # Default hourly/daily rate
    is_active: bool = Field(default=True)
    
    # Relationships
    requests: List["ODCRequest"] = Relationship(back_populates="hotel")

class ODCRequest(SQLModel, table=True):
    """Specific ODC Event Request"""
    __tablename__ = "odc_request"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    hotel_id: int = Field(foreign_key="odc_hotel.id")
    event_name: str
    event_date: date
    report_time: datetime
    duration_hours: float
    vacancies: int
    gender_preference: GenderPreference = Field(default=GenderPreference.ANY)
    pay_amount: float
    transport_provided: bool = Field(default=False)
    status: ODCStatus = Field(default=ODCStatus.OPEN)
    created_by_id: int = Field(foreign_key="user.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    hotel: ODCHotel = Relationship(back_populates="requests")
    applications: List["StudentODCApplication"] = Relationship(back_populates="request")

    @property
    def hotel_name(self) -> str:
        return self.hotel.name if self.hotel else "Unknown Hotel"

class StudentODCApplication(SQLModel, table=True):
    """Student Application for ODC"""
    __tablename__ = "student_odc_application"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    request_id: int = Field(foreign_key="odc_request.id")
    student_id: int = Field(foreign_key="student.id")
    status: ApplicationStatus = Field(default=ApplicationStatus.APPLIED)
    admin_remarks: Optional[str] = None
    
    # Feedback fields
    student_feedback: Optional[str] = None
    student_rating: Optional[int] = Field(default=None, ge=1, le=5)  # 1-5 stars
    hotel_feedback: Optional[str] = None
    hotel_rating: Optional[int] = Field(default=None, ge=1, le=5)  # 1-5 stars
    
    # Payout fields
    payout_status: PayoutStatus = Field(default=PayoutStatus.PENDING)
    payout_amount: Optional[float] = None
    
    # Timestamps
    applied_at: datetime = Field(default_factory=datetime.utcnow)
    attendance_confirmed_at: Optional[datetime] = None
    
    # Relationships
    request: ODCRequest = Relationship(back_populates="applications")
    payout: Optional["ODCPayout"] = Relationship(back_populates="application")

class ODCBilling(SQLModel, table=True):
    """Billing/Invoice for ODC Event sent to Hotel"""
    __tablename__ = "odc_billing"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    request_id: int = Field(foreign_key="odc_request.id", unique=True)
    invoice_number: str = Field(unique=True, index=True)
    
    # Billing details
    total_students: int  # Number of students who attended
    amount_per_student: float
    total_amount: float
    
    # Status and dates
    status: BillingStatus = Field(default=BillingStatus.DRAFT)
    invoice_date: date
    due_date: Optional[date] = None
    paid_date: Optional[date] = None
    
    # Payment details
    payment_method: Optional[PaymentMethod] = None
    payment_reference: Optional[str] = None
    
    # Metadata
    notes: Optional[str] = None
    created_by_id: int = Field(foreign_key="user.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    request: ODCRequest = Relationship()

class ODCPayout(SQLModel, table=True):
    """Payout to Student for ODC Attendance"""
    __tablename__ = "odc_payout"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    application_id: int = Field(foreign_key="student_odc_application.id", unique=True)
    
    # Payout details
    amount: float
    payment_method: PaymentMethod
    transaction_reference: Optional[str] = None
    
    # Dates
    payout_date: date
    processed_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Metadata
    processed_by_id: int = Field(foreign_key="user.id")
    notes: Optional[str] = None
    
    # Relationships
    application: StudentODCApplication = Relationship(back_populates="payout")
