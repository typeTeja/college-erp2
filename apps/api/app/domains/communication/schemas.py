from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel
from .models import CircularTarget, NotificationType, NotificationChannel
from app.shared.enums import CircularTarget, NotificationChannel, NotificationType


# Circular Schemas
class CircularBase(BaseModel):
    title: str
    content: str
    attachment_url: Optional[str] = None
    target_type: CircularTarget = CircularTarget.ALL
    target_ids: Optional[List[int]] = None
    expires_at: Optional[datetime] = None

class CircularCreate(CircularBase):
    pass

class CircularRead(CircularBase):
    id: int
    published_at: datetime
    author_id: int
    is_active: bool

    class Config:
        from_attributes = True

# Notification Schemas
class NotificationBase(BaseModel):
    title: str
    message: str
    type: NotificationType = NotificationType.INFO
    link: Optional[str] = None

class NotificationRead(NotificationBase):
    id: int
    user_id: int
    is_read: bool
    created_at: datetime
    read_at: Optional[datetime] = None

    class Config:
        from_attributes = True

# Notification Log Schemas
class NotificationLogRead(BaseModel):
    id: int
    user_id: Optional[int] = None
    recipient_identifier: str
    channel: NotificationChannel
    message: str
    status: str
    created_at: datetime

    class Config:
        from_attributes = True
