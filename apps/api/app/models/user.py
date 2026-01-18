from typing import TYPE_CHECKING, List, Optional
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship, Column, JSON

if TYPE_CHECKING:
    from .role import Role
    
# Import UserRole for link_model
# It uses forward refs for User/Role so it's safe to import here
from .user_role import UserRole

class User(SQLModel, table=True):
    """User authentication and profile model"""
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True)
    email: str = Field(index=True, unique=True)
    phone: Optional[str] = Field(default=None, index=True)
    full_name: Optional[str] = None
    hashed_password: str
    is_active: bool = Field(default=True)
    is_superuser: bool = Field(default=False)
    
    # Password reset fields
    password_reset_token: Optional[str] = None
    password_reset_expires: Optional[datetime] = None
    
    # Preferences (JSON store for notifications, theme, etc.)
    preferences: Optional[dict] = Field(default_factory=dict, sa_column=Column(JSON))
    
    # Timestamps
    last_login: Optional[datetime] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    roles: List["Role"] = Relationship(back_populates="users", link_model=UserRole)
