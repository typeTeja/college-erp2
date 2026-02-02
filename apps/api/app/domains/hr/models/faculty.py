from typing import TYPE_CHECKING, List, Optional
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from app.domains.academic.models.regulation import Subject
    from app.models.user import User

class Faculty(SQLModel, table=True):
    """Faculty information model - HR Domain Member"""
    __tablename__ = "faculty"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: Optional[int] = Field(default=None, foreign_key="user.id", index=True)
    name: str
    department: Optional[str] = None
    designation: Optional[str] = None # Will be linked to HR.Designation later
    qualification: Optional[str] = None
    phone: Optional[str] = Field(default=None, index=True)
    email: Optional[str] = Field(default=None, index=True)
    max_weekly_hours: int = Field(default=20)  # Workload limit
    
    # Relationships
    subjects: List["Subject"] = Relationship(back_populates="faculty")
