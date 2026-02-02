from typing import List, Optional, Dict
from datetime import datetime
from sqlmodel import Session, select
from fastapi import HTTPException

from ..models.infrastructure import HostelBlock, HostelRoom, BedAllocation, RoomType
from ..models.operations import HostelComplaint, ComplaintStatus
from app.domains.student.models.student import Student

class HostelResidencyService:
    """Service for hostel residency operations (Residency Owner)"""
    
    @staticmethod
    def allocate_room(
        session: Session,
        room_id: int,
        student_id: int,
        bed_number: Optional[str] = None
    ) -> BedAllocation:
        """Allocate room to student"""
        room = session.get(HostelRoom, room_id)
        if not room:
            raise HTTPException(status_code=404, detail="Room not found")
        
        if not room.is_active:
             raise HTTPException(status_code=400, detail="Room is not active")

        if room.current_occupancy >= room.capacity:
            raise HTTPException(status_code=400, detail="Room is full")
        
        student = session.get(Student, student_id)
        if not student:
            raise HTTPException(status_code=404, detail="Student not found")
        
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
        
        allocation = BedAllocation(
            room_id=room_id,
            student_id=student_id,
            bed_number=bed_number or "UNASSIGNED",
            allocation_date=datetime.utcnow(),
            is_active=True
        )
        
        room.current_occupancy += 1
        
        session.add(allocation)
        session.add(room)
        session.commit()
        session.refresh(allocation)
        return allocation
    
    @staticmethod
    def vacate_room(
        session: Session,
        allocation_id: int
    ) -> BedAllocation:
        """Vacate room"""
        allocation = session.get(BedAllocation, allocation_id)
        if not allocation:
            raise HTTPException(status_code=404, detail="Allocation not found")
        
        if not allocation.is_active:
            raise HTTPException(status_code=400, detail="Allocation not active")
        
        allocation.is_active = False
        allocation.deallocation_date = datetime.utcnow()
        
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
        block_id: Optional[int] = None,
        room_type: Optional[RoomType] = None
    ) -> List[HostelRoom]:
        """Get available rooms"""
        stmt = select(HostelRoom).where(HostelRoom.is_active == True)
        
        if block_id:
            stmt = stmt.where(HostelRoom.block_id == block_id)
        if room_type:
            stmt = stmt.where(HostelRoom.room_type == room_type)
        
        rooms = session.exec(stmt).all()
        return [r for r in rooms if r.current_occupancy < r.capacity]
    
    @staticmethod
    def create_complaint(
        session: Session,
        room_id: int,
        student_id: int,
        category: str,
        description: str,
        priority: str = "MEDIUM"
    ) -> HostelComplaint:
        """Create a maintenance complaint for the hostel"""
        complaint = HostelComplaint(
            room_id=room_id,
            student_id=student_id,
            category=category,
            description=description,
            priority=priority,
            status=ComplaintStatus.OPEN
        )
        
        session.add(complaint)
        session.commit()
        session.refresh(complaint)
        return complaint
    
    @staticmethod
    def get_hostel_statistics(
        session: Session,
        block_id: int
    ) -> Dict:
        """Get residency statistics for a hostel block"""
        block = session.get(HostelBlock, block_id)
        if not block:
            raise HTTPException(status_code=404, detail="Hostel block not found")
        
        rooms = block.rooms
        total_rooms = len(rooms)
        total_capacity = sum(r.capacity for r in rooms)
        occupied_count = sum(r.current_occupancy for r in rooms)
        
        stmt = select(HostelComplaint).where(
            HostelComplaint.status == ComplaintStatus.OPEN
        ).join(HostelRoom).where(HostelRoom.block_id == block_id)
        pending_complaints = len(session.exec(stmt).all())
        
        occupancy_rate = (occupied_count / total_capacity * 100) if total_capacity > 0 else 0
        
        return {
            "block_id": block_id,
            "total_rooms": total_rooms,
            "total_capacity": total_capacity,
            "occupied_count": occupied_count,
            "available_capacity": total_capacity - occupied_count,
            "occupancy_rate": round(occupancy_rate, 2),
            "pending_complaints": pending_complaints
        }

hostel_residency_service = HostelResidencyService()
