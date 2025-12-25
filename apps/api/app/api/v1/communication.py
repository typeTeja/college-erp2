from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select, func, and_, or_
from app.api import deps
from app.models.communication import Circular, Notification, NotificationLog, CircularTarget
from app.models.user import User
from app.schemas.communication import CircularCreate, CircularRead, NotificationRead, NotificationLogRead
from datetime import datetime

router = APIRouter()

# Circulars
@router.post("/circulars", response_model=CircularRead)
def create_circular(
    *,
    session: Session = Depends(deps.get_session),
    circular_in: CircularCreate,
    current_user: User = Depends(deps.get_current_user)
):
    """Create a new institutional circular (Admin/HOD)"""
    # In a real app, we'd check if user has permission to create circulars
    circular = Circular.model_validate(circular_in)
    circular.author_id = current_user.id
    session.add(circular)
    session.commit()
    session.refresh(circular)
    return circular

@router.get("/circulars", response_model=List[CircularRead])
def get_circulars(
    *,
    session: Session = Depends(deps.get_session),
    current_user: User = Depends(deps.get_current_user),
    offset: int = 0,
    limit: int = 20
):
    """Get circulars relevant to the current user"""
    # Logic to filter based on target_type and user role/department
    # For now, we fetch all active circulars that haven't expired
    now = datetime.utcnow()
    statement = select(Circular).where(Circular.is_active == True)
    statement = statement.where(or_(Circular.expires_at == None, Circular.expires_at > now))
    
    # Simple targeting logic (can be expanded)
    # If user is STUDENT, show ALL or STUDENTS
    # If user is STAFF, show ALL or STAFF
    # Real logic would check current_user.role and specific target_ids
    
    circulars = session.exec(statement.order_by(Circular.published_at.desc()).offset(offset).limit(limit)).all()
    return circulars

# Notifications
@router.get("/notifications", response_model=List[NotificationRead])
def get_notifications(
    *,
    session: Session = Depends(deps.get_session),
    current_user: User = Depends(deps.get_current_user),
    unread_only: bool = False,
    limit: int = 20
):
    """Fetch in-app notifications for the current user"""
    statement = select(Notification).where(Notification.user_id == current_user.id)
    if unread_only:
        statement = statement.where(Notification.is_read == False)
    
    notifications = session.exec(statement.order_by(Notification.created_at.desc()).limit(limit)).all()
    return notifications

@router.patch("/notifications/{notification_id}/read", response_model=NotificationRead)
def mark_notification_as_read(
    notification_id: int,
    session: Session = Depends(deps.get_session),
    current_user: User = Depends(deps.get_current_user)
):
    """Mark a notification as read"""
    notification = session.get(Notification, notification_id)
    if not notification or notification.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Notification not found")
    
    notification.is_read = True
    notification.read_at = datetime.utcnow()
    session.add(notification)
    session.commit()
    session.refresh(notification)
    return notification

@router.patch("/notifications/read-all")
def mark_all_notifications_as_read(
    session: Session = Depends(deps.get_session),
    current_user: User = Depends(deps.get_current_user)
):
    """Mark all unread notifications for current user as read"""
    statement = select(Notification).where(
        and_(Notification.user_id == current_user.id, Notification.is_read == False)
    )
    unread = session.exec(statement).all()
    for n in unread:
        n.is_read = True
        n.read_at = datetime.utcnow()
        session.add(n)
    session.commit()
    return {"status": "success", "count": len(unread)}
