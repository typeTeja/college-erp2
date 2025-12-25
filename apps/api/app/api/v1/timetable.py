from typing import Any, List, Optional
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlmodel import Session, select, func, and_
from app.api.deps import get_current_user, get_session
from app.models.user import User
from app.models.timetable import (
    TimeSlot, Classroom, ClassSchedule, ClassAdjustment, 
    TimetableTemplate, DayOfWeek, AdjustmentStatus
)
from app.schemas.timetable import (
    TimeSlotCreate, TimeSlotRead,
    ClassroomCreate, ClassroomRead,
    ClassScheduleCreate, ClassScheduleRead,
    ClassAdjustmentCreate, ClassAdjustmentRead, ClassAdjustmentUpdate,
    TimetableTemplateCreate, TimetableTemplateRead
)

router = APIRouter()

# --- Time Slots ---
@router.post("/slots", response_model=TimeSlotRead)
def create_time_slot(
    *, session: Session = Depends(get_session), slot_in: TimeSlotCreate, current_user: User = Depends(get_current_user)
) -> Any:
    """Create a time slot (Admin only)"""
    slot = TimeSlot.model_validate(slot_in)
    session.add(slot)
    session.commit()
    session.refresh(slot)
    return slot

@router.get("/slots", response_model=List[TimeSlotRead])
def get_time_slots(
    *, session: Session = Depends(get_session), current_user: User = Depends(get_current_user)
) -> Any:
    return session.exec(select(TimeSlot)).all()

# --- Utility: Validation ---
def validate_conflict(
    session: Session, 
    day: DayOfWeek, 
    period_id: int, 
    faculty_id: Optional[int] = None, 
    room_id: Optional[int] = None,
    exclude_entry_id: Optional[int] = None
):
    # Check Faculty Conflict
    if faculty_id:
        query = select(ClassSchedule).where(
            ClassSchedule.day_of_week == day,
            ClassSchedule.period_id == period_id,
            ClassSchedule.faculty_id == faculty_id
        )
        if exclude_entry_id:
            query = query.where(ClassSchedule.id != exclude_entry_id)
        if session.exec(query).first():
            raise HTTPException(status_code=400, detail="Faculty already booked for this slot")

    # Check Room Conflict
    if room_id:
        query = select(ClassSchedule).where(
            ClassSchedule.day_of_week == day,
            ClassSchedule.period_id == period_id,
            ClassSchedule.room_id == room_id
        )
        if exclude_entry_id:
            query = query.where(ClassSchedule.id != exclude_entry_id)
        if session.exec(query).first():
            raise HTTPException(status_code=400, detail="Room already occupied for this slot")

@router.post("/validate")
def validate_schedule_entry(
    *, 
    session: Session = Depends(get_session), 
    entry: ClassScheduleCreate, 
    current_user: User = Depends(get_current_user)
) -> Any:
    validate_conflict(
        session, 
        entry.day_of_week, 
        entry.period_id, 
        entry.faculty_id, 
        entry.room_id
    )
    return {"status": "valid"}

# --- Timetable Management ---

@router.post("/entries", response_model=ClassScheduleRead)
def create_schedule_entry(
    *, session: Session = Depends(get_session), entry_in: ClassScheduleCreate, current_user: User = Depends(get_current_user)
) -> Any:
    """Add a class to the timetable"""
    validate_conflict(session, entry_in.day_of_week, entry_in.period_id, entry_in.faculty_id, entry_in.room_id)
    
    db_entry = ClassSchedule.model_validate(entry_in)
    session.add(db_entry)
    session.commit()
    session.refresh(db_entry)
    return db_entry

@router.get("/entries", response_model=List[ClassScheduleRead])
def get_schedule(
    *, 
    session: Session = Depends(get_session), 
    academic_year_id: int, 
    semester_id: int, 
    section_id: Optional[int] = None,
    current_user: User = Depends(get_current_user)
) -> Any:
    """Get timetable for a class"""
    query = select(ClassSchedule).where(
        ClassSchedule.academic_year_id == academic_year_id,
        ClassSchedule.semester_id == semester_id
    )
    if section_id:
        query = query.where(ClassSchedule.section_id == section_id)
    
    return session.exec(query).all()

@router.get("/faculty/{faculty_id}", response_model=List[ClassScheduleRead])
def get_faculty_schedule(
    *, session: Session = Depends(get_session), faculty_id: int, current_user: User = Depends(get_current_user)
) -> Any:
    """Get schedule for a specific faculty"""
    return session.exec(select(ClassSchedule).where(ClassSchedule.faculty_id == faculty_id)).all()

# --- Adjustments / Substitution ---

@router.post("/adjustments", response_model=ClassAdjustmentRead)
def request_adjustment(
    *, session: Session = Depends(get_session), adj_in: ClassAdjustmentCreate, current_user: User = Depends(get_current_user)
) -> Any:
    """Request a substitution"""
    # Verify original entry exists
    entry = session.get(ClassSchedule, adj_in.timetable_entry_id)
    if not entry:
        raise HTTPException(status_code=404, detail="Timetable entry not found")
        
    adj = ClassAdjustment.model_validate(adj_in)
    session.add(adj)
    session.commit()
    session.refresh(adj)
    return adj

@router.get("/adjustments/pending", response_model=List[ClassAdjustmentRead])
def get_pending_adjustments(
    *, session: Session = Depends(get_session), current_user: User = Depends(get_current_user)
) -> Any:
    """Get pending adjustments (for admin/HOD/Substitute to review)"""
    return session.exec(select(ClassAdjustment).where(ClassAdjustment.status == AdjustmentStatus.REQUESTED)).all()

@router.put("/adjustments/{id}", response_model=ClassAdjustmentRead)
def update_adjustment(
    *, 
    session: Session = Depends(get_session), 
    id: int, 
    update_in: ClassAdjustmentUpdate, 
    current_user: User = Depends(get_current_user)
) -> Any:
    """Approve/Reject substitution"""
    adj = session.get(ClassAdjustment, id)
    if not adj:
        raise HTTPException(status_code=404, detail="Adjustment request not found")
        
    adj.status = update_in.status
    if update_in.substitute_faculty_id:
        adj.substitute_faculty_id = update_in.substitute_faculty_id
        
    session.add(adj)
    session.commit()
    session.refresh(adj)
    return adj
