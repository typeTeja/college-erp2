"""
Finance Domain Schemas

API contract schemas for finance operations.

**CONTRACT VERSION: v1.0.0**
**STATUS: FROZEN (2026-02-03)**

⚠️ BREAKING CHANGES POLICY:
- Enum additions: Safe (backward compatible)
- New optional fields: Safe
- Required field changes: Requires migration + 6-month deprecation
- Enum removals: 6-month deprecation period
- Field type changes: Major version bump

Any changes to this file require approval and version bump.
"""

from pydantic import BaseModel, Field, field_validator
from typing import Optional, List
from datetime import datetime, date
from decimal import Decimal
from app.shared.enums import FeeCategory, PaymentMode, PaymentStatus


# ----------------------------------------------------------------------
# Fee Head Schemas
# ----------------------------------------------------------------------

class FeeHeadBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    code: str = Field(..., min_length=1, max_length=20, pattern=r'^[A-Z0-9_]+$')
    description: Optional[str] = Field(None, max_length=500)
    category: str = Field(default="ACADEMIC", max_length=50)
    is_mandatory: bool = True

class FeeHeadCreate(FeeHeadBase):
    pass

class FeeHeadRead(FeeHeadBase):
    id: int
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


# ----------------------------------------------------------------------
# Fee Structure Schemas
# ----------------------------------------------------------------------

class FeeStructureBase(BaseModel):
    program_id: int = Field(..., gt=0)
    academic_year: str = Field(..., min_length=7, max_length=9, pattern=r'^\d{4}-\d{4}$')
    year: int = Field(..., ge=1, le=6)
    slab: str = Field(default="GENERAL", max_length=20)
    category: FeeCategory = FeeCategory.GENERAL

class FeeStructureCreate(FeeStructureBase):
    tuition_fee: Decimal = Field(..., ge=0, decimal_places=2)
    library_fee: Decimal = Field(default=Decimal("0.00"), ge=0, decimal_places=2)
    lab_fee: Decimal = Field(default=Decimal("0.00"), ge=0, decimal_places=2)
    uniform_fee: Decimal = Field(default=Decimal("0.00"), ge=0, decimal_places=2)
    caution_deposit: Decimal = Field(default=Decimal("0.00"), ge=0, decimal_places=2)
    digital_fee: Decimal = Field(default=Decimal("0.00"), ge=0, decimal_places=2)
    miscellaneous_fee: Decimal = Field(default=Decimal("0.00"), ge=0, decimal_places=2)
    number_of_installments: int = Field(default=4, ge=1, le=12)

class FeeStructureRead(FeeStructureBase):
    id: int
    total_annual_fee: Decimal
    total_amount: Decimal
    installment_amount: Decimal
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


# ----------------------------------------------------------------------
# Payment Schemas
# ----------------------------------------------------------------------

class FeePaymentBase(BaseModel):
    student_fee_id: int = Field(..., gt=0)
    amount: Decimal = Field(..., gt=0, decimal_places=2)
    payment_mode: PaymentMode
    
    @field_validator('amount')
    def validate_amount(cls, v):
        if v <= 0:
            raise ValueError('Amount must be positive')
        if v > Decimal("1000000.00"):  # 10 lakh max
            raise ValueError('Amount exceeds maximum limit')
        return v

class FeePaymentCreate(FeePaymentBase):
    transaction_id: Optional[str] = Field(None, min_length=1, max_length=100)
    reference_number: Optional[str] = Field(None, min_length=1, max_length=100)
    bank_name: Optional[str] = Field(None, min_length=1, max_length=100)
    remarks: Optional[str] = Field(None, max_length=500)

class FeePaymentRead(FeePaymentBase):
    id: int
    payment_status: PaymentStatus
    transaction_id: Optional[str]
    payment_date: Optional[datetime]
    created_at: datetime
    
    class Config:
        from_attributes = True


# ----------------------------------------------------------------------
# Online Payment Schemas
# ----------------------------------------------------------------------

class PaymentInitiateRequest(BaseModel):
    student_id: int = Field(..., gt=0)
    student_fee_id: int = Field(..., gt=0)
    amount: Decimal = Field(..., gt=0, decimal_places=2)
    customer_name: str = Field(..., min_length=1, max_length=200)
    customer_email: str = Field(..., min_length=1, max_length=100)
    customer_phone: str = Field(..., pattern=r'^\d{10}$', description="10-digit phone number")
    
    @field_validator('amount')
    def validate_amount(cls, v):
        if v <= 0:
            raise ValueError('Amount must be positive')
        if v > Decimal("1000000.00"):
            raise ValueError('Amount exceeds maximum limit (₹10,00,000)')
        return v

class PaymentInitiateResponse(BaseModel):
    payment_url: str
    transaction_id: str
    gateway_order_id: str
    amount: Decimal
    currency: str = "INR"

class PaymentCallbackData(BaseModel):
    transaction_id: str = Field(..., min_length=1, max_length=100)
    gateway_payment_id: Optional[str] = Field(None, max_length=100)
    gateway_signature: Optional[str] = Field(None, max_length=500)
    status: PaymentStatus
    amount: Decimal = Field(..., gt=0)
    payment_mode: Optional[PaymentMode] = None

class OnlinePaymentRead(BaseModel):
    id: int
    idempotency_key: str
    student_id: int
    amount: float
    payment_status: PaymentStatus
    gateway_transaction_id: Optional[str]
    gateway_order_id: Optional[str]
    customer_name: str
    customer_email: str
    customer_phone: str
    receipt_number: Optional[str]
    receipt_url: Optional[str]
    initiated_at: datetime
    completed_at: Optional[datetime]
    
    class Config:
        from_attributes = True


# ----------------------------------------------------------------------
# Scholarship Schemas
# ----------------------------------------------------------------------

class ScholarshipSlabBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    code: str = Field(..., min_length=1, max_length=50, pattern=r'^[A-Z0-9_]+$')
    description: Optional[str] = Field(None, max_length=500)
    discount_type: str = Field(default="PERCENTAGE", pattern=r'^(PERCENTAGE|FIXED_AMOUNT)$')
    discount_value: Decimal = Field(..., ge=0, decimal_places=2)

class ScholarshipSlabCreate(ScholarshipSlabBase):
    min_percentage: Optional[Decimal] = Field(None, ge=0, le=100, decimal_places=2)
    max_percentage: Optional[Decimal] = Field(None, ge=0, le=100, decimal_places=2)

class ScholarshipSlabRead(ScholarshipSlabBase):
    id: int
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

