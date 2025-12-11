from typing import TYPE_CHECKING, List, Optional
from datetime import date, datetime
from enum import Enum
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from .user import User
    from .student import Student

class GenderPreference(str, Enum):
    MALE = "MALE"
    FEMALE = "FEMALE"
    ANY = "ANY"

class ODCStatus(str, Enum):
    OPEN = "OPEN"
    CLOSED = "CLOSED"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"

class ApplicationStatus(str, Enum):
    APPLIED = "APPLIED"
    SELECTED = "SELECTED"
    REJECTED = "REJECTED"
    ATTENDED = "ATTENDED"
    ABSENT = "ABSENT"
    WITHDRAWN = "WITHDRAWN"

class PayoutStatus(str, Enum):
    PENDING = "PENDING"
    PAID = "PAID"

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

class StudentODCApplication(SQLModel, table=True):
    """Student Application for ODC"""
    __tablename__ = "student_odc_application"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    request_id: int = Field(foreign_key="odc_request.id")
    student_id: int = Field(foreign_key="student.id")
    status: ApplicationStatus = Field(default=ApplicationStatus.APPLIED)
    admin_remarks: Optional[str] = None
    student_feedback: Optional[str] = None
    hotel_feedback: Optional[str] = None
    payout_status: PayoutStatus = Field(default=PayoutStatus.PENDING)
    applied_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    request: ODCRequest = Relationship(back_populates="applications")
    # Student relationship will be defined in Student model or resolved via back_populates if added there
