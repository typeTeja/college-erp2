from typing import Optional, TYPE_CHECKING
from enum import Enum
from datetime import datetime
from sqlmodel import SQLModel, Field, Column, JSON, Text
from app.shared.enums import ComplaintStatus, GatePassStatus, GatePassType


if TYPE_CHECKING:
    from app.domains.student.models.student import Student
    from .infrastructure import HostelRoom


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
