from typing import Optional, List
from datetime import time, datetime
from pydantic import BaseModel
from app.models.operations import TicketStatus, TicketPriority
from app.schemas.staff import StaffRead
from app.shared.enums import TicketPriority, TicketStatus


# --- Shift ---
class ShiftBase(BaseModel):
    name: str
    start_time: time
    end_time: time
    description: Optional[str] = None

class ShiftCreate(ShiftBase):
    pass

class ShiftRead(ShiftBase):
    id: int

# --- Maintenance Ticket ---
class MaintenanceTicketBase(BaseModel):
    title: str
    description: Optional[str] = None
    location: str
    priority: TicketPriority = TicketPriority.MEDIUM

class MaintenanceTicketCreate(MaintenanceTicketBase):
    pass

class MaintenanceTicketUpdate(BaseModel):
    status: Optional[TicketStatus] = None
    assigned_to_id: Optional[int] = None
    description: Optional[str] = None

class MaintenanceTicketRead(MaintenanceTicketBase):
    id: int
    status: TicketStatus
    created_at: datetime
    updated_at: datetime
    reported_by_id: int
    assigned_to_id: Optional[int]
    assigned_to: Optional[StaffRead] = None
