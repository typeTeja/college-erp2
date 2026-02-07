"""
System Domain Router

All API endpoints for the system domain including:
- User management
- Role and permission management
- System settings
- Audit logs
- File management
- Data imports
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from typing import List, Optional

from app.api.deps import get_session, get_current_user, get_current_active_superuser
from app.domains.system.services import SystemService
from app.domains.system.schemas import (
    UserCreate, UserUpdate, UserResponse,
    RoleCreate, RoleUpdate, RoleRead,
    PermissionCreate, PermissionRead,
    SystemSettingCreate, SystemSettingUpdate, SystemSettingRead,
    AuditLogRead,
    DepartmentCreate, DepartmentUpdate, DepartmentRead
)
from app.domains.auth.models import AuthUser as User
from app.domains.system.exceptions import (
    UserNotFoundError, RoleNotFoundError, SettingNotFoundError,
    UserAlreadyExistsError,
    DepartmentNotFoundError, DepartmentAlreadyExistsError
)


router = APIRouter()


# ----------------------------------------------------------------------
# User Endpoints
# ----------------------------------------------------------------------

@router.get("/users", response_model=List[UserResponse])
def list_users(
    skip: int = 0,
    limit: int = 100,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_superuser)
):
    """List all users"""
    service = SystemService(session)
    users = service.list_users(skip=skip, limit=limit)
    return users


@router.get("/users/{user_id}", response_model=UserResponse)
def get_user(
    user_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """Get user by ID"""
    service = SystemService(session)
    try:
        user = service.get_user(user_id)
        return user
    except UserNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/users", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(
    user_data: UserCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_superuser)
):
    """Create a new user"""
    service = SystemService(session)
    try:
        user = service.create_user(user_data)
        return user
    except UserAlreadyExistsError as e:
        raise HTTPException(status_code=400, detail=str(e))


# ----------------------------------------------------------------------
# Role Endpoints
# ----------------------------------------------------------------------

@router.get("/roles", response_model=List[RoleRead])
def list_roles(
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_superuser)
):
    """List all roles"""
    service = SystemService(session)
    roles = service.list_roles()
    return roles


@router.post("/roles", response_model=RoleRead, status_code=status.HTTP_201_CREATED)
def create_role(
    role_data: RoleCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_superuser)
):
    """Create a new role"""
    service = SystemService(session)
    role = service.create_role(role_data)
    return role


# ----------------------------------------------------------------------
# Permission Endpoints
# ----------------------------------------------------------------------

@router.get("/permissions", response_model=List[PermissionRead])
def list_permissions(
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_superuser)
):
    """List all permissions"""
    service = SystemService(session)
    permissions = service.list_permissions()
    return permissions


# ----------------------------------------------------------------------
# System Settings Endpoints
# ----------------------------------------------------------------------

@router.get("/settings", response_model=List[SystemSettingRead])
def list_settings(
    group: Optional[str] = None,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_superuser)
):
    """List all settings"""
    service = SystemService(session)
    settings = service.list_settings(group=group)
    return settings


@router.get("/audit-logs", response_model=List[AuditLogRead])
def list_audit_logs(
    user_id: Optional[int] = None,
    module: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_superuser)
):
    """List audit logs"""
    service = SystemService(session)
    logs = service.list_audit_logs(user_id=user_id, module=module, skip=skip, limit=limit)
    return logs


# ----------------------------------------------------------------------
# Department Endpoints (Core Master)
# ----------------------------------------------------------------------

@router.get("/departments", response_model=List[DepartmentRead])
def list_departments(
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_superuser)
):
    """List all departments"""
    service = SystemService(session)
    return service.list_departments()

@router.get("/departments/{department_id}", response_model=DepartmentRead)
def get_department(
    department_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_superuser)
):
    """Get department by ID"""
    service = SystemService(session)
    try:
        department = service.get_department(department_id)
        return department
    except DepartmentNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.post("/departments", response_model=DepartmentRead, status_code=status.HTTP_201_CREATED)
def create_department(
    data: DepartmentCreate,
    session: Session = Depends(get_session),
    # Only Admin/Principal should create departments
    current_user: User = Depends(get_current_active_superuser)
):
    """Create a new department"""
    service = SystemService(session)
    try:
        department = service.create_department(data)
        return department
    except DepartmentAlreadyExistsError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.patch("/departments/{department_id}", response_model=DepartmentRead)
def update_department(
    department_id: int,
    data: DepartmentUpdate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_superuser)
):
    """Update a department"""
    service = SystemService(session)
    try:
        department = service.update_department(department_id, data)
        return department
    except DepartmentNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except DepartmentAlreadyExistsError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/departments/{department_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_department(
    department_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_superuser)
):
    """Delete a department"""
    service = SystemService(session)
    try:
        service.delete_department(department_id)
    except DepartmentNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
