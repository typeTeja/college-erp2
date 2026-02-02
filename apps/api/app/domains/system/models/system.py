from typing import Optional, Any
from datetime import datetime
from sqlmodel import SQLModel, Field, Column, JSON
from enum import Enum

class SettingGroup(str, Enum):
    PERSONAL = "PERSONAL"
    INSTITUTE = "INSTITUTE"
    ACADEMIC = "ACADEMIC"
    INTEGRATION = "INTEGRATION"
    SECURITY = "SECURITY"

class SystemSetting(SQLModel, table=True):
    """General key-value store for all ERP configurations - System Domain"""
    __tablename__ = "system_setting"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    key: str = Field(index=True, unique=True, description="Unique key like 'institute.name'")
    value: Any = Field(sa_column=Column(JSON))
    group: SettingGroup = Field(index=True)
    is_secret: bool = Field(default=False, description="If true, encrypt at rest and mask in UI")
    description: Optional[str] = None
    
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    updated_by: Optional[int] = Field(default=None, foreign_key="user.id")

class AuditLogAction(str, Enum):
    LOGIN = "LOGIN"
    CREATE = "CREATE"
    UPDATE = "UPDATE"
    DELETE = "DELETE"
    PERMISSION_CHANGE = "PERMISSION_CHANGE"
    SETTING_CHANGE = "SETTING_CHANGE"
    SECURITY_ALERT = "SECURITY_ALERT"

class AuditLog(SQLModel, table=True):
    """System-wide audit trail - System Domain"""
    __tablename__ = "audit_log"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    timestamp: datetime = Field(default_factory=datetime.utcnow, index=True)
    
    user_id: Optional[int] = Field(default=None, foreign_key="user.id", index=True)
    action: AuditLogAction = Field(index=True)
    module: str = Field(index=True)  # e.g., 'SETTINGS', 'ADMISSIONS', 'FEES'
    
    description: str
    target_id: Optional[str] = None  # ID of the record changed
    
    from_value: Optional[Any] = Field(default=None, sa_column=Column(JSON))
    to_value: Optional[Any] = Field(default=None, sa_column=Column(JSON))
    
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None

class InstituteInfo(SQLModel, table=True):
    """Stores basic institute identity information - System Domain"""
    __tablename__ = "institute_info"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(..., description="Institute full name")
    short_code: Optional[str] = Field(None, description="Short code or abbreviation")
    address: Optional[str] = Field(None)
    contact_email: Optional[str] = Field(None)
    contact_phone: Optional[str] = Field(None)
    logo_url: Optional[str] = Field(None, description="URL to stored logo image")
