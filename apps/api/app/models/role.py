from typing import TYPE_CHECKING, List, Optional
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from .user import User

# Import UserRole for link_model
from .user_role import UserRole

class Role(SQLModel, table=True):
    """Role-based access control model"""
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True, unique=True)
    description: Optional[str] = None
    
    # Relationships
    users: List["User"] = Relationship(back_populates="roles", link_model=UserRole)
