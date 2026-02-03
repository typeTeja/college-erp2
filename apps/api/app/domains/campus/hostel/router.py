from typing import Optional, List
from fastapi import APIRouter, Depends, Query
from sqlmodel import Session, select
from pydantic import BaseModel

from app.api.deps import get_session, get_current_active_superuser, get_current_user
from app.models import User
from ..models import HostelBlock, HostelRoom, BedAllocation, GatePass, HostelComplaint
from .services import hostel_residency_service
from app.shared.enums import ComplaintStatus, HostelType, RoomType, GatePassStatus


router = APIRouter(prefix="/hostels", tags=["Hostel Residency"])

# Schemas
class HostelBlockCreate(BaseModel):
    name: str
    type: HostelType
    total_floors: int
    warden_name: Optional[str] = None
    contact_number: Optional[str] = None

class HostelRoomCreate(BaseModel):
    block_id: int
    room_number: str
    floor: int
    capacity: int
    room_type: RoomType = RoomType.NON_AC
    monthly_rent: float

class RoomAllocationRequest(BaseModel):
    room_id: int
    student_id: int
    bed_number: Optional[str] = None

class ComplaintCreate(BaseModel):
    room_id: int
    student_id: int
    category: str
    description: str
    priority: str = "MEDIUM"

# ============================================================================
# Hostel Block Endpoints
# ============================================================================

@router.post("/blocks", response_model=HostelBlock)
def create_hostel_block(
    *,
    session: Session = Depends(get_session),
    block_data: HostelBlockCreate,
    current_user: User = Depends(get_current_active_superuser)
):
    """Create a new hostel block"""
    block = HostelBlock(**block_data.model_dump())
    session.add(block)
    session.commit()
    session.refresh(block)
    return block

@router.get("/blocks", response_model=List[HostelBlock])
def list_hostel_blocks(
    *,
    session: Session = Depends(get_session),
    type: Optional[HostelType] = Query(None)
):
    """List all hostel blocks"""
    stmt = select(HostelBlock)
    if type:
        stmt = stmt.where(HostelBlock.type == type)
    return session.exec(stmt).all()

@router.get("/blocks/{block_id}/statistics")
def get_block_statistics(
    *,
    session: Session = Depends(get_session),
    block_id: int
):
    """Get residency statistics for a block"""
    return hostel_residency_service.get_hostel_statistics(session, block_id)

# ============================================================================
# Room Endpoints
# ============================================================================

@router.post("/rooms", response_model=HostelRoom)
def create_room(
    *,
    session: Session = Depends(get_session),
    room_data: HostelRoomCreate,
    current_user: User = Depends(get_current_active_superuser)
):
    """Create a room in a hostel block"""
    room = HostelRoom(**room_data.model_dump())
    session.add(room)
    session.commit()
    session.refresh(room)
    return room

@router.get("/rooms/available", response_model=List[HostelRoom])
def get_available_rooms(
    *,
    session: Session = Depends(get_session),
    block_id: Optional[int] = Query(None),
    room_type: Optional[RoomType] = Query(None)
):
    """Get available rooms for allocation"""
    return hostel_residency_service.get_available_rooms(session, block_id, room_type)

# ============================================================================
# Allocation Endpoints
# ============================================================================

@router.post("/allocations", response_model=BedAllocation)
def allocate_room(
    *,
    session: Session = Depends(get_session),
    allocation_data: RoomAllocationRequest,
    current_user: User = Depends(get_current_user)
):
    """Allocate a bed to a student"""
    return hostel_residency_service.allocate_room(
        session,
        allocation_data.room_id,
        allocation_data.student_id,
        allocation_data.bed_number
    )

@router.post("/allocations/{allocation_id}/vacate", response_model=BedAllocation)
def vacate_room(
    *,
    session: Session = Depends(get_session),
    allocation_id: int
):
    """Deactivate a room allocation (Student vacating)"""
    return hostel_residency_service.vacate_room(session, allocation_id)

# ============================================================================
# Complaint Endpoints
# ============================================================================

@router.post("/complaints", response_model=HostelComplaint)
def create_complaint(
    *,
    session: Session = Depends(get_session),
    complaint_data: ComplaintCreate
):
    """Submit a residency-related complaint/maintenance request"""
    return hostel_residency_service.create_complaint(
        session,
        complaint_data.room_id,
        complaint_data.student_id,
        complaint_data.category,
        complaint_data.description,
        complaint_data.priority
    )

@router.get("/complaints", response_model=List[HostelComplaint])
def list_complaints(
    *,
    session: Session = Depends(get_session),
    status: Optional[ComplaintStatus] = Query(None),
    limit: int = Query(50)
):
    """List hostel residency complaints"""
    stmt = select(HostelComplaint)
    if status:
        stmt = stmt.where(HostelComplaint.status == status)
    stmt = stmt.order_by(HostelComplaint.created_at.desc()).limit(limit)
    return session.exec(stmt).all()
