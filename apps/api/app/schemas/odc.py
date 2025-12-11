from typing import List, Optional
from datetime import date, datetime
from pydantic import BaseModel, Field
from app.models.odc import GenderPreference, ODCStatus, ApplicationStatus, PayoutStatus

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
