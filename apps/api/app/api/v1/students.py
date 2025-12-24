from typing import Any, List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select, func
from sqlalchemy.orm import selectinload

from app.api.deps import get_current_user, get_session
from app.models.user import User
from app.models.student import Student, StudentStatus
from app.models.program import Program
from app.schemas.student import StudentResponse, StudentListResponse

router = APIRouter()

@router.get("/", response_model=StudentListResponse)
def read_students(
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
    page: int = 1,
    limit: int = 10,
    search: Optional[str] = None,
    program_id: Optional[int] = None,
    batch: Optional[str] = None,
    section: Optional[str] = None,
    status: Optional[StudentStatus] = None,
) -> Any:
    """
    Retrieve students with pagination, search, and filtering.
    """
    # Base query
    query = select(Student).options(selectinload(Student.program))
    
    # Filters
    if search:
        # Search by name or admission number case-insensitive
        query = query.where(
            (Student.name.ilike(f"%{search}%")) | 
            (Student.admission_number.ilike(f"%{search}%"))
        )
        
    if program_id:
        query = query.where(Student.program_id == program_id)
        
    if batch:
        query = query.where(Student.batch == batch)
        
    if section:
        query = query.where(Student.section == section)
        
    if status:
        query = query.where(Student.status == status)

    # Count total
    # Efficient count without loading all data? 
    # For simplicity in SQLModel, we might need a separate count query or fetch all IDs.
    # A standard way with sqlalchemy func.count:
    count_query = select(func.count()).select_from(query.subquery())
    total = session.exec(count_query).one()
    
    # Pagination
    offset = (page - 1) * limit
    query = query.offset(offset).limit(limit)
    
    students = session.exec(query).all()
    
    # Map to response (flattening program details)
    items = []
    for s in students:
        item = StudentResponse(
            id=s.id, # type: ignore
            admission_number=s.admission_number,
            name=s.name,
            dob=str(s.dob) if s.dob else None,
            phone=s.phone,
            email=s.email,
            program_name=s.program.name if s.program else "Unknown",
            program_code=s.program.code if s.program else "UNKNOWN",
            current_year=s.current_year,
            current_semester=s.current_semester,
            section=s.section,
            batch=s.batch,
            status=s.status,
            gender=s.gender
        )
        items.append(item)
        
    return StudentListResponse(
        total=total,
        items=items,
        page=page,
        limit=limit
    )

@router.patch("/{student_id}/verify", response_model=StudentResponse)
def verify_student(
    student_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Verify an imported student and mark as ACTIVE.
    """
    # Check permissions (basic check for now, can be expanded)
    if not current_user.is_superuser:
         # Check roles
        user_roles = {r.name for r in current_user.roles}
        if not {"SUPER_ADMIN", "ADMIN", "ADMISSION_OFFICER"}.intersection(user_roles):
            raise HTTPException(status_code=403, detail="Not authorized to verify students")

    student = session.get(Student, student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
        
    student.status = StudentStatus.ACTIVE
    session.add(student)
    session.commit()
    session.refresh(student)
    
    # We need to reuse the mapping logic or refactor it. For now, inline or helper.
    # Since I cannot easily refactor the whole file in one go without reading it all, I will duplicate logic briefly or assume I can access relationship.
    # Ensure relationships are loaded if needed, or rely on lazy loading (which works in sync mode often or if session attached).
    # Ideally use selectinload again.
    
    # Re-fetch with program
    statement = select(Student).where(Student.id == student_id).options(selectinload(Student.program))
    student = session.exec(statement).one()

    return StudentResponse(
        id=student.id, # type: ignore
        admission_number=student.admission_number,
        name=student.name,
        dob=str(student.dob) if student.dob else None,
        phone=student.phone,
        email=student.email,
        program_name=student.program.name if student.program else "Unknown",
        program_code=student.program.code if student.program else "UNKNOWN",
        current_year=student.current_year,
        current_semester=student.current_semester,
        section=student.section,
        batch=student.batch,
        status=student.status,
        gender=student.gender
    )
