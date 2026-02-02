from typing import List, Optional
from datetime import date, datetime
from pydantic import BaseModel, Field
from app.models.odc import (
from app.shared.enums import ApplicationStatus, BillingStatus, GenderPreference, ODCStatus, PaymentMethod

    GenderPreference, ODCStatus, ApplicationStatus, PayoutStatus,
    BillingStatus, PaymentMethod
)

# Shared properties
class ODCHotelBase(BaseModel):
    name: str
    address: str
    contact_person: str
    phone: str
    email: Optional[str] = None
    default_pay_rate: Optional[float] = None
    is_active: bool = True

class ODCHotelCreate(ODCHotelBase):
    pass

class ODCHotelRead(ODCHotelBase):
    id: int

class ODCRequestBase(BaseModel):
    hotel_id: int
    event_name: str
    event_date: date
    report_time: datetime
    duration_hours: float
    vacancies: int
    gender_preference: GenderPreference = GenderPreference.ANY
    pay_amount: float
    transport_provided: bool = False

class ODCRequestCreate(ODCRequestBase):
    pass

class ODCRequestRead(ODCRequestBase):
    id: int
    status: ODCStatus
    created_by_id: int
    created_at: datetime
    hotel_name: Optional[str] = None  # Flattened for display

class ApplicationCreate(BaseModel):
    request_id: int

class ApplicationRead(BaseModel):
    id: int
    request_id: int
    student_id: int
    status: ApplicationStatus
    applied_at: datetime
    event_name: Optional[str] = None
    event_date: Optional[date] = None

class SelectionUpdate(BaseModel):
    application_ids: List[int]
    status: ApplicationStatus
    remarks: Optional[str] = None

# --- Feedback Schemas ---

class StudentFeedbackSubmit(BaseModel):
    student_feedback: str
    student_rating: int = Field(ge=1, le=5)

class HotelFeedbackSubmit(BaseModel):
    hotel_feedback: str
    hotel_rating: int = Field(ge=1, le=5)

class FeedbackRead(BaseModel):
    student_feedback: Optional[str] = None
    student_rating: Optional[int] = None
    hotel_feedback: Optional[str] = None
    hotel_rating: Optional[int] = None

# --- Billing Schemas ---

class BillingCreate(BaseModel):
    request_id: int
    invoice_date: date
    due_date: Optional[date] = None
    notes: Optional[str] = None

class BillingRead(BaseModel):
    id: int
    request_id: int
    invoice_number: str
    total_students: int
    amount_per_student: float
    total_amount: float
    status: BillingStatus
    invoice_date: date
    due_date: Optional[date] = None
    paid_date: Optional[date] = None
    payment_method: Optional[PaymentMethod] = None
    payment_reference: Optional[str] = None
    notes: Optional[str] = None
    created_at: datetime
    
    # Expanded fields
    event_name: Optional[str] = None
    hotel_name: Optional[str] = None

class BillingMarkPaid(BaseModel):
    payment_method: PaymentMethod
    payment_reference: Optional[str] = None
    paid_date: date
    notes: Optional[str] = None

# --- Payout Schemas ---

class PayoutCreate(BaseModel):
    application_id: int
    amount: float
    payment_method: PaymentMethod
    transaction_reference: Optional[str] = None
    payout_date: date
    notes: Optional[str] = None

class PayoutRead(BaseModel):
    id: int
    application_id: int
    amount: float
    payment_method: PaymentMethod
    transaction_reference: Optional[str] = None
    payout_date: date
    processed_at: datetime
    notes: Optional[str] = None
    
    # Expanded fields
    student_name: Optional[str] = None
    event_name: Optional[str] = None

class PayoutBatchProcess(BaseModel):
    application_ids: List[int]
    payment_method: PaymentMethod
    payout_date: date
    notes: Optional[str] = None

class PayoutSummary(BaseModel):
    total_pending: int
    total_amount_pending: float
    applications: List[ApplicationRead]

