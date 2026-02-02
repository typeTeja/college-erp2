from typing import Optional, TYPE_CHECKING
from datetime import datetime
from sqlmodel import SQLModel, Field

if TYPE_CHECKING:
    from app.models.department import Department

class Designation(SQLModel, table=True):
    """Designation Management - HR Foundational Structure"""
    __tablename__ = "designation"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(unique=True, index=True)  # e.g., "Professor", "Assistant Professor"
    code: str = Field(unique=True, index=True)
    
    level: int = Field(default=1)  # Hierarchy level
    department_id: Optional[int] = Field(default=None, foreign_key="department.id")
    
    min_experience_years: int = Field(default=0)
    min_qualification: Optional[str] = None
    
    is_teaching: bool = Field(default=True)
    is_active: bool = Field(default=True)
    display_order: int = Field(default=0)
    
    created_at: datetime = Field(default_factory=datetime.utcnow)
