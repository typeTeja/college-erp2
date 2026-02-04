from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime, date
from app.shared.enums import ODCStatus, ApplicationStatus, PayoutStatus, BillingStatus, GenderPreference


# ----------------------------------------------------------------------
# Hotel Schemas
# ----------------------------------------------------------------------

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
    
    class Config:
        from_attributes = True


# ----------------------------------------------------------------------
# Request Schemas
# ----------------------------------------------------------------------

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
    status: ODCStatus = ODCStatus.OPEN

class ODCRequestCreate(ODCRequestBase):
    pass

class ODCRequestRead(ODCRequestBase):
    id: int
    created_at: datetime
    hotel_name: Optional[str] = None
    
    class Config:
        from_attributes = True


# ----------------------------------------------------------------------
# Application Schemas
# ----------------------------------------------------------------------

class ODCApplicationBase(BaseModel):
    request_id: int
    student_id: int
    status: ODCStatus = ODCStatus.OPEN

class ODCApplicationRead(ODCApplicationBase):
    id: int
    applied_at: datetime
    event_name: Optional[str] = None
    event_date: Optional[date] = None
    payout_status: PayoutStatus
    
    class Config:
        from_attributes = True

class SelectionUpdate(BaseModel):
    application_ids: List[int]
    status: ODCStatus
    remarks: Optional[str] = None


# ----------------------------------------------------------------------
# Feedback Schemas
# ----------------------------------------------------------------------

class StudentFeedbackSubmit(BaseModel):
    student_feedback: str
    student_rating: int = Field(..., ge=1, le=5)

class HotelFeedbackSubmit(BaseModel):
    hotel_feedback: str
    hotel_rating: int = Field(..., ge=1, le=5)


# ----------------------------------------------------------------------
# Billing Schemas
# ----------------------------------------------------------------------

class ODCBillingBase(BaseModel):
    request_id: int
    invoice_date: date
    due_date: Optional[date] = None
    notes: Optional[str] = None

class ODCBillingCreate(ODCBillingBase):
    pass

class ODCBillingRead(ODCBillingBase):
    id: int
    invoice_number: str
    total_students: int
    amount_per_student: float
    total_amount: float
    status: BillingStatus
    paid_date: Optional[date] = None
    payment_method: Optional[str] = None
    payment_reference: Optional[str] = None
    created_at: datetime
    
    class Config:
        from_attributes = True

class BillingMarkPaid(BaseModel):
    payment_method: str
    payment_reference: Optional[str] = None
    paid_date: date
    notes: Optional[str] = None


# ----------------------------------------------------------------------
# Payout Schemas
# ----------------------------------------------------------------------

class ODCPayoutRead(BaseModel):
    id: int
    application_id: int
    amount: float
    payment_method: str
    transaction_reference: Optional[str] = None
    payout_date: date
    processed_at: datetime
    notes: Optional[str] = None
    student_name: Optional[str] = None
    event_name: Optional[str] = None

    class Config:
        from_attributes = True

class PayoutBatchProcess(BaseModel):
    application_ids: List[int]
    payment_method: str
    payout_date: date
    notes: Optional[str] = None
