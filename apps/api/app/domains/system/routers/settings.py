from typing import List, Optional, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, Query, Request
from sqlmodel import Session, select
from datetime import datetime

from app.api import deps
from app.core import security
from ..models.system import SystemSetting, SettingGroup, AuditLog, AuditLogAction
from ..schemas.system import SystemSettingRead, SystemSettingUpdate, AuditLogRead, BulkSettingsUpdate, ProfileUpdate, PasswordChange
from app.shared.enums import AuditLogAction, SettingGroup


router = APIRouter()

@router.get("/", response_model=List[SystemSettingRead], tags=["System - Settings"])
def get_settings(
    *,
    session: Session = Depends(deps.get_session),
    current_user = Depends(deps.get_current_user),
    group: Optional[SettingGroup] = None
):
    """Fetch settings visible to the current role"""
    statement = select(SystemSetting)
    is_admin = any(role.name in ["SUPER_ADMIN", "ADMIN"] for role in current_user.roles)
    
    if not is_admin:
        statement = statement.where(SystemSetting.group == SettingGroup.PERSONAL)
        
    if group:
        statement = statement.where(SystemSetting.group == group)
        
    settings = session.exec(statement).all()
    return settings

@router.patch("/{setting_id}", response_model=SystemSettingRead, tags=["System - Settings"])
def update_setting(
    setting_id: int,
    setting_in: SystemSettingUpdate,
    request: Request,
    session: Session = Depends(deps.get_session),
    current_user = Depends(deps.get_current_user),
):
    """Update a specific setting with audit trail"""
    setting = session.get(SystemSetting, setting_id)
    if not setting:
        raise HTTPException(status_code=404, detail="Setting not found")
        
    old_value = setting.value
    if setting_in.value is not None:
        setting.value = setting_in.value
    if setting_in.description:
        setting.description = setting_in.description
        
    setting.updated_at = datetime.utcnow()
    setting.updated_by = current_user.id
    
    audit = AuditLog(
        user_id=current_user.id,
        action=AuditLogAction.SETTING_CHANGE,
        module="SETTINGS",
        description=f"Updated setting: {setting.key}",
        target_id=str(setting.id),
        from_value=old_value,
        to_value=setting.value,
        ip_address=request.client.host,
        user_agent=request.headers.get("user-agent")
    )
    
    session.add(setting)
    session.add(audit)
    session.commit()
    session.refresh(setting)
    return setting

@router.get("/audit-logs", response_model=List[AuditLogRead], tags=["System - Audit"])
def get_audit_logs(
    *,
    session: Session = Depends(deps.get_session),
    current_user = Depends(deps.get_current_user),
    module: Optional[str] = None,
    limit: int = 50,
    offset: int = 0
):
    """Fetch system audit logs"""
    is_admin = any(role.name in ["SUPER_ADMIN", "ADMIN"] for role in current_user.roles)
    if not is_admin:
        raise HTTPException(status_code=403, detail="Not enough permissions")
        
    statement = select(AuditLog)
    if module:
        statement = statement.where(AuditLog.module == module)
        
    logs = session.exec(statement.order_by(AuditLog.timestamp.desc()).offset(offset).limit(limit)).all()
    return logs
