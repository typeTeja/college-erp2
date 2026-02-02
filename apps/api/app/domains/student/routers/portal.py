from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlmodel import Session, select
from pydantic import BaseModel

from app.api.deps import get_session, get_current_user
from app.models.user import User
from ..models.portal import (
    StudentPortalAccess, StudentActivity, StudentNotification,
    ActivityType, NotificationPriority
)
from ..services.portal import portal_service

router = APIRouter()

# Schemas
class LoginRequest(BaseModel):
    admission_number: str
    password: str

class NotificationCreate(BaseModel):
    student_id: int
    notification_type: str
    title: str
    message: str
    priority: str = "MEDIUM"
    link: Optional[str] = None
    requires_action: bool = False
    expires_in_days: Optional[int] = None

# Endpoints
@router.post("/activate/{student_id}")
def activate_portal(
    *,
    session: Session = Depends(get_session),
    student_id: int
):
    """Activate portal access for student"""
    return portal_service.activate_portal_access(session, student_id)

@router.get("/dashboard/{student_id}")
def get_dashboard(
    *,
    session: Session = Depends(get_session),
    student_id: int
):
    """Get student dashboard data"""
    return portal_service.get_dashboard_data(session, student_id)

@router.get("/activity/{student_id}")
def get_student_activity(
    *,
    session: Session = Depends(get_session),
    student_id: int,
    limit: int = 50
):
    """Get student activity log"""
    stmt = select(StudentActivity).where(
        StudentActivity.student_id == student_id
    ).order_by(StudentActivity.created_at.desc()).limit(limit)
    return session.exec(stmt).all()

@router.post("/activity/log")
def log_activity(
    *,
    session: Session = Depends(get_session),
    request: Request,
    student_id: int,
    activity_type: str,
    description: str
):
    """Log student activity"""
    ip_address = request.client.host if request.client else None
    user_agent = request.headers.get("user-agent")
    return portal_service.log_activity(
        session,
        student_id,
        ActivityType(activity_type),
        description,
        ip_address=ip_address,
        user_agent=user_agent
    )

@router.post("/notifications")
def create_notification(
    *,
    session: Session = Depends(get_session),
    notification_data: NotificationCreate
):
    """Create a notification"""
    return portal_service.create_notification(
        session,
        notification_data.student_id,
        notification_data.notification_type,
        notification_data.title,
        notification_data.message,
        NotificationPriority(notification_data.priority),
        notification_data.link,
        notification_data.requires_action,
        notification_data.expires_in_days
    )

@router.get("/notifications/{student_id}")
def get_notifications(
    *,
    session: Session = Depends(get_session),
    student_id: int,
    is_read: Optional[bool] = None,
    limit: int = 50
):
    """Get student notifications"""
    stmt = select(StudentNotification).where(StudentNotification.student_id == student_id)
    if is_read is not None:
        stmt = stmt.where(StudentNotification.is_read == is_read)
    stmt = stmt.order_by(StudentNotification.created_at.desc()).limit(limit)
    return session.exec(stmt).all()

@router.post("/notifications/{notification_id}/read")
def mark_notification_read(
    *,
    session: Session = Depends(get_session),
    notification_id: int
):
    """Mark notification as read"""
    return portal_service.mark_notification_read(session, notification_id)
