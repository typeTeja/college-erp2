"""
Student Portal Service Layer

Handles business logic for student portal including:
- Authentication and login
- Activity tracking
- Notification management
- Dashboard data
"""
from typing import List, Optional, Dict
from datetime import datetime, timedelta
from sqlmodel import Session, select
from fastapi import HTTPException
import secrets

from app.models.student_portal import (
    StudentPortalAccess, StudentActivity, Notification,
    ActivityType, NotificationPriority
)
from app.models.student import Student
from app.models.fee import StudentFee


class StudentPortalService:
    """Service for student portal operations"""
    
    @staticmethod
    def activate_portal_access(
        session: Session,
        student_id: int
    ) -> StudentPortalAccess:
        """Activate portal access for a student"""
        student = session.get(Student, student_id)
        if not student:
            raise HTTPException(status_code=404, detail="Student not found")
        
        # Check if access already exists
        stmt = select(StudentPortalAccess).where(
            StudentPortalAccess.student_id == student_id
        )
        access = session.exec(stmt).first()
        
        if access:
            access.is_active = True
            access.activation_date = datetime.utcnow()
        else:
            access = StudentPortalAccess(
                student_id=student_id,
                activation_date=datetime.utcnow()
            )
            session.add(access)
        
        session.commit()
        session.refresh(access)
        return access
    
    @staticmethod
    def record_login(
        session: Session,
        student_id: int,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
        is_successful: bool = True
    ) -> StudentPortalAccess:
        """Record student login attempt"""
        stmt = select(StudentPortalAccess).where(
            StudentPortalAccess.student_id == student_id
        )
        access = session.exec(stmt).first()
        
        if not access:
            raise HTTPException(status_code=404, detail="Portal access not found")
        
        if is_successful:
            access.last_login = datetime.utcnow()
            access.last_login_ip = ip_address
            access.login_count += 1
            access.failed_login_attempts = 0
            
            # Generate session token
            access.current_session_token = secrets.token_urlsafe(32)
            access.session_expires_at = datetime.utcnow() + timedelta(hours=24)
            
            # Log activity
            activity = StudentActivity(
                student_id=student_id,
                student_portal_access_id=access.id,
                activity_type=ActivityType.LOGIN,
                activity_description="Student logged in successfully",
                ip_address=ip_address,
                user_agent=user_agent
            )
            session.add(activity)
        else:
            access.failed_login_attempts += 1
            access.last_failed_login = datetime.utcnow()
            
            # Lock account after 5 failed attempts
            if access.failed_login_attempts >= 5:
                access.is_active = False
                access.deactivation_reason = "Account locked due to multiple failed login attempts"
        
        session.commit()
        session.refresh(access)
        return access
    
    @staticmethod
    def log_activity(
        session: Session,
        student_id: int,
        activity_type: ActivityType,
        description: str,
        metadata: Optional[Dict] = None,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None
    ) -> StudentActivity:
        """Log student activity"""
        stmt = select(StudentPortalAccess).where(
            StudentPortalAccess.student_id == student_id
        )
        access = session.exec(stmt).first()
        
        if not access:
            raise HTTPException(status_code=404, detail="Portal access not found")
        
        activity = StudentActivity(
            student_id=student_id,
            student_portal_access_id=access.id,
            activity_type=activity_type,
            activity_description=description,
            metadata=str(metadata) if metadata else None,
            ip_address=ip_address,
            user_agent=user_agent
        )
        
        session.add(activity)
        session.commit()
        session.refresh(activity)
        return activity
    
    @staticmethod
    def create_notification(
        session: Session,
        student_id: int,
        notification_type: str,
        title: str,
        message: str,
        priority: NotificationPriority = NotificationPriority.MEDIUM,
        link: Optional[str] = None,
        requires_action: bool = False,
        expires_in_days: Optional[int] = None
    ) -> Notification:
        """Create a notification for student"""
        expires_at = None
        if expires_in_days:
            expires_at = datetime.utcnow() + timedelta(days=expires_in_days)
        
        notification = Notification(
            student_id=student_id,
            notification_type=notification_type,
            title=title,
            message=message,
            priority=priority,
            link=link,
            requires_action=requires_action,
            expires_at=expires_at
        )
        
        session.add(notification)
        session.commit()
        session.refresh(notification)
        return notification
    
    @staticmethod
    def mark_notification_read(
        session: Session,
        notification_id: int
    ) -> Notification:
        """Mark notification as read"""
        notification = session.get(Notification, notification_id)
        if not notification:
            raise HTTPException(status_code=404, detail="Notification not found")
        
        notification.is_read = True
        notification.read_at = datetime.utcnow()
        
        session.commit()
        session.refresh(notification)
        return notification
    
    @staticmethod
    def get_dashboard_data(
        session: Session,
        student_id: int
    ) -> Dict:
        """Get dashboard data for student"""
        student = session.get(Student, student_id)
        if not student:
            raise HTTPException(status_code=404, detail="Student not found")
        
        # Get fee summary
        stmt = select(StudentFee).where(StudentFee.student_id == student_id)
        fees = session.exec(stmt).all()
        
        total_pending = sum(f.total_pending for f in fees)
        
        # Get unread notifications
        stmt = select(Notification).where(
            Notification.student_id == student_id,
            Notification.is_read == False
        )
        unread_notifications = len(session.exec(stmt).all())
        
        # Get recent activity
        stmt = select(StudentActivity).where(
            StudentActivity.student_id == student_id
        ).order_by(StudentActivity.created_at.desc()).limit(5)
        recent_activity = session.exec(stmt).all()
        
        return {
            "student": {
                "id": student.id,
                "name": student.name,
                "admission_number": student.admission_number,
                "email": student.email,
                "phone": student.phone
            },
            "fee_summary": {
                "total_pending": float(total_pending),
                "has_dues": total_pending > 0
            },
            "notifications": {
                "unread_count": unread_notifications
            },
            "recent_activity": [
                {
                    "type": a.activity_type,
                    "description": a.activity_description,
                    "timestamp": a.created_at.isoformat()
                }
                for a in recent_activity
            ]
        }
