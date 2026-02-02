from typing import List, Optional, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship
from datetime import date

if TYPE_CHECKING:
    from app.models.operations import Shift
    from app.models.user import User

class StaffBase(SQLModel):
    name: str
    email: str = Field(unique=True, index=True)
    mobile: str = Field(unique=True)
    department: Optional[str] = None
    designation: str # Will be linked to HR.Designation later
    join_date: date
    shift_id: Optional[int] = Field(default=None, foreign_key="shift.id")
    is_active: bool = True

class Staff(StaffBase, table=True):
    """Staff Management Model - HR Domain Member"""
    __tablename__ = "staff"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: Optional[int] = Field(default=None, foreign_key="user.id")
    
    # Relationships
    shift: Optional["Shift"] = Relationship(back_populates="staff_members")
    # user: Optional["User"] = Relationship() # Explicit ref if needed
