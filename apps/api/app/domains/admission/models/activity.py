from typing import TYPE_CHECKING, Optional
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship
from app.shared.enums import ActivityType

if TYPE_CHECKING:
    from .application import Application
    from app.domains.auth.models import AuthUser

class ApplicationActivityLog(SQLModel, table=True):
    """Activity log for tracking all changes to an application"""
    id: Optional[int] = Field(default=None, primary_key=True)
    application_id: int = Field(foreign_key="application.id", index=True)
    activity_type: ActivityType
    description: str
    extra_data: Optional[str] = None  # JSON string for additional data (renamed from metadata to avoid SQLAlchemy conflict)
    performed_by: Optional[int] = Field(default=None, foreign_key="users.id")
    ip_address: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    application: "Application" = Relationship(back_populates="activity_logs")
    performer: Optional["AuthUser"] = Relationship(sa_relationship_kwargs={"foreign_keys": "ApplicationActivityLog.performed_by"})
