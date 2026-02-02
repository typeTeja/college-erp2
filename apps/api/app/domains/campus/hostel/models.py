"""
Hostel Domain Models

Infrastructure and operations models for hostel management.
"""

from typing import Optional, List, TYPE_CHECKING
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship, Column, JSON, Text
from app.shared.enums import (
    HostelType, RoomType, ComplaintStatus, 
    GatePassStatus, GatePassType
)


if TYPE_CHECKING:
    from app.domains.student.models.student import Student
    from app.models.faculty import Faculty


# ======================================================================
# Infrastructure Models
# ======================================================================

class HostelBlock(SQLModel, table=True):
    """Hostel Block - Infrastructure Owner for Residency"""
    __tablename__ = "hostel_block"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(unique=True, index=True)
    type: HostelType
    total_floors: int
    warden_name: Optional[str] = None
    contact_number: Optional[str] = None
    
    rooms: List["HostelRoom"] = Relationship(back_populates="block")


class HostelRoom(SQLModel, table=True):
    """Hostel Room - Resident Living Space"""
    __tablename__ = "hostel_room"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    block_id: int = Field(foreign_key="hostel_block.id")
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
    """Bed Assignment - Specific student residency record"""
    __tablename__ = "bed_allocation"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    room_id: int = Field(foreign_key="hostel_room.id")
    bed_number: str
    student_id: Optional[int] = Field(default=None, foreign_key="student.id")
    faculty_id: Optional[int] = Field(default=None, foreign_key="faculty.id")
    allocation_date: datetime = Field(default_factory=datetime.utcnow)
    deallocation_date: Optional[datetime] = None
    is_active: bool = Field(default=True)
    
    room: HostelRoom = Relationship(back_populates="allocations")


# ======================================================================
# Operations Models
# ======================================================================

class GatePass(SQLModel, table=True):
    """Gate Pass - Student mobility permission"""
    __tablename__ = "gate_pass"
    
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
    """Hostel Complaint - Residency-related service request"""
    __tablename__ = "hostel_complaint"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    student_id: int = Field(foreign_key="student.id")
    room_id: int = Field(foreign_key="hostel_room.id")
    category: str  # Plumbing, Electrical, Cleaning, etc.
    description: str = Field(sa_column=Column(Text))
    priority: str = Field(default="MEDIUM") # LOW, MEDIUM, HIGH, URGENT
    status: ComplaintStatus = Field(default=ComplaintStatus.OPEN)
    resolution_note: Optional[str] = Field(default=None, sa_column=Column(Text))
    resolved_at: Optional[datetime] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
