from typing import TYPE_CHECKING, List, Optional
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from .program import Program

class Department(SQLModel, table=True):
    """Academic department model"""
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True, unique=True)
    code: str = Field(index=True, unique=True)
    description: Optional[str] = None
    
    # Relationships
    programs: List["Program"] = Relationship(back_populates="department")
