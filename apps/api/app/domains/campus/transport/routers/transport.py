from typing import Optional, List
from fastapi import APIRouter, Depends, Query
from sqlmodel import Session, select
from pydantic import BaseModel

from app.api.deps import get_session, get_current_active_superuser
from app.models import User
from ..models.logistics import Vehicle, TransportRoute, TransportAllocation, VehicleGPSLog
from ..services.logistics import transport_logistics_service

router = APIRouter(prefix="/transport", tags=["Transport Logistics"])

# Schemas
class VehicleCreate(BaseModel):
    registration_number: str
    vehicle_type: str
    capacity: int

class RouteCreate(BaseModel):
    name: str
    code: str
    start_point: str
    end_point: str
    fare_amount: float

class TransportAllocationRequest(BaseModel):
    student_id: int
    route_id: int
    pickup_point: str
    drop_point: str
    academic_year: str
    vehicle_id: Optional[int] = None

class GPSData(BaseModel):
    vehicle_id: int
    latitude: float
    longitude: float
    speed: Optional[float] = None

# ============================================================================
# Vehicle Endpoints
# ============================================================================

@router.post("/vehicles", response_model=Vehicle)
def create_vehicle(
    *,
    session: Session = Depends(get_session),
    vehicle_data: VehicleCreate,
    current_user: User = Depends(get_current_active_superuser)
):
    """Add a new vehicle to the transport fleet"""
    vehicle = Vehicle(**vehicle_data.model_dump())
    session.add(vehicle)
    session.commit()
    session.refresh(vehicle)
    return vehicle

@router.get("/vehicles", response_model=List[Vehicle])
def list_vehicles(
    *,
    session: Session = Depends(get_session),
    is_active: bool = Query(True)
):
    """List vehicles in the fleet"""
    stmt = select(Vehicle).where(Vehicle.is_active == is_active)
    return session.exec(stmt).all()

# ============================================================================
# Route Endpoints
# ============================================================================

@router.post("/routes", response_model=TransportRoute)
def create_route(
    *,
    session: Session = Depends(get_session),
    route_data: RouteCreate,
    current_user: User = Depends(get_current_active_superuser)
):
    """Define a new transport route"""
    route = TransportRoute(**route_data.model_dump())
    session.add(route)
    session.commit()
    session.refresh(route)
    return route

@router.get("/routes", response_model=List[TransportRoute])
def list_routes(
    *,
    session: Session = Depends(get_session)
):
    """List all transport routes"""
    return session.exec(select(TransportRoute)).all()

# ============================================================================
# Allocation Endpoints
# ============================================================================

@router.post("/allocations", response_model=TransportAllocation)
def allocate_transport(
    *,
    session: Session = Depends(get_session),
    allocation_data: TransportAllocationRequest
):
    """Assign a student to a transport route and vehicle"""
    return transport_logistics_service.allocate_transport(session, allocation_data.model_dump())

@router.get("/allocations", response_model=List[TransportAllocation])
def list_allocations(
    *,
    session: Session = Depends(get_session),
    student_id: Optional[int] = Query(None),
    route_id: Optional[int] = Query(None)
):
    """List transport allocations"""
    stmt = select(TransportAllocation)
    if student_id:
        stmt = stmt.where(TransportAllocation.student_id == student_id)
    if route_id:
        stmt = stmt.where(TransportAllocation.route_id == route_id)
    return session.exec(stmt).all()

# ============================================================================
# Tracking Endpoints
# ============================================================================

@router.post("/tracking", response_model=VehicleGPSLog)
def log_gps_data(
    *,
    session: Session = Depends(get_session),
    tracking_data: GPSData
):
    """Record GPS location for a vehicle"""
    return transport_logistics_service.log_gps_data(session, tracking_data.model_dump())

# ============================================================================
# Statistics Endpoints
# ============================================================================

@router.get("/statistics/summary")
def get_fleet_statistics(
    *,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_superuser)
):
    """Get overall transport statistics"""
    return transport_logistics_service.get_fleet_statistics(session)
