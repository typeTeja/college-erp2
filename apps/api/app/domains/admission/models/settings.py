from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field

class AdmissionSettings(SQLModel, table=True):
    """Global admission settings for configuring application workflow"""
    __tablename__ = "admission_settings"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    
    # Application Fee Configuration
    application_fee_enabled: bool = Field(default=True)
    application_fee_amount: float = Field(default=500.0)
    
    # Payment Method Configuration
    online_payment_enabled: bool = Field(default=True)
    offline_payment_enabled: bool = Field(default=True)
    
    # Payment Gateway Settings
    payment_gateway: str = Field(default="easebuzz")  # easebuzz, razorpay, etc.
    payment_gateway_key: Optional[str] = None  # API key for payment gateway
    payment_gateway_secret: Optional[str] = None  # API secret for payment gateway
    
    # Email/SMS Configuration
    send_credentials_email: bool = Field(default=True)
    send_credentials_sms: bool = Field(default=False)  # Default false until SMS gateway configured
    sms_gateway: Optional[str] = None  # twilio, aws_sns, etc.
    sms_gateway_key: Optional[str] = None
    sms_gateway_secret: Optional[str] = None
    
    # Auto-account Creation
    auto_create_student_account: bool = Field(default=True)
    
    # Portal Configuration
    portal_base_url: str = Field(default="https://portal.college.edu")
    
    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    updated_by: Optional[int] = Field(default=None, foreign_key="users.id")
