from typing import TYPE_CHECKING, List, Optional
from datetime import datetime
from enum import Enum
from sqlmodel import SQLModel, Field, Relationship, JSON, Column
from app.shared.enums import CircularTarget, NotificationChannel, NotificationType


if TYPE_CHECKING:
    from app.models.user import User


class Circular(SQLModel, table=True):
    """Internal institutional circulars/notices - Communication Domain"""
    __tablename__ = "circular"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(index=True)
    content: str
    attachment_url: Optional[str] = None
    
    target_type: CircularTarget = Field(default=CircularTarget.ALL)
    # JSON list of role IDs or department IDs if target_type is SPECIFIC_*
    target_ids: Optional[List[int]] = Field(default=None, sa_column=Column(JSON))
    
    is_active: bool = Field(default=True)
    published_at: datetime = Field(default_factory=datetime.utcnow)
    expires_at: Optional[datetime] = None
    
    author_id: int = Field(foreign_key="user.id")
    
    # Relationships
    author: "User" = Relationship()


class Notification(SQLModel, table=True):
    """In-app notifications for users - Communication Domain"""
    __tablename__ = "notification"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id", index=True)
    
    title: str
    message: str
    type: NotificationType = Field(default=NotificationType.INFO)
    link: Optional[str] = None  # UI link to redirect
    
    is_read: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    read_at: Optional[datetime] = None
    
    # Relationships
    user: "User" = Relationship()


class NotificationLog(SQLModel, table=True):
    """external communication logs - Communication Domain"""
    __tablename__ = "notification_log"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: Optional[int] = Field(default=None, foreign_key="user.id", index=True)
    recipient_identifier: str  # Phone number or email
    
    channel: NotificationChannel
    title: Optional[str] = None
    message: str
    
    status: str = Field(default="SENT")  # SENT, DELIVERED, FAILED
    provider_response: Optional[str] = None
    
    created_at: datetime = Field(default_factory=datetime.utcnow)
