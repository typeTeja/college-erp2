"""
Auth Domain Models

Authentication and Authorization models following DDD principles.
"""

from typing import Optional, List, TYPE_CHECKING
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    pass


class UserRole(SQLModel, table=True):
    """Link table for AuthUser-Role relationship"""
    __tablename__ = "user_role"
    
    user_id: int = Field(foreign_key="users.id", primary_key=True)
    role_id: int = Field(foreign_key="role.id", primary_key=True)
    assigned_at: datetime = Field(default_factory=datetime.utcnow)


class RolePermission(SQLModel, table=True):
    """Link table for Role-Permission relationship"""
    __tablename__ = "role_permission"
    
    role_id: int = Field(foreign_key="role.id", primary_key=True)
    permission_id: int = Field(foreign_key="permission.id", primary_key=True)
    assigned_at: datetime = Field(default_factory=datetime.utcnow)


class AuthUser(SQLModel, table=True):
    """
    Authentication User - Auth Domain
    
    Renamed from User to AuthUser to clarify this is auth-specific.
    Table name remains 'users' for backward compatibility.
    
    Business domains reference this via auth_user_id foreign key.
    """
    __tablename__ = "users"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True)
    email: str = Field(index=True, unique=True)
    hashed_password: str
    full_name: Optional[str] = None
    
    # Status
    is_active: bool = Field(default=True)
    is_superuser: bool = Field(default=False)
    
    # Password reset
    password_reset_token: Optional[str] = None
    password_reset_expires: Optional[datetime] = None
    
    # Audit
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    last_login: Optional[datetime] = None
    
    # Relationships
    roles: List["Role"] = Relationship(back_populates="users", link_model=UserRole)


class Role(SQLModel, table=True):
    """
    Role for RBAC - Auth Domain
    
    Examples: ADMIN, FACULTY, STUDENT, HOD, PRINCIPAL
    """
    __tablename__ = "role"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True, unique=True)
    description: Optional[str] = None
    is_system: bool = Field(default=False)  # System roles cannot be deleted
    
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    users: List[AuthUser] = Relationship(back_populates="roles", link_model=UserRole)
    permissions: List["Permission"] = Relationship(back_populates="roles", link_model=RolePermission)


class Permission(SQLModel, table=True):
    """
    Action-based permissions - Auth Domain
    
    Semantic, action-based permissions (NOT route-based).
    Examples:
    - EXAM_MARK_ENTRY
    - STUDENT_ADMISSION_APPROVE
    - FEE_PAYMENT_VERIFY
    - ATTENDANCE_MARK
    - TIMETABLE_MANAGE
    """
    __tablename__ = "permission"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True, unique=True)  # e.g., "EXAM_MARK_ENTRY"
    description: Optional[str] = None
    category: Optional[str] = None  # e.g., "ACADEMIC", "FINANCE", "ADMISSION"
    
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    roles: List[Role] = Relationship(back_populates="permissions", link_model=RolePermission)
