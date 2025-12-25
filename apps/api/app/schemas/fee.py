from typing import Optional, List
from datetime import date, datetime
from decimal import Decimal
from pydantic import BaseModel, Field
from app.models.fee import FeeCategory, PaymentMode, PaymentStatus

# ============================================================================
# Fee Structure Schemas
# ============================================================================

class FeeComponentCreate(BaseModel):
    """Schema for creating a fee component"""
    name: str
    amount: Decimal
    is_refundable: bool = False

class FeeComponentResponse(BaseModel):
    """Schema for fee component response"""
    id: int
    name: str
    amount: Decimal
    is_refundable: bool
    
    class Config:
        from_attributes = True

class FeeInstallmentCreate(BaseModel):
    """Schema for creating a fee installment"""
    installment_number: int
    amount: Decimal
    due_date: date

class FeeInstallmentResponse(BaseModel):
    """Schema for fee installment response"""
    id: int
    installment_number: int
    amount: Decimal
    due_date: date
    
    class Config:
        from_attributes = True

class FeeStructureCreate(BaseModel):
    """Schema for creating a fee structure"""
    program_id: int
    academic_year: str
    year: int
    category: FeeCategory = FeeCategory.GENERAL
    components: List[FeeComponentCreate]
    installments: List[FeeInstallmentCreate]

class FeeStructureResponse(BaseModel):
    """Schema for fee structure response"""
    id: int
    program_id: int
    academic_year: str
    year: int
    category: FeeCategory
    total_amount: Decimal
    components: List[FeeComponentResponse]
    installments: List[FeeInstallmentResponse]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

# ============================================================================
# Student Fee Schemas
# ============================================================================

class StudentFeeCreate(BaseModel):
    """Schema for assigning fee structure to student"""
    student_id: int
    fee_structure_id: int
    academic_year: str

class StudentFeeResponse(BaseModel):
    """Schema for student fee response"""
    id: int
    student_id: int
    fee_structure_id: int
    academic_year: str
    total_fee: Decimal
    concession_amount: Decimal
    fine_amount: Decimal
    paid_amount: Decimal
    balance: Decimal
    is_blocked: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class StudentFeeSummary(BaseModel):
    """Detailed fee summary for a student"""
    student_id: int
    student_name: str
    admission_number: str
    academic_year: str
    total_fee: Decimal
    concession_amount: Decimal
    fine_amount: Decimal
    paid_amount: Decimal
    balance: Decimal
    is_blocked: bool
    installments: List[dict]  # Installment details with payment status
    payments: List[dict]  # Payment history

# ============================================================================
# Payment Schemas
# ============================================================================

class FeePaymentCreate(BaseModel):
    """Schema for creating a fee payment"""
    student_fee_id: int
    amount: Decimal
    payment_mode: PaymentMode
    reference_number: Optional[str] = None
    bank_name: Optional[str] = None
    remarks: Optional[str] = None

class PaymentInitiateRequest(BaseModel):
    """Schema for initiating online payment"""
    student_fee_id: int
    amount: Decimal

class PaymentInitiateResponse(BaseModel):
    """Schema for payment initiation response"""
    payment_id: int
    transaction_id: str
    payment_url: str
    amount: Decimal

class PaymentWebhookData(BaseModel):
    """Schema for payment gateway webhook"""
    transaction_id: str
    status: str
    amount: Decimal
    gateway_response: dict

class FeePaymentResponse(BaseModel):
    """Schema for fee payment response"""
    id: int
    student_fee_id: int
    amount: Decimal
    payment_mode: PaymentMode
    payment_status: PaymentStatus
    transaction_id: Optional[str]
    reference_number: Optional[str]
    bank_name: Optional[str]
    payment_date: Optional[datetime]
    created_at: datetime
    remarks: Optional[str]
    
    class Config:
        from_attributes = True

# ============================================================================
# Concession Schemas
# ============================================================================

class FeeConcessionCreate(BaseModel):
    """Schema for creating a fee concession"""
    student_fee_id: int
    concession_type: str
    amount: Optional[Decimal] = None
    percentage: Optional[Decimal] = None
    remarks: Optional[str] = None

class FeeConcessionResponse(BaseModel):
    """Schema for fee concession response"""
    id: int
    student_fee_id: int
    concession_type: str
    amount: Decimal
    percentage: Optional[Decimal]
    approved_by: Optional[str]
    approved_at: Optional[datetime]
    remarks: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True

# ============================================================================
# Fine Schemas
# ============================================================================

class FeeFineCreate(BaseModel):
    """Schema for creating a fee fine"""
    student_fee_id: int
    installment_number: int
    fine_amount: Decimal
    reason: str

class FeeFineResponse(BaseModel):
    """Schema for fee fine response"""
    id: int
    student_fee_id: int
    installment_number: int
    fine_amount: Decimal
    reason: str
    waived: bool
    waived_by: Optional[str]
    waived_at: Optional[datetime]
    created_at: datetime
    
    class Config:
        from_attributes = True

# ============================================================================
# Defaulter Schemas
# ============================================================================

class FeeDefaulter(BaseModel):
    """Schema for fee defaulter"""
    student_id: int
    student_name: str
    admission_number: str
    program: str
    year: int
    total_due: Decimal
    overdue_installments: int
    last_payment_date: Optional[date]
    days_overdue: int
