from typing import List, Optional, Dict
from datetime import datetime
from sqlmodel import Session, select, func
from fastapi import HTTPException

from .models import Vehicle, TransportRoute, TransportAllocation, VehicleGPSLog
from app.domains.student.models import Student

class TransportLogisticsService:
    """Service for transport logistics operations (Logistics Owner)"""
    
    @staticmethod
    def allocate_transport(
        session: Session,
        allocation_data: Dict
    ) -> TransportAllocation:
        """Allocate transport to student"""
        student_id = allocation_data["student_id"]
        route_id = allocation_data["route_id"]
        
        student = session.get(Student, student_id)
        if not student:
            raise HTTPException(status_code=404, detail="Student not found")
        
        route = session.get(TransportRoute, route_id)
        if not route:
            raise HTTPException(status_code=404, detail="Route not found")
        
        # Check existing allocation
        stmt = select(TransportAllocation).where(
            TransportAllocation.student_id == student_id,
            TransportAllocation.status == "ACTIVE"
        )
        existing = session.exec(stmt).first()
        if existing:
            raise HTTPException(status_code=400, detail="Student already has active transport")
        
        # Check vehicle capacity if vehicle_id provided
        if allocation_data.get("vehicle_id"):
            vehicle = session.get(Vehicle, allocation_data["vehicle_id"])
            if not vehicle:
                raise HTTPException(status_code=404, detail="Vehicle not found")
            
            # Count current active allocations for this vehicle
            count_stmt = select(func.count(TransportAllocation.id)).where(
                TransportAllocation.vehicle_id == vehicle.id,
                TransportAllocation.status == "ACTIVE"
            )
            current_count = session.exec(count_stmt).one()
            if current_count >= vehicle.capacity:
                raise HTTPException(status_code=400, detail="Vehicle is at full capacity")
        
        allocation = TransportAllocation(**allocation_data)
        session.add(allocation)
        session.commit()
        session.refresh(allocation)
        return allocation
    
    @staticmethod
    def log_gps_data(
        session: Session,
        gps_data: Dict
    ) -> VehicleGPSLog:
        """Record vehicle GPS tracking data"""
        vehicle = session.get(Vehicle, gps_data["vehicle_id"])
        if not vehicle:
            raise HTTPException(status_code=404, detail="Vehicle not found")
        
        log = VehicleGPSLog(**gps_data)
        session.add(log)
        session.commit()
        session.refresh(log)
        return log
    
    @staticmethod
    def get_fleet_statistics(session: Session) -> Dict:
        """Get overall transport fleet statistics"""
        total_vehicles = session.exec(select(func.count(Vehicle.id))).one()
        active_vehicles = session.exec(select(func.count(Vehicle.id)).where(Vehicle.is_active == True)).one()
        total_routes = session.exec(select(func.count(TransportRoute.id))).one()
        active_allocations = session.exec(select(func.count(TransportAllocation.id)).where(TransportAllocation.status == "ACTIVE")).one()
        
        return {
            "total_vehicles": total_vehicles,
            "active_vehicles": active_vehicles,
            "total_routes": total_routes,
            "active_allocations": active_allocations
        }

transport_logistics_service = TransportLogisticsService()

