from typing import TYPE_CHECKING, List, Optional
from datetime import datetime
from enum import Enum
from sqlmodel import SQLModel, Field, Relationship, Column
from sqlalchemy import Text, JSON
from app.shared.enums import PaymentMode, PaymentStatus


if TYPE_CHECKING:
    from app.domains.student.models.student import Student
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
