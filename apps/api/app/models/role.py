from typing import TYPE_CHECKING, List, Optional
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from .user import User

# Import UserRole and RolePermission for link_models
from .user_role import UserRole
from .permission import RolePermission

class Role(SQLModel, table=True):
    """Role-based access control model"""
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True, unique=True)
    description: Optional[str] = None
    is_system: bool = Field(default=False)
    is_active: bool = Field(default=True)
    
    # Relationships
    users: List["User"] = Relationship(back_populates="roles", link_model=UserRole)
    permissions: List["Permission"] = Relationship(back_populates="roles", link_model=RolePermission)
