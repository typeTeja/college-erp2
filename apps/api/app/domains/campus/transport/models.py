from typing import Optional, List, TYPE_CHECKING
from datetime import datetime, date
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from app.domains.student.models.student import Student

class Vehicle(SQLModel, table=True):
    """Transport Fleet - Vehicle Identity ownership"""
    __tablename__ = "transport_vehicle"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    registration_number: str = Field(unique=True, index=True)
    vehicle_type: str  # Bus, Van, etc.
    capacity: int
    is_active: bool = Field(default=True)
    
    allocations: List["TransportAllocation"] = Relationship(back_populates="vehicle")
    tracking_logs: List["VehicleGPSLog"] = Relationship(back_populates="vehicle")

class TransportRoute(SQLModel, table=True):
    """Logistics Flow - Path and pricing for commute"""
    __tablename__ = "transport_route"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    code: str = Field(unique=True, index=True)
    start_point: str
    end_point: str
    fare_amount: float
    is_active: bool = Field(default=True)
    
    allocations: List["TransportAllocation"] = Relationship(back_populates="route")

class TransportAllocation(SQLModel, table=True):
    """Commute Assignment - Linking student to logistics"""
    __tablename__ = "transport_allocation"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    student_id: int = Field(foreign_key="student.id", index=True)
    route_id: int = Field(foreign_key="transport_route.id", index=True)
    vehicle_id: Optional[int] = Field(default=None, foreign_key="transport_vehicle.id")
    
    pickup_point: str
    drop_point: str
    academic_year: str
    status: str = Field(default="ACTIVE") # ACTIVE, CANCELLED, EXPIRED
    
    # Relationships
    route: TransportRoute = Relationship(back_populates="allocations")
    vehicle: Optional[Vehicle] = Relationship(back_populates="allocations")

class VehicleGPSLog(SQLModel, table=True):
    """GPS Telemetry - Real-time vehicle tracking data"""
    __tablename__ = "vehicle_gps_log"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    vehicle_id: int = Field(foreign_key="transport_vehicle.id", index=True)
    latitude: float
    longitude: float
    speed: Optional[float] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    
    vehicle: Vehicle = Relationship(back_populates="tracking_logs")
