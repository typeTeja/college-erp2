"""
Finance Domain Models

All database models for the finance domain including:
- Fee configuration and management
- Payment gateway integration
- Online payment tracking
"""



# ======================================================================
# Config
# ======================================================================

from typing import TYPE_CHECKING, List, Optional
from datetime import datetime
from decimal import Decimal
from sqlmodel import SQLModel, Field, Relationship, Column
from sqlalchemy import DECIMAL, JSON

if TYPE_CHECKING:
    from app.domains.admission.models import EntranceExamResult
    from app.domains.admission.models import AdmissionSettings

class FeeHead(SQLModel, table=True):
    """Fee Heads Management - Types of fees (Tuition, Lab, etc.)"""
    __tablename__ = "fee_head"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(unique=True, index=True)
    code: str = Field(unique=True, index=True)
    description: Optional[str] = None
    
    is_refundable: bool = Field(default=False)
    is_recurring: bool = Field(default=True)
    is_mandatory: bool = Field(default=True)
    
    display_order: int = Field(default=0)
    is_active: bool = Field(default=True)
    
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class InstallmentPlan(SQLModel, table=True):
    """Installment Plan Management - Payment schedules"""
    __tablename__ = "installment_plan"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(unique=True, index=True)
    code: str = Field(unique=True, index=True)
    description: Optional[str] = None
    
    number_of_installments: int = Field(default=4)
    installment_schedule: List[dict] = Field(default=[], sa_column=Column(JSON))
    
    late_fee_per_day: Decimal = Field(default=Decimal("0.00"), sa_column=Column(DECIMAL(10, 2)))
    grace_period_days: int = Field(default=7)
    max_late_fee: Decimal = Field(default=Decimal("500.00"), sa_column=Column(DECIMAL(10, 2)))
    
    is_active: bool = Field(default=True)
    
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class ScholarshipSlab(SQLModel, table=True):
    """Scholarship Slab Management - Merit-based discounts"""
    __tablename__ = "scholarship_slab"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    code: str = Field(unique=True, index=True)
    description: Optional[str] = None
    
    min_percentage: Decimal = Field(default=Decimal("0.00"), sa_column=Column(DECIMAL(5, 2)))
    max_percentage: Decimal = Field(default=Decimal("100.00"), sa_column=Column(DECIMAL(5, 2)))
    
    discount_type: str = Field(default="PERCENTAGE")
    discount_value: Decimal = Field(default=Decimal("0.00"), sa_column=Column(DECIMAL(10, 2)))
    max_discount_amount: Optional[Decimal] = Field(default=None, sa_column=Column(DECIMAL(10, 2)))
    
    applicable_fee_heads: List[str] = Field(default=[], sa_column=Column(JSON))
    
    academic_year_id: Optional[int] = Field(default=None, foreign_key="academic_year.id")
    program_id: Optional[int] = Field(default=None, foreign_key="program.id")
    
    is_active: bool = Field(default=True)
    
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    results: List["EntranceExamResult"] = Relationship(back_populates="scholarship_slab")


# ======================================================================
# Fee
# ======================================================================

from typing import TYPE_CHECKING, List, Optional
from datetime import datetime, date
from enum import Enum
from decimal import Decimal
from sqlmodel import SQLModel, Field, Relationship, Column
from sqlalchemy import DECIMAL
from app.shared.enums import FeeCategory, PaymentMode, PaymentStatus


if TYPE_CHECKING:
    from app.domains.student.models import Student
    from app.domains.academic.models import Program


class FeeStructure(SQLModel, table=True):
    __tablename__ = "fee_structure"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    program_id: int = Field(foreign_key="program.id", index=True)
    academic_year: str = Field(index=True)
    year: int
    slab: str = Field(default="GENERAL", max_length=20)
    
    tuition_fee: Decimal = Field(default=Decimal("0.00"), sa_column=Column(DECIMAL(10, 2)))
    library_fee: Decimal = Field(default=Decimal("0.00"), sa_column=Column(DECIMAL(10, 2)))
    lab_fee: Decimal = Field(default=Decimal("0.00"), sa_column=Column(DECIMAL(10, 2)))
    uniform_fee: Decimal = Field(default=Decimal("0.00"), sa_column=Column(DECIMAL(10, 2)))
    caution_deposit: Decimal = Field(default=Decimal("0.00"), sa_column=Column(DECIMAL(10, 2)))
    digital_fee: Decimal = Field(default=Decimal("0.00"), sa_column=Column(DECIMAL(10, 2)))
    miscellaneous_fee: Decimal = Field(default=Decimal("0.00"), sa_column=Column(DECIMAL(10, 2)))
    
    total_annual_fee: Decimal = Field(sa_column=Column(DECIMAL(10, 2)))
    number_of_installments: int = Field(default=4)
    installment_amount: Decimal = Field(sa_column=Column(DECIMAL(10, 2)))
    
    category: FeeCategory = Field(default=FeeCategory.GENERAL)
    total_amount: Decimal = Field(sa_column=Column(DECIMAL(10, 2)))
    
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    program: "Program" = Relationship(back_populates="fee_structures")
    components: List["FeeComponent"] = Relationship(back_populates="fee_structure")
    installments: List["FeeInstallment"] = Relationship(back_populates="fee_structure")
    student_fees: List["StudentFee"] = Relationship(back_populates="fee_structure")

class FeeComponent(SQLModel, table=True):
    __tablename__ = "fee_component"
    id: Optional[int] = Field(default=None, primary_key=True)
    fee_structure_id: int = Field(foreign_key="fee_structure.id", index=True)
    fee_head_id: Optional[int] = Field(default=None, foreign_key="fee_head.id", index=True)
    name: str
    amount: Decimal = Field(sa_column=Column(DECIMAL(10, 2)))
    is_refundable: bool = Field(default=False)
    fee_structure: "FeeStructure" = Relationship(back_populates="components")

class FeeInstallment(SQLModel, table=True):
    __tablename__ = "fee_installment"
    id: Optional[int] = Field(default=None, primary_key=True)
    fee_structure_id: int = Field(foreign_key="fee_structure.id", index=True)
    installment_number: int
    amount: Decimal = Field(sa_column=Column(DECIMAL(10, 2)))
    due_date: date
    description: Optional[str] = None
    fee_structure: "FeeStructure" = Relationship(back_populates="installments")

class StudentFee(SQLModel, table=True):
    __tablename__ = "student_fee"
    id: Optional[int] = Field(default=None, primary_key=True)
    student_id: int = Field(foreign_key="student.id", index=True)
    fee_structure_id: int = Field(foreign_key="fee_structure.id", index=True)
    academic_year: str = Field(index=True)
    total_annual_fee: Decimal = Field(sa_column=Column(DECIMAL(10, 2)))
    concession_amount: Decimal = Field(default=Decimal("0.00"), sa_column=Column(DECIMAL(10, 2)))
    net_annual_fee: Decimal = Field(sa_column=Column(DECIMAL(10, 2)))
    number_of_installments: int = Field(default=4)
    installment_amount: Decimal = Field(sa_column=Column(DECIMAL(10, 2)))
    fee_heads: Optional[str] = None
    old_dues: Decimal = Field(default=Decimal("0.00"), sa_column=Column(DECIMAL(10, 2)))
    total_paid: Decimal = Field(default=Decimal("0.00"), sa_column=Column(DECIMAL(10, 2)))
    total_pending: Decimal = Field(sa_column=Column(DECIMAL(10, 2)))
    total_fee: Decimal = Field(sa_column=Column(DECIMAL(10, 2)))
    fine_amount: Decimal = Field(default=Decimal("0.00"), sa_column=Column(DECIMAL(10, 2)))
    paid_amount: Decimal = Field(default=Decimal("0.00"), sa_column=Column(DECIMAL(10, 2)))
    is_blocked: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    student: "Student" = Relationship()
    fee_structure: "FeeStructure" = Relationship(back_populates="student_fees")
    payments: List["FeePayment"] = Relationship(back_populates="student_fee")
    concessions: List["FeeConcession"] = Relationship(back_populates="student_fee")
    fines: List["FeeFine"] = Relationship(back_populates="student_fee")
    student_installments: List["StudentFeeInstallment"] = Relationship(back_populates="student_fee")

class FeePayment(SQLModel, table=True):
    __tablename__ = "fee_payment"
    id: Optional[int] = Field(default=None, primary_key=True)
    student_fee_id: int = Field(foreign_key="student_fee.id", index=True)
    amount: Decimal = Field(sa_column=Column(DECIMAL(10, 2)))
    payment_mode: PaymentMode
    payment_status: PaymentStatus = Field(default=PaymentStatus.PENDING)
    transaction_id: Optional[str] = Field(default=None, index=True)
    gateway_response: Optional[str] = None
    reference_number: Optional[str] = None
    bank_name: Optional[str] = None
    payment_date: Optional[datetime] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    remarks: Optional[str] = None
    student_fee: "StudentFee" = Relationship(back_populates="payments")

class FeeConcession(SQLModel, table=True):
    __tablename__ = "fee_concession"
    id: Optional[int] = Field(default=None, primary_key=True)
    student_fee_id: int = Field(foreign_key="student_fee.id", index=True)
    concession_type: str
    amount: Decimal = Field(sa_column=Column(DECIMAL(10, 2)))
    percentage: Optional[Decimal] = Field(default=None, sa_column=Column(DECIMAL(5, 2)))
    approved_by: Optional[str] = None
    approved_at: Optional[datetime] = None
    remarks: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    student_fee: "StudentFee" = Relationship(back_populates="concessions")

class FeeFine(SQLModel, table=True):
    __tablename__ = "fee_fine"
    id: Optional[int] = Field(default=None, primary_key=True)
    student_fee_id: int = Field(foreign_key="student_fee.id", index=True)
    installment_number: int
    fine_amount: Decimal = Field(sa_column=Column(DECIMAL(10, 2)))
    reason: str
    waived: bool = Field(default=False)
    waived_by: Optional[str] = None
    waived_at: Optional[datetime] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    student_fee: "StudentFee" = Relationship(back_populates="fines")

class StudentFeeInstallment(SQLModel, table=True):
    __tablename__ = "student_fee_installment"
    id: Optional[int] = Field(default=None, primary_key=True)
    student_fee_id: int = Field(foreign_key="student_fee.id", index=True)
    student_id: int = Field(foreign_key="student.id", index=True)
    installment_number: int
    amount: Decimal = Field(sa_column=Column(DECIMAL(10, 2)))
    due_date: date
    individual_fee_heads: Optional[str] = None
    bulk_fee_heads: Optional[str] = None
    supply_exam_fee: Decimal = Field(default=Decimal("0.00"), sa_column=Column(DECIMAL(10, 2)))
    old_dues_included: Decimal = Field(default=Decimal("0.00"), sa_column=Column(DECIMAL(10, 2)))
    total_amount: Decimal = Field(sa_column=Column(DECIMAL(10, 2)))
    paid_amount: Decimal = Field(default=Decimal("0.00"), sa_column=Column(DECIMAL(10, 2)))
    payment_status: str = Field(default="pending")
    payment_date: Optional[date] = None
    fine_amount: Decimal = Field(default=Decimal("0.00"), sa_column=Column(DECIMAL(10, 2)))
    fine_waived: bool = Field(default=False)
    fine_waived_by: Optional[int] = Field(default=None, foreign_key="users.id")
    fine_waived_date: Optional[datetime] = None
    fine_waiver_reason: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    student_fee: "StudentFee" = Relationship(back_populates="student_installments")


# ======================================================================
# Gateway
# ======================================================================

from typing import TYPE_CHECKING, List, Optional
from datetime import datetime
from enum import Enum
from sqlmodel import SQLModel, Field, Relationship, Column
from sqlalchemy import Text, JSON
from app.shared.enums import PaymentMode, PaymentStatus


if TYPE_CHECKING:
    from app.domains.student.models import Student
    from .fee import StudentFee


class PaymentGatewayConfig(SQLModel, table=True):
    """Payment gateway configuration"""
    __tablename__ = "payment_gateway_config"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    gateway_name: str = Field(max_length=100)
    gateway_code: str = Field(unique=True, index=True, max_length=50)
    merchant_id: str
    api_key: str
    api_secret: str
    webhook_secret: Optional[str] = None
    is_active: bool = Field(default=True)
    is_test_mode: bool = Field(default=True)
    is_default: bool = Field(default=False)
    supported_payment_modes: List[str] = Field(default=[], sa_column=Column(JSON))
    callback_url: Optional[str] = None
    webhook_url: Optional[str] = None
    transaction_fee_percentage: float = Field(default=0.0)
    transaction_fee_fixed: float = Field(default=0.0)
    min_transaction_amount: float = Field(default=1.0)
    max_transaction_amount: float = Field(default=100000.0)
    auto_capture: bool = Field(default=True)
    settlement_period_days: int = Field(default=1)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    payments: List["OnlinePayment"] = Relationship(back_populates="gateway_config")


class OnlinePayment(SQLModel, table=True):
    """Online payment transactions"""
    __tablename__ = "online_payment"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    
    # Idempotency protection for webhooks
    idempotency_key: str = Field(unique=True, index=True)  # Prevents duplicate webhook processing
    
    student_id: int = Field(foreign_key="student.id", index=True)
    student_fee_id: int = Field(foreign_key="student_fee.id", index=True)
    payment_gateway_config_id: int = Field(foreign_key="payment_gateway_config.id")
    amount: float = Field(ge=0)
    payment_mode: Optional[PaymentMode] = None
    currency: str = Field(default="INR")
    gateway_transaction_id: Optional[str] = Field(default=None, index=True)
    gateway_order_id: Optional[str] = Field(default=None, index=True)
    gateway_payment_id: Optional[str] = None
    gateway_signature: Optional[str] = None
    gateway_response: Optional[dict] = Field(default=None, sa_column=Column(JSON))
    gateway_error_code: Optional[str] = None
    gateway_error_message: Optional[str] = None
    payment_status: PaymentStatus = Field(default=PaymentStatus.INITIATED, index=True)
    initiated_at: datetime = Field(default_factory=datetime.utcnow)
    completed_at: Optional[datetime] = None
    failed_at: Optional[datetime] = None
    refunded_at: Optional[datetime] = None
    customer_name: str
    customer_email: str
    customer_phone: str
    billing_address: Optional[str] = Field(default=None, sa_column=Column(Text))
    receipt_number: Optional[str] = None
    receipt_url: Optional[str] = None
    receipt_generated: bool = Field(default=False)
    refund_amount: Optional[float] = None
    refund_reason: Optional[str] = Field(default=None, sa_column=Column(Text))
    refund_transaction_id: Optional[str] = None
    transaction_fee: float = Field(default=0.0)
    net_amount: float = Field(default=0.0)
    meta_data: Optional[dict] = Field(default=None, sa_column=Column(JSON))
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    student: "Student" = Relationship()
    student_fee: "StudentFee" = Relationship()
    gateway_config: "PaymentGatewayConfig" = Relationship(back_populates="payments")
    receipt: Optional["PaymentReceipt"] = Relationship(back_populates="payment")


class PaymentReceipt(SQLModel, table=True):
    """Payment receipts"""
    __tablename__ = "payment_receipt"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    online_payment_id: int = Field(foreign_key="online_payment.id", unique=True, index=True)
    receipt_number: str = Field(unique=True, index=True)
    receipt_date: datetime = Field(default_factory=datetime.utcnow)
    amount: float
    transaction_fee: float = Field(default=0.0)
    net_amount: float
    pdf_url: Optional[str] = None
    pdf_generated: bool = Field(default=False)
    pdf_generated_at: Optional[datetime] = None
    email_sent: bool = Field(default=False)
    email_sent_at: Optional[datetime] = None
    email_sent_to: Optional[str] = None
    sms_sent: bool = Field(default=False)
    sms_sent_at: Optional[datetime] = None
    sms_sent_to: Optional[str] = None
    download_count: int = Field(default=0)
    last_downloaded_at: Optional[datetime] = None
    generated_at: datetime = Field(default_factory=datetime.utcnow)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    payment: "OnlinePayment" = Relationship(back_populates="receipt")
