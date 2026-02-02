"""
Audit Logging Utility
Helper functions to log changes to academic entities
"""
from typing import Optional, Any, Dict
from sqlmodel import Session
from fastapi import Request

from app.models.audit_log import AuditLog
from app.models import User

def log_audit(
    session: Session,
    table_name: str,
    record_id: int,
    action: str,
    user: Optional[User] = None,
    old_values: Optional[Dict[str, Any]] = None,
    new_values: Optional[Dict[str, Any]] = None,
    request: Optional[Request] = None,
    description: Optional[str] = None
) -> AuditLog:
    """
    Create an audit log entry
    
    Args:
        session: Database session
        table_name: Name of the table being modified
        record_id: ID of the record
        action: "CREATE", "UPDATE", or "DELETE"
        user: User making the change
        old_values: Previous state (for UPDATE/DELETE)
        new_values: New state (for CREATE/UPDATE)
        request: FastAPI request object (for IP and user agent)
        description: Human-readable description
    """
    # Extract request context
    ip_address = None
    user_agent = None
    if request:
        ip_address = request.client.host if request.client else None
        user_agent = request.headers.get("user-agent")
    
    # Create audit log
    audit = AuditLog(
        table_name=table_name,
        record_id=record_id,
        action=action,
        user_id=user.id if user else None,
        user_email=user.email if user else None,
        old_values=old_values,
        new_values=new_values,
        ip_address=ip_address,
        user_agent=user_agent,
        description=description
    )
    
    session.add(audit)
    session.commit()
    session.refresh(audit)
    
    return audit


def log_create(
    session: Session,
    table_name: str,
    record_id: int,
    new_values: Dict[str, Any],
    user: Optional[User] = None,
    request: Optional[Request] = None
) -> AuditLog:
    """Log a CREATE operation"""
    return log_audit(
        session=session,
        table_name=table_name,
        record_id=record_id,
        action="CREATE",
        user=user,
        new_values=new_values,
        request=request,
        description=f"Created {table_name} #{record_id}"
    )


def log_update(
    session: Session,
    table_name: str,
    record_id: int,
    old_values: Dict[str, Any],
    new_values: Dict[str, Any],
    user: Optional[User] = None,
    request: Optional[Request] = None
) -> AuditLog:
    """Log an UPDATE operation"""
    # Calculate what changed
    changes = {k: v for k, v in new_values.items() if old_values.get(k) != v}
    
    return log_audit(
        session=session,
        table_name=table_name,
        record_id=record_id,
        action="UPDATE",
        user=user,
        old_values=old_values,
        new_values=new_values,
        request=request,
        description=f"Updated {table_name} #{record_id}: {', '.join(changes.keys())}"
    )


def log_delete(
    session: Session,
    table_name: str,
    record_id: int,
    old_values: Dict[str, Any],
    user: Optional[User] = None,
    request: Optional[Request] = None
) -> AuditLog:
    """Log a DELETE operation"""
    return log_audit(
        session=session,
        table_name=table_name,
        record_id=record_id,
        action="DELETE",
        user=user,
        old_values=old_values,
        request=request,
        description=f"Deleted {table_name} #{record_id}"
    )


def model_to_dict(model: Any, exclude: Optional[list] = None) -> Dict[str, Any]:
    """
    Convert SQLModel instance to dictionary for audit logging
    
    Args:
        model: SQLModel instance
        exclude: List of fields to exclude
    """
    exclude = exclude or []
    return {
        key: value
        for key, value in model.dict().items()
        if key not in exclude and not key.startswith('_')
    }
