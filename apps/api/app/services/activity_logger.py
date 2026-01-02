"""Activity logging service for tracking application changes"""
from typing import Optional
from sqlmodel import Session
from app.models.admissions import ApplicationActivityLog, ActivityType
from datetime import datetime
import json

def log_activity(
    session: Session,
    application_id: int,
    activity_type: ActivityType,
    description: str,
    performed_by: Optional[int] = None,
    ip_address: Optional[str] = None,
    extra_data: Optional[dict] = None
) -> ApplicationActivityLog:
    """
    Log an activity for an application
    
    Args:
        session: Database session
        application_id: ID of the application
        activity_type: Type of activity
        description: Human-readable description
        performed_by: User ID who performed the action
        ip_address: IP address of the requester
        extra_data: Additional data to store as JSON
    
    Returns:
        Created activity log entry
    """
    log_entry = ApplicationActivityLog(
        application_id=application_id,
        activity_type=activity_type,
        description=description,
        performed_by=performed_by,
        ip_address=ip_address,
        extra_data=json.dumps(extra_data) if extra_data else None,
        created_at=datetime.utcnow()
    )
    
    session.add(log_entry)
    session.flush()  # Don't commit, let the caller handle transaction
    
    return log_entry
