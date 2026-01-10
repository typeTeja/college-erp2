"""
Audit Log Schemas
"""
from typing import Optional, Any
from datetime import datetime
from pydantic import BaseModel

class AuditLogBase(BaseModel):
    table_name: str
    record_id: int
    action: str
    user_id: Optional[int] = None
    user_email: Optional[str] = None
    old_values: Optional[Any] = None
    new_values: Optional[Any] = None
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    description: Optional[str] = None

class AuditLogCreate(AuditLogBase):
    pass

class AuditLogRead(AuditLogBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True
