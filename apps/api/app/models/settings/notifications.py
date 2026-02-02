from typing import Optional, Any
from datetime import datetime
from sqlmodel import SQLModel, Field, Column, JSON
from sqlalchemy import Text

class EmailTemplate(SQLModel, table=True):
    """Email Templates for various notifications"""
    __tablename__ = "email_template"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(unique=True, index=True)  # e.g., "welcome_email", "fee_reminder"
    subject: str
    body: str = Field(sa_column=Column(Text))
    
    template_type: str = Field(default="TRANSACTIONAL")  # TRANSACTIONAL, PROMOTIONAL
    
    variables: Any = Field(default=[], sa_column=Column(JSON))  # List of available variables
    
    is_active: bool = Field(default=True)
    
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class SMSTemplate(SQLModel, table=True):
    """SMS Templates for various notifications"""
    __tablename__ = "sms_template"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(unique=True, index=True)
    content: str = Field(sa_column=Column(Text))
    
    dlt_template_id: Optional[str] = None  # DLT registered template ID (India specific)
    sender_id: Optional[str] = None  # e.g., "RCHMCT"
    
    template_type: str = Field(default="TRANSACTIONAL")
    
    variables: Any = Field(default=[], sa_column=Column(JSON))
    
    is_active: bool = Field(default=True)
    
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
