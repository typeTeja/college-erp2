"""
Hostel Management API Endpoints

Provides hostel management functionality
"""
from typing import Optional
from fastapi import APIRouter, Depends, Query
from sqlmodel import Session, select
from pydantic import BaseModel

from app.api.deps import get_session, get_current_active_superuser, get_current_user
from app.models.user import User
from app.models.hostel import HostelBlock, HostelRoom, BedAllocation, GatePass, HostelComplaint#, MessMenu, VisitorLog
from app.services.hostel_service import HostelService

router = APIRouter(prefix="/hostel", tags=["Hostel Management"])


# Schemas
class HostelCreate(BaseModel):
    name: str
    hostel_code: str
    hostel_type: str
    warden_id: Optional[int] = None
    monthly_rent: float = 0.0
    security_deposit: float = 0.0


class RoomCreate(BaseModel):
    hostel_id: int
    room_number: str
    floor: int
    room_type: str
    capacity: int
    rent_per_month: float = 0.0


class RoomAllocationRequest(BaseModel):
    room_id: int
    student_id: int
    academic_year: str
    bed_number: Optional[str] = None


class MaintenanceRequestCreate(BaseModel):
    room_id: int
    student_id: int
    issue_type: str
    description: str
    priority: str = "MEDIUM"


class VisitorLogCreate(BaseModel):
    student_id: int
    visitor_name: str
    visitor_phone: str
    purpose: str
    relationship: Optional[str] = None


# ============================================================================
# Hostel Management Endpoints
# ============================================================================

@router.post("/hostels")
def create_hostel(
    *,
    session: Session = Depends(get_session),
    hostel_data: HostelCreate,
    current_user: User = Depends(get_current_active_superuser)
):
    """Create hostel"""
    hostel = HostelBlock(**hostel_data.model_dump())
    session.add(hostel)
    session.commit()
    session.refresh(hostel)
    return hostel


@router.get("/hostels")
def list_hostels(
    *,
    session: Session = Depends(get_session),
    hostel_type: Optional[str] = Query(None)
):
    """List hostels"""
    stmt = select(Hostel).where(Hostel.is_active == True)
    
    if hostel_type:
        stmt = stmt.where(Hostel.hostel_type == hostel_type)
    
    return session.exec(stmt).all()


@router.get("/hostels/{hostel_id}/statistics")
def get_hostel_statistics(
    *,
    session: Session = Depends(get_session),
    hostel_id: int
):
    """Get hostel statistics"""
    return HostelService.get_hostel_statistics(session, hostel_id)


# ============================================================================
# Room Management Endpoints
# ============================================================================

@router.post("/rooms")
def create_room(
    *,
    session: Session = Depends(get_session),
    room_data: RoomCreate,
    current_user: User = Depends(get_current_active_superuser)
):
    """Create room"""
    room = HostelRoom(**room_data.model_dump())
    session.add(room)
    
    # Update hostel total rooms
    hostel = session.get(HostelBlock, room_data.block_id)
    # hostel.total_rooms += 1 # Total rooms might be computed or property now, check model
    # hostel.total_capacity += room_data.capacity
    
    session.commit()
    session.refresh(room)
    return room


@router.get("/rooms/available")
def get_available_rooms(
    *,
    session: Session = Depends(get_session),
    hostel_id: Optional[int] = Query(None),
    room_type: Optional[str] = Query(None)
):
    """Get available rooms"""
    from app.models.hostel import RoomType
    room_type_enum = RoomType(room_type) if room_type else None
    return HostelService.get_available_rooms(session, hostel_id, room_type_enum)


# ============================================================================
# Room Allocation Endpoints
# ============================================================================

@router.post("/allocations")
def allocate_room(
    *,
    session: Session = Depends(get_session),
    allocation_data: RoomAllocationRequest,
    current_user: User = Depends(get_current_user)
):
    """Allocate room to student"""
    return HostelService.allocate_room(
        session,
        allocation_data.room_id,
        allocation_data.student_id,
        allocation_data.academic_year,
        current_user.id,
        allocation_data.bed_number
    )


@router.post("/allocations/{allocation_id}/vacate")
def vacate_room(
    *,
    session: Session = Depends(get_session),
    allocation_id: int,
    remarks: Optional[str] = None
):
    """Vacate room"""
    return HostelService.vacate_room(session, allocation_id, remarks)


@router.get("/allocations")
def list_allocations(
    *,
    session: Session = Depends(get_session),
    student_id: Optional[int] = Query(None),
    hostel_id: Optional[int] = Query(None),
    # status: Optional[str] = Query(None), # BedAllocation might not have status like before
    limit: int = Query(50)
):
    """List room allocations"""
    stmt = select(BedAllocation)
    
    if student_id:
        stmt = stmt.where(BedAllocation.student_id == student_id)
    # if status:
    #     stmt = stmt.where(BedAllocation.status == status)
    if hostel_id:
        stmt = stmt.join(HostelRoom).where(HostelRoom.block_id == hostel_id)
    
    stmt = stmt.order_by(BedAllocation.allocation_date.desc()).limit(limit)
    return session.exec(stmt).all()


# ============================================================================
# Mess Menu Endpoints
# ============================================================================

# @router.post("/mess-menu")
# def create_mess_menu(
#     *,
#     session: Session = Depends(get_session),
#     hostel_id: int,
#     day_of_week: int,
#     meal_type: str,
#     menu_items: list,
#     serving_time: str,
#     current_user: User = Depends(get_current_active_superuser)
# ):
#     """Create mess menu"""
#     # menu = MessMenu(
#     #     hostel_id=hostel_id,
#     #     day_of_week=day_of_week,
#     #     meal_type=meal_type,
#     #     menu_items=str(menu_items),
#     #     serving_time=serving_time
#     # )
#     # session.add(menu)
#     # session.commit()
#     # session.refresh(menu)
#     return {"message": "Mess Menu feature temporarily disabled"}


# @router.get("/mess-menu/{hostel_id}")
# def get_mess_menu(
#     *,
#     session: Session = Depends(get_session),
#     hostel_id: int,
#     day_of_week: Optional[int] = Query(None)
# ):
#     """Get mess menu"""
#     # stmt = select(MessMenu).where(
#     #     MessMenu.hostel_id == hostel_id,
#     #     MessMenu.is_active == True
#     # )
    
#     # if day_of_week is not None:
#     #     stmt = stmt.where(MessMenu.day_of_week == day_of_week)
    
#     # return session.exec(stmt).all()
#     return []


# ============================================================================
# Visitor Management Endpoints
# ============================================================================

# @router.post("/visitors")
# def log_visitor(
#     *,
#     session: Session = Depends(get_session),
#     visitor_data: VisitorLogCreate,
#     current_user: User = Depends(get_current_user)
# ):
#     """Log visitor entry"""
#     # return HostelService.log_visitor(
#     #     session,
#     #     visitor_data.student_id,
#     #     visitor_data.visitor_name,
#     #     visitor_data.visitor_phone,
#     #     visitor_data.purpose,
#     #     current_user.id,
#     #     visitor_data.relationship
#     # )
#     return {"message": "Visitor log temporarily disabled"}


# @router.post("/visitors/{visitor_id}/checkout")
# def checkout_visitor(
#     *,
#     session: Session = Depends(get_session),
#     visitor_id: int
# ):
#     """Checkout visitor"""
#     # return HostelService.checkout_visitor(session, visitor_id)
#     return {"message": "Visitor checkout temporarily disabled"}


# ============================================================================
# Maintenance Endpoints
# ============================================================================

@router.post("/maintenance")
def create_maintenance_request(
    *,
    session: Session = Depends(get_session),
    request_data: MaintenanceRequestCreate
):
    """Create maintenance request"""
    return HostelService.create_maintenance_request(
        session,
        request_data.room_id,
        request_data.student_id,
        request_data.issue_type,
        request_data.description,
        request_data.priority
    )


@router.get("/maintenance")
def list_maintenance_requests(
    *,
    session: Session = Depends(get_session),
    status: Optional[str] = Query(None),
    priority: Optional[str] = Query(None),
    limit: int = Query(50)
):
    """List maintenance requests"""
    stmt = select(HostelComplaint)
    
    if status:
        stmt = stmt.where(HostelComplaint.status == status)
    if priority:
        stmt = stmt.where(HostelComplaint.priority == priority)
    
    stmt = stmt.order_by(HostelComplaint.created_at.desc()).limit(limit)
    return session.exec(stmt).all()
