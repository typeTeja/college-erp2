from enum import Enum
from typing import Optional, List, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime

if TYPE_CHECKING:
    from .student import Student
    from .faculty import Faculty

class HostelType(str, Enum):
    BOYS = "BOYS"
    GIRLS = "GIRLS"
    STAFF = "STAFF"
    GUEST = "GUEST"

class RoomType(str, Enum):
    AC = "AC"
    NON_AC = "NON_AC"
    SUITE = "SUITE"

class GatePassType(str, Enum):
    LOCAL = "LOCAL"
    HOME = "HOME"
    EMERGENCY = "EMERGENCY"

class GatePassStatus(str, Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    OUT = "OUT"
    RETURNED = "RETURNED"
    EXPIRED = "EXPIRED"

class ComplaintStatus(str, Enum):
    OPEN = "OPEN"
    IN_PROGRESS = "IN_PROGRESS"
    RESOLVED = "RESOLVED"
    CLOSED = "CLOSED"

# --- Infrastructure ---

class HostelBlock(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(unique=True, index=True)
    type: HostelType
    total_floors: int
    warden_name: Optional[str] = None
    contact_number: Optional[str] = None
    
    rooms: List["HostelRoom"] = Relationship(back_populates="block")

class HostelRoom(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    block_id: int = Field(foreign_key="hostelblock.id")
    room_number: str = Field(index=True)
    floor: int
    capacity: int
    current_occupancy: int = Field(default=0)
    room_type: RoomType = Field(default=RoomType.NON_AC)
    monthly_rent: float
    is_active: bool = Field(default=True)

    block: HostelBlock = Relationship(back_populates="rooms")
    allocations: List["BedAllocation"] = Relationship(back_populates="room")

class BedAllocation(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    room_id: int = Field(foreign_key="hostelroom.id")
    bed_number: str
    student_id: Optional[int] = Field(default=None, foreign_key="student.id")
    faculty_id: Optional[int] = Field(default=None, foreign_key="faculty.id")
    allocation_date: datetime = Field(default_factory=datetime.utcnow)
    deallocation_date: Optional[datetime] = None
    is_active: bool = Field(default=True)
    
    room: HostelRoom = Relationship(back_populates="allocations")

# --- Operations ---

class GatePass(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    student_id: int = Field(foreign_key="student.id")
    type: GatePassType
    out_time: datetime
    expected_in_time: datetime
    actual_in_time: Optional[datetime] = None
    reason: str
    status: GatePassStatus = Field(default=GatePassStatus.PENDING)
    approved_by: Optional[int] = Field(default=None, foreign_key="user.id")
    remarks: Optional[str] = None

class HostelComplaint(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    student_id: int = Field(foreign_key="student.id")
    room_id: int = Field(foreign_key="hostelroom.id")
    category: str  # Plumbing, Electrical, Cleaning, etc.
    description: str
    priority: str = Field(default="MEDIUM") # LOW, MEDIUM, HIGH, URGENT
    status: ComplaintStatus = Field(default=ComplaintStatus.OPEN)
    resolution_note: Optional[str] = None
    resolved_at: Optional[datetime] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
