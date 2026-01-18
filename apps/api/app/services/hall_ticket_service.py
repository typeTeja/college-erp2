"""
Hall Ticket Service Layer

Handles business logic for hall ticket generation including:
- Eligibility checking
- PDF generation
- QR code generation
- Bulk generation
- Download tracking
"""
from typing import List, Optional, Dict
from datetime import datetime
import qrcode
from io import BytesIO
import base64
from sqlmodel import Session, select
from fastapi import HTTPException

from app.models.academic.hall_ticket import (
    HallTicketConfig, HallTicket, DisciplineBlock,
    HallTicketStatus, BlockReason
)
from app.models.student import Student
from app.models.fee import StudentFee


class HallTicketService:
    """Service for hall ticket operations"""
    
    @staticmethod
    def check_eligibility(
        session: Session,
        student_id: int,
        config_id: int
    ) -> Dict:
        """Check if student is eligible for hall ticket"""
        student = session.get(Student, student_id)
        if not student:
            raise HTTPException(status_code=404, detail="Student not found")
        
        issues = []
        is_eligible = True
        
        # Check for active discipline blocks
        stmt = select(DisciplineBlock).where(
            DisciplineBlock.student_id == student_id,
            DisciplineBlock.is_active == True
        )
        blocks = session.exec(stmt).all()
        
        if blocks:
            is_eligible = False
            for block in blocks:
                issues.append({
                    "type": "discipline_block",
                    "reason": block.block_reason,
                    "description": block.block_description
                })
        
        # Check fee dues
        stmt = select(StudentFee).where(
            StudentFee.student_id == student_id,
            StudentFee.total_pending > 0
        )
        fee_dues = session.exec(stmt).all()
        
        if fee_dues:
            total_pending = sum(f.total_pending for f in fee_dues)
            if total_pending > 0:
                is_eligible = False
                issues.append({
                    "type": "fee_dues",
                    "amount": float(total_pending),
                    "description": f"Pending fee amount: ₹{total_pending}"
                })
        
        # Check if already generated
        stmt = select(HallTicket).where(
            HallTicket.student_id == student_id,
            HallTicket.hall_ticket_config_id == config_id,
            HallTicket.status != HallTicketStatus.CANCELLED
        )
        existing = session.exec(stmt).first()
        
        if existing:
            issues.append({
                "type": "already_generated",
                "hall_ticket_number": existing.hall_ticket_number,
                "description": "Hall ticket already generated"
            })
        
        return {
            "student_id": student_id,
            "is_eligible": is_eligible,
            "issues": issues
        }
    
    @staticmethod
    def generate_qr_code(data: str) -> str:
        """Generate QR code and return base64 encoded image"""
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(data)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Convert to base64
        buffer = BytesIO()
        img.save(buffer, format='PNG')
        img_str = base64.b64encode(buffer.getvalue()).decode()
        
        return f"data:image/png;base64,{img_str}"
    
    @staticmethod
    def generate_hall_ticket_number(
        session: Session,
        config: HallTicketConfig,
        student: Student
    ) -> str:
        """Generate unique hall ticket number"""
        # Format: HT-{YEAR}-{EXAM_CODE}-{SEQUENCE}
        year = config.academic_year.split('-')[0]
        
        # Get count of existing hall tickets for this config
        stmt = select(HallTicket).where(
            HallTicket.hall_ticket_config_id == config.id
        )
        count = len(session.exec(stmt).all())
        
        sequence = str(count + 1).zfill(6)
        return f"HT-{year}-{config.exam_code}-{sequence}"
    
    @staticmethod
    def generate_hall_ticket(
        session: Session,
        student_id: int,
        config_id: int,
        generated_by: int,
        force: bool = False
    ) -> HallTicket:
        """Generate hall ticket for a student"""
        # Check eligibility
        if not force:
            eligibility = HallTicketService.check_eligibility(session, student_id, config_id)
            if not eligibility["is_eligible"]:
                raise HTTPException(
                    status_code=400,
                    detail=f"Student not eligible: {eligibility['issues']}"
                )
        
        # Get student and config
        student = session.get(Student, student_id)
        config = session.get(HallTicketConfig, config_id)
        
        if not student or not config:
            raise HTTPException(status_code=404, detail="Student or config not found")
        
        # Generate hall ticket number
        hall_ticket_number = HallTicketService.generate_hall_ticket_number(
            session, config, student
        )
        
        # Generate QR code
        qr_data = f"{hall_ticket_number}|{student.admission_number}|{config.exam_code}"
        qr_code_url = HallTicketService.generate_qr_code(qr_data)
        
        # Create hall ticket
        hall_ticket = HallTicket(
            student_id=student_id,
            hall_ticket_config_id=config_id,
            hall_ticket_number=hall_ticket_number,
            student_name=student.name,
            admission_number=student.admission_number,
            program_name=student.program.name if student.program else "N/A",
            year=student.current_year or 1,
            semester=student.current_semester or 1,
            photo_url=student.photo_url,
            qr_code_url=qr_code_url,
            generated_by=generated_by
        )
        
        session.add(hall_ticket)
        session.commit()
        session.refresh(hall_ticket)
        
        # TODO: Generate PDF in background task
        # hall_ticket.pdf_url = generate_pdf(hall_ticket, config)
        
        return hall_ticket
    
    @staticmethod
    def bulk_generate(
        session: Session,
        config_id: int,
        student_ids: List[int],
        generated_by: int,
        force: bool = False
    ) -> Dict:
        """Bulk generate hall tickets"""
        results = {
            "success": [],
            "failed": []
        }
        
        for student_id in student_ids:
            try:
                hall_ticket = HallTicketService.generate_hall_ticket(
                    session, student_id, config_id, generated_by, force
                )
                results["success"].append({
                    "student_id": student_id,
                    "hall_ticket_number": hall_ticket.hall_ticket_number
                })
            except Exception as e:
                results["failed"].append({
                    "student_id": student_id,
                    "error": str(e)
                })
        
        return results
    
    @staticmethod
    def track_download(
        session: Session,
        hall_ticket_id: int
    ) -> HallTicket:
        """Track hall ticket download"""
        hall_ticket = session.get(HallTicket, hall_ticket_id)
        if not hall_ticket:
            raise HTTPException(status_code=404, detail="Hall ticket not found")
        
        hall_ticket.download_count += 1
        hall_ticket.last_downloaded_at = datetime.utcnow()
        
        if not hall_ticket.first_downloaded_at:
            hall_ticket.first_downloaded_at = datetime.utcnow()
            hall_ticket.status = HallTicketStatus.DOWNLOADED
        
        session.commit()
        session.refresh(hall_ticket)
        return hall_ticket
    
    @staticmethod
    def cancel_hall_ticket(
        session: Session,
        hall_ticket_id: int,
        cancelled_by: int,
        reason: str
    ) -> HallTicket:
        """Cancel a hall ticket"""
        hall_ticket = session.get(HallTicket, hall_ticket_id)
        if not hall_ticket:
            raise HTTPException(status_code=404, detail="Hall ticket not found")
        
        hall_ticket.status = HallTicketStatus.CANCELLED
        hall_ticket.cancelled_at = datetime.utcnow()
        hall_ticket.cancelled_by = cancelled_by
        hall_ticket.cancellation_reason = reason
        
        session.commit()
        session.refresh(hall_ticket)
        return hall_ticket
    
    @staticmethod
    def reissue_hall_ticket(
        session: Session,
        hall_ticket_id: int,
        reissued_by: int,
        reason: str
    ) -> HallTicket:
        """Reissue a hall ticket"""
        old_ticket = session.get(HallTicket, hall_ticket_id)
        if not old_ticket:
            raise HTTPException(status_code=404, detail="Hall ticket not found")
        
        # Cancel old ticket
        old_ticket.status = HallTicketStatus.CANCELLED
        old_ticket.cancelled_at = datetime.utcnow()
        old_ticket.cancelled_by = reissued_by
        old_ticket.cancellation_reason = f"Reissued: {reason}"
        
        # Generate new ticket
        new_ticket = HallTicketService.generate_hall_ticket(
            session,
            old_ticket.student_id,
            old_ticket.hall_ticket_config_id,
            reissued_by,
            force=True
        )
        
        new_ticket.status = HallTicketStatus.REISSUED
        new_ticket.reissued_at = datetime.utcnow()
        new_ticket.reissued_by = reissued_by
        new_ticket.reissue_reason = reason
        
        session.commit()
        return new_ticket
    
    @staticmethod
    def block_student(
        session: Session,
        student_id: int,
        block_reason: BlockReason,
        description: str,
        blocked_by: int
    ) -> DisciplineBlock:
        """Block a student from hall ticket generation"""
        block = DisciplineBlock(
            student_id=student_id,
            block_reason=block_reason,
            block_description=description,
            blocked_by=blocked_by
        )
        
        session.add(block)
        session.commit()
        session.refresh(block)
        return block
    
    @staticmethod
    def unblock_student(
        session: Session,
        block_id: int,
        unblocked_by: int,
        remarks: str
    ) -> DisciplineBlock:
        """Unblock a student"""
        block = session.get(DisciplineBlock, block_id)
        if not block:
            raise HTTPException(status_code=404, detail="Block not found")
        
        block.is_active = False
        block.unblocked_by = unblocked_by
        block.unblocked_at = datetime.utcnow()
        block.unblock_remarks = remarks
        
        session.commit()
        session.refresh(block)
        return block
