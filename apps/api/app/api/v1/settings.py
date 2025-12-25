from typing import List, Optional, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, Query, Request
from sqlmodel import Session, select, func
from app.api import deps
from app.models.settings import SystemSetting, SettingGroup, AuditLog, AuditLogAction
from app.models.user import User
from app.schemas.settings import (
    SystemSettingRead, SystemSettingUpdate, AuditLogRead, 
    PasswordChange, ProfileUpdate, BulkSettingsUpdate
)
from app.core import security
from datetime import datetime

router = APIRouter()

@router.get("/", response_model=List[SystemSettingRead])
def get_settings(
    *,
    session: Session = Depends(deps.get_session),
    current_user: User = Depends(deps.get_current_user),
    group: Optional[SettingGroup] = None
):
    """Fetch settings visible to the current role"""
    statement = select(SystemSetting)
    
    # RBAC filtering
    is_admin = any(role.name in ["SUPER_ADMIN", "ADMIN"] for role in current_user.roles)
    is_super_admin = any(role.name == "SUPER_ADMIN" for role in current_user.roles)
    
    if not is_admin:
        # Students/Faculty can only see PERSONAL group
        statement = statement.where(SystemSetting.group == SettingGroup.PERSONAL)
    elif not is_super_admin:
        # Admins cannot see INTEGRATION group (or sensitive ones)
        statement = statement.where(SystemSetting.group != SettingGroup.INTEGRATION)
        
    if group:
        statement = statement.where(SystemSetting.group == group)
        
    settings = session.exec(statement).all()
    
    # Mask secrets if user is not Super Admin
    for s in settings:
        if s.is_secret and not is_super_admin:
            s.value = "********"
            
    return settings

@router.patch("/{setting_id}", response_model=SystemSettingRead)
def update_setting(
    setting_id: int,
    setting_in: SystemSettingUpdate,
    request: Request,
    session: Session = Depends(deps.get_session),
    current_user: User = Depends(deps.get_current_user),
):
    """Update a specific setting with audit trail"""
    setting = session.get(SystemSetting, setting_id)
    if not setting:
        raise HTTPException(status_code=404, detail="Setting not found")
        
    # Check permission
    is_super_admin = any(role.name == "SUPER_ADMIN" for role in current_user.roles)
    if setting.group == SettingGroup.INTEGRATION and not is_super_admin:
        raise HTTPException(status_code=403, detail="Only Super Admin can update integration settings")
        
    old_value = setting.value
    
    if setting_in.value is not None:
        setting.value = setting_in.value
    if setting_in.description:
        setting.description = setting_in.description
        
    setting.updated_at = datetime.utcnow()
    setting.updated_by = current_user.id
    
    # Audit Logging
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

@router.post("/bulk", response_model=Dict[str, str])
def bulk_update_settings(
    data: BulkSettingsUpdate,
    request: Request,
    session: Session = Depends(deps.get_session),
    current_user: User = Depends(deps.get_current_user),
):
    """Update multiple settings in one transaction"""
    is_admin = any(role.name in ["SUPER_ADMIN", "ADMIN"] for role in current_user.roles)
    if not is_admin:
        raise HTTPException(status_code=403, detail="Only admins can bulk update settings")
        
    for key, value in data.settings.items():
        setting = session.exec(select(SystemSetting).where(SystemSetting.key == key)).first()
        if not setting:
            continue
            
        is_super_admin = any(role.name == "SUPER_ADMIN" for role in current_user.roles)
        if setting.group == SettingGroup.INTEGRATION and not is_super_admin:
            continue # Skip integration settings if not super admin
            
        old_value = setting.value
        setting.value = value
        setting.updated_at = datetime.utcnow()
        setting.updated_by = current_user.id
        
        # Audit Logging for each change
        audit = AuditLog(
            user_id=current_user.id,
            action=AuditLogAction.SETTING_CHANGE,
            module="SETTINGS",
            description=f"Bulk updated setting: {key}",
            target_id=str(setting.id),
            from_value=old_value,
            to_value=value,
            ip_address=request.client.host,
            user_agent=request.headers.get("user-agent")
        )
        session.add(setting)
        session.add(audit)
        
    session.commit()
    return {"status": "success", "message": "Settings updated successfully"}

@router.post("/profile", response_model=Dict[str, str])
def update_profile(
    profile_in: ProfileUpdate,
    session: Session = Depends(deps.get_session),
    current_user: User = Depends(deps.get_current_user),
):
    """Update current user profile and preferences"""
    if profile_in.full_name:
        current_user.full_name = profile_in.full_name
    if profile_in.email:
        current_user.email = profile_in.email
    if profile_in.preferences is not None:
        # Merge preferences
        if current_user.preferences is None:
            current_user.preferences = {}
        current_user.preferences.update(profile_in.preferences)
        # Force SQLAlchemy to recognize the JSON change
        from sqlalchemy.orm.attributes import flag_modified
        flag_modified(current_user, "preferences")
    
    current_user.updated_at = datetime.utcnow()
    session.add(current_user)
    session.commit()
    return {"status": "success", "message": "Profile and preferences updated"}

@router.post("/change-password")
def change_password(
    data: PasswordChange,
    session: Session = Depends(deps.get_session),
    current_user: User = Depends(deps.get_current_user),
):
    """Change current user password"""
    if not security.verify_password(data.current_password, current_user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect current password")
        
    current_user.hashed_password = security.get_password_hash(data.new_password)
    session.add(current_user)
    session.commit()
    return {"status": "success", "message": "Password changed successfully"}

@router.get("/audit-logs", response_model=List[AuditLogRead])
def get_audit_logs(
    *,
    session: Session = Depends(deps.get_session),
    current_user: User = Depends(deps.get_current_user),
    module: Optional[str] = None,
    limit: int = 50,
    offset: int = 0
):
    """Fetch system audit logs (Admin/Super Admin only)"""
    is_admin = any(role.name in ["SUPER_ADMIN", "ADMIN"] for role in current_user.roles)
    if not is_admin:
        raise HTTPException(status_code=403, detail="Not enough permissions")
        
    statement = select(AuditLog)
    if module:
        statement = statement.where(AuditLog.module == module)
        
    logs = session.exec(statement.order_by(AuditLog.timestamp.desc()).offset(offset).limit(limit)).all()
    return logs

@router.post("/test-connection")
def test_connection(
    gateway: str = Query(..., enum=["msg91", "gmail", "easebuzz"]),
    current_user: User = Depends(deps.get_current_user)
):
    """Stub to test API connections"""
    is_super_admin = any(role.name == "SUPER_ADMIN" for role in current_user.roles)
    if not is_super_admin:
        raise HTTPException(status_code=403, detail="Not authorized")
        
    # In a real app, logic to call 3rd party API with configured keys
    return {"status": "success", "message": f"Connection to {gateway} successful (Simulated)"}
