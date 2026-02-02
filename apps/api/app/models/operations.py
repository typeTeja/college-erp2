from typing import Optional, List
from sqlmodel import Field, SQLModel, Relationship
from datetime import time, datetime
from enum import Enum
from app.shared.enums import TicketPriority, TicketStatus


# --- Shift Models ---
class ShiftBase(SQLModel):
    name: str # e.g., "Morning Shift", "Night Watch"
    start_time: time
    end_time: time
    description: Optional[str] = None

class Shift(ShiftBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    
    staff_members: List["Staff"] = Relationship(back_populates="shift")

class ShiftCreate(ShiftBase):
    pass

class ShiftRead(ShiftBase):
    id: int

# --- Maintenance Ticket Models ---
class MaintenanceTicketBase(SQLModel):
    title: str
    description: Optional[str] = None
    location: str # e.g., "Lab 1", "Library AC"
    priority: TicketPriority = TicketPriority.MEDIUM
    status: TicketStatus = TicketStatus.OPEN

class MaintenanceTicket(MaintenanceTicketBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    reported_by_id: int = Field(foreign_key="user.id")
    assigned_to_id: Optional[int] = Field(default=None, foreign_key="staff.id")

class MaintenanceTicketCreate(MaintenanceTicketBase):
    pass

class MaintenanceTicketRead(MaintenanceTicketBase):
    id: int
    created_at: datetime
    updated_at: datetime
    reported_by_id: int
    assigned_to_id: Optional[int]

class MaintenanceTicketUpdate(SQLModel):
    status: Optional[TicketStatus] = None
    assigned_to_id: Optional[int] = None
    description: Optional[str] = None
