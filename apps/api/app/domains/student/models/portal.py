"""
Student Portal Models - Portal Access, Activity & Notifications
"""
from typing import TYPE_CHECKING, List, Optional
from datetime import datetime
from enum import Enum
from sqlmodel import SQLModel, Field, Relationship, Column
from sqlalchemy import Text, JSON

if TYPE_CHECKING:
    from .student import Student
    from app.models.user import User


class ActivityType(str, Enum):
    """Student activity types"""
    LOGIN = "LOGIN"
    LOGOUT = "LOGOUT"
    PROFILE_UPDATE = "PROFILE_UPDATE"
    DOCUMENT_UPLOAD = "DOCUMENT_UPLOAD"
    FEE_PAYMENT = "FEE_PAYMENT"
    EXAM_REGISTRATION = "EXAM_REGISTRATION"
    HALL_TICKET_DOWNLOAD = "HALL_TICKET_DOWNLOAD"
    RESULT_VIEW = "RESULT_VIEW"


class NotificationPriority(str, Enum):
    """Notification priority levels"""
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    URGENT = "URGENT"


class StudentPortalAccess(SQLModel, table=True):
    """Student portal access and authentication"""
    __tablename__ = "student_portal_access"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    
    # Links
    student_id: int = Field(foreign_key="student.id", unique=True, index=True)
    user_id: Optional[int] = Field(default=None, foreign_key="user.id")
    
    # Access status
    is_active: bool = Field(default=True)
    activation_date: Optional[datetime] = None
    deactivation_date: Optional[datetime] = None
    deactivation_reason: Optional[str] = Field(default=None, sa_column=Column(Text))
    
    # Login tracking
    last_login: Optional[datetime] = None
    last_login_ip: Optional[str] = None
    login_count: int = Field(default=0)
    failed_login_attempts: int = Field(default=0)
    last_failed_login: Optional[datetime] = None
    
    # Security
    password_reset_required: bool = Field(default=False)
    password_reset_token: Optional[str] = None
    password_reset_expires: Optional[datetime] = None
    two_factor_enabled: bool = Field(default=False)
    two_factor_secret: Optional[str] = None
    
    # Session management
    current_session_token: Optional[str] = None
    session_expires_at: Optional[datetime] = None
    
    # Preferences
    email_notifications: bool = Field(default=True)
    sms_notifications: bool = Field(default=False)
    language_preference: str = Field(default="en")
    theme_preference: str = Field(default="light")
    
    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    student: "Student" = Relationship()
    activities: List["StudentActivity"] = Relationship(
        back_populates="student_portal",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )


class StudentActivity(SQLModel, table=True):
    """Student activity log"""
    __tablename__ = "student_activity"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    
    # Links
    student_id: int = Field(foreign_key="student.id", index=True)
    student_portal_access_id: int = Field(foreign_key="student_portal_access.id", index=True)
    
    # Activity details
    activity_type: ActivityType
    activity_description: str
    meta_data: Optional[str] = Field(default=None, sa_column=Column(JSON))
    
    # Request details
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    device_type: Optional[str] = None  # mobile, desktop, tablet
    
    # Status
    is_successful: bool = Field(default=True)
    error_message: Optional[str] = None
    
    # Timestamp
    created_at: datetime = Field(default_factory=datetime.utcnow, index=True)
    
    # Relationships
    student: "Student" = Relationship()
    student_portal: "StudentPortalAccess" = Relationship(back_populates="activities")


class StudentNotification(SQLModel, table=True):
    """Student notifications"""
    __tablename__ = "student_notification"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    
    # Links
    student_id: int = Field(foreign_key="student.id", index=True)
    
    # Notification details
    notification_type: str  # FEE_DUE, EXAM_SCHEDULE, RESULT_PUBLISHED, etc.
    title: str = Field(max_length=200)
    message: str = Field(sa_column=Column(Text))
    link: Optional[str] = None  # Link to relevant page
    
    # Priority
    priority: NotificationPriority = Field(default=NotificationPriority.MEDIUM)
    
    # Read status
    is_read: bool = Field(default=False)
    read_at: Optional[datetime] = None
    
    # Delivery
    sent_via_email: bool = Field(default=False)
    email_sent_at: Optional[datetime] = None
    sent_via_sms: bool = Field(default=False)
    sms_sent_at: Optional[datetime] = None
    
    # Action required
    requires_action: bool = Field(default=False)
    action_completed: bool = Field(default=False)
    action_completed_at: Optional[datetime] = None
    
    # Expiry
    expires_at: Optional[datetime] = None
    is_expired: bool = Field(default=False)
    
    # Metadata
    meta_data: Optional[str] = Field(default=None, sa_column=Column(JSON))
    
    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow, index=True)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    student: "Student" = Relationship()
