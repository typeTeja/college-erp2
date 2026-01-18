"""
Student Portal API Endpoints

Provides student portal functionality
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlmodel import Session, select
from pydantic import BaseModel

from app.api.deps import get_session, get_current_user
from app.models.user import User
from app.models.student_portal import (
    StudentPortalAccess, StudentActivity, Notification,
    ActivityType, NotificationPriority
)
from app.services.student_portal_service import StudentPortalService

router = APIRouter(prefix="/portal", tags=["Student Portal"])


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


# ============================================================================
# Authentication Endpoints
# ============================================================================

@router.post("/activate/{student_id}")
def activate_portal(
    *,
    session: Session = Depends(get_session),
    student_id: int
):
    """Activate portal access for student"""
    return StudentPortalService.activate_portal_access(session, student_id)


@router.post("/login")
def student_login(
    *,
    session: Session = Depends(get_session),
    request: Request,
    login_data: LoginRequest
):
    """Student portal login"""
    # This is a simplified version - should integrate with actual auth
    # For now, just record the login attempt
    
    # Get IP address
    ip_address = request.client.host if request.client else None
    user_agent = request.headers.get("user-agent")
    
    # In production, verify credentials here
    # For now, assume successful login
    
    return {
        "message": "Login successful",
        "admission_number": login_data.admission_number
    }


# ============================================================================
# Dashboard Endpoints
# ============================================================================

@router.get("/dashboard/{student_id}")
def get_dashboard(
    *,
    session: Session = Depends(get_session),
    student_id: int
):
    """Get student dashboard data"""
    return StudentPortalService.get_dashboard_data(session, student_id)


# ============================================================================
# Activity Endpoints
# ============================================================================

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
    
    return StudentPortalService.log_activity(
        session,
        student_id,
        ActivityType(activity_type),
        description,
        ip_address=ip_address,
        user_agent=user_agent
    )


# ============================================================================
# Notification Endpoints
# ============================================================================

@router.post("/notifications")
def create_notification(
    *,
    session: Session = Depends(get_session),
    notification_data: NotificationCreate
):
    """Create a notification"""
    return StudentPortalService.create_notification(
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
    stmt = select(Notification).where(Notification.student_id == student_id)
    
    if is_read is not None:
        stmt = stmt.where(Notification.is_read == is_read)
    
    stmt = stmt.order_by(Notification.created_at.desc()).limit(limit)
    return session.exec(stmt).all()


@router.post("/notifications/{notification_id}/read")
def mark_notification_read(
    *,
    session: Session = Depends(get_session),
    notification_id: int
):
    """Mark notification as read"""
    return StudentPortalService.mark_notification_read(session, notification_id)


@router.get("/notifications/{student_id}/unread-count")
def get_unread_count(
    *,
    session: Session = Depends(get_session),
    student_id: int
):
    """Get unread notification count"""
    stmt = select(Notification).where(
        Notification.student_id == student_id,
        Notification.is_read == False
    )
    count = len(session.exec(stmt).all())
    return {"unread_count": count}


# ============================================================================
# Profile Endpoints
# ============================================================================

@router.get("/profile/{student_id}")
def get_profile(
    *,
    session: Session = Depends(get_session),
    student_id: int
):
    """Get student profile"""
    from app.models.student import Student
    student = session.get(Student, student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student


@router.get("/preferences/{student_id}")
def get_preferences(
    *,
    session: Session = Depends(get_session),
    student_id: int
):
    """Get student portal preferences"""
    stmt = select(StudentPortalAccess).where(
        StudentPortalAccess.student_id == student_id
    )
    access = session.exec(stmt).first()
    
    if not access:
        raise HTTPException(status_code=404, detail="Portal access not found")
    
    return {
        "email_notifications": access.email_notifications,
        "sms_notifications": access.sms_notifications,
        "language_preference": access.language_preference,
        "theme_preference": access.theme_preference
    }
