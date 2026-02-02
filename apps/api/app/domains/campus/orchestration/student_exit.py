from typing import Dict, Optional
from sqlmodel import Session
from fastapi import HTTPException

from ..hostel.services import hostel_residency_service
from ..library.services import library_circulation_service
from ..transport.services import transport_logistics_service
from ..inventory.services import inventory_service

class StudentExitOrchestrator:
    """
    Coordinates the process of a student leaving the institution.
    Rule: COORDINATION ONLY. No business rules computed here.
    """
    
    @staticmethod
    def process_full_exit(
        session: Session,
        student_id: int
    ) -> Dict:
        """
        Sequence of checks and actions across Campus subdomains for student exit.
        """
        # 1. Check Library Dues/Books
        # Note: In a real system, we might query a read model or service
        library_stats = library_circulation_service.get_member_statistics(session, student_id)
        if library_stats["currently_issued"] > 0:
            return {
                "status": "BLOCKED",
                "reason": f"Student has {library_stats['currently_issued']} books pending return in Library.",
                "domain": "library"
            }
            
        # 2. Check Hostel Residency
        # We need to find the active allocation
        from ..hostel.models.infrastructure import BedAllocation
        from sqlmodel import select
        stmt = select(BedAllocation).where(BedAllocation.student_id == student_id, BedAllocation.is_active == True)
        hostel_allocation = session.exec(stmt).first()
        
        if hostel_allocation:
            # We don't vacate here, we just flag it
            return {
                "status": "BLOCKED",
                "reason": "Student has an active Hostel room allocation. Please vacate first.",
                "domain": "hostel"
            }
            
        # 3. Check Transport Pass
        from ..transport.models.logistics import TransportAllocation
        stmt = select(TransportAllocation).where(TransportAllocation.student_id == student_id, TransportAllocation.status == "ACTIVE")
        transport_allocation = session.exec(stmt).first()
        
        # 4. Success - Clear to exit Campus domains
        return {
            "status": "CLEARED",
            "message": "Student is cleared from all Campus & Infrastructure domains.",
            "details": {
                "library": "No pending books",
                "hostel": "No active allocation",
                "transport": "Transport pass checked"
            }
        }

student_exit_orchestrator = StudentExitOrchestrator()
