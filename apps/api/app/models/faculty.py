from typing import TYPE_CHECKING, List, Optional
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from .subject import Subject

class Faculty(SQLModel, table=True):
    """Faculty information model"""
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: Optional[int] = Field(default=None, foreign_key="user.id", index=True)
    name: str
    department: Optional[str] = None
    qualification: Optional[str] = None
    phone: Optional[str] = Field(default=None, index=True)
    email: Optional[str] = Field(default=None, index=True)
    
    # Relationships
    subjects: List["Subject"] = Relationship(back_populates="faculty")
