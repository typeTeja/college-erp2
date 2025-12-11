from typing import Optional
from sqlmodel import SQLModel, Field

class UserRole(SQLModel, table=True):
    """Link table for User-Role many-to-many relationship"""
    __tablename__ = "user_role"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id", index=True)
    role_id: int = Field(foreign_key="role.id", index=True)
