from typing import List, Optional
from datetime import date, datetime
from pydantic import BaseModel, Field
from ..models.odc import ODCStatus, ODCApplicationStatus, BillingStatus, ODCPaymentMethod

class ODCHotelBase(BaseModel):
    name: str
    address: str
    contact_person: str
    phone: str
    email: Optional[str] = None
    default_pay_rate: Optional[float] = None

class ODCHotelCreate(ODCHotelBase):
    pass

class ODCRequestBase(BaseModel):
    hotel_id: int
    event_name: str
    event_date: date
    report_time: datetime
    duration_hours: float
    vacancies: int
    pay_amount: float
    transport_provided: bool = False

class ODCRequestCreate(ODCRequestBase):
    pass

class ApplicationCreate(BaseModel):
    request_id: int

class SelectionUpdate(BaseModel):
    application_ids: List[int]
    status: ODCApplicationStatus
    remarks: Optional[str] = None
