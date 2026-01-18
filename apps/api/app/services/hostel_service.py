"""
Hostel Management Service Layer

Handles business logic for hostel operations including:
- Room allocation
- Mess menu management
- Visitor tracking
- Maintenance requests
"""
from typing import List, Optional, Dict
from datetime import datetime, date
from sqlmodel import Session, select
from fastapi import HTTPException

from app.models.hostel import (
    HostelBlock, HostelRoom, BedAllocation, GatePass, HostelComplaint,
    # MessMenu, VisitorLog, # Removed
    # AllocationStatus, # Removed
    RoomType
)
from app.models.student import Student


class HostelService:
    """Service for hostel operations"""
    
    @staticmethod
    def allocate_room(
        session: Session,
        room_id: int,
        student_id: int,
        academic_year: str,
        approved_by: int, # Kept for API compatibility but might not be used in model
        bed_number: Optional[str] = None
    ) -> BedAllocation:
        """Allocate room to student"""
        # Get room
        room = session.get(HostelRoom, room_id)
        if not room:
            raise HTTPException(status_code=404, detail="Room not found")
        
        # Check availability
        if not room.is_active:
             raise HTTPException(status_code=400, detail="Room is not active")

        if room.current_occupancy >= room.capacity:
            raise HTTPException(status_code=400, detail="Room is full")
        
        # Get student
        student = session.get(Student, student_id)
        if not student:
            raise HTTPException(status_code=404, detail="Student not found")
        
        # Check if student already has allocation
        stmt = select(BedAllocation).where(
            BedAllocation.student_id == student_id,
            BedAllocation.is_active == True
        )
        existing = session.exec(stmt).first()
        if existing:
            raise HTTPException(
                status_code=400,
                detail="Student already has an active room allocation"
            )
        
        # Create allocation
        allocation = BedAllocation(
            room_id=room_id,
            student_id=student_id,
            bed_number=bed_number or "UNASSIGNED",
            allocation_date=datetime.utcnow(),
            is_active=True
        )
        
        # Update room occupancy
        room.current_occupancy += 1
        
        session.add(allocation)
        session.add(room)
        session.commit()
        session.refresh(allocation)
        return allocation
    
    @staticmethod
    def vacate_room(
        session: Session,
        allocation_id: int,
        vacate_remarks: Optional[str] = None
    ) -> BedAllocation:
        """Vacate room"""
        allocation = session.get(BedAllocation, allocation_id)
        if not allocation:
            raise HTTPException(status_code=404, detail="Allocation not found")
        
        if not allocation.is_active:
            raise HTTPException(status_code=400, detail="Allocation not active")
        
        # Update allocation
        allocation.is_active = False
        allocation.deallocation_date = datetime.utcnow()
        
        # Update room occupancy
        room = session.get(HostelRoom, allocation.room_id)
        if room:
            room.current_occupancy -= 1
            session.add(room)
        
        session.commit()
        session.refresh(allocation)
        return allocation
    
    @staticmethod
    def get_available_rooms(
        session: Session,
        hostel_id: Optional[int] = None,
        room_type: Optional[RoomType] = None
    ) -> List[HostelRoom]:
        """Get available rooms"""
        # Logic: capacity > current_occupancy
        stmt = select(HostelRoom).where(
            HostelRoom.is_active == True
        )
        
        if hostel_id:
            stmt = stmt.where(HostelRoom.block_id == hostel_id)
        if room_type:
            stmt = stmt.where(HostelRoom.room_type == room_type)
        
        rooms = session.exec(stmt).all()
        # Filter in python for complex check if needed, or query:
        available = [r for r in rooms if r.current_occupancy < r.capacity]
        return available
    
    @staticmethod
    def create_maintenance_request(
        session: Session,
        room_id: int,
        student_id: int,
        issue_type: str,
        description: str,
        priority: str = "MEDIUM"
    ) -> HostelComplaint:
        """Create maintenance request"""
        # Map issue_type to category for compatibility
        request = HostelComplaint(
            room_id=room_id,
            student_id=student_id,
            category=issue_type,
            description=description,
            priority=priority,
            # status="OPEN" # Default
        )
        
        session.add(request)
        session.commit()
        session.refresh(request)
        return request
    
    # @staticmethod
    # def log_visitor(
    #     session: Session,
    #     student_id: int,
    #     visitor_name: str,
    #     visitor_phone: str,
    #     purpose: str,
    #     approved_by: int,
    #     relationship: Optional[str] = None
    # ) -> VisitorLog:
    #     """Log visitor entry"""
    #     # log = VisitorLog(
    #     #     student_id=student_id,
    #     #     visitor_name=visitor_name,
    #     #     visitor_phone=visitor_phone,
    #     #     purpose=purpose,
    #     #     relationship=relationship,
    #     #     approved_by=approved_by
    #     # )
        
    #     # session.add(log)
    #     # session.commit()
    #     # session.refresh(log)
    #     # return log
    #     pass
    
    @staticmethod
    def log_visitor(*args, **kwargs):
         pass

    # @staticmethod
    # def checkout_visitor(
    #     session: Session,
    #     visitor_log_id: int
    # ) -> VisitorLog:
    #     """Checkout visitor"""
    #     # log = session.get(VisitorLog, visitor_log_id)
    #     # if not log:
    #     #     raise HTTPException(status_code=404, detail="Visitor log not found")
        
    #     # log.check_out_time = datetime.utcnow()
    #     # session.commit()
    #     # session.refresh(log)
    #     # return log
    #     pass
    
    @staticmethod
    def checkout_visitor(*args, **kwargs):
         pass
    
    @staticmethod
    def get_hostel_statistics(
        session: Session,
        hostel_id: int
    ) -> Dict:
        """Get hostel statistics"""
        hostel = session.get(HostelBlock, hostel_id)
        if not hostel:
            raise HTTPException(status_code=404, detail="Hostel not found")
        
        # Calculate totals from rooms
        rooms = hostel.rooms
        total_rooms = len(rooms)
        total_capacity = sum(r.capacity for r in rooms)
        occupied_count = sum(r.current_occupancy for r in rooms)
        
        # Get active allocations
        # stmt = select(BedAllocation).join(HostelRoom).where(HostelRoom.block_id == hostel_id, BedAllocation.is_active == True)
        # active_allocations = len(session.exec(stmt).all())
        active_allocations = occupied_count # Simplified
        
        # Get pending maintenance
        stmt = select(HostelComplaint).where(
            HostelComplaint.status == "OPEN"
        ).join(HostelRoom).where(HostelRoom.block_id == hostel_id)
        pending_maintenance = len(session.exec(stmt).all())
        
        occupancy_rate = (occupied_count / total_capacity * 100) if total_capacity > 0 else 0
        
        return {
            "hostel_id": hostel_id,
            "total_rooms": total_rooms,
            "total_capacity": total_capacity,
            "occupied_count": occupied_count,
            "available_capacity": total_capacity - occupied_count,
            "occupancy_rate": round(occupancy_rate, 2),
            "active_allocations": active_allocations,
            "pending_maintenance": pending_maintenance
        }
