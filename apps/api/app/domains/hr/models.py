"""
HR Domain Models

All database models for the HR domain including:
- Designation (job titles and roles)
- Staff (non-teaching employees)
- Faculty (teaching staff)
"""

from typing import TYPE_CHECKING, List, Optional
from datetime import datetime, date
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from app.models.department import Department
    from app.models.operations import Shift
    from app.domains.system.models import User
    from app.domains.academic.models import Subject


# ----------------------------------------------------------------------
# Core Models
# ----------------------------------------------------------------------

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


class StaffBase(SQLModel):
    """Base model for staff"""
    name: str
    email: str = Field(unique=True, index=True)
    mobile: str = Field(unique=True)
    department: Optional[str] = None
    designation: str  # Will be linked to HR.Designation later
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


class Faculty(SQLModel, table=True):
    """Faculty information model - HR Domain Member"""
    __tablename__ = "faculty"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: Optional[int] = Field(default=None, foreign_key="user.id", index=True)
    name: str
    department: Optional[str] = None
    designation: Optional[str] = None  # Will be linked to HR.Designation later
    qualification: Optional[str] = None
    phone: Optional[str] = Field(default=None, index=True)
    email: Optional[str] = Field(default=None, index=True)
    max_weekly_hours: int = Field(default=20)  # Workload limit
    
    # Relationships
    subjects: List["Subject"] = Relationship(back_populates="faculty")
