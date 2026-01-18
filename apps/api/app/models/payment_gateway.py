"""
Payment Gateway Models - Online Payment Integration

Manages payment gateway configuration, online payments, and receipts
"""
from typing import TYPE_CHECKING, List, Optional
from datetime import datetime
from enum import Enum
from sqlmodel import SQLModel, Field, Relationship, Column
from sqlalchemy import Text, JSON

if TYPE_CHECKING:
    from ..student import Student
    from ..fee import StudentFee


class PaymentStatus(str, Enum):
    """Payment status"""
    INITIATED = "INITIATED"
    PENDING = "PENDING"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"
    REFUNDED = "REFUNDED"


class PaymentMode(str, Enum):
    """Payment modes"""
    UPI = "UPI"
    CARD = "CARD"
    NET_BANKING = "NET_BANKING"
    WALLET = "WALLET"
    EMI = "EMI"


class PaymentGatewayConfig(SQLModel, table=True):
    """Payment gateway configuration"""
    __tablename__ = "payment_gateway_config"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    
    # Gateway details
    gateway_name: str = Field(max_length=100)  # "Razorpay", "Easebuzz"
    gateway_code: str = Field(unique=True, index=True, max_length=50)
    
    # Credentials
    merchant_id: str
    api_key: str
    api_secret: str  # Should be encrypted in production
    webhook_secret: Optional[str] = None
    
    # Configuration
    is_active: bool = Field(default=True)
    is_test_mode: bool = Field(default=True)
    is_default: bool = Field(default=False)
    
    # Supported features
    supported_payment_modes: str = Field(sa_column=Column(JSON))
    # Example: ["UPI", "CARD", "NET_BANKING", "WALLET"]
    
    # URLs
    callback_url: Optional[str] = None
    webhook_url: Optional[str] = None
    
    # Fees
    transaction_fee_percentage: float = Field(default=0.0, ge=0, le=100)
    transaction_fee_fixed: float = Field(default=0.0, ge=0)
    
    # Limits
    min_transaction_amount: float = Field(default=1.0)
    max_transaction_amount: float = Field(default=100000.0)
    
    # Settings
    auto_capture: bool = Field(default=True)
    settlement_period_days: int = Field(default=1)
    
    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    payments: List["OnlinePayment"] = Relationship(
        back_populates="gateway_config",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )


class OnlinePayment(SQLModel, table=True):
    """Online payment transactions"""
    __tablename__ = "online_payment"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    
    # Links
    student_id: int = Field(foreign_key="student.id", index=True)
    student_fee_id: int = Field(foreign_key="student_fee.id", index=True)
    payment_gateway_config_id: int = Field(foreign_key="payment_gateway_config.id")
    
    # Payment details
    amount: float = Field(ge=0)
    payment_mode: Optional[PaymentMode] = None
    currency: str = Field(default="INR")
    
    # Gateway transaction details
    gateway_transaction_id: Optional[str] = Field(default=None, index=True)
    gateway_order_id: Optional[str] = Field(default=None, index=True)
    gateway_payment_id: Optional[str] = None
    gateway_signature: Optional[str] = None
    
    # Gateway response
    gateway_response: Optional[str] = Field(default=None, sa_column=Column(JSON))
    gateway_error_code: Optional[str] = None
    gateway_error_message: Optional[str] = None
    
    # Status
    payment_status: PaymentStatus = Field(default=PaymentStatus.INITIATED, index=True)
    
    # Timestamps
    initiated_at: datetime = Field(default_factory=datetime.utcnow)
    completed_at: Optional[datetime] = None
    failed_at: Optional[datetime] = None
    refunded_at: Optional[datetime] = None
    
    # Customer details
    customer_name: str
    customer_email: str
    customer_phone: str
    
    # Billing address
    billing_address: Optional[str] = Field(default=None, sa_column=Column(Text))
    
    # Receipt
    receipt_number: Optional[str] = None
    receipt_url: Optional[str] = None
    receipt_generated: bool = Field(default=False)
    
    # Refund details
    refund_amount: Optional[float] = None
    refund_reason: Optional[str] = Field(default=None, sa_column=Column(Text))
    refund_transaction_id: Optional[str] = None
    
    # Fees
    transaction_fee: float = Field(default=0.0)
    net_amount: float = Field(default=0.0)  # amount - transaction_fee
    
    # Metadata
    metadata: Optional[str] = Field(default=None, sa_column=Column(JSON))
    
    # IP tracking
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    
    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    student: "Student" = Relationship()
    student_fee: "StudentFee" = Relationship()
    gateway_config: "PaymentGatewayConfig" = Relationship(back_populates="payments")
    receipt: Optional["PaymentReceipt"] = Relationship(
        back_populates="payment",
        sa_relationship_kwargs={"uselist": False}
    )


class PaymentReceipt(SQLModel, table=True):
    """Payment receipts"""
    __tablename__ = "payment_receipt"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    
    # Links
    online_payment_id: int = Field(foreign_key="online_payment.id", unique=True, index=True)
    
    # Receipt details
    receipt_number: str = Field(unique=True, index=True)
    receipt_date: datetime = Field(default_factory=datetime.utcnow)
    
    # Amount details
    amount: float
    transaction_fee: float = Field(default=0.0)
    net_amount: float
    
    # PDF
    pdf_url: Optional[str] = None
    pdf_generated: bool = Field(default=False)
    pdf_generated_at: Optional[datetime] = None
    
    # Email
    email_sent: bool = Field(default=False)
    email_sent_at: Optional[datetime] = None
    email_sent_to: Optional[str] = None
    
    # SMS
    sms_sent: bool = Field(default=False)
    sms_sent_at: Optional[datetime] = None
    sms_sent_to: Optional[str] = None
    
    # Download tracking
    download_count: int = Field(default=0)
    last_downloaded_at: Optional[datetime] = None
    
    # Timestamps
    generated_at: datetime = Field(default_factory=datetime.utcnow)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    payment: "OnlinePayment" = Relationship(back_populates="receipt")
