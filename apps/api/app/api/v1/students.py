from typing import Any, List, Optional
from fastapi import APIRouter, Depends, Query
from sqlmodel import Session, select, func
from app.api.deps import get_current_user, get_session
from app.models.user import User
from app.models.student import Student
from app.schemas.student import StudentResponse

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
    """
    Retrieve students.
    """
    # Build query
    query = select(Student)
    
    if program_id:
        query = query.where(Student.program_id == program_id)
        
    if semester_id:
        query = query.where(Student.semester_id == semester_id)
        
    if search:
        query = query.where(Student.name.contains(search) | Student.admission_number.contains(search))
        
    # Count total (optional, for pagination)
    # total = session.exec(select(func.count()).select_from(query.subquery())).one()
    
    # Execute with pagination
    students = session.exec(query.offset(skip).limit(limit)).all()
    
    # Enhance response with program name (if needed for StudentRead)
    # Assuming StudentRead expects flattened structure or we return raw model
    # For now returning model directly which matches schema if fields align
    
    results = []
    for s in students:
        # We might need to manually construct the response if StudentRead has fields 
        # that are not on Student model directly (like program_name)
        # Checking apps/api/app/schemas/student.py...
        # It has program_name: str
        
        program_name = "Unknown"
        if s.program:
            program_name = s.program.name
            
        student_data = s.model_dump()
        student_data["program_name"] = program_name
        # current_year is on model? Check model.
        # If not, deriving it or leaving default.
        
        results.append(student_data)
        
    return results
