from typing import Optional
from sqlmodel import Field, SQLModel, Relationship
from datetime import date

class StaffBase(SQLModel):
    name: str
    email: str = Field(unique=True, index=True)
    mobile: str = Field(unique=True)
    department: Optional[str] = None
    designation: str
    join_date: date
    shift_id: Optional[int] = Field(default=None, foreign_key="shift.id")
    is_active: bool = True

class Staff(StaffBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: Optional[int] = Field(default=None, foreign_key="user.id")
    
    # Relationships
    shift: Optional["Shift"] = Relationship(back_populates="staff_members")
    # user relationship will be defined in User model or solved via foreign key directly

class StaffCreate(StaffBase):
    pass

class StaffRead(StaffBase):
    id: int
    user_id: Optional[int]

class StaffUpdate(SQLModel):
    name: Optional[str] = None
    email: Optional[str] = None
    mobile: Optional[str] = None
    department: Optional[str] = None
    designation: Optional[str] = None
    shift_id: Optional[int] = None
    is_active: Optional[bool] = None
