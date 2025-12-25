from typing import TYPE_CHECKING, List, Optional
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from .role import Role
    from .user import User

class RolePermission(SQLModel, table=True):
    """Link table for Role-Permission many-to-many relationship"""
    __tablename__ = "role_permission"
    
    role_id: int = Field(foreign_key="role.id", primary_key=True)
    permission_id: int = Field(foreign_key="permission.id", primary_key=True)

class Permission(SQLModel, table=True):
    """Granular permission model"""
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True, unique=True)  # e.g., "admissions:read"
    description: Optional[str] = None
    module: str = Field(index=True)  # e.g., "Admissions", "Fees" (for grouping)
    
    # Relationships
    roles: List["Role"] = Relationship(back_populates="permissions", link_model=RolePermission)

class PermissionAuditLog(SQLModel, table=True):
    """Logs changes to role permissions for compliance"""
    __tablename__ = "permission_audit_log"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    actor_id: int = Field(foreign_key="user.id", index=True)
    role_id: int = Field(foreign_key="role.id", index=True)
    action: str  # "ADD_PERMISSION", "REMOVE_PERMISSION"
    permission_name: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    actor: "User" = Relationship()
    role: "Role" = Relationship()
