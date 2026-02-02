from typing import Optional, List
from fastapi import APIRouter, Depends, Query
from sqlmodel import Session, select, col
from datetime import datetime

from app.api.deps import get_session, get_current_active_superuser
from ..models.system import AuditLog
from ..schemas.system import AuditLogRead

router = APIRouter()

@router.get("/", response_model=List[AuditLogRead], tags=["System - Audit"])
def get_audit_logs(
    *,
    session: Session = Depends(get_session),
    current_user = Depends(get_current_active_superuser),
    table_name: Optional[str] = Query(None),
    record_id: Optional[int] = Query(None),
    user_id: Optional[int] = Query(None),
    action: Optional[str] = Query(None),
    start_date: Optional[datetime] = Query(None),
    end_date: Optional[datetime] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100)
):
    """Get system audit logs"""
    query = select(AuditLog)
    
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
    
    query = query.order_by(AuditLog.timestamp.desc())
    query = query.offset(skip).limit(limit)
    
    return session.exec(query).all()
