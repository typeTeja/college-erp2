from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.api.deps import get_current_user, get_session
from app.models.user import User
from app.models.student import Student
from app.models.subject import Subject
from app.models.exam import (
    Exam, ExamSchedule, ExamResult, ExamStatus
)
from app.schemas.exam import (
    ExamCreate, ExamRead, ExamUpdate,
    ExamScheduleCreate, ExamScheduleRead, ExamScheduleUpdate,
    ExamResultCreate, ExamResultRead, BulkMarksEntry
)

router = APIRouter()

# --- Exam Management ---

@router.post("/", response_model=ExamRead)
def create_exam(
    *,
    session: Session = Depends(get_session),
    exam_in: ExamCreate,
    current_user: User = Depends(get_current_user),
) -> Any:
    """Create a new exam cycle."""
    # Check permissions (Admin only)
    # if not current_user.is_superuser: ...
    
    exam = Exam.model_validate(exam_in)
    session.add(exam)
    session.commit()
    session.refresh(exam)
    return exam

@router.get("/", response_model=List[ExamRead])
def get_exams(
    *,
    session: Session = Depends(get_session),
    skip: int = 0,
    limit: int = 100,
    semester_id: int = None,
    current_user: User = Depends(get_current_user),
) -> Any:
    """List exams."""
    query = select(Exam)
    if semester_id:
        query = query.where(Exam.semester_id == semester_id)
    
    query = query.offset(skip).limit(limit).order_by(Exam.start_date.desc())
    return session.exec(query).all()

@router.get("/{exam_id}", response_model=ExamRead)
def get_exam(
    *,
    session: Session = Depends(get_session),
    exam_id: int,
    current_user: User = Depends(get_current_user),
) -> Any:
    """Get exam details."""
    exam = session.get(Exam, exam_id)
    if not exam:
        raise HTTPException(status_code=404, detail="Exam not found")
    return exam

# --- Exam Schedule ---

@router.post("/{exam_id}/schedules", response_model=ExamScheduleRead)
def create_exam_schedule(
    *,
    session: Session = Depends(get_session),
    exam_id: int,
    schedule_in: ExamScheduleCreate,
    current_user: User = Depends(get_current_user),
) -> Any:
    """Add a subject to an exam schedule."""
    if schedule_in.exam_id != exam_id:
        raise HTTPException(status_code=400, detail="Exam ID mismatch")
        
    schedule = ExamSchedule.model_validate(schedule_in)
    session.add(schedule)
    session.commit()
    session.refresh(schedule)
    return schedule

@router.get("/{exam_id}/schedules", response_model=List[ExamScheduleRead])
def get_exam_schedules(
    *,
    session: Session = Depends(get_session),
    exam_id: int,
    current_user: User = Depends(get_current_user),
) -> Any:
    """Get timetable for an exam."""
    schedules = session.exec(
        select(ExamSchedule).where(ExamSchedule.exam_id == exam_id)
    ).all()
    
    # Enrich with Subject names
    results = []
    for sched in schedules:
        sched_read = ExamScheduleRead.model_validate(sched)
        if sched.subject:
            sched_read.subject_name = sched.subject.name
        results.append(sched_read)
        
    return results

# --- Marks Entry ---

@router.post("/marks/bulk", response_model=List[ExamResultRead])
def bulk_enter_marks(
    *,
    session: Session = Depends(get_session),
    bulk_in: BulkMarksEntry,
    current_user: User = Depends(get_current_user),
) -> Any:
    """Bulk entry of marks for a specific exam schedule."""
    schedule = session.get(ExamSchedule, bulk_in.exam_schedule_id)
    if not schedule:
        raise HTTPException(status_code=404, detail="Exam schedule not found")
        
    created_results = []
    
    for record_in in bulk_in.records:
        if record_in.exam_schedule_id != bulk_in.exam_schedule_id:
            continue

        # Check existing result
        existing = session.exec(
            select(ExamResult)
            .where(ExamResult.exam_schedule_id == bulk_in.exam_schedule_id)
            .where(ExamResult.student_id == record_in.student_id)
        ).first()
        
        if existing:
            existing.marks_obtained = record_in.marks_obtained
            existing.grade = record_in.grade
            existing.remarks = record_in.remarks
            existing.is_absent = record_in.is_absent
            session.add(existing)
            created_results.append(existing)
        else:
            result = ExamResult.model_validate(record_in)
            session.add(result)
            created_results.append(result)
            
    session.commit()
    for res in created_results:
        session.refresh(res)
        
    return created_results

@router.get("/{exam_schedule_id}/students", response_model=List[Any])
def get_students_for_exam_schedule(
    *,
    session: Session = Depends(get_session),
    exam_schedule_id: int,
    current_user: User = Depends(get_current_user),
) -> Any:
    """Get list of students eligible for an exam schedule (enrolled in the subject)."""
    schedule = session.get(ExamSchedule, exam_schedule_id)
    if not schedule:
        raise HTTPException(status_code=404, detail="Exam schedule not found")
        
    # Find students enrolled in the subject
    # Assuming Enrollment model links student and subject
    from app.models.enrollment import Enrollment
    from app.models.student import Student
    
    statement = (
        select(Student)
        .join(Enrollment, Enrollment.student_id == Student.id)
        .where(Enrollment.subject_id == schedule.subject_id)
        # Optional: Filter by academic year matching the exam?
        # .where(Enrollment.academic_year == schedule.exam.academic_year) 
    )
    
    students = session.exec(statement).all()
    
    # Return basic student info needed for marks entry
    return [{"id": s.id, "name": s.name, "admission_number": s.admission_number} for s in students]

@router.get("/student/{student_id}/results", response_model=List[ExamResultRead])
def get_student_results(
    *,
    session: Session = Depends(get_session),
    student_id: int,
    current_user: User = Depends(get_current_user),
) -> Any:
    """Get all exam results for a student."""
    results = session.exec(
        select(ExamResult).where(ExamResult.student_id == student_id)
    ).all()
    
    # Enrich data
    enriched_results = []
    for res in results:
        read_obj = ExamResultRead.model_validate(res)
        if res.exam_schedule:
            if res.exam_schedule.exam:
                read_obj.exam_name = res.exam_schedule.exam.name
            if res.exam_schedule.subject:
                read_obj.subject_name = res.exam_schedule.subject.name
        enriched_results.append(read_obj)
        
    return enriched_results
