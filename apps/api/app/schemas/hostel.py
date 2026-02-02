from typing import Optional, List
from pydantic import BaseModel
from datetime import datetime
from app.models.hostel import HostelType, RoomType, GatePassType, GatePassStatus, ComplaintStatus
from app.shared.enums import ComplaintStatus, GatePassStatus, GatePassType, HostelType, RoomType


# --- Block Schemas ---
class HostelBlockBase(BaseModel):
    name: str
    type: HostelType
    total_floors: int
    warden_name: Optional[str] = None
    contact_number: Optional[str] = None

class HostelBlockCreate(HostelBlockBase):
    pass

class HostelBlockRead(HostelBlockBase):
    id: int

# --- Room Schemas ---
class HostelRoomBase(BaseModel):
    block_id: int
    room_number: str
    floor: int
    capacity: int
    room_type: RoomType = RoomType.NON_AC
    monthly_rent: float

class HostelRoomCreate(HostelRoomBase):
    pass

class HostelRoomRead(HostelRoomBase):
    id: int
    current_occupancy: int
    is_active: bool

# --- Allocation Schemas ---
class BedAllocationBase(BaseModel):
    room_id: int
    bed_number: str
    student_id: Optional[int] = None
    faculty_id: Optional[int] = None

class BedAllocationCreate(BedAllocationBase):
    pass

class BedAllocationRead(BedAllocationBase):
    id: int
    allocation_date: datetime
    deallocation_date: Optional[datetime] = None
    is_active: bool

# --- GatePass Schemas ---
class GatePassBase(BaseModel):
    student_id: int
    type: GatePassType
    out_time: datetime
    expected_in_time: datetime
    reason: str

class GatePassCreate(GatePassBase):
    pass

class GatePassRead(GatePassBase):
    id: int
    actual_in_time: Optional[datetime] = None
    status: GatePassStatus
    approved_by: Optional[int] = None
    remarks: Optional[str] = None

# --- Complaint Schemas ---
class HostelComplaintBase(BaseModel):
    student_id: int
    room_id: int
    category: str
    description: str
    priority: str = "MEDIUM"

class HostelComplaintCreate(HostelComplaintBase):
    pass

class HostelComplaintRead(HostelComplaintBase):
    id: int
    status: ComplaintStatus
    resolution_note: Optional[str] = None
    resolved_at: Optional[datetime] = None
    created_at: datetime
