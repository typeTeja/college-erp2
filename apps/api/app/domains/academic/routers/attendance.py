from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select, func
from app.api.deps import get_current_user, get_session
from app.models.user import User
from app.domains.academic.models import AttendanceSession, AttendanceRecord, AttendanceStatus
from app.schemas.attendance import (
    AttendanceSessionCreate,
    AttendanceSessionRead,
    AttendanceSessionUpdate,
    BulkAttendanceCreate,
    AttendanceStats,
    AttendanceRecordRead
)

router = APIRouter()

@router.post("/sessions", response_model=AttendanceSessionRead)
def create_session(
    *,
    session: Session = Depends(get_session),
    session_in: AttendanceSessionCreate,
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Create a new attendance session.
    """
    attendance_session = AttendanceSession.model_validate(session_in)
    session.add(attendance_session)
    session.commit()
    session.refresh(attendance_session)
    return attendance_session

@router.get("/sessions", response_model=List[AttendanceSessionRead])
def get_sessions(
    *,
    session: Session = Depends(get_session),
    skip: int = 0,
    limit: int = 100,
    faculty_id: int = None,
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Retrieve attendance sessions.
    """
    query = select(AttendanceSession)
    if faculty_id:
        query = query.where(AttendanceSession.faculty_id == faculty_id)
    
    query = query.offset(skip).limit(limit).order_by(AttendanceSession.session_date.desc())
    return session.exec(query).all()

@router.get("/sessions/{session_id}", response_model=AttendanceSessionRead)
def get_session_by_id(
    *,
    session: Session = Depends(get_session),
    session_id: int,
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Get attendance session by ID.
    """
    attendance_session = session.get(AttendanceSession, session_id)
    if not attendance_session:
        raise HTTPException(status_code=404, detail="Attendance session not found")
    return attendance_session

@router.post("/mark", response_model=List[AttendanceRecordRead])
def mark_bulk_attendance(
    *,
    session: Session = Depends(get_session),
    bulk_in: BulkAttendanceCreate,
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Mark attendance for multiple students in a session.
    """
    attendance_session = session.get(AttendanceSession, bulk_in.session_id)
    if not attendance_session:
        raise HTTPException(status_code=404, detail="Attendance session not found")

    created_records = []
    
    # Process each record
    for record_in in bulk_in.records:
        # Check if record already exists for this student and session
        existing_record = session.exec(
            select(AttendanceRecord)
            .where(AttendanceRecord.session_id == bulk_in.session_id)
            .where(AttendanceRecord.student_id == record_in.student_id)
        ).first()

        if existing_record:
            # Update existing
            existing_record.status = record_in.status
            existing_record.remarks = record_in.remarks
            session.add(existing_record)
            created_records.append(existing_record)
        else:
            # Create new
            record = AttendanceRecord(
                session_id=bulk_in.session_id,
                student_id=record_in.student_id,
                status=record_in.status,
                remarks=record_in.remarks
            )
            session.add(record)
            created_records.append(record)
    
    session.commit()
    for record in created_records:
        session.refresh(record)
        
    return created_records

@router.get("/student/{student_id}/stats", response_model=AttendanceStats)
def get_student_stats(
    *,
    session: Session = Depends(get_session),
    student_id: int,
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Get attendance statistics for a student.
    """
    records = session.exec(
        select(AttendanceRecord).where(AttendanceRecord.student_id == student_id)
    ).all()
    
    total_classes = len(records)
    if total_classes == 0:
        return AttendanceStats(
            total_classes=0, present=0, absent=0, late=0, on_duty=0, attendance_percentage=0.0
        )
        
    present = sum(1 for r in records if r.status == AttendanceStatus.PRESENT)
    absent = sum(1 for r in records if r.status == AttendanceStatus.ABSENT)
    late = sum(1 for r in records if r.status == AttendanceStatus.LATE)
    on_duty = sum(1 for r in records if r.status == AttendanceStatus.ON_DUTY)
    
    # Consider PRESENT, LATE, and ON_DUTY as present for calculation
    effective_present = present + late + on_duty
    percentage = (effective_present / total_classes) * 100
    
    return AttendanceStats(
        total_classes=total_classes,
        present=present,
        absent=absent,
        late=late,
        on_duty=on_duty,
        attendance_percentage=round(percentage, 2)
    )

@router.get("/student/{student_id}/history", response_model=List[AttendanceRecordRead])
def get_student_history(
    *,
    session: Session = Depends(get_session),
    student_id: int,
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Get attendance history for a student.
    """
    query = select(AttendanceRecord).where(AttendanceRecord.student_id == student_id)
    query = query.order_by(AttendanceRecord.created_at.desc()).offset(skip).limit(limit)
    return session.exec(query).all()
