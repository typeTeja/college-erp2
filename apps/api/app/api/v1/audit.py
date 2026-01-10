"""
Academic Audit Log API Endpoints
"""
from typing import Optional, List
from fastapi import APIRouter, Depends, Query
from sqlmodel import Session, select, col
from datetime import datetime

from app.api.deps import get_session, get_current_active_superuser
from app.models.audit_log import AuditLog
from app.models.user import User
from app.schemas.audit_log import AuditLogRead

router = APIRouter()


@router.get("/", response_model=List[AuditLogRead])
def get_audit_logs(
    *,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_superuser),
    table_name: Optional[str] = Query(None, description="Filter by table name"),
    record_id: Optional[int] = Query(None, description="Filter by record ID"),
    user_id: Optional[int] = Query(None, description="Filter by user ID"),
    action: Optional[str] = Query(None, description="Filter by action (CREATE/UPDATE/DELETE)"),
    start_date: Optional[datetime] = Query(None, description="Filter by start date"),
    end_date: Optional[datetime] = Query(None, description="Filter by end date"),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100)
):
    """
    Get audit logs with optional filtering
    
    Requires SUPER_ADMIN or ADMIN role
    """
    # Build query
    query = select(AuditLog)
    
    # Apply filters
    if table_name:
        query = query.where(AuditLog.table_name == table_name)
    if record_id is not None:
        query = query.where(AuditLog.record_id == record_id)
    if user_id is not None:
        query = query.where(AuditLog.user_id == user_id)
    if action:
        query = query.where(AuditLog.action == action)
    if start_date:
        query = query.where(AuditLog.created_at >= start_date)
    if end_date:
        query = query.where(AuditLog.created_at <= end_date)
    
    # Order by most recent first
    query = query.order_by(col(AuditLog.created_at).desc())
    
    # Pagination
    query = query.offset(skip).limit(limit)
    
    # Execute
    audit_logs = session.exec(query).all()
    
    return audit_logs


@router.get("/{id}", response_model=AuditLogRead)
def get_audit_log(
    *,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_superuser),
    id: int
):
    """
    Get a specific audit log entry
    
    Requires SUPER_ADMIN or ADMIN role
    """
    audit_log = session.get(AuditLog, id)
    if not audit_log:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Audit log not found")
    
    return audit_log
