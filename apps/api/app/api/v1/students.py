from typing import Any, List, Optional
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlmodel import Session, select, func
from app.api.deps import get_current_user, get_session
from app.models import User
from app.models.student import Student
from app.schemas.student import StudentResponse, StudentCreate

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
        program_name = "Unknown"
        batch_code = None
        
        if s.program:
            program_name = s.program.name
            
        # Manually fetch batch code if relationship not loaded or lazy
        # If batch relationship exists in Student model:
        # if s.batch_rel: batch_code = s.batch_rel.batch_code
        # For now leaving as None or implement fetch if needed.
            
        student_data = s.model_dump()
        student_data["program_name"] = program_name
        student_data["batch_code"] = batch_code 
        
        results.append(student_data)
        
    return results


from app.services.academic_service import academic_validation_service

@router.post("/", response_model=StudentResponse)
def create_student(
    *,
    session: Session = Depends(get_session),
    student_in: StudentCreate,
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Create new student (Admin only).
    Enforces strict academic structure.
    """
    # 1. Check permissions (Admin only)
    is_admin = any(role.name in ["SUPER_ADMIN", "ADMIN", "PRINCIPAL", "ADMISSION_OFFICER"] for role in current_user.roles)
    if not is_admin:
        raise HTTPException(status_code=403, detail="Not authorized to create students")
        
    # 2. Verify hierarchy validity (Strict)
    academic_validation_service.validate_hierarchy(
        session=session,
        batch_id=student_in.batch_id,
        program_year_id=student_in.program_year_id,
        batch_semester_id=student_in.batch_semester_id,
        section_id=student_in.section_id,
        # practical_batch_id not yet in StudentCreate schema, likely assigned later?
        # If it is, pass it here. Checking schema... 
        # StudentCreate has section_id (Optional). No practical_batch_id in create schema yet?
    )
    
    # Check admission number uniqueness
    existing = session.exec(select(Student).where(Student.admission_number == student_in.admission_number)).first()
    if existing:
        raise HTTPException(status_code=400, detail="Admission number already exists")

    student_data = student_in.model_dump()
    db_student = Student(**student_data)
    
    session.add(db_student)
    session.commit()
    session.refresh(db_student)
    
    # Populate flattened fields for response
    # (In a real app, might want to eager load these)
    program_name = "Unknown"
    if db_student.program:
        program_name = db_student.program.name
        
    response_data = db_student.model_dump()
    response_data["program_name"] = program_name
    
    return response_data
