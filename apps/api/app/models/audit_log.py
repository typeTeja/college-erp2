"""
Audit Log Model - Track all changes to academic entities
"""
from typing import Optional, Any
from datetime import datetime
from sqlmodel import SQLModel, Field, Column
from sqlalchemy import JSON, Text

class AuditLog(SQLModel, table=True):
    """
    Audit log for tracking changes to academic structure
    Tracks CREATE, UPDATE, DELETE operations with full context
    """
    __tablename__ = "academic_audit_log"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    
    # What was changed
    table_name: str = Field(max_length=100, index=True)  # "section", "batch_semester", etc.
    record_id: int = Field(index=True)  # ID of the record that was changed
    action: str = Field(max_length=20, index=True)  # "CREATE", "UPDATE", "DELETE"
    
    # Who made the change
    user_id: Optional[int] = Field(default=None, foreign_key="user.id", index=True)
    user_email: Optional[str] = Field(default=None, max_length=255)  # Denormalized for quick access
    
    # Change details
    old_values: Optional[Any] = Field(default=None, sa_column=Column(JSON))  # Previous state (for UPDATE/DELETE)
    new_values: Optional[Any] = Field(default=None, sa_column=Column(JSON))  # New state (for CREATE/UPDATE)
    
    # Context
    ip_address: Optional[str] = Field(default=None, max_length=45)  # IPv4 or IPv6
    user_agent: Optional[str] = Field(default=None, sa_column=Column(Text))  # Browser/client info
    description: Optional[str] = Field(default=None, sa_column=Column(Text))  # Human-readable description
    
    # Timestamp
    created_at: datetime = Field(default_factory=datetime.utcnow, index=True)
    
    class Config:
        arbitrary_types_allowed = True
