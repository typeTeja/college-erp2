"""
Finance Domain Schemas

Pydantic schemas for the finance domain.
Note: This is a simplified version. Full schemas can be added as needed.
"""

from pydantic import BaseModel
from typing import Optional
from datetime import datetime, date
from decimal import Decimal


# ----------------------------------------------------------------------
# Fee Configuration Schemas
# ----------------------------------------------------------------------

class FeeHeadBase(BaseModel):
    name: str
    code: str
    amount: Decimal
    is_mandatory: bool = True


class FeeHeadCreate(FeeHeadBase):
    pass


class FeeHeadRead(FeeHeadBase):
    id: int
    
    class Config:
        from_attributes = True


# ----------------------------------------------------------------------
# Fee Payment Schemas
# ----------------------------------------------------------------------

class FeePaymentBase(BaseModel):
    student_id: int
    amount: Decimal
    payment_mode: str
    payment_date: date


class FeePaymentCreate(FeePaymentBase):
    pass


class FeePaymentRead(FeePaymentBase):
    id: int
    transaction_id: Optional[str] = None
    status: str
    created_at: datetime
    
    class Config:
        from_attributes = True


# ----------------------------------------------------------------------
# Payment Gateway Schemas
# ----------------------------------------------------------------------

class PaymentInitiateRequest(BaseModel):
    amount: Decimal
    student_id: int
    purpose: str


class PaymentInitiateResponse(BaseModel):
    payment_url: str
    transaction_id: str
    amount: Decimal


class PaymentCallbackData(BaseModel):
    transaction_id: str
    status: str
    amount: Decimal
    payment_mode: Optional[str] = None
