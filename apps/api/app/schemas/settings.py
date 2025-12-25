from typing import List, Optional, Any, Dict
from pydantic import BaseModel
from datetime import datetime
from app.models.settings import SettingGroup, AuditLogAction

class SystemSettingBase(BaseModel):
    key: str
    value: Any
    group: SettingGroup
    is_secret: bool = False
    description: Optional[str] = None

class SystemSettingCreate(SystemSettingBase):
    pass

class SystemSettingRead(SystemSettingBase):
    id: int
    updated_at: datetime
    updated_by: Optional[int]

class SystemSettingUpdate(BaseModel):
    value: Optional[Any] = None
    description: Optional[str] = None

class AuditLogRead(BaseModel):
    id: int
    timestamp: datetime
    user_id: Optional[int]
    action: AuditLogAction
    module: str
    description: str
    target_id: Optional[str] = None
    from_value: Optional[Any] = None
    to_value: Optional[Any] = None
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None

class PasswordChange(BaseModel):
    current_password: str
    new_password: str

class ProfileUpdate(BaseModel):
    full_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    preferences: Optional[dict] = None

class BulkSettingsUpdate(BaseModel):
    settings: Dict[str, Any]  # Key-Value pairs
