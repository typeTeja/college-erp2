from typing import List, Optional
from datetime import datetime, date, time
from sqlmodel import Session, select, and_
from fastapi import HTTPException

from app.domains.academic.models.attendance import AttendanceSession, AttendanceRecord
from app.domains.academic.schemas import (
    AttendanceSessionCreate, 
    AttendanceRecordCreate,
    BulkAttendanceMark
)
from app.shared.enums import AttendanceStatus, SessionStatus

class AttendanceService:
    """Service for handling attendance operations"""
    
    @staticmethod
    def create_session(session: Session, data: AttendanceSessionCreate) -> AttendanceSession:
        """Create a new attendance session"""
        
        # Convert str times to time objects if necessary
        start_time = data.start_time
        if isinstance(start_time, str):
            h, m = map(int, start_time.split(':'))
            start_time = time(hour=h, minute=m)
            
        end_time = data.end_time
        if isinstance(end_time, str):
            h, m = map(int, end_time.split(':'))
            end_time = time(hour=h, minute=m)
            
        db_session = AttendanceSession(
            subject_id=data.subject_id,
            faculty_id=data.faculty_id,
            program_id=data.program_id,
            program_year_id=data.program_year_id,
            semester=data.semester,
            section=data.section,
            practical_batch_id=data.practical_batch_id,
            session_date=data.session_date,
            start_time=start_time,
            end_time=end_time,
            status=data.status
        )
        
        session.add(db_session)
        session.commit()
        session.refresh(db_session)
        return db_session

    @staticmethod
    def mark_bulk_attendance(session: Session, data: BulkAttendanceMark) -> List[AttendanceRecord]:
        """Mark attendance for multiple students in a session"""
        
        # Verify session exists
        db_session = session.get(AttendanceSession, data.session_id)
        if not db_session:
            raise HTTPException(status_code=404, detail="Attendance session not found")
            
        records = []
        for record_data in data.attendance_data:
            # Check if record already exists (to avoid duplicates or handle updates)
            existing = session.exec(
                select(AttendanceRecord).where(
                    and_(
                        AttendanceRecord.session_id == data.session_id,
                        AttendanceRecord.student_id == record_data.student_id
                    )
                )
            ).first()
            
            if existing:
                existing.status = record_data.status
                existing.remarks = record_data.remarks
                existing.updated_at = datetime.utcnow()
                records.append(existing)
            else:
                new_record = AttendanceRecord(
                    session_id=data.session_id,
                    student_id=record_data.student_id,
                    status=record_data.status,
                    remarks=record_data.remarks
                )
                session.add(new_record)
                records.append(new_record)
        
        # Update session status to COMPLETED if it was SCHEDULED
        if db_session.status == SessionStatus.SCHEDULED:
            db_session.status = SessionStatus.COMPLETED
            db_session.updated_at = datetime.utcnow()
            
        session.commit()
        for r in records:
            session.refresh(r)
            
        return records

    @staticmethod
    def get_session_attendance(session: Session, session_id: int) -> List[AttendanceRecord]:
        """Get all attendance records for a specific session"""
        return session.exec(
            select(AttendanceRecord).where(AttendanceRecord.session_id == session_id)
        ).all()

    @staticmethod
    def get_student_attendance_summary(session: Session, student_id: int, subject_id: Optional[int] = None):
        """Get attendance summary for a student"""
        statement = select(AttendanceRecord).where(AttendanceRecord.student_id == student_id)
        if subject_id:
             statement = statement.join(AttendanceSession).where(AttendanceSession.subject_id == subject_id)
             
        records = session.exec(statement).all()
        
        total = len(records)
        present = len([r for r in records if r.status == AttendanceStatus.PRESENT])
        percentage = (present / total * 100) if total > 0 else 0
        
        return {
            "total_sessions": total,
            "present_count": present,
            "percentage": percentage
        }

attendance_service = AttendanceService()
