from typing import Any, List, Optional
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlmodel import Session
from app.api.deps import get_current_user, get_session
from app.models.user import User
from ..service import student_service
from ..schemas.student import StudentResponse, StudentCreate

router = APIRouter()

@router.get("/", response_model=List[StudentResponse])
def get_students(
    *,
    session: Session = Depends(get_session),
    skip: int = 0,
    limit: int = 100,
    program_id: Optional[int] = None,
    semester_id: Optional[int] = None,
    search: Optional[str] = None,
    current_user: User = Depends(get_current_user),
) -> Any:
    """Retrieve students."""
    return student_service.get_students(
        session=session,
        skip=skip,
        limit=limit,
        program_id=program_id,
        semester_id=semester_id,
        search=search
    )

@router.post("/", response_model=StudentResponse)
def create_student(
    *,
    session: Session = Depends(get_session),
    student_in: StudentCreate,
    current_user: User = Depends(get_current_user),
) -> Any:
    """Create new student (Admin only)."""
    # Authorization check
    is_admin = any(role.name in ["SUPER_ADMIN", "ADMIN", "PRINCIPAL", "ADMISSION_OFFICER"] for role in current_user.roles)
    if not is_admin:
        raise HTTPException(status_code=403, detail="Not authorized to create students")
        
    db_student = student_service.create_student(
        session=session,
        student_in_data=student_in.model_dump(),
        current_user_id=current_user.id
    )
    
    # Flatten response if needed
    response_data = db_student.model_dump()
    response_data["program_name"] = db_student.program.name if db_student.program else "Unknown"
    
    return response_data
