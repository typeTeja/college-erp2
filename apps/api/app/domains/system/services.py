"""
System Domain Services

Business logic for system domain including:
- System settings
- File storage
- Data imports
- Audit logging

Note: User, Role, Permission management moved to Auth domain
"""

from typing import List, Optional, Any
from sqlmodel import Session, select
from datetime import datetime, timedelta
import secrets

# System domain models
from app.domains.system.models import (
    SystemSetting, InstituteInfo, AuditLog, PermissionAuditLog,
    FileMetadata, ImportLog
)

# Auth domain models (moved from system)
from app.domains.auth.models import (
    AuthUser as User,
    Role,
    Permission,
    UserRole,
    RolePermission,
)

from app.domains.system.schemas import (
    UserCreate, UserUpdate,
    RoleCreate, RoleUpdate,
    PermissionCreate,
    SystemSettingCreate, SystemSettingUpdate,
    AuditLogCreate
)
from app.domains.system.exceptions import (
    UserNotFoundError, RoleNotFoundError, PermissionNotFoundError,
    UserAlreadyExistsError, SettingNotFoundError
)
from app.core.security import get_password_hash, verify_password


class SystemService:
    """Service for system domain operations"""
    
    def __init__(self, session: Session):
        self.session = session
    
    # ----------------------------------------------------------------------
    # User Management
    # ----------------------------------------------------------------------
    
    def get_user(self, user_id: int) -> User:
        """Get user by ID"""
        user = self.session.get(User, user_id)
        if not user:
            raise UserNotFoundError(f"User with ID {user_id} not found")
        return user
    
    def get_user_by_email(self, email: str) -> Optional[User]:
        """Get user by email"""
        statement = select(User).where(User.email == email)
        return self.session.exec(statement).first()
    
    def get_user_by_username(self, username: str) -> Optional[User]:
        """Get user by username"""
        statement = select(User).where(User.username == username)
        return self.session.exec(statement).first()
    
    def list_users(self, skip: int = 0, limit: int = 100) -> List[User]:
        """List all users"""
        statement = select(User).offset(skip).limit(limit)
        return list(self.session.exec(statement).all())
    
    def create_user(self, user_data: UserCreate) -> User:
        """Create a new user"""
        # Check if user already exists
        if self.get_user_by_email(user_data.email):
            raise UserAlreadyExistsError(f"User with email {user_data.email} already exists")
        if self.get_user_by_username(user_data.username):
            raise UserAlreadyExistsError(f"User with username {user_data.username} already exists")
        
        # Create user
        user = User(
            username=user_data.username,
            email=user_data.email,
            full_name=user_data.full_name,
            phone=user_data.phone,
            hashed_password=get_password_hash(user_data.password),
            preferences=user_data.preferences or {}
        )
        
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        
        # Assign roles
        if user_data.role_ids:
            for role_id in user_data.role_ids:
                user_role = UserRole(user_id=user.id, role_id=role_id)
                self.session.add(user_role)
            self.session.commit()
        
        return user
    
    def update_user(self, user_id: int, user_data: UserUpdate) -> User:
        """Update a user"""
        user = self.get_user(user_id)
        
        # Update fields
        if user_data.email is not None:
            user.email = user_data.email
        if user_data.full_name is not None:
            user.full_name = user_data.full_name
        if user_data.phone is not None:
            user.phone = user_data.phone
        if user_data.preferences is not None:
            user.preferences = user_data.preferences
        if user_data.is_active is not None:
            user.is_active = user_data.is_active
        
        user.updated_at = datetime.utcnow()
        
        # Update roles
        if user_data.role_ids is not None:
            # Delete existing roles
            statement = select(UserRole).where(UserRole.user_id == user_id)
            existing_roles = self.session.exec(statement).all()
            for user_role in existing_roles:
                self.session.delete(user_role)
            
            # Add new roles
            for role_id in user_data.role_ids:
                user_role = UserRole(user_id=user.id, role_id=role_id)
                self.session.add(user_role)
        
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        
        return user
    
    def delete_user(self, user_id: int) -> None:
        """Delete a user"""
        user = self.get_user(user_id)
        self.session.delete(user)
        self.session.commit()
    
    # ----------------------------------------------------------------------
    # Role Management
    # ----------------------------------------------------------------------
    
    def get_role(self, role_id: int) -> Role:
        """Get role by ID"""
        role = self.session.get(Role, role_id)
        if not role:
            raise RoleNotFoundError(f"Role with ID {role_id} not found")
        return role
    
    def list_roles(self) -> List[Role]:
        """List all roles"""
        statement = select(Role)
        return list(self.session.exec(statement).all())
    
    def create_role(self, role_data: RoleCreate) -> Role:
        """Create a new role"""
        role = Role(
            name=role_data.name,
            description=role_data.description,
            is_system=role_data.is_system,
            is_active=role_data.is_active
        )
        
        self.session.add(role)
        self.session.commit()
        self.session.refresh(role)
        
        # Assign permissions
        if role_data.permission_ids:
            for permission_id in role_data.permission_ids:
                role_permission = RolePermission(role_id=role.id, permission_id=permission_id)
                self.session.add(role_permission)
            self.session.commit()
        
        return role
    
    def update_role(self, role_id: int, role_data: RoleUpdate) -> Role:
        """Update a role"""
        role = self.get_role(role_id)
        
        if role_data.name is not None:
            role.name = role_data.name
        if role_data.description is not None:
            role.description = role_data.description
        if role_data.is_active is not None:
            role.is_active = role_data.is_active
        
        # Update permissions
        if role_data.permission_ids is not None:
            # Delete existing permissions
            statement = select(RolePermission).where(RolePermission.role_id == role_id)
            existing_perms = self.session.exec(statement).all()
            for role_perm in existing_perms:
                self.session.delete(role_perm)
            
            # Add new permissions
            for permission_id in role_data.permission_ids:
                role_permission = RolePermission(role_id=role.id, permission_id=permission_id)
                self.session.add(role_permission)
        
        self.session.add(role)
        self.session.commit()
        self.session.refresh(role)
        
        return role
    
    # ----------------------------------------------------------------------
    # Permission Management
    # ----------------------------------------------------------------------
    
    def list_permissions(self) -> List[Permission]:
        """List all permissions"""
        statement = select(Permission)
        return list(self.session.exec(statement).all())
    
    def create_permission(self, permission_data: PermissionCreate) -> Permission:
        """Create a new permission"""
        permission = Permission(
            name=permission_data.name,
            description=permission_data.description,
            module=permission_data.module
        )
        
        self.session.add(permission)
        self.session.commit()
        self.session.refresh(permission)
        
        return permission
    
    # ----------------------------------------------------------------------
    # System Settings
    # ----------------------------------------------------------------------
    
    def get_setting(self, key: str) -> SystemSetting:
        """Get setting by key"""
        statement = select(SystemSetting).where(SystemSetting.key == key)
        setting = self.session.exec(statement).first()
        if not setting:
            raise SettingNotFoundError(f"Setting with key '{key}' not found")
        return setting
    
    def list_settings(self, group: Optional[str] = None) -> List[SystemSetting]:
        """List all settings, optionally filtered by group"""
        statement = select(SystemSetting)
        if group:
            statement = statement.where(SystemSetting.group == group)
        return list(self.session.exec(statement).all())
    
    def create_setting(self, setting_data: SystemSettingCreate, user_id: int) -> SystemSetting:
        """Create a new setting"""
        setting = SystemSetting(
            key=setting_data.key,
            value=setting_data.value,
            group=setting_data.group,
            is_secret=setting_data.is_secret,
            description=setting_data.description,
            updated_by=user_id
        )
        
        self.session.add(setting)
        self.session.commit()
        self.session.refresh(setting)
        
        return setting
    
    def update_setting(self, key: str, setting_data: SystemSettingUpdate, user_id: int) -> SystemSetting:
        """Update a setting"""
        setting = self.get_setting(key)
        
        if setting_data.value is not None:
            setting.value = setting_data.value
        if setting_data.description is not None:
            setting.description = setting_data.description
        
        setting.updated_at = datetime.utcnow()
        setting.updated_by = user_id
        
        self.session.add(setting)
        self.session.commit()
        self.session.refresh(setting)
        
        return setting
    
    # ----------------------------------------------------------------------
    # Audit Logging
    # ----------------------------------------------------------------------
    
    def create_audit_log(self, log_data: AuditLogCreate) -> AuditLog:
        """Create an audit log entry"""
        log = AuditLog(**log_data.model_dump())
        
        self.session.add(log)
        self.session.commit()
        self.session.refresh(log)
        
        return log
    
    def list_audit_logs(
        self,
        user_id: Optional[int] = None,
        module: Optional[str] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[AuditLog]:
        """List audit logs with optional filters"""
        statement = select(AuditLog)
        
        if user_id:
            statement = statement.where(AuditLog.user_id == user_id)
        if module:
            statement = statement.where(AuditLog.module == module)
        
        statement = statement.order_by(AuditLog.timestamp.desc()).offset(skip).limit(limit)
        
        return list(self.session.exec(statement).all())
