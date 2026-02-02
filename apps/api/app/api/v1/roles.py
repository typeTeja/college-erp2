from typing import Any, List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select
from app.api.deps import get_current_user, get_session, get_current_active_superuser
from app.models import User
from app.models import Role
from app.models import Permission, RolePermission, PermissionAuditLog
from app.schemas.role import RoleRead, RoleCreate, RoleUpdate, PermissionAuditLogRead
from app.schemas.permission import PermissionRead, PermissionGroup

router = APIRouter()

@router.get("/", response_model=List[RoleRead])
def get_roles(
    *,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_superuser),
) -> Any:
    """Retrieve all roles with their permissions."""
    return session.exec(select(Role)).all()

@router.get("/permissions", response_model=List[PermissionGroup])
def get_permissions(
    *,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_superuser),
) -> Any:
    """Retrieve all permissions grouped by module."""
    permissions = session.exec(select(Permission)).all()
    
    # Group by module
    grouped = {}
    for p in permissions:
        if p.module not in grouped:
            grouped[p.module] = []
        grouped[p.module].append(p)
    
    return [{"module": mod, "permissions": perms} for mod, perms in grouped.items()]

@router.post("/", response_model=RoleRead)
def create_role(
    *,
    session: Session = Depends(get_session),
    role_in: RoleCreate,
    current_user: User = Depends(get_current_active_superuser),
) -> Any:
    """Create a new role and assign permissions."""
    existing = session.exec(select(Role).where(Role.name == role_in.name)).first()
    if existing:
        raise HTTPException(status_code=400, detail="Role already exists")
    
    db_role = Role(
        name=role_in.name,
        description=role_in.description,
        is_system=False
    )
    
    # Add permissions
    if role_in.permission_ids:
        permissions = session.exec(select(Permission).where(Permission.id.in_(role_in.permission_ids))).all()
        db_role.permissions = permissions
        
    session.add(db_role)
    session.commit()
    session.refresh(db_role)
    
    # Audit log
    for p in db_role.permissions:
        audit = PermissionAuditLog(
            actor_id=current_user.id,
            role_id=db_role.id,
            action="ADD_PERMISSION",
            permission_name=p.name
        )
        session.add(audit)
    session.commit()
    
    return db_role

@router.patch("/{id}", response_model=RoleRead)
def update_role(
    *,
    session: Session = Depends(get_session),
    id: int,
    role_in: RoleUpdate,
    current_user: User = Depends(get_current_active_superuser),
) -> Any:
    """Update role details and permissions."""
    db_role = session.get(Role, id)
    if not db_role:
        raise HTTPException(status_code=404, detail="Role not found")
    
    if db_role.is_system and role_in.name:
        raise HTTPException(status_code=400, detail="Cannot rename system roles")

    # Update basic fields
    update_data = role_in.dict(exclude_unset=True)
    if "permission_ids" in update_data:
        new_permissions = session.exec(select(Permission).where(Permission.id.in_(role_in.permission_ids))).all()
        
        # Determine changed permissions for auditing
        current_p_names = {p.name for p in db_role.permissions}
        new_p_names = {p.name for p in new_permissions}
        
        added = new_p_names - current_p_names
        removed = current_p_names - new_p_names
        
        # Protection: Prevent removing all permissions from ADMIN/SUPER_ADMIN
        if db_role.name in ["SUPER_ADMIN", "ADMIN"] and not new_permissions:
            raise HTTPException(status_code=400, detail="Cannot remove all permissions from core administrative roles")

        db_role.permissions = new_permissions
        
        # Audit
        for p_name in added:
            session.add(PermissionAuditLog(actor_id=current_user.id, role_id=db_role.id, action="ADD_PERMISSION", permission_name=p_name))
        for p_name in removed:
            session.add(PermissionAuditLog(actor_id=current_user.id, role_id=db_role.id, action="REMOVE_PERMISSION", permission_name=p_name))

    for field in ["description", "is_active"]:
        if field in update_data:
            setattr(db_role, field, update_data[field])
            
    session.add(db_role)
    session.commit()
    session.refresh(db_role)
    return db_role

@router.get("/audit", response_model=List[PermissionAuditLogRead])
def get_rbac_audit_logs(
    *,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_superuser),
    limit: int = 100
) -> Any:
    """Retrieve RBAC audit logs."""
    statement = select(PermissionAuditLog).order_by(PermissionAuditLog.timestamp.desc()).limit(limit)
    results = session.exec(statement).all()
    
    # Manually flatten for response schema if needed
    formatted = []
    for log in results:
        data = log.model_dump()
        data["actor_name"] = log.actor.full_name if log.actor else "System"
        data["role_name"] = log.role.name if log.role else "Deleted Role"
        data["timestamp"] = log.timestamp.isoformat()
        formatted.append(data)
    return formatted
